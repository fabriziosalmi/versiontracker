# GitHub Version Tracker Configuration

# Default settings
DEFAULT_USERNAME = "your-github-username"
DEFAULT_FORMAT = "rich"
INCLUDE_FORKS = False

# GitHub API settings
GITHUB_API_BASE = "https://api.github.com"
REQUESTS_PER_HOUR_NO_TOKEN = 60
REQUESTS_PER_HOUR_WITH_TOKEN = 5000

# Output settings
DEFAULT_OUTPUT_DIR = "reports"
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Report customization
TRUNCATE_DESCRIPTION_LENGTH = 100
MAX_REPOS_TO_ANALYZE = 100  # Set to None for no limit

# Supported package types
SUPPORTED_PACKAGE_TYPES = {
    "npm": {
        "files": ["package.json"],
        "registry_url": "https://registry.npmjs.org/",
        "package_url_template": "https://www.npmjs.com/package/{name}"
    },
    "python": {
        "files": ["setup.py", "pyproject.toml", "setup.cfg"],
        "registry_url": "https://pypi.org/",
        "package_url_template": "https://pypi.org/project/{name}/"
    }
}

# Display settings
RICH_THEME = {
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "highlight": "cyan"
}
