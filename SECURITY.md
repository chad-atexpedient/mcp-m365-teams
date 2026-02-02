# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these steps:

### Please DO NOT:
- Open a public GitHub issue
- Disclose the vulnerability publicly before it has been addressed

### Please DO:
1. **Report via Email**: Send details to the repository maintainer
2. **Include Details**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested fixes

### What to Expect:
- **Initial Response**: Within 48 hours
- **Status Updates**: Every 7 days until resolved
- **Resolution Timeline**: We aim to address critical issues within 30 days

## Security Best Practices

When using this MCP server:

### Credentials Management
- **Never commit credentials** to version control
- Use **environment variables** for sensitive data
- Store credentials in secure secret managers
- Rotate client secrets regularly (every 90 days recommended)
- Use different credentials for dev/staging/production

### Azure AD Configuration
- Follow the **principle of least privilege**
- Only grant required API permissions
- Require admin consent for sensitive permissions
- Monitor API usage and set up alerts
- Enable conditional access policies

### Network Security
- Use **HTTPS** for all communications
- Implement IP restrictions when possible
- Enable audit logging in Azure AD
- Monitor for unusual activity patterns

### Application Security
- Keep dependencies up to date
- Run security scans regularly
- Use virtual environments
- Validate all input data
- Handle errors securely (don't expose sensitive info)

## Known Security Considerations

### Authentication
- This server uses OAuth 2.0 client credentials flow
- Tokens are obtained on-demand and cached by the SDK
- Ensure your Azure AD app is properly secured

### Permissions
Required Microsoft Graph permissions may allow broad access:
- Review permissions before granting consent
- Audit access regularly
- Remove unused permissions

### Data Handling
- Messages and data are accessed via Microsoft Graph API
- Data is not stored by the MCP server
- Ensure compliance with your organization's data policies

## Security Updates

Security updates will be:
- Released as patch versions (e.g., 0.1.1)
- Documented in CHANGELOG.md
- Announced in GitHub releases
- Tagged with `security` label

## Vulnerability Disclosure Timeline

1. **Day 0**: Vulnerability reported
2. **Day 1-2**: Initial assessment and response
3. **Day 3-7**: Investigation and fix development
4. **Day 8-14**: Testing and validation
5. **Day 15-30**: Release and disclosure

Critical vulnerabilities may be expedited.

## Security Checklist for Deployments

- [ ] Environment variables are properly secured
- [ ] Azure AD app has minimum required permissions
- [ ] Admin consent is granted
- [ ] Client secrets are stored securely
- [ ] Regular security updates are applied
- [ ] Audit logging is enabled
- [ ] Access is restricted to authorized users
- [ ] Dependencies are up to date
- [ ] Error handling doesn't leak sensitive info
- [ ] Monitoring and alerting is configured

## Third-Party Dependencies

This project relies on:
- `mcp` - Model Context Protocol SDK
- `msgraph-sdk` - Microsoft Graph Python SDK
- `azure-identity` - Azure authentication

We monitor these for security vulnerabilities and update promptly when issues are discovered.

## Compliance

When deploying this server, consider:
- GDPR compliance for EU users
- HIPAA compliance for healthcare data
- SOC 2 requirements
- Your organization's security policies

## Resources

- [Microsoft Graph Security Documentation](https://learn.microsoft.com/en-us/graph/security-concept-overview)
- [Azure AD Best Practices](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/security-best-practices)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)

## Contact

For security concerns, please contact the repository maintainers.

Thank you for helping keep this project secure!
