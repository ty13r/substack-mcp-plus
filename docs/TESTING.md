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

The comprehensive test suite was instrumental in achieving a reliable, production-ready MCP server. It caught numerous edge cases and helped us iterate quickly during the development process.