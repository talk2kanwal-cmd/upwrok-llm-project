# Contributing to AI Customer Support Hub

Thank you for your interest in contributing to this project! This document provides guidelines for contributors.

## Getting Started

### Prerequisites
- Python 3.10+
- Git
- A Groq API key (for testing)

### Setup
1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment: `python -m venv .venv`
4. Activate it: `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and add your Groq API key

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Testing
- Write tests for new features
- Run existing tests before submitting: `python -m pytest`
- Ensure all tests pass

### Commit Messages
- Use clear, descriptive commit messages
- Format: `type(scope): description`
  - `feat`: new features
  - `fix`: bug fixes
  - `docs`: documentation
  - `style`: formatting
  - `refactor`: code refactoring
  - `test`: tests

### Pull Requests
1. Create a new branch from main: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Add tests if applicable
4. Ensure all tests pass
5. Commit your changes with clear messages
6. Push to your fork
7. Create a pull request with:
   - Clear title and description
   - Reference any related issues
   - Screenshots if UI changes

## Project Structure

```
app/
  core/          # Configuration and settings
  services/      # Business logic services
  models/        # Data models
  api/           # API endpoints
tests/           # Test files
docs/           # Documentation
```

## Areas for Contribution

- **Documentation**: Improve README, add tutorials
- **Testing**: Expand test coverage, add integration tests
- **Features**: New UI components, additional LLM providers
- **Performance**: Optimize vector search, improve response times
- **Security**: Add input validation, improve error handling

## Questions

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about contributing
- Documentation improvements

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
