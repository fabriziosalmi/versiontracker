#!/usr/bin/env python3
"""
Security Configuration for GitHub Version Tracker
Contains security-related constants and configurations.
"""

# Rate limiting configurations
RATE_LIMITS = {
    'api_stats': "30 per minute",
    'api_refresh': "5 per minute",
    'global_default': "200 per day",
    'hourly_default': "50 per hour"
}

# Content Security Policy
CSP_POLICY = {
    'default-src': "'self'",
    'style-src': "'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com",
    'font-src': "'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com",
    'script-src': "'self' 'nonce-{nonce}'",
    'img-src': "'self' data: https:",
    'connect-src': "'self'",
    'object-src': "'none'",
    'base-uri': "'self'",
    'form-action': "'self'"
}

# HTML sanitization settings
ALLOWED_HTML_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'i', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'hr'
]

ALLOWED_HTML_ATTRIBUTES = {
    'a': ['href', 'title'],
    'code': ['class'],
    'pre': ['class']
}

# Security headers
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
}

# Content limits
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
MAX_DESCRIPTION_LENGTH = 50000  # 50KB
USERNAME_MAX_LENGTH = 39
USERNAME_MIN_LENGTH = 1

# Cache settings
CACHE_DURATION_HOURS = 24
BACKGROUND_UPDATE_INTERVAL = 300  # 5 minutes

# Logging configuration
SECURITY_LOG_FORMAT = "%(asctime)s - SECURITY - %(levelname)s - %(message)s"
