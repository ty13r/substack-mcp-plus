# Security Policy

## ⚠️ Important Security Notice

**This is an UNOFFICIAL tool** that interacts with Substack's private API endpoints:
- We have no control over Substack's security measures or API changes
- Your credentials are used to authenticate directly with Substack
- We recommend using a dedicated Substack account for automation if possible
- Always comply with Substack's Terms of Service and security policies

## 🔐 Security Best Practices

When using Substack MCP Plus, please follow these security best practices:

### Environment Variables
- **Never commit your `.env` file** to version control
- Use `.env.example` as a template and create your own `.env` file
- Store credentials securely and rotate them regularly
- Consider using a secrets management service for production use

### Authentication
- **Email/Password Method** (Recommended):
  - Use a strong, unique password for your Substack account
  - Enable two-factor authentication on your Substack account if available
  
- **Session Token Method** (Alternative):
  - Session tokens expire and need to be refreshed periodically
  - Never share or expose your session tokens
  - Revoke tokens immediately if compromised

### API Usage
- Be mindful of Substack's rate limits
- Implement appropriate error handling and retry logic
- Log errors but never log credentials or sensitive data

## 🚨 Reporting Security Vulnerabilities

We take security seriously. If you discover a security vulnerability in Substack MCP Plus, please follow these steps:

### 1. Do NOT Create a Public Issue
Security vulnerabilities should be reported privately to prevent exploitation.

### 2. Report Via Email
Send details to: ruggd@proton.me

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Wait for Response
We will acknowledge receipt within 48 hours and provide an estimated timeline for a fix.

### 4. Responsible Disclosure
Please give us reasonable time to address the issue before public disclosure. We'll work with you to ensure proper credit for the discovery.

## 🛡️ Security Features

### Current Security Measures
- Environment variable-based credential management
- No hardcoded secrets in code
- Secure authentication flow with Substack API
- Input sanitization for content creation

### Planned Improvements
- [ ] Enhanced input validation across all handlers
- [ ] Secure temporary file handling with proper permissions
- [ ] Rate limiting implementation
- [ ] Request signing/validation
- [ ] Automated security scanning in CI/CD

## 📋 Security Checklist for Contributors

Before submitting a pull request:
- [ ] No credentials or secrets in code
- [ ] All user inputs are validated
- [ ] Error messages don't expose sensitive information
- [ ] Dependencies are up to date
- [ ] Security warnings from linters are addressed

## 🔄 Security Updates

Security updates will be released as soon as possible after discovery and fix. Users are encouraged to:
- Watch this repository for security advisories
- Keep dependencies up to date
- Review the changelog for security-related updates

## 📚 Additional Resources

- [OWASP Security Guidelines](https://owasp.org/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [Substack API Documentation](https://substack.com/api)

---

Thank you for helping keep Substack MCP Plus secure!