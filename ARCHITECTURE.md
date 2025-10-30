# Architecture Overview

## Project Structure

```
versiontracker/
├── version_tracker.py      # Core library with GitHubVersionTracker class
├── web_app.py             # Flask web application
├── launch_web.py          # Web app launcher with browser opening
├── quickstart.py          # Quick start script for CLI usage
├── example.py             # Basic usage example
├── batch_analyzer.py      # Batch processing for multiple users
├── config.py              # Configuration constants
├── security_config.py     # Security-related configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── templates/
│   └── index.html        # Web interface HTML template
├── static/
│   └── style.css         # Web interface styles
└── docs/
    ├── README.md         # Main documentation
    ├── CONTRIBUTING.md   # Contribution guidelines
    ├── CHANGELOG.md      # Version history
    └── SECURITY_REPORT.md # Security audit report
```

## Core Components

### 1. GitHubVersionTracker Class (`version_tracker.py`)

The main class that provides GitHub repository analysis functionality.

**Key Methods:**
- `get_user_repos()` - Fetches all repositories for a user
- `get_latest_release()` - Gets the latest release information
- `get_packages()` - Detects published packages (npm, PyPI)
- `generate_report()` - Generates formatted reports

**Design Pattern:** Single Responsibility Principle
- Handles only GitHub API interaction and data processing
- Separates concerns between data fetching and display

### 2. Web Application (`web_app.py`)

Flask-based web interface with modern UI.

**Architecture:**
```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────────────────────┐
│      Flask App              │
│  ┌────────────────────────┐ │
│  │  Routes                │ │
│  │  - GET /               │ │
│  │  - GET /api/stats      │ │
│  │  - POST /api/refresh   │ │
│  └────────────────────────┘ │
│  ┌────────────────────────┐ │
│  │  Middleware            │ │
│  │  - Rate Limiter        │ │
│  │  - CORS                │ │
│  │  - Security Headers    │ │
│  └────────────────────────┘ │
│  ┌────────────────────────┐ │
│  │  Cache                 │ │
│  │  - In-memory (5 min)   │ │
│  └────────────────────────┘ │
└──────────┬──────────────────┘
           │
           ▼
   ┌───────────────────┐
   │  GitHubVersionTracker  │
   └───────┬───────────┘
           │
           ▼
   ┌───────────────┐
   │  GitHub API   │
   └───────────────┘
```

**Security Features:**
- Rate limiting (Flask-Limiter)
- CORS configuration
- Content Security Policy (CSP)
- Input validation and sanitization
- Security headers

### 3. CLI Interface

Command-line interface built with Click framework.

**Flow:**
```
User Command
    ↓
Click Argument Parsing
    ↓
GitHubVersionTracker Instance
    ↓
API Calls (with retry logic)
    ↓
Data Processing
    ↓
Format Selection (Rich/Table/JSON)
    ↓
Output (Console or File)
```

## Data Flow

### Repository Analysis Flow

```
1. Input: GitHub Username
        ↓
2. Fetch all repositories (paginated)
        ↓
3. For each repository:
   a. Get latest release (if exists)
   b. Detect package files
   c. Query package registries
        ↓
4. Aggregate data:
   - Total repositories
   - Total releases
   - Download counts
   - Stars and forks
        ↓
5. Format and display
```

### Caching Strategy (Web App)

```
Request → Cache Check → [HIT] → Return cached data
                      ↘ [MISS]
                             ↓
                        Fetch from GitHub
                             ↓
                        Store in cache (5 min TTL)
                             ↓
                        Return fresh data
```

## API Integration

### GitHub REST API

**Endpoints Used:**
- `GET /users/{username}/repos` - List user repositories
- `GET /repos/{owner}/{repo}/releases/latest` - Get latest release
- `GET /repos/{owner}/{repo}/contents/{path}` - Get file contents

**Rate Limits:**
- Unauthenticated: 60 requests/hour
- Authenticated: 5,000 requests/hour

**Error Handling:**
- 404: Repository/release not found → Return None
- 403: Rate limit exceeded → Display error with reset time
- 500: Server error → Retry with exponential backoff

### Package Registries

**npm Registry:**
- Endpoint: `https://registry.npmjs.org/{package}`
- Returns: Package metadata including latest version

**PyPI:**
- Endpoint: `https://pypi.org/pypi/{package}/json`
- Returns: Package info including versions and download stats

## Security Architecture

### Input Validation

```python
# Username validation
- Alphanumeric, hyphens only
- Length: 1-39 characters
- Pattern: ^[a-zA-Z0-9-]+$

# Path validation
- No directory traversal
- Whitelist allowed characters
```

### Security Headers

Applied to all web responses:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Content-Security-Policy: [nonce-based]`

### Rate Limiting Strategy

**Web API:**
- Global: 200 requests/day, 50 requests/hour
- Stats endpoint: 30 requests/minute
- Refresh endpoint: 5 requests/minute

**Purpose:**
- Prevent abuse
- Protect GitHub API quota
- Ensure fair usage

## Output Formats

### 1. Rich Format
- **Target:** Interactive terminal use
- **Features:** Colors, tables, panels
- **Library:** python-rich
- **Use Case:** Development, manual inspection

### 2. Table Format
- **Target:** Plain text output
- **Features:** Simple ASCII tables
- **Library:** tabulate
- **Use Case:** File output, simple terminals

### 3. JSON Format
- **Target:** Programmatic consumption
- **Features:** Structured data
- **Library:** Python json
- **Use Case:** CI/CD, automation, integration

## Technology Stack

### Backend
- **Python 3.7+** - Core language
- **Flask 3.0.3** - Web framework
- **Requests 2.32.4** - HTTP client
- **Click 8.1.7** - CLI framework
- **Rich 13.8.1** - Terminal formatting

### Security
- **Flask-Limiter 3.8.0** - Rate limiting
- **Bleach 6.1.0** - HTML sanitization
- **Flask-CORS 6.0.0** - CORS handling

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (cyberpunk theme)
- **Vanilla JavaScript** - Interactivity
- **No heavy frameworks** - Lightweight approach

## Design Decisions

### Why Flask over FastAPI?
- Simpler for this use case
- Better templating support
- Wider adoption and documentation
- Sufficient performance for our needs

### Why Rich Console?
- Beautiful terminal output
- Great developer experience
- Maintains readability in files
- Popular in Python community

### Why In-Memory Cache?
- Simple deployment (no Redis required)
- Sufficient for single-instance usage
- Easy to understand and debug
- Can upgrade to Redis if needed

### Why No Database?
- No persistent data needed
- Data comes from GitHub API
- Reduces complexity
- Stateless design

## Performance Considerations

### API Call Optimization
- Pagination (100 repos per page)
- Parallel requests where possible
- Caching responses (web app)
- Conditional requests (ETags)

### Memory Usage
- Stream large responses
- Limit data retention
- Clear old cache entries
- No database overhead

### Response Times
- Typical: 2-5 seconds for 10 repos
- With cache: < 100ms
- Rate limit aware
- Progressive loading

## Scalability

### Current Limitations
- Single-instance web app
- In-memory caching only
- No horizontal scaling
- GitHub API rate limits

### Future Improvements
- Redis for distributed caching
- Worker queues for background jobs
- Database for persistent storage
- Multi-instance deployment
- WebSocket for real-time updates

## Error Handling Strategy

### Graceful Degradation
```
Full Success
    ↓
Partial Success (some repos fail)
    ↓
Partial Success (no releases found)
    ↓
Failure (user not found)
    ↓
Critical Failure (network/auth)
```

### User Feedback
- Success: Show results
- Warning: Show partial results + warning
- Error: Show helpful error message
- Critical: Show error + how to fix

## Testing Strategy

### Current State
- Manual testing
- Example scripts for verification

### Future Plans
- Unit tests (pytest)
- Integration tests
- End-to-end tests
- API mocking
- CI/CD pipeline

## Deployment Options

### 1. Local Development
```bash
python launch_web.py
```

### 2. Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:8080 web_app:app
```

### 3. Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "web_app:app"]
```

### 4. Cloud Platforms
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service

## Contributing Guidelines

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- PR process
- Adding new features

## Security

See [SECURITY_REPORT.md](SECURITY_REPORT.md) for:
- Security audit results
- Vulnerability fixes
- Best practices
- Deployment recommendations
