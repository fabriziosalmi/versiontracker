# Contributing to GitHub Version Tracker

First off, thank you for considering contributing to GitHub Version Tracker! It's people like you that make this tool better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Adding New Features](#adding-new-features)
- [Reporting Bugs](#reporting-bugs)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. With parameters '...'
3. See error

**Expected behavior**
A clear description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g., Ubuntu 22.04, macOS 13, Windows 11]
 - Python Version: [e.g., 3.9.7]
 - Version: [e.g., commit hash or release tag]

**Additional context**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- Explain why this enhancement would be useful
- Provide examples of how it would be used

### Your First Code Contribution

Unsure where to begin? You can start by looking through these issues:

- Issues labeled `good first issue` - simple issues for beginners
- Issues labeled `help wanted` - more involved issues

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- A text editor or IDE (VS Code, PyCharm, etc.)

### Setup Steps

1. **Fork and clone the repository**

   ```bash
   # Fork the repo on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/versiontracker.git
   cd versiontracker
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your GitHub token**

   ```bash
   cp .env.example .env
   # Edit .env and add your GitHub token
   ```

5. **Test your setup**

   ```bash
   # Test CLI
   python version_tracker.py --username fabriziosalmi

   # Test web interface
   python launch_web.py
   ```

### Development Workflow

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes**

   - Write clean, documented code
   - Follow the style guidelines below
   - Test your changes thoroughly

3. **Commit your changes**

   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

   Use conventional commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Remove:` for removing code or features
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

4. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**

   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template
   - Submit for review

## Pull Request Process

1. **Update documentation** - If your changes affect how users interact with the tool, update the README.md and relevant documentation.

2. **Test thoroughly** - Ensure your changes work as expected:
   - Test CLI commands
   - Test web interface (if applicable)
   - Test with different GitHub users
   - Test edge cases

3. **Code review** - Be responsive to feedback:
   - Address reviewer comments
   - Make requested changes
   - Ask questions if something is unclear

4. **Merge** - Once approved, a maintainer will merge your PR.

### Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows the style guidelines
- [ ] All functions have docstrings
- [ ] Documentation has been updated
- [ ] Commit messages are clear and descriptive
- [ ] Changes have been tested locally
- [ ] No unnecessary files are included (check `.gitignore`)

## Style Guidelines

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some additional guidelines:

**Imports:**
```python
# Standard library imports first
import os
import sys
from datetime import datetime

# Third-party imports
import requests
from flask import Flask

# Local imports
from version_tracker import GitHubVersionTracker
```

**Type Hints:**
```python
def get_user_repos(username: str, include_forks: bool = False) -> List[Dict[str, Any]]:
    """
    Get all repositories for a user.
    
    Args:
        username: GitHub username to query
        include_forks: Whether to include forked repositories
        
    Returns:
        List of repository dictionaries
    """
    pass
```

**Docstrings:**

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 0) -> bool:
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important notes.
    
    Args:
        param1: Description of param1
        param2: Description of param2, defaults to 0
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
        
    Example:
        >>> result = example_function("test", 5)
        >>> print(result)
        True
    """
    pass
```

**Naming Conventions:**

- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Descriptive names over short names

```python
# Good
def get_latest_release(repo_owner: str) -> Optional[ReleaseInfo]:
    max_retries = 3
    API_BASE_URL = "https://api.github.com"
    
# Avoid
def glr(ro: str) -> Optional[ReleaseInfo]:
    m = 3
    url = "https://api.github.com"
```

**Code Organization:**

- Keep functions short and focused (ideally under 50 lines)
- Use meaningful variable names
- Add comments for complex logic
- Group related functions together
- Use classes for related functionality

### Documentation Style

**Markdown:**
- Use headers hierarchically (don't skip levels)
- Include code blocks with language specifiers
- Use tables for structured data
- Add links where relevant
- Keep line length reasonable (around 80-120 characters)

**Code Examples:**
- Show both the command and expected output
- Include error cases when relevant
- Use realistic examples
- Keep examples concise but complete

## Adding New Features

### Adding Support for New Package Types

To add a new package registry (e.g., Ruby Gems, Go Modules):

1. **Update `config.py`:**

   ```python
   SUPPORTED_PACKAGE_TYPES = {
       # ... existing types ...
       "ruby": {
           "files": ["Gemfile", "*.gemspec"],
           "registry_url": "https://rubygems.org/api/v1/",
           "package_url_template": "https://rubygems.org/gems/{name}"
       }
   }
   ```

2. **Update `version_tracker.py`:**

   Add detection logic in the `get_packages()` method:

   ```python
   # Check for Ruby gems
   gemspec_files = self._get_repo_files(repo_owner, repo_name, "*.gemspec")
   if gemspec_files:
       # Extract gem name and version
       # Query rubygems.org API
       # Create PackageInfo object
       pass
   ```

3. **Test thoroughly:**

   ```bash
   # Test with a repository that has the new package type
   python version_tracker.py --username ruby-user-example
   ```

4. **Update documentation:**

   - Add the new package type to README.md
   - Include examples
   - Document any limitations

### Adding Web Interface Features

1. **Backend (web_app.py):**
   - Add new routes with proper error handling
   - Apply rate limiting to new endpoints
   - Validate all inputs
   - Add security headers

2. **Frontend (templates/index.html):**
   - Maintain the existing design aesthetic
   - Ensure mobile responsiveness
   - Add loading states
   - Handle errors gracefully

3. **Test:**
   - Test in multiple browsers
   - Test on mobile devices
   - Test with slow connections
   - Test error scenarios

## Testing

### Manual Testing

Before submitting a PR, test:

1. **CLI functionality:**
   ```bash
   # Basic usage
   python version_tracker.py --username fabriziosalmi
   
   # All output formats
   python version_tracker.py --username fabriziosalmi --format rich
   python version_tracker.py --username fabriziosalmi --format table
   python version_tracker.py --username fabriziosalmi --format json
   
   # With options
   python version_tracker.py --username fabriziosalmi --include-forks
   python version_tracker.py --username fabriziosalmi --save test.txt
   ```

2. **Web interface:**
   ```bash
   python launch_web.py
   # Test in browser at http://localhost:8080
   # Try different usernames
   # Test refresh functionality
   # Test on mobile view
   ```

3. **Edge cases:**
   - User with no repositories
   - User with no releases
   - Invalid username
   - Private repositories
   - Rate limiting scenarios

### Future: Automated Testing

We plan to add automated tests. If you'd like to help with this:

- Unit tests for individual functions
- Integration tests for API calls
- End-to-end tests for workflows
- Tests should use pytest framework

## Questions?

Don't hesitate to ask questions:

- Open a GitHub issue with the `question` label
- Check existing issues and discussions
- Reach out to maintainers

## Recognition

Contributors will be:
- Listed in the project's contributors page
- Mentioned in release notes for significant contributions
- Credited in documentation for major features

Thank you for contributing! 🎉
