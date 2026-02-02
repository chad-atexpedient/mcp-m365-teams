# Contributing to MCP M365 Teams

Thank you for your interest in contributing to the MCP M365 Teams server! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## Getting Started

1. **Fork the Repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp-m365-teams.git
   cd mcp-m365-teams
   ```

3. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Making Changes

1. Make your changes in your feature branch
2. Write or update tests as needed
3. Ensure your code follows the project's style guidelines
4. Run tests and linting

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/mcp_m365_teams

# Run specific test file
pytest tests/test_server.py -v
```

### Code Style

We use several tools to maintain code quality:

```bash
# Format code with black
black src/ tests/

# Check for linting issues
ruff check src/ tests/

# Type checking
mypy src/ --ignore-missing-imports
```

### Before Submitting

1. **Run all tests**: `pytest`
2. **Format code**: `black src/ tests/`
3. **Check linting**: `ruff check src/ tests/`
4. **Update documentation**: If you've changed functionality, update the README
5. **Write clear commit messages**: Use descriptive commit messages

## Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add support for Teams meeting creation

- Implement create_meeting tool
- Add meeting configuration options
- Update documentation with examples

Fixes #123
```

## Pull Request Process

1. **Update the README** with details of changes if applicable
2. **Update tests** to cover your changes
3. **Ensure CI passes** - all tests and linting checks must pass
4. **Request review** from maintainers
5. **Address feedback** promptly and professionally

### Pull Request Template

When creating a PR, please include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you've added or run

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
```

## Adding New Features

When adding a new tool or feature:

1. **Implement the tool** in `server.py`
2. **Add to the tool list** in the `list_tools()` handler
3. **Add handler** in the `call_tool()` method
4. **Write tests** in `tests/test_server.py`
5. **Update README** with usage examples
6. **Add API permissions** documentation if needed

### Example: Adding a New Tool

```python
# In list_tools():
types.Tool(
    name="my_new_tool",
    description="Description of what it does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Description of param1",
            },
        },
        "required": ["param1"],
    },
)

# In call_tool():
elif name == "my_new_tool":
    result = await self._my_new_tool(arguments["param1"])

# Implement the method:
async def _my_new_tool(self, param1: str) -> dict:
    """Implementation"""
    # Your code here
    return {"result": "success"}
```

## Testing Guidelines

- Write tests for all new features
- Maintain or improve code coverage
- Use meaningful test names
- Mock external API calls
- Test both success and error cases

## Documentation

- Keep README.md up to date
- Document all new tools and parameters
- Include usage examples
- Update CHANGELOG.md for significant changes

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in the project documentation and release notes.

Thank you for contributing! 🎉
