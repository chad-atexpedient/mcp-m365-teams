# MCP M365 Teams Server

A Model Context Protocol (MCP) server that provides integration with Microsoft 365 Teams. This server enables AI assistants and other MCP clients to interact with Microsoft Teams through a standardized interface.

## Features

- **List Teams**: Get all teams the user is a member of
- **Channel Management**: List, create, and manage team channels
- **Messaging**: Send and retrieve messages from channels
- **Team Creation**: Create new Microsoft Teams
- **Member Management**: Add members to teams with specific roles
- **Presence Information**: Get user availability and presence status
- **Message Search**: Search for messages across all teams

## Installation

### From PyPI (when published)

```bash
pip install mcp-m365-teams
```

### From Source

```bash
git clone https://github.com/chad-atexpedient/mcp-m365-teams.git
cd mcp-m365-teams
pip install -e .
```

## Prerequisites

Before using this MCP server, you need to:

1. **Register an Azure AD Application**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Navigate to "Azure Active Directory" > "App registrations"
   - Click "New registration"
   - Give it a name (e.g., "MCP Teams Integration")
   - Choose supported account types
   - Click "Register"

2. **Configure API Permissions**:
   - In your app registration, go to "API permissions"
   - Add the following Microsoft Graph permissions:
     - `Team.ReadBasic.All` - Read basic team info
     - `Channel.ReadBasic.All` - Read channel info
     - `ChannelMessage.Read.All` - Read channel messages
     - `ChannelMessage.Send` - Send channel messages
     - `TeamMember.ReadWrite.All` - Manage team members
     - `Presence.Read.All` - Read user presence
   - Grant admin consent for your organization

3. **Create a Client Secret**:
   - Go to "Certificates & secrets"
   - Click "New client secret"
   - Add a description and set expiration
   - Copy the secret value (you won't be able to see it again!)

4. **Set Environment Variables**:

```bash
export M365_TENANT_ID="your-tenant-id"
export M365_CLIENT_ID="your-client-id"
export M365_CLIENT_SECRET="your-client-secret"
```

## Usage

### Running the Server

```bash
mcp-m365-teams
```

Or using Python:

```bash
python -m mcp_m365_teams.server
```

### Configuration with MCP Clients

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "m365-teams": {
      "command": "mcp-m365-teams",
      "env": {
        "M365_TENANT_ID": "your-tenant-id",
        "M365_CLIENT_ID": "your-client-id",
        "M365_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

Or with uvx:

```json
{
  "mcpServers": {
    "m365-teams": {
      "command": "uvx",
      "args": ["mcp-m365-teams"],
      "env": {
        "M365_TENANT_ID": "your-tenant-id",
        "M365_CLIENT_ID": "your-client-id",
        "M365_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

## Available Tools

### list_teams
List all teams the authenticated user is a member of.

**Parameters**: None

**Example Response**:
```json
{
  "teams": [
    {
      "id": "team-id-123",
      "display_name": "Engineering Team",
      "description": "Engineering department team"
    }
  ],
  "count": 1
}
```

### get_team_channels
Get all channels in a specific team.

**Parameters**:
- `team_id` (string, required): The ID of the team

### send_channel_message
Send a message to a Teams channel.

**Parameters**:
- `team_id` (string, required): The ID of the team
- `channel_id` (string, required): The ID of the channel
- `message` (string, required): The message content

### get_channel_messages
Get recent messages from a Teams channel.

**Parameters**:
- `team_id` (string, required): The ID of the team
- `channel_id` (string, required): The ID of the channel
- `limit` (integer, optional): Maximum number of messages to retrieve (default: 10)

### create_team
Create a new Microsoft Team.

**Parameters**:
- `display_name` (string, required): The name of the team
- `description` (string, optional): Description of the team

### add_team_member
Add a member to a team.

**Parameters**:
- `team_id` (string, required): The ID of the team
- `user_email` (string, required): Email address of the user to add
- `role` (string, optional): Role - 'owner' or 'member' (default: 'member')

### create_channel
Create a new channel in a team.

**Parameters**:
- `team_id` (string, required): The ID of the team
- `display_name` (string, required): The name of the channel
- `description` (string, optional): Description of the channel

### get_user_presence
Get presence information for a user.

**Parameters**:
- `user_email` (string, required): Email address of the user

### search_messages
Search for messages across all teams.

**Parameters**:
- `query` (string, required): Search query
- `limit` (integer, optional): Maximum number of results (default: 10)

## Security Considerations

- Store credentials securely (use environment variables or a secrets manager)
- Never commit credentials to version control
- Use the principle of least privilege when configuring API permissions
- Regularly rotate client secrets
- Monitor API usage and set up alerts for unusual activity

## Development

### Setup Development Environment

```bash
git clone https://github.com/chad-atexpedient/mcp-m365-teams.git
cd mcp-m365-teams
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
ruff check src/
```

## Troubleshooting

### Authentication Errors

If you encounter authentication errors:
1. Verify your environment variables are set correctly
2. Check that your Azure AD app has the correct permissions
3. Ensure admin consent has been granted
4. Verify the client secret hasn't expired

### Permission Errors

If you get permission denied errors:
1. Check the API permissions in Azure AD
2. Ensure admin consent is granted
3. Verify the user has access to the teams/channels

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Microsoft Graph API Documentation](https://learn.microsoft.com/en-us/graph/overview)
- [Microsoft Teams API Reference](https://learn.microsoft.com/en-us/graph/api/resources/teams-api-overview)

## Support

For issues and questions:
- Open an issue on [GitHub](https://github.com/chad-atexpedient/mcp-m365-teams/issues)
- Check existing issues for solutions

## Changelog

### v0.1.0 (Initial Release)
- Basic Teams integration
- Channel management
- Message sending and retrieval
- Team creation
- Member management
- Presence information
- Message search
