# Usage Examples

This document provides practical examples of using the MCP M365 Teams server.

## Prerequisites

Ensure you have:
1. Configured your Azure AD application
2. Set up environment variables
3. Installed and configured the MCP server

## Example Scenarios

### 1. List All Your Teams

**Request:**
```json
{
  "tool": "list_teams"
}
```

**Response:**
```json
{
  "teams": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "display_name": "Engineering Team",
      "description": "Main engineering team workspace"
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "display_name": "Marketing Team",
      "description": "Marketing and communications"
    }
  ],
  "count": 2
}
```

### 2. Get Channels in a Team

**Request:**
```json
{
  "tool": "get_team_channels",
  "arguments": {
    "team_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  }
}
```

**Response:**
```json
{
  "channels": [
    {
      "id": "channel-123",
      "display_name": "General",
      "description": "General discussion",
      "email": "engineering.general@company.onmicrosoft.com"
    },
    {
      "id": "channel-456",
      "display_name": "Development",
      "description": "Development discussions",
      "email": "engineering.dev@company.onmicrosoft.com"
    }
  ],
  "count": 2
}
```

### 3. Send a Message to a Channel

**Request:**
```json
{
  "tool": "send_channel_message",
  "arguments": {
    "team_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "channel_id": "channel-123",
    "message": "Hello team! This is an automated message from the MCP server."
  }
}
```

**Response:**
```json
{
  "success": true,
  "message_id": "message-789",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 4. Get Recent Messages from a Channel

**Request:**
```json
{
  "tool": "get_channel_messages",
  "arguments": {
    "team_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "channel_id": "channel-123",
    "limit": 5
  }
}
```

**Response:**
```json
{
  "messages": [
    {
      "id": "msg-1",
      "content": "Meeting notes uploaded to SharePoint",
      "from": "John Doe",
      "created_at": "2024-01-15T09:00:00Z"
    },
    {
      "id": "msg-2",
      "content": "Please review the PR when you get a chance",
      "from": "Jane Smith",
      "created_at": "2024-01-15T08:30:00Z"
    }
  ],
  "count": 2
}
```

### 5. Create a New Team

**Request:**
```json
{
  "tool": "create_team",
  "arguments": {
    "display_name": "Product Launch Team",
    "description": "Cross-functional team for Q1 product launch"
  }
}
```

**Response:**
```json
{
  "success": true,
  "team_id": "new-team-123",
  "display_name": "Product Launch Team"
}
```

### 6. Add a Member to a Team

**Request:**
```json
{
  "tool": "add_team_member",
  "arguments": {
    "team_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "user_email": "newmember@company.com",
    "role": "member"
  }
}
```

**Response:**
```json
{
  "success": true,
  "member_id": "member-456"
}
```

### 7. Create a New Channel

**Request:**
```json
{
  "tool": "create_channel",
  "arguments": {
    "team_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "display_name": "Project Alpha",
    "description": "Discussion channel for Project Alpha"
  }
}
```

**Response:**
```json
{
  "success": true,
  "channel_id": "new-channel-789",
  "display_name": "Project Alpha"
}
```

### 8. Check User Presence

**Request:**
```json
{
  "tool": "get_user_presence",
  "arguments": {
    "user_email": "colleague@company.com"
  }
}
```

**Response:**
```json
{
  "user_email": "colleague@company.com",
  "availability": "Available",
  "activity": "Available"
}
```

### 9. Search Messages

**Request:**
```json
{
  "tool": "search_messages",
  "arguments": {
    "query": "deployment",
    "limit": 10
  }
}
```

**Response:**
```json
{
  "messages": [
    {
      "id": "msg-search-1",
      "content": "Deployment completed successfully to production",
      "from": "DevOps Team",
      "created_at": "2024-01-15T14:00:00Z",
      "team_name": "Engineering Team",
      "channel_name": "Deployments"
    },
    {
      "id": "msg-search-2",
      "content": "Next deployment scheduled for Friday",
      "from": "Release Manager",
      "created_at": "2024-01-14T16:30:00Z",
      "team_name": "Engineering Team",
      "channel_name": "General"
    }
  ],
  "count": 2
}
```

## Common Workflows

### Daily Standup Bot

```python
# Pseudo-code for a standup reminder bot
async def daily_standup():
    teams = await call_tool("list_teams")
    
    for team in teams["teams"]:
        if "Engineering" in team["display_name"]:
            channels = await call_tool("get_team_channels", {
                "team_id": team["id"]
            })
            
            for channel in channels["channels"]:
                if channel["display_name"] == "Standup":
                    await call_tool("send_channel_message", {
                        "team_id": team["id"],
                        "channel_id": channel["id"],
                        "message": "Good morning! Daily standup in 15 minutes."
                    })
```

### Message Monitoring

```python
# Pseudo-code for monitoring urgent messages
async def monitor_urgent_messages():
    urgent_keywords = ["urgent", "critical", "emergency"]
    
    results = await call_tool("search_messages", {
        "query": " OR ".join(urgent_keywords),
        "limit": 50
    })
    
    # Process and notify about urgent messages
    for msg in results["messages"]:
        print(f"Urgent message in {msg['team_name']}/{msg['channel_name']}: {msg['content']}")
```

### Automated Team Provisioning

```python
# Pseudo-code for creating a project team
async def create_project_team(project_name, team_members):
    # Create team
    team = await call_tool("create_team", {
        "display_name": f"Project: {project_name}",
        "description": f"Team workspace for {project_name}"
    })
    
    # Create channels
    channels = ["General", "Development", "Testing", "Documentation"]
    for channel_name in channels:
        await call_tool("create_channel", {
            "team_id": team["team_id"],
            "display_name": channel_name,
            "description": f"{channel_name} discussions"
        })
    
    # Add members
    for member_email in team_members:
        await call_tool("add_team_member", {
            "team_id": team["team_id"],
            "user_email": member_email,
            "role": "member"
        })
```

## Integration with AI Assistants

When using with an AI assistant (like Claude), you can use natural language:

**Example Conversation:**

> User: "Can you send a message to the Engineering team's General channel saying the deployment is complete?"

> Assistant: I'll send that message for you. Let me first find the Engineering team and its General channel.
> 
> *[Uses list_teams to find the Engineering team]*
> *[Uses get_team_channels to find the General channel]*
> *[Uses send_channel_message to send the message]*
> 
> Done! I've sent the message to the Engineering team's General channel.

## Error Handling

### Missing Permissions

If you get permission errors, ensure your Azure AD app has the required permissions:

```json
{
  "error": "Insufficient privileges to complete the operation",
  "message": "Check Azure AD app permissions"
}
```

### Invalid Team or Channel ID

```json
{
  "error": "Resource not found",
  "message": "The specified team or channel does not exist"
}
```

### Authentication Failures

```json
{
  "error": "Authentication failed",
  "message": "Check your M365_TENANT_ID, M365_CLIENT_ID, and M365_CLIENT_SECRET"
}
```

## Best Practices

1. **Cache team and channel IDs** to reduce API calls
2. **Rate limiting**: Be mindful of Microsoft Graph API rate limits
3. **Error handling**: Always handle errors gracefully
4. **Logging**: Enable logging for troubleshooting
5. **Security**: Never log or expose credentials

## Additional Resources

- [Microsoft Graph Teams API Documentation](https://learn.microsoft.com/en-us/graph/api/resources/teams-api-overview)
- [Teams Message Format](https://learn.microsoft.com/en-us/graph/api/channel-post-messages)
- [MCP Protocol Documentation](https://modelcontextprotocol.io)
