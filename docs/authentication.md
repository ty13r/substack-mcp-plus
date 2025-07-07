# Authentication Guide for Substack MCP Plus

This guide explains how to set up authentication for Substack MCP Plus. Our enhanced authentication system provides a **foolproof setup** that handles everything automatically, including CAPTCHA challenges and token management.

## 🚀 Quick Setup (Recommended)

The easiest way to set up authentication is using our interactive setup wizard:

```bash
python setup_auth.py
```

This wizard will:
1. ✅ Ask how you want to sign in (magic link or password)
2. ✅ Request your Substack email
3. ✅ If using password, ask for your password
4. ✅ Open a browser window for secure login
5. ✅ Handle CAPTCHA challenges if they appear
6. ✅ Extract and securely store your session token
7. ✅ Test the connection automatically
8. ✅ Configure everything for you

**That's it!** No manual token extraction, no dealing with browser developer tools, no configuration files to edit.

### Authentication Methods

#### 🔗 Magic Link (Email Code)
- Substack sends a 6-digit code to your email
- Enter the code in the browser when prompted
- No password needed - more secure!

#### 🔑 Password Authentication  
- Traditional email + password login
- The wizard automatically clicks "Sign in with password"
- Faster if you have your password ready

## 🔐 How It Works

Our authentication system uses a three-tier approach for maximum reliability:

1. **Secure Token Storage** (Primary)
   - Tokens are encrypted and stored in your system keyring
   - Automatically used when available
   - Checked for expiration and refreshed as needed

2. **Environment Variables** (Fallback)
   - Supports traditional environment variable configuration
   - Useful for CI/CD environments

3. **Automatic Fallback** (Seamless)
   - If stored token fails, tries environment variables
   - Provides clear guidance if re-authentication is needed

## 📝 Configuration

After running `setup_auth.py`, you only need to provide the publication URL in your Claude Desktop config:

```json
{
  "mcpServers": {
    "substack-mcp-plus": {
      "command": "python",
      "args": ["-m", "src.server"],
      "env": {
        "SUBSTACK_PUBLICATION_URL": "https://yourpublication.substack.com"
      }
    }
  }
}
```

**No passwords or tokens in the config!** Authentication is handled automatically.

## 🔄 Token Management

### Automatic Features
- **Secure Storage**: Tokens are encrypted using your system's keyring
- **Expiration Tracking**: Monitors token age and prompts for refresh
- **Cache Management**: Reuses authenticated sessions for performance
- **Clear Error Messages**: Helpful guidance when authentication fails

### Manual Token Refresh
If needed, simply run the setup wizard again:
```bash
python setup_auth.py
```

It will detect existing authentication and ask if you want to replace it.

## 🛠 Alternative Setup Methods

### Method 1: Environment Variables

If you prefer traditional environment variables (e.g., for CI/CD):

Create a `.env` file:
```env
SUBSTACK_EMAIL=your-email@example.com
SUBSTACK_PASSWORD=your-password
SUBSTACK_PUBLICATION_URL=https://yourpublication.substack.com
```

Or set them in your shell:
```bash
export SUBSTACK_EMAIL="your-email@example.com"
export SUBSTACK_PASSWORD="your-password"
export SUBSTACK_PUBLICATION_URL="https://yourpublication.substack.com"
```

### Method 2: Session Token (Advanced)

If you already have a session token:

```env
SUBSTACK_SESSION_TOKEN=s%3AYourLongSessionTokenHere...
SUBSTACK_PUBLICATION_URL=https://yourpublication.substack.com
```

## 🚨 Troubleshooting

### "No authentication found" Error
**Solution**: Run `python setup_auth.py`

### CAPTCHA Issues
The setup wizard handles CAPTCHA automatically. If you still have issues:
1. Clear your browser cookies for substack.com
2. Try using magic link authentication instead of password
3. Log in manually once in your browser
4. Wait 5 minutes
5. Run `python setup_auth.py` again

### Token Expired
**Solution**: Run `python setup_auth.py` to refresh

### "Authentication failed" Error
1. Verify your email is correct
2. If using password auth, verify your password is correct
3. Try using magic link authentication instead
4. Check that your publication URL includes `https://`
5. Ensure you have access to the publication

## 🔒 Security Best Practices

1. **Never commit credentials** to version control
2. **Use the setup wizard** for the most secure configuration
3. **Tokens are encrypted** in your system keyring
4. **Enable 2FA** on your Substack account
5. **Rotate passwords** periodically

## 📚 Advanced Topics

### How Tokens Are Stored

Tokens are stored using:
- **Keyring**: OS-level secure credential storage
- **Encryption**: Additional layer using Fernet symmetric encryption
- **Metadata**: Expiration tracking and email association

### Authentication Priority

The system tries authentication in this order:
1. Stored token (from setup wizard)
2. Environment session token
3. Email/password from environment
4. Clear error with setup instructions

### Token Expiration

- Tokens are set to expire after 30 days
- System checks for expiration before each use
- Automatic refresh reminders at 7 days before expiry
- Future updates will support automatic refresh

## 🎯 Summary

For 99% of users, just run:
```bash
python setup_auth.py
```

Follow the prompts, and you're done! The system handles everything else automatically.