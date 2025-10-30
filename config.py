# GitHub Version Tracker Configuration
"""
Configuration file for GitHub Version Tracker.

This file contains default settings, API configurations, and customization
options for both CLI and web interface.
"""

# Default settings for CLI usage
DEFAULT_USERNAME = "your-github-username"  # Change to your GitHub username for quick testing
DEFAULT_FORMAT = "rich"  # Output format: "rich", "table", or "json"
INCLUDE_FORKS = False  # Whether to include forked repositories by default

# GitHub API settings
GITHUB_API_BASE = "https://api.github.com"  # GitHub REST API base URL
REQUESTS_PER_HOUR_NO_TOKEN = 60  # Rate limit without authentication
REQUESTS_PER_HOUR_WITH_TOKEN = 5000  # Rate limit with personal access token

# Output settings
DEFAULT_OUTPUT_DIR = "reports"  # Directory for saving batch analysis reports
DATE_FORMAT = "%Y-%m-%d"  # Format for displaying dates (e.g., 2025-10-30)
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"  # Format for displaying timestamps

# Report customization
TRUNCATE_DESCRIPTION_LENGTH = 100  # Max characters to display in release descriptions
MAX_REPOS_TO_ANALYZE = 100  # Maximum repositories to analyze (None = unlimited)

# Supported package types and their registry configurations
SUPPORTED_PACKAGE_TYPES = {
    "npm": {
        "files": ["package.json"],  # Files that indicate npm package
        "registry_url": "https://registry.npmjs.org/",  # npm registry API
        "package_url_template": "https://www.npmjs.com/package/{name}"  # Package page URL
    },
    "python": {
        "files": ["setup.py", "pyproject.toml", "setup.cfg"],  # Python package files
        "registry_url": "https://pypi.org/",  # PyPI registry
        "package_url_template": "https://pypi.org/project/{name}/"  # PyPI package page
    }
}

# Display settings for rich terminal output
RICH_THEME = {
    "success": "green",  # Color for success messages
    "error": "red",  # Color for error messages
    "warning": "yellow",  # Color for warnings
    "info": "blue",  # Color for informational messages
    "highlight": "cyan"  # Color for highlighted text
}
