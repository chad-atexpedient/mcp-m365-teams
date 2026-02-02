# Quick Start Guide

Get up and running with MCP M365 Teams in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- A Microsoft 365 account with Teams
- Admin access to Azure AD (or work with your admin)

## Step 1: Azure AD Setup (5 minutes)

### Register App in Azure Portal

1. Go to [Azure Portal](https://portal.azure.com) → Azure Active Directory → App registrations
2. Click **New registration**
3. Name: `MCP Teams Integration`
4. Click **Register**

### Copy Your Credentials

From the app Overview page, copy:
- **Directory (tenant) ID**
- **Application (client) ID**

### Create Secret

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Copy the **Value** (you won't see it again!)

### Add Permissions

1. Go to **API permissions**
2. Click **Add a permission** → Microsoft Graph → Application permissions
3. Add these permissions:
   - Channel.Create
   - Channel.ReadBasic.All
   - ChannelMessage.Read.All
   - ChannelMessage.Send
   - Team.ReadBasic.All
   - TeamMember.ReadWrite.All
   - User.Read.All
   - Presence.Read.All

4. Click **Grant admin consent for [Your Organization]**

> **Need help?** See the [detailed Azure setup guide](AZURE_SETUP.md)

## Step 2: Install the Server (1 minute)

```bash
# Install from source (once published, use: pip install mcp-m365-teams)
git clone https://github.com/chad-atexpedient/mcp-m365-teams.git
cd mcp-m365-teams
pip install -e .
```

## Step 3: Configure Credentials (1 minute)

Create a `.env` file or set environment variables:

```bash
export M365_TENANT_ID="your-tenant-id"
export M365_CLIENT_ID="your-client-id"
export M365_CLIENT_SECRET="your-client-secret"
```

Or on Windows PowerShell:

```powershell
$env:M365_TENANT_ID="your-tenant-id"
$env:M365_CLIENT_ID="your-client-id"
$env:M365_CLIENT_SECRET="your-client-secret"
```

## Step 4: Test the Connection (1 minute)

```bash
# Run the server (test mode)
python -m mcp_m365_teams.server
```

If configured correctly, the server will start without errors.

## Step 5: Configure Your MCP Client (2 minutes)

### For Claude Desktop

Edit your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

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

### For Other MCP Clients

Follow your client's documentation for adding MCP servers, using:
- **Command**: `python -m mcp_m365_teams.server`
- **Environment variables**: As shown above

## Step 6: Try It Out!

Restart your MCP client and try these commands:

### List Your Teams

> "Can you list all my Teams?"

### Send a Message

> "Send a message to the Engineering team's General channel saying 'Hello from MCP!'"

### Get Recent Messages

> "Show me the latest messages from the Marketing team's General channel"

### Check Presence

> "What's the status of john@company.com?"

## Common Issues

### "Insufficient privileges" Error

**Solution**: Make sure you granted admin consent in Step 1

### "Authentication failed" Error

**Solution**: Double-check your credentials are correct (no extra spaces!)

### "Resource not found" Error

**Solution**: Verify you have access to the teams/channels you're trying to access

## Next Steps

- Read the [full documentation](../README.md)
- Check out [usage examples](../examples/usage_examples.md)
- Review [security best practices](../SECURITY.md)
- Explore the [Azure setup guide](AZURE_SETUP.md)

## What You Can Do Now

✅ List all your Teams and channels  
✅ Send messages to channels  
✅ Read messages from channels  
✅ Create new teams and channels  
✅ Add members to teams  
✅ Check user presence/availability  
✅ Search messages across teams  

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/chad-atexpedient/mcp-m365-teams/issues)
- **Documentation**: Check the `/docs` folder
- **Examples**: See `/examples` folder

## Tips for Success

1. **Start small**: Test with one team first
2. **Check permissions**: Verify you have access to the teams
3. **Monitor usage**: Keep an eye on API rate limits
4. **Secure credentials**: Never commit secrets to git
5. **Rotate secrets**: Set a reminder to rotate secrets every 90 days

## Architecture Overview

```
┌─────────────────┐
│   MCP Client    │
│ (Claude, etc.)  │
└────────┬────────┘
         │ MCP Protocol
         │
┌────────▼────────┐
│   MCP Server    │
│ (This Package)  │
└────────┬────────┘
         │ Microsoft Graph API
         │
┌────────▼────────┐
│  Microsoft 365  │
│     Teams       │
└─────────────────┘
```

## Development Mode

Want to modify the server?

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/

# Lint
ruff check src/ tests/
```

## Production Deployment

For production use:

1. **Use a secret manager** (Azure Key Vault, AWS Secrets Manager)
2. **Rotate secrets regularly** (every 90 days)
3. **Monitor API usage** via Azure portal
4. **Set up logging** for troubleshooting
5. **Use separate apps** for dev/staging/prod

## Performance Tips

- **Cache team/channel IDs** to reduce API calls
- **Batch operations** when possible
- **Use async operations** for better performance
- **Monitor rate limits** (Graph API limits apply)

## Support Checklist

Before asking for help, please check:

- [ ] All three credentials are correct
- [ ] Admin consent is granted
- [ ] App has all required permissions
- [ ] Environment variables are set correctly
- [ ] Python version is 3.10+
- [ ] All dependencies are installed
- [ ] You have access to the teams you're trying to use

## Success! 🎉

You're now ready to integrate Microsoft Teams with AI assistants and automation tools!

Enjoy using MCP M365 Teams!
