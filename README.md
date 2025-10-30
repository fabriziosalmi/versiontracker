# GitHub Version Tracker

A comprehensive tool to generate reports of your latest published versions across GitHub repositories, including releases and packages. Now with a **stunning web interface**! 🚀

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Web Interface](#-web-interface-recommended)
  - [Command Line Interface](#-command-line-interface-advanced)
  - [Batch Analysis](#batch-analysis)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Output Formats](#output-formats)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Modern Web Interface

**Experience your GitHub data like never before!**

- 🎨 **Ultra-modern cyberpunk design** with glassmorphism effects
- 📊 **Interactive dashboards** and real-time statistics
- 📱 **Fully responsive** - works on desktop, tablet, and mobile
- ⚡ **Real-time data** with smart caching
- 🎯 **Developer-focused** UI with terminal aesthetics

### Quick Start Web Interface

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the web app
python launch_web.py

# 3. Open http://localhost:8080 in your browser
```

## Features

### 🖥️ **Web Interface (NEW!)**
- **Modern cyberpunk UI** with dark theme and neon accents
- **Real-time dashboard** with interactive statistics
- **Responsive design** for all screen sizes
- **Smart caching** for optimal performance
- **Beautiful visualizations** of your GitHub data

### 📊 **Command Line Interface**
- 📊 **Comprehensive Reports**: Track releases and packages across all your repositories
- 🎨 **Multiple Output Formats**: Rich console output, simple tables, or JSON
- 📦 **Package Detection**: Automatically detects npm and Python packages
- 📈 **Useful Statistics**: Download counts, stars, forks, and more
- 🔍 **Filtering Options**: Include/exclude forked repositories
- 💾 **Export Options**: Save reports to files
- 🚀 **GitHub API Integration**: Uses official GitHub API with optional token support

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (for cloning the repository)
- Internet connection
- A GitHub account

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/fabriziosalmi/versiontracker.git
   cd versiontracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional but Recommended) Set up a GitHub personal access token**
   
   Without a token, you're limited to 60 API requests per hour. With a token, you get 5,000 requests per hour.
   
   a. Create a token:
      - Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
      - Click "Generate new token (classic)"
      - Select scopes: `public_repo` (for public repos) or `repo` (for private repos)
      - Generate and copy the token
   
   b. Configure the token (choose one method):
      - **Method 1**: Using `.env` file (recommended)
        ```bash
        cp .env.example .env
        # Edit .env and add your token: GITHUB_TOKEN=your_token_here
        ```
      - **Method 2**: Environment variable
        ```bash
        export GITHUB_TOKEN=your_token_here
        ```
      - **Method 3**: Command line parameter
        ```bash
        python version_tracker.py --username YOUR_USERNAME --token your_token_here
        ```

## Quick Start

### Option 1: Web Interface (Easiest)

Launch the modern web interface in just 3 commands:

```bash
# 1. Install dependencies (if not done already)
pip install -r requirements.txt

# 2. Launch the web app
python launch_web.py

# 3. Your browser will automatically open to http://localhost:8080
```

**What you'll see:**
- A modern cyberpunk-themed interface
- Enter any GitHub username to see their repositories
- Real-time statistics and visualizations
- Interactive project cards with release information

### Option 2: Command Line Quick Start

For a quick CLI report, use the quickstart script:

```bash
# 1. Edit quickstart.py and set your username
# Change: YOUR_GITHUB_USERNAME = "your-username-here"
# To:     YOUR_GITHUB_USERNAME = "fabriziosalmi"

# 2. Run the script
python quickstart.py
```

**Expected Output:**
```
🚀 Generating GitHub version report for fabriziosalmi...

Fetching repositories for fabriziosalmi...
Processing releases...

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    GitHub Version Report - fabriziosalmi                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Total Repositories with Releases: 5
Total Download Count: 1,234
Total Stars: 567
...
```

### Option 3: One-Line CLI Command

```bash
python version_tracker.py --username YOUR_USERNAME
```

## Usage

### 🚀 Web Interface (Recommended)

The easiest and most beautiful way to explore your GitHub data:

```bash
# Launch the modern web interface
python launch_web.py

# Or start manually
python web_app.py
```

Then open **http://localhost:8080** in your browser and enter any GitHub username!

**Web Interface Features:**
- 🎨 **Stunning cyberpunk UI** with glassmorphism effects
- 📊 **Interactive dashboard** with real-time statistics
- 📱 **Fully responsive** design for all devices
- 🔥 **Live data** with smart caching
- 📈 **Beautiful charts** and visualizations
- 🚀 **Project cards** with detailed information
- 🎯 **Package tracking** across registries

### 💻 Command Line Interface (Advanced)

For automation, scripting, and quick terminal usage:

#### Quick Start Script
```bash
# Edit quickstart.py and set your username, then run:
python quickstart.py
```

#### Basic Usage

```bash
# Replace 'your-username' with your actual GitHub username
python version_tracker.py --username your-username
```

### Batch Analysis

Analyze multiple users at once using the batch analyzer:

```bash
# Edit batch_analyzer.py to add usernames, then run:
python batch_analyzer.py
```

This will create individual reports for each user plus a combined summary.

### Advanced Options

```bash
# Include forked repositories in analysis
python version_tracker.py --username YOUR_USERNAME --include-forks

# Use a specific GitHub token for higher rate limits
python version_tracker.py --username YOUR_USERNAME --token YOUR_GITHUB_TOKEN

# Change output format to JSON for scripting/automation
python version_tracker.py --username YOUR_USERNAME --format json

# Save report to a file
python version_tracker.py --username YOUR_USERNAME --save report.txt

# Combine multiple options
python version_tracker.py --username YOUR_USERNAME \
    --include-forks \
    --format json \
    --save report.json \
    --token YOUR_TOKEN
```

### All Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--username` | `-u` | GitHub username to analyze | *Required* |
| `--token` | `-t` | GitHub personal access token | None |
| `--include-forks` | `-f` | Include forked repositories | False |
| `--format` | `-F` | Output format: `table`, `rich`, or `json` | `table` |
| `--save` | `-s` | Save report to specified file | None |
| `--help` | | Show help message and exit | |

### Output Formats

1. **Rich** (default): Beautiful, colored console output with tables and panels
2. **Table**: Simple tabular format suitable for terminals and files
3. **JSON**: Machine-readable format for integration with other tools

## What Information is Collected

### Repository Releases
- Repository name
- Latest version/tag
- Release date
- Programming language
- Star count
- Fork count
- Download count (for release assets)
- Pre-release status
- Release description

### Published Packages
- Package type (npm, Python, etc.)
- Latest version
- Package registry URL
- Repository association

## Sample Output

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                          GitHub Version Report - username                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Total Repositories with Releases: 15
Total Download Count: 12,450
Total Stars: 8,920
Total Forks: 1,230
Report Generated: 2025-06-15 10:30:45

                                    Latest Releases                                    
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ Repository              ┃ Version    ┃ Release Date ┃ Language   ┃ Stars ┃ Downloads  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ username/awesome-proj   │ v2.1.0     │ 2025-06-10   │ JavaScript │ 2,340 │ 5,678      │
│ username/python-lib     │ v1.5.2     │ 2025-06-08   │ Python     │ 1,890 │ 3,456      │
└─────────────────────────┴────────────┴──────────────┴────────────┴───────┴────────────┘
```

## Command Line Options

- `--username, -u`: GitHub username to analyze (required)
- `--token, -t`: GitHub personal access token (optional, for higher rate limits)
- `--include-forks, -f`: Include forked repositories in the analysis
- `--format, -F`: Output format (table, rich, json)
- `--save, -s`: Save report to specified file

## Rate Limits

- **Without token**: 60 requests per hour
- **With token**: 5,000 requests per hour

For users with many repositories, using a GitHub personal access token is recommended.

## GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `public_repo` scope (or `repo` for private repos)
3. Set it as an environment variable or use the `--token` option

## Requirements

- Python 3.7+
- Internet connection
- GitHub account (for the repositories to analyze)

## Supported Package Types

Currently supports automatic detection of:

| Package Type | Detection Files | Registry |
|-------------|-----------------|----------|
| **npm** | `package.json` | [npmjs.com](https://www.npmjs.com) |
| **Python** | `setup.py`, `pyproject.toml`, `setup.cfg` | [pypi.org](https://pypi.org) |

**Want to add more package types?** See [Contributing](#contributing) section.

## Configuration

### Environment Variables

The application supports the following environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GITHUB_TOKEN` | GitHub personal access token | None | No |
| `SECRET_KEY` | Flask secret key for web app | Auto-generated | No |
| `FLASK_DEBUG` | Enable Flask debug mode | `False` | No |
| `BEHIND_PROXY` | Running behind reverse proxy | `False` | No |
| `MAX_CONTENT_LENGTH` | Max request size (bytes) | 16777216 (16MB) | No |

### Configuration File

You can customize default settings by editing `config.py`:

```python
# Default settings
DEFAULT_USERNAME = "your-github-username"
DEFAULT_FORMAT = "rich"  # Options: "rich", "table", "json"
INCLUDE_FORKS = False

# Report customization
TRUNCATE_DESCRIPTION_LENGTH = 100  # Characters to show in descriptions
MAX_REPOS_TO_ANALYZE = 100  # Set to None for no limit

# Display settings
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
```

## API Documentation

### GitHubVersionTracker Class

The main class for interacting with GitHub repositories.

#### Initialization

```python
from version_tracker import GitHubVersionTracker

# Without authentication (60 requests/hour)
tracker = GitHubVersionTracker()

# With authentication (5,000 requests/hour)
tracker = GitHubVersionTracker(token="your_github_token")
```

#### Methods

**`get_user_repos(username: str, include_forks: bool = False) -> List[Dict]`**

Get all repositories for a user.

```python
repos = tracker.get_user_repos("fabriziosalmi", include_forks=False)
for repo in repos:
    print(f"{repo['name']}: {repo['description']}")
```

**Parameters:**
- `username` (str): GitHub username
- `include_forks` (bool): Include forked repositories

**Returns:** List of repository dictionaries

---

**`get_latest_release(repo_owner: str, repo_name: str) -> Optional[ReleaseInfo]`**

Get the latest release information for a repository.

```python
release = tracker.get_latest_release("fabriziosalmi", "versiontracker")
if release:
    print(f"Latest version: {release.latest_version}")
    print(f"Downloads: {release.download_count}")
```

**Parameters:**
- `repo_owner` (str): Repository owner username
- `repo_name` (str): Repository name

**Returns:** ReleaseInfo object or None if no release

---

**`get_packages(repo_owner: str, repo_name: str) -> List[PackageInfo]`**

Get published packages for a repository.

```python
packages = tracker.get_packages("fabriziosalmi", "versiontracker")
for pkg in packages:
    print(f"{pkg.package_type}: {pkg.latest_version}")
```

**Parameters:**
- `repo_owner` (str): Repository owner username
- `repo_name` (str): Repository name

**Returns:** List of PackageInfo objects

---

**`generate_report(username: str, include_forks: bool = False, output_format: str = 'table') -> None`**

Generate and display a comprehensive version report.

```python
tracker.generate_report(
    username="fabriziosalmi",
    include_forks=False,
    output_format="rich"  # Options: "rich", "table", "json"
)
```

**Parameters:**
- `username` (str): GitHub username
- `include_forks` (bool): Include forked repositories
- `output_format` (str): Output format ('rich', 'table', or 'json')

### Data Classes

**ReleaseInfo**

```python
@dataclass
class ReleaseInfo:
    repo_name: str          # Full repo name (owner/name)
    latest_version: str     # Version tag (e.g., "v1.0.0")
    release_date: str       # Release date (YYYY-MM-DD)
    release_url: str        # GitHub release URL
    download_count: int     # Total asset downloads
    is_prerelease: bool     # Pre-release flag
    description: str        # Release description
    language: str           # Primary programming language
    stars: int             # Repository stars
    forks: int             # Repository forks
```

**PackageInfo**

```python
@dataclass
class PackageInfo:
    repo_name: str         # Full repo name (owner/name)
    package_type: str      # Package type (e.g., "npm", "python")
    latest_version: str    # Latest package version
    package_url: str       # Package registry URL
    downloads: int         # Download count (if available)
```

### Web API Endpoints

When running the web interface (`python launch_web.py`):

**GET `/api/stats/<username>`**

Get repository statistics and releases for a user.

```bash
curl http://localhost:8080/api/stats/fabriziosalmi
```

**Response:**
```json
{
  "username": "fabriziosalmi",
  "stats": {
    "total_repos": 25,
    "total_releases": 10,
    "total_downloads": 5432,
    "total_stars": 1234,
    "total_forks": 89
  },
  "repos": [...],
  "cached": false
}
```

**POST `/api/refresh/<username>`**

Force refresh cached data for a user (rate limited: 5 requests/minute).

```bash
curl -X POST http://localhost:8080/api/refresh/fabriziosalmi
```

## Troubleshooting

### Common Issues

#### Issue: "Rate limit exceeded"

**Problem:** You've exceeded GitHub's API rate limit.

**Solution:**
1. Set up a GitHub personal access token (see [Installation](#installation))
2. Wait for the rate limit to reset (shown in error message)
3. For web app: Rate limits are per IP address

```bash
# Check your current rate limit status
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/rate_limit
```

---

#### Issue: "No module named 'tabulate'" or similar import errors

**Problem:** Dependencies are not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

For specific packages:
```bash
pip install tabulate rich click requests flask
```

---

#### Issue: Web interface won't start - "Address already in use"

**Problem:** Port 8080 is already in use by another application.

**Solution:**
1. Find and stop the process using port 8080:
   ```bash
   # Linux/Mac
   lsof -ti:8080 | xargs kill -9
   
   # Windows
   netstat -ano | findstr :8080
   taskkill /PID <PID> /F
   ```

2. Or modify `launch_web.py` to use a different port:
   ```python
   app.run(debug=False, host='0.0.0.0', port=8081)  # Changed to 8081
   ```

---

#### Issue: "401 Unauthorized" or "403 Forbidden" errors

**Problem:** Invalid or expired GitHub token, or insufficient permissions.

**Solution:**
1. Verify your token is correct
2. Check token hasn't expired (tokens can have expiration dates)
3. Ensure token has correct scopes:
   - `public_repo` for public repositories
   - `repo` for private repositories
4. Regenerate token if necessary

---

#### Issue: Empty or incomplete reports

**Problem:** User has no releases or repositories are private.

**Solution:**
1. Check if the user has public repositories with releases
2. For private repos, use a token with `repo` scope
3. Use `--include-forks` flag if you want to include forked repositories

---

#### Issue: Slow performance with many repositories

**Problem:** Large number of repositories causing many API calls.

**Solution:**
1. Use a GitHub token for higher rate limits
2. Use web interface which has built-in caching
3. Limit repositories in `config.py`:
   ```python
   MAX_REPOS_TO_ANALYZE = 50  # Analyze only first 50 repos
   ```

### Debug Mode

Enable debug mode for more detailed error messages:

```bash
# For CLI
python -v version_tracker.py --username YOUR_USERNAME

# For web app
export FLASK_DEBUG=True
python web_app.py
```

### Getting Help

If you're still experiencing issues:

1. Check existing [GitHub Issues](https://github.com/fabriziosalmi/versiontracker/issues)
2. Create a new issue with:
   - Python version (`python --version`)
   - Operating system
   - Full error message
   - Steps to reproduce

## FAQ

### General Questions

**Q: Do I need a GitHub account to use this tool?**

A: No, you don't need an account to analyze public repositories. However, using a GitHub token gives you higher API rate limits.

---

**Q: Can I analyze private repositories?**

A: Yes, but you need a GitHub personal access token with `repo` scope (not just `public_repo`).

---

**Q: Is this tool affiliated with GitHub?**

A: No, this is an independent tool that uses GitHub's public API.

---

**Q: Does this tool work with GitLab or Bitbucket?**

A: Currently, no. This tool is specifically designed for GitHub. Support for other platforms could be added (see Contributing).

### Technical Questions

**Q: What's the difference between releases and packages?**

A: 
- **Releases**: GitHub releases/tags created on the repository
- **Packages**: Published packages on package registries (npm, PyPI, etc.)

A repository can have releases without packages, packages without releases, or both.

---

**Q: Why am I getting rate limited even with a token?**

A: GitHub has rate limits even with tokens:
- 5,000 requests per hour with authentication
- Some endpoints have additional secondary rate limits

The web interface uses caching to minimize API calls.

---

**Q: Can I use this in CI/CD pipelines?**

A: Yes! Use JSON output format for easy parsing:

```bash
# In CI/CD
python version_tracker.py \
  --username YOUR_USERNAME \
  --format json \
  --save report.json \
  --token $GITHUB_TOKEN

# Parse with jq
cat report.json | jq '.releases[0].latest_version'
```

---

**Q: How accurate is the download count?**

A: Download counts are:
- **Accurate** for GitHub release assets
- **Not available** for package registries (npm, PyPI) through this tool
- **Updated** in real-time from GitHub API

---

**Q: Can I analyze multiple users at once?**

A: Yes! Use the batch analyzer:

```bash
# Edit batch_analyzer.py to add usernames
python batch_analyzer.py
```

This creates individual reports plus a combined summary.

---

**Q: Is my GitHub token stored or logged?**

A: No. Tokens are:
- Used only for API authentication
- Never stored persistently
- Never logged to files
- Only kept in memory during execution

### Usage Questions

**Q: What output format should I use?**

A:
- **`rich`**: Beautiful terminal output with colors and tables (default for interactive use)
- **`table`**: Simple text tables, good for saving to files
- **`json`**: Machine-readable format for automation and integration

---

**Q: Can I customize the report appearance?**

A: Yes! Edit `config.py` to customize:
- Date formats
- Description length
- Color themes (in `RICH_THEME`)
- Maximum repositories to analyze

---

**Q: How often is the web interface data refreshed?**

A: 
- Cached for 5 minutes after first load
- Click "Refresh" button to force update
- Rate limited to 5 refreshes per minute to prevent API abuse

---

**Q: Can I self-host the web interface?**

A: Yes! The web interface is a Flask app:

```bash
# Development
python launch_web.py

# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 web_app:app

# With Docker
docker build -t versiontracker .
docker run -p 8080:8080 -e GITHUB_TOKEN=your_token versiontracker
```

## Architecture

For developers interested in understanding the internal structure and design decisions:

### Project Structure

The project is organized into clear, focused modules:

- **`version_tracker.py`** - Core library with the main `GitHubVersionTracker` class
- **`web_app.py`** - Flask web application with REST API
- **`config.py`** - Configuration constants and settings
- **`security_config.py`** - Security-related configuration

### Key Design Principles

1. **Separation of Concerns** - CLI, web, and core logic are separate
2. **Single Responsibility** - Each module has a clear, focused purpose
3. **Graceful Degradation** - Works even when some data is unavailable
4. **Security First** - Input validation, rate limiting, security headers

### Data Flow

```
User Input → GitHubVersionTracker → GitHub API → Data Processing → Output Formatting
```

For detailed architecture documentation including:
- Component diagrams
- API integration details
- Security architecture
- Caching strategy
- Deployment options

See **[ARCHITECTURE.md](ARCHITECTURE.md)** for comprehensive technical documentation.

## Contributing

We welcome contributions! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### Quick Start for Contributors

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/versiontracker.git
   cd versiontracker
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Test CLI
   python version_tracker.py --username fabriziosalmi
   
   # Test web interface
   python launch_web.py
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Describe your changes
   - Submit for review

### Development Setup

```bash
# Clone and setup
git clone https://github.com/fabriziosalmi/versiontracker.git
cd versiontracker

# Install dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_DEBUG=True
python web_app.py
```

### Code Style Guidelines

- Follow PEP 8 for Python code
- Use type hints where possible
- Write docstrings for all functions and classes
- Keep functions focused and single-purpose
- Add comments for complex logic

### Adding New Package Types

To add support for a new package type (e.g., Ruby gems, Go modules):

1. Edit `config.py` and add to `SUPPORTED_PACKAGE_TYPES`:
   ```python
   "ruby": {
       "files": ["Gemfile"],
       "registry_url": "https://rubygems.org/",
       "package_url_template": "https://rubygems.org/gems/{name}"
   }
   ```

2. Update `get_packages()` method in `version_tracker.py`

3. Test thoroughly and submit a PR

### Ideas for Contributions

- 🌐 Add support for more package registries (Ruby, Go, Rust, etc.)
- 📊 Add more visualization options in web interface
- 🔍 Add search and filter capabilities
- 📈 Add historical trending data
- 🐳 Create Docker deployment configuration
- 📱 Improve mobile responsiveness
- 🌍 Add internationalization (i18n)
- ⚡ Performance optimizations
- 📚 More comprehensive documentation
- 🧪 Add automated tests

## License

This project is open source and available under the MIT License.

```
MIT License

Copyright (c) 2025 Fabrizio Salmi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/) for the web interface
- Uses [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Powered by [GitHub REST API](https://docs.github.com/en/rest)

---

**Star ⭐ this repository if you find it useful!**

For questions, issues, or suggestions, please [open an issue](https://github.com/fabriziosalmi/versiontracker/issues).
