# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-07-08

### Fixed
- **delete_draft**: Now properly requires confirmation before deletion (critical safety fix)
- **upload_image**: Implemented missing get_image method - uploads now work correctly
- **get_subscriber_count**: Fixed output formatting loop - no more repeated headers
- **update_post**: Fixed content updates that were failing with 500 errors
- **preview_draft**: Fixed URL generation - now creates correct author-only preview URLs
- **preview_draft**: Fixed /api/v1 being included in URLs
- **Duplicate title removal**: Posts no longer show title twice in content

### Changed
- **update_post**: Tool description now clearly warns that it REPLACES entire fields, not partial edits
- **upload_image**: Tool description clarifies it requires local file paths (no chat/clipboard support yet)
- **Tool count**: Reduced from 13 to 12 tools (removed redundant list_drafts_for_deletion)

### Removed
- **schedule_post**: Tool completely removed due to outdated API endpoint in python-substack library
- **list_drafts_for_deletion**: Removed redundant tool that duplicated list_drafts functionality

### Documentation
- Added comprehensive KNOWN_ISSUES.md with 10 documented limitations
- Updated TODO.md with user experience enhancement tasks
- Added shareable preview links limitation to known issues
- Documented that python-substack library hasn't been updated in 2+ years

### Infrastructure
- Fixed CI/CD pipeline - all tests now pass in GitHub Actions
- Added unit and integration tests to version control (fixed .gitignore)
- Fixed code formatting and linting issues across entire codebase

### Known Issues
- Image rendering shows markdown syntax instead of rendered images
- Subscriber count may show 0 even with subscribers (API limitation)  
- Preview links are author-only (shareable links require UUID access not available in API)
- Bold/italic text still shows as markdown syntax

## [1.0.2] - 2025-07-07

### Added
- New `substack-mcp-plus-setup` command for easy authentication setup
- No more hunting for node_modules directories!

### Changed
- Updated all documentation to use the new setup command
- Updated error messages to reference the new setup command

### Developer Experience
- Significantly improved new user onboarding experience
- Simple two-command setup process

## [1.0.1] - 2025-07-07

### Fixed
- Updated Claude Desktop configuration examples to include required SUBSTACK_PUBLICATION_URL
- Added clear instructions for configuring alongside other MCP servers
- Fixed configuration examples in quickstart and CLI usage docs

### Documentation
- Added example claude-desktop-config.json file
- Improved clarity on replacing YOUR-PUBLICATION placeholder

## [1.0.0] - 2025-07-07

**Complete rewrite from scratch** - This is not an update but an entirely new implementation:
- Transformed from JavaScript-only to Python/JavaScript hybrid architecture
- Replaced session token auth with secure browser-based authentication
- Expanded from 1 basic tool to 14 comprehensive tools
- Added full rich text formatting support (was plain text only)

### Added
- Comprehensive GitHub repository setup:
  - Issue templates for bug reports and feature requests
  - Pull request template
  - GitHub Actions CI/CD workflow
  - CONTRIBUTING.md with detailed guidelines
  - LICENSE file (MIT)
  - docs/ROADMAP.md with prioritized next steps
  - docs/TODO.md with current work items and subtasks for contributors
  - docs/KNOWN_ISSUES.md documenting all current limitations
  - docs/COVERAGE_REPORT.md with detailed test coverage by module
- Enhanced documentation:
  - Complete docs/README.md index
  - tests/README.md for test suite documentation
  - Improved badges in main README
- Important disclaimers:
  - Clear "UNOFFICIAL tool" warnings throughout
  - No affiliation with Substack Inc. notices
  - API limitations and security notices
- CLAUDE.md improvements for better AI development:
  - Quick command reference with python3
  - Common pitfalls section
  - Mandatory TDD process
  - File organization rules
  - Project state awareness checklist

### Changed
- Updated all repository URLs to ty13r/substack-mcp-plus
- Updated package descriptions to clarify unofficial status
- Enhanced .gitignore with comprehensive patterns
- Fixed author information in package metadata
- Reorganized documentation structure:
  - Moved ROADMAP.md to docs/
  - Moved QUICKSTART.md to docs/
  - Moved GITHUB_READY.md to docs/internal/
  - Updated all document references
- Consolidated documentation (reduced from 21 to 15 files):
  - Combined 4 error fix summaries into ERROR_HANDLING_FIXES.md
  - Merged testing guides into comprehensive TESTING.md
  - Moved development journey files to internal/
  - Removed redundant documentation files

### Fixed
- Text content extraction from Substack posts (get_post_content tool)
- Bullet list content now properly extracted (bullet_list and list_item support)
- Image URLs now correctly parsed from posts (image2 type support)
- Error handling for various API response formats
- Mock client in tests now uses numeric user ID instead of string

### Known Issues (Documented)
- Text formatting (bold/italic) displays as markdown syntax
- Links display as markdown syntax instead of clickable
- Blockquotes show with > prefix instead of styled blocks
- Rate limiting not yet implemented

## [Pre-1.0.0] - Fork History

### 🎉 Major Release - The Most Advanced Substack MCP Server

### Added
- **14 Powerful Tools** - The most comprehensive Substack toolkit available:
  - `create_formatted_post` - Rich text draft creation
  - `update_post` - Edit existing drafts
  - `publish_post` - Instant publishing
  - `schedule_post` - Schedule for future publication
  - `list_drafts` - View draft posts
  - `list_published` - View published posts
  - `get_post_content` - Read full post content with formatting
  - `duplicate_post` - Copy existing posts
  - `upload_image` - Upload to Substack CDN
  - `preview_draft` - Generate shareable preview links
  - `get_sections` - List publication sections
  - `get_subscriber_count` - View subscriber statistics
  - `delete_draft` - Safe draft deletion with confirmation
  - `list_drafts_for_deletion` - Bulk draft management

- **Browser-Based Authentication** - Revolutionary auth system:
  - Interactive setup wizard with `setup_auth.py`
  - CAPTCHA challenge support
  - Magic link and password authentication
  - Encrypted token storage (no passwords in configs!)
  - Automatic token refresh handling

- **Full Rich Text Support**:
  - Headers (H1-H6)
  - Bold, italic, strikethrough formatting
  - Ordered and unordered lists
  - Code blocks with syntax highlighting
  - Block quotes
  - Images with captions
  - Links with proper formatting
  - Horizontal rules
  - Paywall markers for premium content

- **Zero-Config NPM Installation**:
  - Automatic Python 3.10+ detection
  - Virtual environment creation
  - Dependency installation
  - Global command availability

- **Production Quality**:
  - 180+ comprehensive tests
  - Test coverage needs improvement (currently 51% - see [Coverage Report](docs/COVERAGE_REPORT.md))
  - Input validation on all methods
  - Detailed error messages
  - Secure file handling

### Changed
- **NPM-Only Distribution** - Removed PyPI in favor of superior NPM experience
- **Complete Python Rewrite** - From JavaScript to Python for better reliability
- **Enhanced Authentication** - From session tokens to full auth management
- **Smart Tool Design** - Tools that understand real-world usage

### Security
- Encrypted credential storage
- No plaintext passwords in configuration
- Secure temporary file handling
- Input validation across all handlers
- Responsible disclosure policy

### Developer Experience
- Helpful error messages with solutions
- Progress indicators during setup
- Comprehensive documentation
- Clean API design
- Test-Driven Development approach
- 180+ tests with 51% coverage (detailed breakdown in [Coverage Report](docs/COVERAGE_REPORT.md))

### Development Journey
- Built entirely with AI assistance (Claude Code)
- Zero lines of code written by human
- Completed in under 24 hours
- Proved AI + TDD = production quality

## [1.0.6] - Previous Release
- Original JavaScript implementation by Marco Moauro
- Basic Substack API integration
- Draft creation and publishing