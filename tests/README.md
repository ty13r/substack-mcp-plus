# Test Suite Documentation

This directory contains all tests for the Substack MCP Plus project. We practice Test-Driven Development (TDD) to ensure code quality and reliability.

## Test Structure

```
tests/
├── unit/                  # Unit tests for individual components
│   ├── test_auth_handler.py
│   ├── test_block_builder.py
│   ├── test_html_converter.py
│   ├── test_image_handler.py
│   ├── test_markdown_converter.py
│   ├── test_post_handler.py
│   └── test_upload_image_tool.py
├── integration/          # Integration tests for end-to-end workflows
│   └── ... (various integration test files)
└── test_*.py            # Additional test files for specific features
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage report
```bash
pytest --cov=src --cov-report=html
```

### Run specific test file
```bash
pytest tests/unit/test_markdown_converter.py
```

### Run tests matching a pattern
```bash
pytest -k "test_create"
```

### Run tests with verbose output
```bash
pytest -v
```

## Test Categories

### Unit Tests (`tests/unit/`)
- Test individual components in isolation
- Mock external dependencies
- Fast execution
- High coverage of edge cases

### Integration Tests (`tests/integration/`)
- Test complete workflows
- Use real Substack API (in test mode)
- Verify end-to-end functionality
- May be slower due to network calls

## Writing Tests

Follow these guidelines when writing tests:

1. **Test-Driven Development**: Write tests before implementation
2. **Descriptive Names**: Use clear, descriptive test function names
3. **Arrange-Act-Assert**: Structure tests with clear sections
4. **One Assertion**: Prefer one assertion per test when possible
5. **Edge Cases**: Always test edge cases and error conditions

Example test structure:
```python
async def test_create_formatted_post_with_markdown():
    """Test creating a post with markdown formatting"""
    # Arrange
    handler = PostHandler()
    title = "Test Post"
    content = "**Bold** and *italic*"
    
    # Act
    result = await handler.create_formatted_post(
        title=title,
        content=content,
        content_type="markdown"
    )
    
    # Assert
    assert result["success"] is True
    assert result["title"] == title
```

## Coverage Goals

We aim for:
- Overall coverage: >80%
- Critical paths: 100%
- Error handling: 100%
- New features: Must include tests

View coverage report:
```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## Continuous Integration

Tests run automatically on:
- Every push to main branch
- Every pull request
- Multiple Python versions (3.10, 3.11, 3.12)
- Multiple Node versions (18.x, 20.x)

See `.github/workflows/ci.yml` for CI configuration.