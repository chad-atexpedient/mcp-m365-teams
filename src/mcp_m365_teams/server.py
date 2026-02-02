"""
MCP Server for Microsoft 365 Teams Integration
"""
import asyncio
import os
from typing import Any, Optional
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from msgraph import GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from msgraph.generated.teams.teams_request_builder import TeamsRequestBuilder
from msgraph.generated.me.me_request_builder import MeRequestBuilder
from azure.identity import ClientSecretCredential
import json


class M365TeamsServer:
    def __init__(self):
        self.app = Server("mcp-m365-teams")
        self.client: Optional[GraphServiceClient] = None
        self._setup_handlers()
        
    def _setup_handlers(self):
        """Setup MCP protocol handlers"""
        
        @self.app.list_tools()
        async def list_tools() -> list[types.Tool]:
            """List available Microsoft Teams tools"""
            return [
                types.Tool(
                    name="list_teams",
                    description="List all teams the user is a member of",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
                types.Tool(
                    name="get_team_channels",
                    description="Get all channels in a specific team",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "team_id": {
                                "type": "string",
                                "description": "The ID of the team",
                            },
                        },
                        "required": ["team_id"],
                    },
                ),
                types.Tool(
                    name="send_channel_message",
                    description="Send a message to a Teams channel",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "team_id": {
                                "type": "string",
                                "description": "The ID of the team",
                            },
                            "channel_id": {
                                "type": "string",
                                "description": "The ID of the channel",
                            },
                            "message": {
                                "type": "string",
                                "description": "The message content",
                            },
                        },
                        "required": ["team_id", "channel_id", "message"],
                    },
                ),
                types.Tool(
                    name="get_channel_messages",
                    description="Get recent messages from a Teams channel",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "team_id": {
                                "type": "string",
                                "description": "The ID of the team",
                            },
                            "channel_id": {
                                "type": "string",
                                "description": "The ID of the channel",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of messages to retrieve (default: 10)",
                                "default": 10,
                            },
                        },
                        "required": ["team_id", "channel_id"],
                    },
                ),
                types.Tool(
                    name="create_team",
                    description="Create a new Microsoft Team",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "display_name": {
                                "type": "string",
                                "description": "The name of the team",
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the team",
                            },
                        },
                        "required": ["display_name"],
                    },
                ),
                types.Tool(
                    name="add_team_member",
                    description="Add a member to a team",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "team_id": {
                                "type": "string",
                                "description": "The ID of the team",
                            },
                            "user_email": {
                                "type": "string",
                                "description": "Email address of the user to add",
                            },
                            "role": {
                                "type": "string",
                                "description": "Role: 'owner' or 'member' (default: member)",
                                "default": "member",
                            },
                        },
                        "required": ["team_id", "user_email"],
                    },
                ),
                types.Tool(
                    name="create_channel",
                    description="Create a new channel in a team",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "team_id": {
                                "type": "string",
                                "description": "The ID of the team",
                            },
                            "display_name": {
                                "type": "string",
                                "description": "The name of the channel",
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the channel",
                            },
                        },
                        "required": ["team_id", "display_name"],
                    },
                ),
                types.Tool(
                    name="get_user_presence",
                    description="Get presence information for a user",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_email": {
                                "type": "string",
                                "description": "Email address of the user",
                            },
                        },
                        "required": ["user_email"],
                    },
                ),
                types.Tool(
                    name="search_messages",
                    description="Search for messages across all teams",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results (default: 10)",
                                "default": 10,
                            },
                        },
                        "required": ["query"],
                    },
                ),
            ]
        
        @self.app.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[types.TextContent]:
            """Handle tool execution"""
            try:
                if not self.client:
                    await self._initialize_client()
                
                if name == "list_teams":
                    result = await self._list_teams()
                elif name == "get_team_channels":
                    result = await self._get_team_channels(arguments["team_id"])
                elif name == "send_channel_message":
                    result = await self._send_channel_message(
                        arguments["team_id"],
                        arguments["channel_id"],
                        arguments["message"]
                    )
                elif name == "get_channel_messages":
                    result = await self._get_channel_messages(
                        arguments["team_id"],
                        arguments["channel_id"],
                        arguments.get("limit", 10)
                    )
                elif name == "create_team":
                    result = await self._create_team(
                        arguments["display_name"],
                        arguments.get("description", "")
                    )
                elif name == "add_team_member":
                    result = await self._add_team_member(
                        arguments["team_id"],
                        arguments["user_email"],
                        arguments.get("role", "member")
                    )
                elif name == "create_channel":
                    result = await self._create_channel(
                        arguments["team_id"],
                        arguments["display_name"],
                        arguments.get("description", "")
                    )
                elif name == "get_user_presence":
                    result = await self._get_user_presence(arguments["user_email"])
                elif name == "search_messages":
                    result = await self._search_messages(
                        arguments["query"],
                        arguments.get("limit", 10)
                    )
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _initialize_client(self):
        """Initialize Microsoft Graph client"""
        tenant_id = os.getenv("M365_TENANT_ID")
        client_id = os.getenv("M365_CLIENT_ID")
        client_secret = os.getenv("M365_CLIENT_SECRET")
        
        if not all([tenant_id, client_id, client_secret]):
            raise ValueError(
                "Missing required environment variables: "
                "M365_TENANT_ID, M365_CLIENT_ID, M365_CLIENT_SECRET"
            )
        
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        
        self.client = GraphServiceClient(credential)
    
    async def _list_teams(self) -> dict:
        """List all teams"""
        teams = await self.client.me.joined_teams.get()
        
        result = []
        if teams and teams.value:
            for team in teams.value:
                result.append({
                    "id": team.id,
                    "display_name": team.display_name,
                    "description": team.description,
                })
        
        return {"teams": result, "count": len(result)}
    
    async def _get_team_channels(self, team_id: str) -> dict:
        """Get channels in a team"""
        channels = await self.client.teams.by_team_id(team_id).channels.get()
        
        result = []
        if channels and channels.value:
            for channel in channels.value:
                result.append({
                    "id": channel.id,
                    "display_name": channel.display_name,
                    "description": channel.description,
                    "email": channel.email,
                })
        
        return {"channels": result, "count": len(result)}
    
    async def _send_channel_message(self, team_id: str, channel_id: str, message: str) -> dict:
        """Send a message to a channel"""
        from msgraph.generated.models.chat_message import ChatMessage
        from msgraph.generated.models.item_body import ItemBody
        from msgraph.generated.models.body_type import BodyType
        
        chat_message = ChatMessage()
        chat_message.body = ItemBody()
        chat_message.body.content = message
        chat_message.body.content_type = BodyType.Text
        
        result = await self.client.teams.by_team_id(team_id).channels.by_channel_id(
            channel_id
        ).messages.post(chat_message)
        
        return {
            "success": True,
            "message_id": result.id,
            "created_at": result.created_date_time.isoformat() if result.created_date_time else None,
        }
    
    async def _get_channel_messages(self, team_id: str, channel_id: str, limit: int) -> dict:
        """Get messages from a channel"""
        messages = await self.client.teams.by_team_id(team_id).channels.by_channel_id(
            channel_id
        ).messages.get()
        
        result = []
        if messages and messages.value:
            for msg in messages.value[:limit]:
                result.append({
                    "id": msg.id,
                    "content": msg.body.content if msg.body else None,
                    "from": msg.from_property.user.display_name if msg.from_property and msg.from_property.user else None,
                    "created_at": msg.created_date_time.isoformat() if msg.created_date_time else None,
                })
        
        return {"messages": result, "count": len(result)}
    
    async def _create_team(self, display_name: str, description: str) -> dict:
        """Create a new team"""
        from msgraph.generated.models.team import Team
        
        team = Team()
        team.display_name = display_name
        team.description = description
        
        result = await self.client.teams.post(team)
        
        return {
            "success": True,
            "team_id": result.id,
            "display_name": result.display_name,
        }
    
    async def _add_team_member(self, team_id: str, user_email: str, role: str) -> dict:
        """Add a member to a team"""
        from msgraph.generated.models.aad_user_conversation_member import AadUserConversationMember
        
        # First get user ID from email
        users = await self.client.users.get(filter=f"mail eq '{user_email}'")
        if not users or not users.value:
            raise ValueError(f"User not found: {user_email}")
        
        user_id = users.value[0].id
        
        member = AadUserConversationMember()
        member.roles = ["owner"] if role == "owner" else []
        member.additional_data = {
            "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user_id}')"
        }
        
        result = await self.client.teams.by_team_id(team_id).members.post(member)
        
        return {
            "success": True,
            "member_id": result.id,
        }
    
    async def _create_channel(self, team_id: str, display_name: str, description: str) -> dict:
        """Create a new channel"""
        from msgraph.generated.models.channel import Channel
        
        channel = Channel()
        channel.display_name = display_name
        channel.description = description
        
        result = await self.client.teams.by_team_id(team_id).channels.post(channel)
        
        return {
            "success": True,
            "channel_id": result.id,
            "display_name": result.display_name,
        }
    
    async def _get_user_presence(self, user_email: str) -> dict:
        """Get user presence information"""
        # First get user ID from email
        users = await self.client.users.get(filter=f"mail eq '{user_email}'")
        if not users or not users.value:
            raise ValueError(f"User not found: {user_email}")
        
        user_id = users.value[0].id
        
        presence = await self.client.users.by_user_id(user_id).presence.get()
        
        return {
            "user_email": user_email,
            "availability": presence.availability,
            "activity": presence.activity,
        }
    
    async def _search_messages(self, query: str, limit: int) -> dict:
        """Search for messages across teams"""
        # Note: This is a simplified implementation
        # Full text search requires Microsoft Search API
        teams = await self._list_teams()
        
        all_messages = []
        for team in teams.get("teams", []):
            channels = await self._get_team_channels(team["id"])
            for channel in channels.get("channels", []):
                messages = await self._get_channel_messages(
                    team["id"], 
                    channel["id"], 
                    limit
                )
                for msg in messages.get("messages", []):
                    if query.lower() in (msg.get("content", "") or "").lower():
                        msg["team_name"] = team["display_name"]
                        msg["channel_name"] = channel["display_name"]
                        all_messages.append(msg)
        
        return {
            "messages": all_messages[:limit],
            "count": len(all_messages[:limit]),
        }
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                self.app.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = M365TeamsServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
