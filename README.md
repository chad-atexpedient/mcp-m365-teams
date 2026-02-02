# MCP M365 Teams Server

A Model Context Protocol (MCP) server that provides integration with Microsoft 365 Teams. This server enables AI assistants and other MCP clients to interact with Microsoft Teams through a standardized interface.

> **🚀 Quick Start**: New to this project? Check out the [Quick Start Guide](docs/QUICKSTART.md) to get up and running in 5 minutes!

## Features

- **List Teams**: Get all teams the user is a member of
- **Channel Management**: List, create, and manage team channels
- **Messaging**: Send and retrieve messages from channels
- **Team Creation**: Create new Microsoft Teams
- **Member Management**: Add members to teams with specific roles
- **Presence Information**: Get user availability and presence status
- **Message Search**: Search for messages across all teams

## Documentation

- 📖 [Quick Start Guide](docs/QUICKSTART.md) - Get started in 5 minutes
- 🔧 [Azure AD Setup Guide](docs/AZURE_SETUP.md) - Detailed Azure configuration
- 💡 [Usage Examples](examples/usage_examples.md) - Practical examples and workflows
- 🔒 [Security Policy](SECURITY.md) - Security best practices
- 🤝 [Contributing Guide](CONTRIBUTING.md) - How to contribute

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

## Quick Setup

1. **Register Azure AD App** - [Detailed guide](docs/AZURE_SETUP.md)
2. **Set Environment Variables**:
   ```bash
   export M365_TENANT_ID="your-tenant-id"
   export M365_CLIENT_ID="your-client-id"
   export M365_CLIENT_SECRET="your-client-secret"
   ```
3. **Run the Server**:
   ```bash
   mcp-m365-teams
   ```

For detailed setup instructions, see the [Quick Start Guide](docs/QUICKSTART.md).

## Configuration with MCP Clients

### Claude Desktop

Add to your Claude Desktop config:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "m365-teams": {
      "command": "python",
      "args": ["-m", "mcp_m365_teams.server"],
      "env": {
        "M365_TENANT_ID": "your-tenant-id",
        "M365_CLIENT_ID": "your-client-id",
        "M365_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

### Other MCP Clients

For other MCP clients, use:
- **Command**: `python -m mcp_m365_teams.server`
- **Environment**: Set the three M365 variables

## Available Tools

| Tool | Description |
|------|-------------|
| `list_teams` | List all teams the user is a member of |
| `get_team_channels` | Get all channels in a specific team |
| `send_channel_message` | Send a message to a Teams channel |
| `get_channel_messages` | Get recent messages from a channel |
| `create_team` | Create a new Microsoft Team |
| `add_team_member` | Add a member to a team |
| `create_channel` | Create a new channel in a team |
| `get_user_presence` | Get user presence/availability status |
| `search_messages` | Search for messages across all teams |

For detailed tool documentation and examples, see [Usage Examples](examples/usage_examples.md).

## Example Usage

### With an AI Assistant (e.g., Claude)

> **User**: "Can you send a message to the Engineering team's General channel saying 'Deployment complete'?"

> **Assistant**: I'll send that message for you.
> 
> *[Uses list_teams → get_team_channels → send_channel_message]*
> 
> ✅ Message sent to Engineering > General: "Deployment complete"

### Programmatic Usage

```python
# See examples/usage_examples.md for detailed code examples
```

## Architecture

```
┌─────────────────┐
│   MCP Client    │
│ (Claude, etc.)  │
└────────┬────────┘
         │ MCP Protocol
         │
┌────────▼────────┐
│  MCP M365 Teams │
│     Server      │
└────────┬────────┘
         │ Microsoft Graph API
         │
┌────────▼────────┐
│  Microsoft 365  │
│     Teams       │
└─────────────────┘
```

## Prerequisites

- Python 3.10 or higher
- Microsoft 365 account with Teams
- Azure AD admin access (for app registration)

### Required Azure AD Permissions

The following Microsoft Graph API permissions are required:

| Permission | Type | Reason |
|------------|------|--------|
| `Team.ReadBasic.All` | Application | Read team information |
| `Channel.ReadBasic.All` | Application | Read channel information |
| `ChannelMessage.Read.All` | Application | Read channel messages |
| `ChannelMessage.Send` | Application | Send messages to channels |
| `TeamMember.ReadWrite.All` | Application | Manage team members |
| `User.Read.All` | Application | Read user information |
| `Presence.Read.All` | Application | Read user presence |

See the [Azure Setup Guide](docs/AZURE_SETUP.md) for detailed configuration instructions.

## Security

- 🔒 Never commit credentials to version control
- 🔐 Use environment variables or secret managers
- 🔄 Rotate client secrets regularly (every 90 days)
- 👮 Apply principle of least privilege
- 📊 Monitor API usage and set up alerts

For comprehensive security guidance, see [SECURITY.md](SECURITY.md).

## Development

### Setup Development Environment

```bash
git clone https://github.com/chad-atexpedient/mcp-m365-teams.git
cd mcp-m365-teams
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest                    # Run all tests
pytest --cov             # Run with coverage
```

### Code Quality

```bash
black src/ tests/        # Format code
ruff check src/ tests/   # Lint code
mypy src/                # Type checking
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Insufficient privileges" | Ensure admin consent is granted in Azure AD |
| "Authentication failed" | Verify all three credentials are correct |
| "Resource not found" | Check you have access to the teams/channels |

For more help, see [Troubleshooting](docs/AZURE_SETUP.md#troubleshooting) or [open an issue](https://github.com/chad-atexpedient/mcp-m365-teams/issues).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Microsoft Graph API Documentation](https://learn.microsoft.com/en-us/graph/overview)
- [Microsoft Teams API Reference](https://learn.microsoft.com/en-us/graph/api/resources/teams-api-overview)
- [Azure AD Best Practices](https://learn.microsoft.com/en-us/azure/active-directory/develop/identity-platform-integration-checklist)

## Support

- 📫 [Open an issue](https://github.com/chad-atexpedient/mcp-m365-teams/issues) for bugs or feature requests
- 💬 Check [existing issues](https://github.com/chad-atexpedient/mcp-m365-teams/issues) for solutions
- 📚 Read the [documentation](docs/) for detailed guides

## Roadmap

Future enhancements planned:

- [ ] Support for Teams meetings
- [ ] File sharing capabilities
- [ ] Tab management
- [ ] Calendar integration
- [ ] Webhooks support
- [ ] Adaptive Cards support

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

## Star History

If you find this project useful, please consider giving it a ⭐!

---

**Made with ❤️ for the MCP community**
