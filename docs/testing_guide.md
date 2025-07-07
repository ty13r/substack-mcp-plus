# Substack MCP Plus - Testing Guide

## Welcome, Tester! 👋

This guide will walk you through testing the Substack MCP Plus server, even if you've never tested an MCP server before. We'll start from the very basics and guide you through every step.

## Table of Contents
1. [What is MCP?](#what-is-mcp)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [Understanding the Project](#understanding-the-project)
5. [Running Automated Tests](#running-automated-tests)
6. [Setting Up Claude Desktop](#setting-up-claude-desktop)
7. [Manual Testing Checklist](#manual-testing-checklist)
8. [Troubleshooting](#troubleshooting)

## What is MCP?

MCP (Model Context Protocol) is a way for AI assistants like Claude to interact with external tools and services. Think of it as giving Claude superpowers to:
- Create blog posts on Substack
- Upload images
- Format text with rich styling
- Manage drafts and publications

Our server acts as a bridge between Claude and Substack's API.

## Prerequisites

Before we begin, you'll need:

1. **A computer with**:
   - macOS, Windows, or Linux
   - Internet connection
   - Terminal/Command Prompt access

2. **Software to install**:
   - Python 3.8 or higher
   - Claude Desktop app
   - Git (for cloning the repository)

3. **Accounts**:
   - Substack account with a publication
   - Claude account (for Claude Desktop)

## Environment Setup

### 🚀 Quick Setup (Recommended)

We've created an automated setup script that handles everything for you!

```bash
# Clone the repository
git clone [repository-url]
cd substack-mcp-plus

# Run the automated setup
./setup.sh
```

The setup script will:
- ✅ Check Python version (3.8+ required)
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create .env file from template
- ✅ Run basic tests to verify installation

### Manual Setup (Alternative)

<details>
<summary>Click here for manual setup steps</summary>

#### Step 1: Install Python

**macOS/Linux:**
```bash
# Check if Python is installed
python3 --version

# If not installed, install it:
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip
```

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer (CHECK "Add Python to PATH")
3. Open Command Prompt and verify:
```cmd
python --version
```

#### Step 2: Clone and Setup

```bash
# Clone the repository
git clone [repository-url]
cd substack-mcp-plus

# Create a virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -e .
pip install pytest pytest-asyncio pytest-cov
```

</details>

### Configure Environment Variables

1. The setup script creates `.env` from `.env.example`. Edit it:
```bash
# Open in your text editor
nano .env  # or code .env or vim .env
```

2. Fill in your Substack credentials (see `.env.example` for detailed instructions):
```env
# Required: Your Substack publication URL
SUBSTACK_PUBLICATION_URL=https://yourpublication.substack.com

# Option 1: Session Token (Recommended - avoids CAPTCHA)
SUBSTACK_SESSION_TOKEN=s%3AYourSessionTokenHere...

# Option 2: Email/Password (may trigger CAPTCHA)
SUBSTACK_EMAIL=your-email@example.com
SUBSTACK_PASSWORD=your-password
```

### How to Get Session Token:

#### Option A: Automatic (Recommended)
```bash
# Set email/password in .env first, then run:
python3 get_session_token.py
```

#### Option B: Manual Browser Extraction
1. Log into Substack in your browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies → substack.com
4. Find `substack.sid` (starts with `s%3A`)
5. Copy the full value to your .env file

### 🔍 Verify Your Setup

After setup, run these helper scripts:

```bash
# 1. Check system health
python health_check.py

# 2. Test authentication
python debug_auth.py

# 3. Generate test content
python generate_test_content.py
```

## Understanding the Project

### Key Components

1. **Converters**: Transform content to Substack format
   - `MarkdownConverter`: Converts Markdown to Substack blocks
   - `HTMLConverter`: Converts HTML to Substack blocks
   - `BlockBuilder`: Creates Substack content blocks

2. **Handlers**: Manage core functionality
   - `AuthHandler`: Handles authentication
   - `PostHandler`: Creates and manages posts
   - `ImageHandler`: Uploads images to CDN

3. **Tools**: MCP tools that Claude can use
   - `create_formatted_post`: Create rich text posts
   - `update_post`: Modify existing drafts
   - `publish_post`: Publish or schedule posts
   - `list_drafts`: View draft posts
   - `upload_image`: Upload images

## Helper Scripts

We've created several helper scripts to make testing easier:

### 📋 Available Scripts

1. **`setup.sh`** - Automated environment setup
   ```bash
   ./setup.sh  # Sets up everything in one command
   ```

2. **`health_check.py`** - System health verification
   ```bash
   python health_check.py
   ```
   Checks:
   - ✅ Python version
   - ✅ Dependencies installed
   - ✅ Project structure
   - ✅ Environment configuration
   - ✅ Claude Desktop setup
   - ✅ Network connectivity

3. **`debug_auth.py`** - Authentication testing
   ```bash
   python debug_auth.py
   ```
   Features:
   - Tests both auth methods
   - Lists your drafts
   - Optionally creates a test post
   - Color-coded output

4. **`generate_test_content.py`** - Create test files
   ```bash
   python generate_test_content.py
   ```
   Generates:
   - Basic formatting examples
   - Complex nested content
   - Edge cases
   - Real-world blog posts
   - Newsletter templates

## Running Automated Tests

### Basic Test Run

```bash
# Run all tests (105 tests)
python -m pytest

# Run with verbose output
python -m pytest -v

# Run with coverage report
python -m pytest --cov=src --cov-report=term-missing
```

### Understanding Test Output

Good output looks like:
```
============================= test session starts ==============================
collected 105 items

tests/unit/test_auth_handler.py::TestAuthHandler::test_init_with_email_password PASSED
...
============================== 105 passed in 0.29s =============================
```

If tests fail, you'll see:
```
FAILED tests/unit/test_auth_handler.py::TestAuthHandler::test_init_with_email_password
```

### Running Specific Tests

```bash
# Run only unit tests
python -m pytest tests/unit/

# Run only integration tests
python -m pytest tests/integration/

# Run tests for a specific component
python -m pytest tests/unit/test_markdown_converter.py

# Run a specific test
python -m pytest tests/unit/test_auth_handler.py::TestAuthHandler::test_init_with_email_password
```

## Setting Up Claude Desktop

### Step 1: Install Claude Desktop

1. Download from [claude.ai/desktop](https://claude.ai/desktop)
2. Install and log in with your Claude account

### Step 2: Configure MCP Server

1. Find your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add our server configuration:
```json
{
  "mcpServers": {
    "substack": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/substack-mcp-plus",
      "env": {
        "SUBSTACK_PUBLICATION_URL": "https://yourpublication.substack.com",
        "SUBSTACK_EMAIL": "your-email@example.com",
        "SUBSTACK_PASSWORD": "your-password"
      }
    }
  }
}
```

3. Restart Claude Desktop

### Step 3: Verify Connection

In Claude Desktop, type:
```
What MCP tools do you have available?
```

Claude should list our 5 tools:
- create_formatted_post
- update_post  
- publish_post
- list_drafts
- upload_image

## Manual Testing Checklist

### 🧪 Test 0: Pre-Flight Check

**Before testing with Claude, verify everything works**

```bash
# Run the comprehensive health check
python health_check.py

# Test authentication independently
python debug_auth.py
```

If both pass, you're ready for Claude Desktop testing!

### 🧪 Test 1: Authentication

**Test both authentication methods work correctly**

1. **Email/Password Auth**:
   - Configure `.env` with email/password only
   - Ask Claude: "List my draft posts"
   - ✅ Should see draft posts or "No drafts found"
   - ❌ Should NOT see authentication errors

2. **Session Token Auth**:
   - Configure `.env` with session token/user ID only
   - Ask Claude: "List my draft posts"
   - ✅ Should work the same as email/password

### 🧪 Test 2: Create Formatted Post

**Test creating posts with different content types**

1. **Using Generated Test Content**:
   ```
   Create a post from test_content/basic_formatting.md
   ```
   - ✅ Should handle all basic markdown elements
   - ✅ Check formatting in Substack dashboard

2. **Technical Blog Post**:
   ```
   Create a post from test_content/technical_post.md
   ```
   - ✅ Code blocks with syntax highlighting
   - ✅ Complex nested lists and formatting

3. **HTML Content**:
   ```
   Create a post from test_content/complex_html.html
   ```
   - ✅ Should convert HTML to Substack blocks

4. **Edge Cases**:
   ```
   Create a post from test_content/format_chaos.md
   ```
   - ✅ Should handle nested formatting gracefully
   - ✅ Special characters should work

5. **Paywall Post**:
   ```
   Create a post from test_content/paywall_post.md
   ```
   - ✅ Content after <!--paywall--> should be marked as premium

### 🧪 Test 3: Update Post

**Test updating existing drafts**

1. **Update Title**:
   ```
   Update the draft titled "Test Post" with a new title "Updated Test Post"
   ```
   - ✅ Title should change in Substack

2. **Update Content**:
   ```
   Update the content of my latest draft to add a new paragraph
   ```
   - ✅ Content should be updated

### 🧪 Test 4: Publish Post

**Test publishing and scheduling**

1. **Immediate Publish**:
   ```
   Publish my draft titled "Test Post"
   ```
   - ✅ Post should go live immediately
   - ✅ Should appear on your Substack

2. **Scheduled Publish** (if supported):
   ```
   Schedule my draft "Test Post" for tomorrow at 9 AM
   ```
   - ✅ Post should be scheduled

### 🧪 Test 5: List Drafts

**Test listing functionality**

1. **Basic List**:
   ```
   Show me my draft posts
   ```
   - ✅ Should list all drafts with titles and dates

2. **With Limit**:
   ```
   Show me my 5 most recent drafts
   ```
   - ✅ Should show maximum 5 drafts

### 🧪 Test 6: Upload Image

**Test image upload functionality**

1. **Local File Upload**:
   ```
   Upload the image at /path/to/test-image.jpg
   ```
   - ✅ Should return CDN URL
   - ✅ URL should load in browser

2. **URL Upload**:
   ```
   Upload this image: https://picsum.photos/800/400
   ```
   - ✅ Should download and upload to Substack CDN

3. **Optimization Levels**:
   ```
   Upload image.jpg optimized for email
   Upload image.jpg as a thumbnail
   ```
   - ✅ Should return different sized images

### 🧪 Test 7: Error Handling

**Test that errors are handled gracefully**

1. **Invalid Credentials**:
   - Use wrong password in `.env`
   - ✅ Should see clear error message

2. **Network Issues**:
   - Disconnect internet
   - Try creating a post
   - ✅ Should see network error message

3. **Invalid Content**:
   ```
   Create a post with content type "invalid"
   ```
   - ✅ Should see helpful error message

## Troubleshooting

### 🚑 Quick Diagnosis

**First, run the health check:**
```bash
python health_check.py
```

This will identify most common issues automatically!

### Common Issues and Solutions

#### 1. "Module not found" Error
```bash
ModuleNotFoundError: No module named 'src'
```
**Solutions**:
- ✅ Run: `pip install -e .`
- ✅ Ensure virtual environment is activated: `source venv/bin/activate`
- ✅ If still failing: `python -m pip install --force-reinstall -e .`

#### 2. Authentication Fails
```
Authentication failed: Invalid credentials
```
**Quick Fix with Debug Script:**
```bash
python debug_auth.py  # This will show exactly what's wrong
```

**Manual Solutions**:
- ✅ Check `.env` has no extra spaces or quotes
- ✅ Try session token method (more reliable)
- ✅ Verify publication URL is correct
- ✅ Ensure account has publication access

#### 3. "No MCP tools available" in Claude
**Solutions**:
1. Check config location is correct:
   ```bash
   # macOS
   ls ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows
   dir %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Verify Python path in config:
   ```json
   "command": "python"  # or "python3" on some systems
   ```

3. Check absolute path to project:
   ```json
   "cwd": "/absolute/path/to/substack-mcp-plus"
   ```

4. **Restart Claude Desktop** (required after config changes)

#### 4. Virtual Environment Issues
```bash
'venv' is not recognized  # or similar
```
**Solutions**:
- ✅ Create venv: `python3 -m venv venv`
- ✅ Activate it:
  - macOS/Linux: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- ✅ Verify activated: `which python` should show venv path

#### 5. Import Errors
```python
ImportError: cannot import name 'Api' from 'substack'
```
**Solutions**:
- ✅ Update dependencies: `pip install --upgrade python-substack`
- ✅ Clear cache: `find . -type d -name __pycache__ -exec rm -r {} +`
- ✅ Reinstall everything: `pip install -e . --force-reinstall`

#### 6. Session Token Issues
```
Session token expired or invalid
```
**Solutions**:
1. Get fresh tokens from browser:
   - Open Substack in browser
   - F12 → Application → Cookies
   - Copy new `substack.sid` and `substack.uid`
2. Update `.env` with new values
3. Test with: `python debug_auth.py`

### Advanced Debugging

#### 1. Enable Verbose Logging
```bash
# In .env
LOG_LEVEL=DEBUG

# Or when running
LOG_LEVEL=DEBUG python -m src.server
```

#### 2. Test Server Manually
```bash
# See all output
python -m src.server

# Test specific component
python -c "
from src.handlers.auth_handler import AuthHandler
h = AuthHandler()
print('Auth handler created successfully')
"
```

#### 3. Check Dependencies
```bash
# List all installed packages
pip list | grep -E "(substack|mcp|markdown|pydantic)"

# Verify versions match requirements
pip show python-substack mcp
```

#### 4. Reset Everything
If all else fails, start fresh:
```bash
# Backup your .env
cp .env .env.backup

# Clean install
rm -rf venv __pycache__ .pytest_cache
./setup.sh

# Restore .env
cp .env.backup .env
```

### Platform-Specific Issues

#### macOS
- If `python` command not found, use `python3`
- May need to allow terminal access in Security settings

#### Windows
- Use `python` not `python3`
- Run as Administrator if permission errors
- Use PowerShell, not Command Prompt

#### Linux
- May need `python3-venv` package: `sudo apt install python3-venv`
- Check firewall isn't blocking connections

## Test Reporting

After completing all tests, create a report with:

1. **Test Summary**:
   - Total tests run
   - Passed/Failed counts
   - Any blocked tests

2. **Issues Found**:
   - Description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

3. **Environment Info**:
   - OS version
   - Python version
   - Claude Desktop version

## Quick Reference

### 🚀 Essential Commands

```bash
# Initial setup
./setup.sh

# Pre-flight checks
python health_check.py
python debug_auth.py

# Generate test content
python generate_test_content.py

# Run tests
python -m pytest                    # All tests
python -m pytest -v                 # Verbose
python -m pytest --cov=src          # With coverage

# Manual server test
python -m src.server
```

### 📝 Test Content Files

After running `generate_test_content.py`:

| File | Description | Tests |
|------|-------------|-------|
| `basic_formatting.md` | All basic markdown elements | Headers, lists, links, images |
| `nested_formatting.md` | Complex nested structures | Bold/italic in lists, quotes |
| `paywall_post.md` | Premium content example | Paywall marker handling |
| `complex_html.html` | Nested HTML elements | HTML to blocks conversion |
| `format_chaos.md` | Edge cases and special chars | Parser robustness |
| `technical_post.md` | Real blog post example | Code blocks, tables |
| `newsletter.md` | Newsletter format | Mixed content types |

### 🔧 Config Paths

**Claude Desktop Config:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`  
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Environment File:**
- `.env` (create from `.env.example`)

## Conclusion

Congratulations! You've completed the testing guide. 

### ✅ Testing Checklist Summary

- [ ] Run `./setup.sh` for environment setup
- [ ] Configure `.env` with credentials
- [ ] Run `python health_check.py`
- [ ] Test auth with `python debug_auth.py`
- [ ] Generate content with `python generate_test_content.py`
- [ ] Configure Claude Desktop
- [ ] Complete manual testing checklist
- [ ] Document any issues found

### 📚 Additional Resources

- **[QUICKSTART.md](QUICKSTART.md)** - For experienced developers
- **[README.md](README.md)** - Project overview
- **[AUTHENTICATION.md](AUTHENTICATION.md)** - Auth details
- **[FORMATTING.md](FORMATTING.md)** - Content formatting guide
- **[RETROSPECTIVE.md](RETROSPECTIVE.md)** - Development journey

Happy testing! 🎉

---

**Need Help?**
1. Run `python health_check.py` for diagnosis
2. Check troubleshooting section above
3. Review error messages carefully - they're designed to be helpful!