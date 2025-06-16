# GitHub Version Tracker

A comprehensive tool to generate reports of your latest published versions across GitHub repositories, including releases and packages. Now with a **stunning web interface**! 🚀

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

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Set up a GitHub personal access token for higher API rate limits:
   - Copy `.env.example` to `.env`
   - Add your GitHub token to the `.env` file
   - Or set the `GITHUB_TOKEN` environment variable

## Quick Start

The easiest way to get started is to use the `quickstart.py` script:

1. Edit `quickstart.py` and set your GitHub username:
   ```python
   YOUR_GITHUB_USERNAME = "your-actual-username"
   ```

2. Run the script:
   ```bash
   python quickstart.py
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
# Include forked repositories
python version_tracker.py --username YOUR_USERNAME --include-forks

# Use a specific GitHub token
python version_tracker.py --username YOUR_USERNAME --token YOUR_GITHUB_TOKEN

# Change output format
python version_tracker.py --username YOUR_USERNAME --format json

# Save report to file
python version_tracker.py --username YOUR_USERNAME --save report.txt

# Combine options
python version_tracker.py --username YOUR_USERNAME --include-forks --format json --save report.json
```

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

Currently supports detection of:
- **npm packages** (package.json)
- **Python packages** (setup.py, pyproject.toml, setup.cfg)

Additional package types can be added by extending the `get_packages` method.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
