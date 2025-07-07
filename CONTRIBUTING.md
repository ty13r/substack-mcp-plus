# Contributing to Substack MCP Plus

First off, thank you for considering contributing to Substack MCP Plus! It's people like you that make Substack MCP Plus such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

**Explain the problem and include additional details to help maintainers reproduce the problem:**

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible
* Include your environment details (OS, Python version, Node version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### What to Work On

Check our [TODO.md](docs/TODO.md) for current work items with detailed subtasks you can claim.
Also see [ROADMAP.md](docs/ROADMAP.md) for longer-term features and improvements.

We especially welcome:
* Bug fixes (always high priority)
* **Test coverage improvements** (currently 51% - see [Coverage Report](docs/COVERAGE_REPORT.md))
* Text formatting fixes
* Rate limiting implementation
* Documentation enhancements

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Include screenshots and animated GIFs in your pull request whenever possible
* Follow the Python and JavaScript style guides
* Include thoughtfully-worded, comprehensive commit messages
* Document new code
* End all files with a newline

## Development Process

### Setting Up Your Development Environment

1. Fork the repo and create your branch from `main`
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/substack-mcp-plus.git
   cd substack-mcp-plus
   ```

3. Install dependencies:
   ```bash
   npm install
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks (optional but recommended):
   ```bash
   pre-commit install
   ```

### Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards

3. Write or update tests as needed

4. Run tests to ensure everything passes:
   ```bash
   pytest
   npm test  # if applicable
   ```

5. Format your code:
   ```bash
   black src tests
   mypy src
   ```

### Coding Standards

#### Python Code Style

* Follow PEP 8
* Use Black for formatting (line length: 88)
* Use type hints where possible
* Write descriptive docstrings for all public functions and classes
* Keep functions focused and small
* Prefer descriptive variable names

#### JavaScript Code Style

* Use ES6+ features
* Use meaningful variable and function names
* Add JSDoc comments for functions
* Keep functions small and focused

#### General Guidelines

* **ABOUTME Comments**: All code files should start with two "ABOUTME:" comment lines explaining what the file does
* **No Mocks**: We use real data and real APIs - never implement mock modes
* **Error Handling**: Always handle errors gracefully with informative messages
* **Security**: Never commit secrets, API keys, or sensitive information

### Testing

* **Write Tests First (TDD)**: We practice Test-Driven Development
  1. Write a failing test
  2. Write minimal code to make it pass
  3. Refactor while keeping tests green
  
* **Test Coverage**: Aim for high test coverage
  ```bash
  pytest --cov=src
  ```

* **Test Types**: Include unit tests, integration tests, and end-to-end tests

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider using [conventional commits](https://www.conventionalcommits.org/)

Example:
```
feat: add support for scheduling posts

- Add schedule_post tool to MCP server
- Update post handler to support scheduled_at parameter
- Add tests for scheduling functionality

Fixes #123
```

### Documentation

* Update the README.md if you change functionality
* Update or add documentation in the docs/ folder as needed
* Keep examples up to date
* Document any new environment variables or configuration options

## Project Structure

```
substack-mcp-plus/
├── src/                 # Source code
│   ├── converters/      # Format converters
│   ├── handlers/        # API handlers
│   ├── tools/           # MCP tool implementations
│   └── server.py        # Main MCP server
├── tests/               # Test suite
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── docs/               # Documentation
└── scripts/            # Utility scripts
```

## Release Process

1. Update version in package.json and pyproject.toml
2. Update CHANGELOG.md
3. Create a pull request with version bump
4. After merge, create a GitHub release
5. The package will be automatically published to NPM

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## Attribution

This project was originally forked from [substack-mcp](https://github.com/marcomoauro/substack-mcp) by Marco Moauro. We're grateful for the foundation it provided!

Thank you for contributing! 🎉