# Azure AD Setup Guide

This guide walks you through setting up Azure AD for the MCP M365 Teams server.

## Step 1: Register Azure AD Application

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Go to **Azure Active Directory**
3. Select **App registrations** from the left menu
4. Click **New registration**

### Application Registration Details

- **Name**: `MCP Teams Integration` (or your preferred name)
- **Supported account types**: 
  - Choose "Accounts in this organizational directory only" for single tenant
  - Or "Accounts in any organizational directory" for multi-tenant
- **Redirect URI**: Leave blank (not needed for server-to-server auth)

Click **Register**

## Step 2: Note Your IDs

After registration, you'll see the **Overview** page. Copy these values:

- **Application (client) ID**: This is your `M365_CLIENT_ID`
- **Directory (tenant) ID**: This is your `M365_TENANT_ID`

## Step 3: Create Client Secret

1. In your app registration, go to **Certificates & secrets**
2. Click **New client secret**
3. Add a description: `MCP Server Secret`
4. Choose an expiration period:
   - 6 months (recommended for development)
   - 12 months
   - 24 months
   - Custom
5. Click **Add**
6. **IMPORTANT**: Copy the secret **Value** immediately (you won't see it again!)
   - This is your `M365_CLIENT_SECRET`

## Step 4: Configure API Permissions

1. Go to **API permissions** in your app registration
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Application permissions** (not Delegated)

### Required Permissions

Add the following permissions:

#### Team Operations
- `Team.ReadBasic.All` - Read the names and descriptions of teams
- `Team.Create` - Create teams
- `TeamSettings.ReadWrite.All` - Read and change all teams' settings

#### Channel Operations
- `Channel.ReadBasic.All` - Read the names and descriptions of channels
- `Channel.Create` - Create channels
- `ChannelSettings.ReadWrite.All` - Read and change all channel settings

#### Message Operations
- `ChannelMessage.Read.All` - Read all channel messages
- `ChannelMessage.Send` - Send channel messages

#### Member Operations
- `TeamMember.ReadWrite.All` - Add and remove members from all teams

#### User/Presence Operations
- `User.Read.All` - Read all users' full profiles
- `Presence.Read.All` - Read presence information of all users

### Visual Checklist

After adding all permissions, you should see:

```
✓ Channel.Create
✓ Channel.ReadBasic.All
✓ ChannelMessage.Read.All
✓ ChannelMessage.Send
✓ ChannelSettings.ReadWrite.All
✓ Presence.Read.All
✓ Team.Create
✓ Team.ReadBasic.All
✓ TeamMember.ReadWrite.All
✓ TeamSettings.ReadWrite.All
✓ User.Read.All
```

## Step 5: Grant Admin Consent

**IMPORTANT**: Application permissions require admin consent.

1. Click **Grant admin consent for [Your Organization]**
2. Confirm the consent dialog
3. Wait for the status to show "Granted for [Your Organization]" in green

### If You Don't Have Admin Rights

If you're not an admin:
1. Share the Application ID with your Azure AD administrator
2. Ask them to grant consent via PowerShell:

```powershell
Connect-AzureAD
New-AzureADServiceAppRoleAssignment -ObjectId <ServicePrincipalObjectId> -PrincipalId <ServicePrincipalObjectId> -ResourceId <ResourceServicePrincipalObjectId> -Id <AppRoleId>
```

Or they can grant consent through the Azure Portal as described above.

## Step 6: Set Environment Variables

Create a `.env` file or set environment variables:

```bash
export M365_TENANT_ID="your-tenant-id-here"
export M365_CLIENT_ID="your-client-id-here"
export M365_CLIENT_SECRET="your-client-secret-here"
```

### On Windows (PowerShell)

```powershell
$env:M365_TENANT_ID="your-tenant-id-here"
$env:M365_CLIENT_ID="your-client-id-here"
$env:M365_CLIENT_SECRET="your-client-secret-here"
```

### On Windows (Command Prompt)

```cmd
set M365_TENANT_ID=your-tenant-id-here
set M365_CLIENT_ID=your-client-id-here
set M365_CLIENT_SECRET=your-client-secret-here
```

## Step 7: Test the Setup

Test your configuration:

```bash
# Install the package
pip install mcp-m365-teams

# Run the server (it will fail if credentials are wrong)
mcp-m365-teams
```

## Security Best Practices

### Secret Management

**Development**:
- Use `.env` files (add to `.gitignore`)
- Use environment variables
- Use development/staging Azure AD apps separate from production

**Production**:
- Use Azure Key Vault
- Use managed identities when possible
- Use secret management tools (HashiCorp Vault, AWS Secrets Manager, etc.)

### Secret Rotation

Set up a rotation schedule:
1. Create a second client secret before the first expires
2. Update your deployment with the new secret
3. Verify the new secret works
4. Delete the old secret
5. Document the rotation in your change log

### Monitoring

Enable audit logging:
1. Go to **Azure Active Directory** > **Monitoring** > **Audit logs**
2. Filter by your application
3. Set up alerts for unusual activity

## Troubleshooting

### "Insufficient privileges" Error

**Problem**: App doesn't have required permissions

**Solution**:
1. Verify all permissions are added
2. Ensure admin consent is granted
3. Wait a few minutes for permissions to propagate

### "Invalid client secret" Error

**Problem**: Client secret is wrong or expired

**Solution**:
1. Verify the secret value is correct
2. Check if the secret has expired
3. Create a new secret if needed

### "AADSTS700016" Error

**Problem**: Application not found in directory

**Solution**:
1. Verify the Tenant ID is correct
2. Ensure the app is in the right directory
3. Check that the Client ID matches

### "Unauthorized" Error

**Problem**: Authentication failed

**Solution**:
1. Double-check all three credentials (Tenant ID, Client ID, Secret)
2. Ensure there are no extra spaces or characters
3. Verify the app registration is active (not deleted)

## Advanced Configuration

### Multi-Tenant Setup

For multi-tenant applications:

1. Change supported account types to "Multitenant"
2. Each tenant admin must consent to the app
3. Use the common endpoint for authentication

### Conditional Access

Apply conditional access policies:
1. Go to **Azure AD** > **Security** > **Conditional Access**
2. Create policy for the application
3. Set conditions (IP restrictions, device compliance, etc.)

### Application Proxy

If using from external network:
1. Set up Azure AD Application Proxy
2. Configure connector
3. Update MCP configuration with proxy settings

## Useful PowerShell Commands

### List App Permissions

```powershell
Connect-AzureAD
$app = Get-AzureADApplication -Filter "DisplayName eq 'MCP Teams Integration'"
$app.RequiredResourceAccess
```

### Check Service Principal

```powershell
Get-AzureADServicePrincipal -Filter "DisplayName eq 'MCP Teams Integration'"
```

### Revoke Consent

```powershell
# Remove all consents (requires re-consent)
Remove-AzureADServicePrincipalOAuth2PermissionGrant -ObjectId <ObjectId>
```

## Resources

- [Azure AD App Registration](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Microsoft Graph Permissions Reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [Client Credentials Flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow)
- [Azure AD Best Practices](https://learn.microsoft.com/en-us/azure/active-directory/develop/identity-platform-integration-checklist)

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review Azure AD audit logs
3. Open an issue on GitHub
4. Contact your Azure AD administrator
