# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-06

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
  - 61% code coverage
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

## [1.0.6] - Previous Release
- Original JavaScript implementation by Marco Moauro
- Basic Substack API integration
- Draft creation and publishing