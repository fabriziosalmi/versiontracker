# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation improvements
- CONTRIBUTING.md with detailed contribution guidelines
- CHANGELOG.md to track version changes
- Troubleshooting section in README
- FAQ section in README
- Detailed API documentation
- Configuration documentation
- Enhanced function docstrings

### Changed
- README.md restructured with Table of Contents
- Improved installation instructions with step-by-step guidance
- Enhanced Quick Start section with expected outputs
- Better organization of command-line options

## [1.0.0] - 2025-10-30

### Added
- Modern cyberpunk-themed web interface
- Real-time GitHub repository and release tracking
- Interactive dashboard with statistics
- Smart caching system for web interface
- Rate limiting for API protection
- Security enhancements (CSP, security headers)
- Support for npm package detection
- Support for Python package detection (PyPI)
- Multiple output formats (rich, table, JSON)
- Batch analysis for multiple users
- Command-line interface with Click
- Rich terminal output with colors and tables
- Download count tracking for releases
- Star and fork statistics
- Pre-release detection

### Security
- Secure secret key generation
- Content Security Policy (CSP) implementation
- Input validation and sanitization
- Rate limiting on API endpoints
- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- HTML sanitization with bleach
- CORS configuration for API endpoints
- Comprehensive security logging

## Version History

### Initial Development

The project started as a simple command-line tool to track GitHub releases and has evolved into a comprehensive version tracking system with both CLI and web interfaces.

---

## Release Notes Template

When preparing a new release, use this template:

```markdown
## [Version] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Features that will be removed in future releases

### Removed
- Features that have been removed

### Fixed
- Bug fixes

### Security
- Security improvements and vulnerability fixes
```

---

[Unreleased]: https://github.com/fabriziosalmi/versiontracker/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/fabriziosalmi/versiontracker/releases/tag/v1.0.0
