# Test Coverage Report

Last Updated: January 2025

## Overall Coverage: 51%

This document tracks test coverage across all modules to help contributors identify areas needing improvement.

## Coverage by Module

### ✅ Excellent Coverage (90-100%)
| Module | Coverage | Missing Lines | Priority |
|--------|----------|---------------|----------|
| `src/converters/block_builder.py` | 100% | None | - |
| `src/tools/upload_image_tool.py` | 100% | None | - |
| `src/__init__.py` | 100% | None | - |
| `src/converters/__init__.py` | 100% | None | - |
| `src/handlers/__init__.py` | 100% | None | - |
| `src/tools/__init__.py` | 100% | None | - |
| `src/utils/__init__.py` | 100% | None | - |
| `src/converters/markdown_converter.py` | 95% | 9 lines | Low |
| `src/converters/html_converter.py` | 90% | 14 lines | Low |
| `src/simple_auth_manager.py` | 90% | 7 lines | Low |

### 🟡 Moderate Coverage (50-89%)
| Module | Coverage | Missing Lines | Priority |
|--------|----------|---------------|----------|
| `src/handlers/image_handler.py` | 80% | 19 lines | Medium |
| `src/handlers/post_handler.py` | 62% | 235 lines | **HIGH** |
| `src/handlers/auth_handler.py` | 54% | 56 lines | **HIGH** |

### ❌ Low Coverage (0-49%)
| Module | Coverage | Missing Lines | Priority |
|--------|----------|---------------|----------|
| `src/utils/api_wrapper.py` | 26% | 124 lines | **HIGH** |
| `src/server.py` | 12% | 246 lines | Medium |
| `src/auth_manager.py` | 0% | 92 lines | **HIGH** |
| `src/server_mcp.py` | 0% | 70 lines | Low |
| `src/tools/create_formatted_post.py` | 0% | 16 lines | Medium |
| `src/tools/list_drafts.py` | 0% | 16 lines | Medium |
| `src/tools/publish_post.py` | 0% | 24 lines | Medium |
| `src/tools/update_post.py` | 0% | 19 lines | Medium |
| `src/tools/debug_post_structure.py` | 0% | 24 lines | Low |

## Priority Areas for Testing

### 🚨 Critical Priority
These modules are core to functionality and have poor coverage:

1. **`src/auth_manager.py` (0%)**
   - Handles authentication flow
   - Critical for all operations
   - 92 lines need coverage

2. **`src/utils/api_wrapper.py` (26%)**
   - Central API error handling
   - Used by all tools
   - 124 lines need coverage

3. **`src/handlers/auth_handler.py` (54%)**
   - Authentication handler
   - Missing error cases
   - 56 lines need coverage

4. **`src/handlers/post_handler.py` (62%)**
   - Core functionality
   - Largest module (615 lines)
   - 235 lines need coverage

### 🟡 Medium Priority
Important but less critical:

1. **`src/server.py` (12%)**
   - MCP server implementation
   - Large module but mostly boilerplate
   - 246 lines need coverage

2. **Tool modules (0% each)**
   - `create_formatted_post.py`
   - `list_drafts.py`
   - `publish_post.py`
   - `update_post.py`
   - Small modules, easy wins

### 🟢 Low Priority
Already well-covered or less critical:

1. **Converters** - Already 90-100% covered
2. **`src/server_mcp.py`** - Alternative server implementation
3. **`src/simple_auth_manager.py`** - Already 90% covered

## Test Failures

Current test run shows several recurring errors:
- `ValueError` in auth_handler.py:31
- `ValueError` in post_handler.py:565, 611
- `SubstackAPIError` in api_wrapper.py:112

These should be investigated and fixed before adding new tests.

## Recommendations for Contributors

### Quick Wins (Good First Issues)
1. Add tests for tool modules (16-24 lines each)
2. Cover missing lines in `simple_auth_manager.py` (7 lines)
3. Cover missing lines in converters (9-14 lines each)

### High Impact Improvements
1. Create comprehensive test suite for `auth_manager.py`
2. Expand `api_wrapper.py` tests to cover error cases
3. Add integration tests for `post_handler.py` workflows

### Testing Strategy
1. Fix failing tests first
2. Focus on high-priority modules
3. Aim for 80% coverage before adding new features
4. Write tests for bug fixes

## How to Run Coverage

```bash
# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Generate HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Run specific module tests
pytest tests/unit/test_auth_handler.py -v

# Run with markers
pytest -m "not slow" --cov=src
```

## Coverage Goals

- **Immediate**: Fix failing tests
- **Short-term**: Achieve 70% overall coverage
- **Long-term**: Maintain 90%+ coverage
- **Per PR**: No PR should decrease coverage

---

*This report should be updated regularly as coverage improves.*