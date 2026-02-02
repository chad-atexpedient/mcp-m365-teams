# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-01-XX

### Added
- Initial release of MCP M365 Teams server
- Core functionality for Microsoft Teams integration:
  - `list_teams` - List all teams user is a member of
  - `get_team_channels` - Get channels in a specific team
  - `send_channel_message` - Send messages to channels
  - `get_channel_messages` - Retrieve messages from channels
  - `create_team` - Create new Microsoft Teams
  - `add_team_member` - Add members to teams
  - `create_channel` - Create new channels in teams
  - `get_user_presence` - Get user presence/availability
  - `search_messages` - Search messages across teams
- Azure AD authentication support using client credentials flow
- Comprehensive documentation and setup guide
- Unit tests with pytest
- GitHub Actions CI/CD workflow
- Code quality tools (black, ruff, mypy)
- MIT License

### Security
- Secure credential handling via environment variables
- Required Microsoft Graph API permissions documented
- Security best practices guide

[Unreleased]: https://github.com/chad-atexpedient/mcp-m365-teams/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/chad-atexpedient/mcp-m365-teams/releases/tag/v0.1.0
