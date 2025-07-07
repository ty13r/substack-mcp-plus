# 🧪 Comprehensive Testing Suite

The Substack MCP Plus project includes an extensive testing suite that was crucial during development, especially when troubleshooting authentication issues and ensuring all formatting features work correctly.

## 📁 Test Structure

```
tests/
├── unit/                      # Unit tests for individual components
│   ├── test_block_builder.py  # Tests for BlockBuilder
│   ├── test_markdown_converter.py  # Tests for MarkdownConverter
│   └── test_html_converter.py # Tests for HTMLConverter
├── integration/               # Integration tests
│   ├── test_create_post_flow.py  # End-to-end post creation
│   ├── test_auth_flow.py      # Authentication workflows
│   └── test_formatting_integration.py  # Formatting tests
└── debug/                     # Debug utilities (not in repo)
```

## 🚀 Quick Setup

### Automated Setup (Recommended)
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

### Helper Scripts

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

## 🚀 Running Tests

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=src --cov-report=html
# View coverage report at htmlcov/index.html
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_markdown_converter.py

# Specific test function
pytest tests/unit/test_markdown_converter.py::test_parse_bold_text
```

### Run with Verbose Output
```bash
pytest -v  # Show test names
pytest -vv # Show detailed assertions
pytest -s  # Show print statements
```

## 🔍 Key Test Files

### Unit Tests

#### `test_block_builder.py`
Tests all block creation methods:
- Paragraph blocks
- Heading blocks (H1-H6)
- List blocks (ordered/unordered)
- Code blocks
- Image blocks
- Blockquote blocks
- Horizontal rule blocks
- Paywall blocks

#### `test_markdown_converter.py`
Tests markdown parsing and conversion:
- Inline formatting (bold, italic, code)
- Links and images
- Headers
- Lists (including nested)
- Code blocks with language detection
- Blockquotes
- Edge cases (empty content, malformed markdown)

#### `test_html_converter.py`
Tests HTML to Substack block conversion:
- Basic HTML tags
- Nested structures
- Attributes handling
- Entity decoding

### Integration Tests

#### `test_create_post_flow.py`
End-to-end testing of post creation:
- Draft creation with various content types
- Publishing workflow
- Scheduling posts
- Error handling

#### `test_auth_flow.py`
Authentication testing:
- Email/password authentication
- Session token authentication
- Cookie handling
- Error scenarios

#### `test_formatting_integration.py`
Comprehensive formatting tests:
- Mixed content types
- Complex nested structures
- Special characters
- Large content handling

## 🛠️ Testing Utilities

During development, we created several helpful testing utilities:

### `debug_auth.py`
Standalone authentication tester:
```python
python debug_auth.py
```
- Tests authentication methods
- Validates credentials
- Shows detailed error messages

### `generate_test_content.py`
Generates test posts with various content:
```python
python generate_test_content.py
```
- Creates posts with all formatting options
- Tests edge cases
- Useful for manual testing

### `health_check.py`
System health checker:
```python
python health_check.py
```
- Verifies Python version
- Checks dependencies
- Tests API connectivity

## 📊 Test Coverage

The test suite achieves high coverage:
- BlockBuilder: 100%
- MarkdownConverter: 95%+
- HTMLConverter: 90%+
- Authentication handlers: 85%+
- Post handlers: 90%+

## ✅ Test Patterns

### Fixture Usage
```python
@pytest.fixture
def auth_handler():
    """Provide authenticated handler for tests"""
    return AuthHandler()

def test_create_post(auth_handler):
    # Use the fixture
    client = auth_handler.authenticate()
```

### Mocking External Services
```python
@mock.patch('src.handlers.auth_handler.SubstackApi')
def test_auth_without_network(mock_api):
    # Test without hitting real API
    mock_api.return_value.login.return_value = True
```

### Parametrized Tests
```python
@pytest.mark.parametrize("markdown,expected", [
    ("**bold**", [{"type": "text", "content": "bold", "marks": [{"type": "strong"}]}]),
    ("*italic*", [{"type": "text", "content": "italic", "marks": [{"type": "em"}]}]),
])
def test_inline_formatting(markdown, expected):
    result = converter.parse_inline_formatting(markdown)
    assert result == expected
```

## 🐛 Debugging Tips

1. **Use pytest's built-in debugger**:
   ```bash
   pytest --pdb  # Drop into debugger on failure
   ```

2. **Capture print output**:
   ```bash
   pytest -s  # Show all print statements
   ```

3. **Run specific test with extra verbosity**:
   ```bash
   pytest -vv tests/unit/test_markdown_converter.py::test_parse_bold_text
   ```

4. **Generate detailed failure reports**:
   ```bash
   pytest --tb=long  # Long traceback format
   pytest --tb=short # Short traceback format
   ```

## 🏆 Testing Best Practices

1. **Test file naming**: All test files start with `test_`
2. **Test function naming**: Descriptive names like `test_parse_bold_text_with_spaces`
3. **Arrange-Act-Assert**: Clear test structure
4. **One assertion per test**: When possible
5. **Mock external dependencies**: Don't hit real APIs in unit tests
6. **Use fixtures**: For common setup code
7. **Test edge cases**: Empty inputs, special characters, large data

## 🚨 Common Test Scenarios

### Authentication Issues
```python
def test_captcha_error_handling():
    """Test handling of CAPTCHA challenges"""
    # This was crucial during development
```

### Content Display Issues
```python
def test_empty_post_prevention():
    """Ensure posts never appear empty"""
    # Helped identify the formatting issues
```

### Formatting Edge Cases
```python
def test_nested_formatting():
    """Test bold inside links, etc."""
    # Found several parser bugs
```

## 🔄 Continuous Testing

For development, use pytest-watch:
```bash
pip install pytest-watch
ptw  # Runs tests automatically on file changes
```

## 📝 Adding New Tests

When adding features:
1. Write tests first (TDD approach)
2. Test both success and failure cases
3. Include edge cases
4. Update this documentation

## 🖥️ Claude Desktop Testing

### Setting Up Claude Desktop

1. **Install Claude Desktop**
   - Download from [claude.ai/desktop](https://claude.ai/desktop)
   - Install and log in with your Claude account

2. **Configure MCP Server**
   
   Find your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

   Add our server configuration:
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

3. **Restart Claude Desktop** (required after config changes)

### Pre-Test Setup

```bash
# Kill any existing MCP processes
pkill -f substack-mcp-plus

# Clear any test drafts from your Substack account (optional)
# Log into Substack web UI and delete test drafts

# Verify authentication is set up
python debug_auth.py
```

### Testing All 14 Tools

#### Tool 1: create_formatted_post ✅
**Test the confirmation system and rich formatting**

```
Test 1A - Basic Creation with Confirmation:
1. Say: "Create a new Substack draft with the title 'Test Post 1' and content 'This is a test'"
2. EXPECT: Confirmation warning appears
3. Say: "No" 
4. VERIFY: Draft is NOT created
5. Repeat step 1, then say "Yes"
6. VERIFY: Draft is created successfully

Test 1B - Rich Formatting:
Create a draft with complex formatting including headers, bold/italic, lists, code blocks, blockquotes, and paywall markers.
```

#### Tool 2: list_drafts ✅
**No confirmation needed - read-only operation**
- Test listing recent drafts
- Test listing with limit

#### Tool 3: update_post ✅
**Test partial updates and confirmation**
- Update subtitle only
- Update title only
- Update multiple fields
- Verify confirmation shows only fields being changed

#### Tool 4: get_post_content ✅
**Read-only operation - no confirmation needed**
- Read draft content with full formatting

#### Tool 5: duplicate_post ✅
**Test duplication with confirmation**
- Duplicate with default "Copy of" title
- Duplicate with custom title

#### Tool 6: preview_draft ✅
**Read-only - generates preview link**
- Generate preview URL and verify it works

#### Tool 7: schedule_post ⚠️
**Test scheduling with confirmation**
- Schedule for future date/time
- Verify confirmation shows formatted date and warning

#### Tool 8: publish_post ⚠️
**DANGER: This sends emails! Use test account if possible**
- Test confirmation shows subscriber count and "CANNOT be undone" warning
- Only actually publish if using test account

#### Tool 9: upload_image ✅
**No confirmation needed**
- Upload local image file
- Verify CDN URL is returned and works

#### Tool 10: delete_draft ✅
**Already has built-in confirmation**
- Test deletion with confirmation parameter

#### Tool 11: list_drafts_for_deletion ✅
**Read-only - lists drafts with deletion instructions**

#### Tool 12: list_published ✅
**Read-only operation**

#### Tool 13: get_sections ✅
**Read-only operation**

#### Tool 14: get_subscriber_count ✅
**Read-only operation**

### Final Verification Checklist

- [ ] All 14 tools appear in Claude Desktop
- [ ] Confirmation prompts work for all protected tools
- [ ] Saying "no" cancels operations
- [ ] Saying "yes" proceeds with operations
- [ ] Partial updates only change specified fields
- [ ] Rich text formatting is preserved
- [ ] Paywall markers work correctly
- [ ] Error messages are helpful
- [ ] Preview links are functional
- [ ] Image uploads return valid URLs
- [ ] No tools execute without appropriate confirmation

## 🚑 Troubleshooting

### Quick Diagnosis

**First, run the health check:**
```bash
python health_check.py
```

This will identify most common issues automatically!

### Common Issues and Solutions

#### "Module not found" Error
```bash
# Solutions:
pip install -e .
# Ensure virtual environment is activated
source venv/bin/activate
# Force reinstall if needed
python -m pip install --force-reinstall -e .
```

#### Authentication Fails
```bash
# Quick diagnosis
python debug_auth.py

# Solutions:
- Check .env has no extra spaces or quotes
- Try session token method (more reliable)
- Verify publication URL is correct
- Ensure account has publication access
```

#### "No MCP tools available" in Claude
1. Check config location is correct
2. Verify Python path in config ("python" or "python3")
3. Check absolute path to project in "cwd"
4. **Restart Claude Desktop** (required after config changes)

#### Session Token Issues
1. Get fresh tokens from browser (F12 → Application → Cookies)
2. Copy new `substack.sid` and `substack.uid`
3. Update `.env` with new values
4. Test with: `python debug_auth.py`

### Platform-Specific Issues

**macOS**
- If `python` command not found, use `python3`
- May need to allow terminal access in Security settings

**Windows**
- Use `python` not `python3`
- Run as Administrator if permission errors
- Use PowerShell, not Command Prompt

**Linux**
- May need `python3-venv` package: `sudo apt install python3-venv`
- Check firewall isn't blocking connections

## 📋 Test Content Files

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

The comprehensive test suite was instrumental in achieving a reliable, production-ready MCP server. It caught numerous edge cases and helped us iterate quickly during the development process.