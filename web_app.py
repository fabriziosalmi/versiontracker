#!/usr/bin/env python3
"""
Modern Web Interface for GitHub Version Tracker
A sleek, minimalist web app to showcase your published software and stats.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import json
import markdown
import re
import bleach
import logging
from datetime import datetime, timedelta
from version_tracker import GitHubVersionTracker
from typing import Dict, List, Any
import threading
import time
from werkzeug.middleware.proxy_fix import ProxyFix
import secrets

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enhanced security configurations
def generate_secret_key():
    """Generate a secure random secret key."""
    return secrets.token_urlsafe(32)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', generate_secret_key())
app.config['WTF_CSRF_TIME_LIMIT'] = None
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# CORS configuration for API endpoints only
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:*", "https://localhost:*"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Handle reverse proxy headers securely
if os.getenv('BEHIND_PROXY', 'False').lower() == 'true':
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Security headers
@app.after_request
def add_security_headers(response):
    """Add comprehensive security headers to all responses."""
    # Basic security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # HSTS for HTTPS deployment
    if request.is_secure:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Enhanced CSP - stricter policy
    nonce = secrets.token_urlsafe(16)
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; "
        f"style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        f"font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        f"script-src 'self' 'nonce-{nonce}'; "
        f"img-src 'self' data: https:; "
        f"connect-src 'self'; "
        f"object-src 'none'; "
        f"base-uri 'self'; "
        f"form-action 'self';"
    )
    
    # Add nonce to response for use in templates
    response.nonce = nonce
    return response

# Input validation functions
def validate_username(username: str) -> bool:
    """Validate GitHub username format."""
    if not username or len(username) > 39:
        return False
    # GitHub username rules: alphanumeric and hyphens, cannot start/end with hyphen
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$'
    return bool(re.match(pattern, username))

def sanitize_html_content(content: str) -> str:
    """Sanitize HTML content to prevent XSS."""
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'u', 'i', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'hr'
    ]
    allowed_attributes = {
        'a': ['href', 'title'],
        'code': ['class'],
        'pre': ['class']
    }
    return bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes)

def log_security_event(event_type: str, details: str, ip_address: str = None):
    """Log security events for monitoring."""
    ip = ip_address or request.remote_addr
    logger.warning(f"SECURITY EVENT - {event_type}: {details} from IP: {ip}")

def is_recent_release(date_str: str) -> bool:
    """Check if a release is within the last 30 days."""
    try:
        if not date_str or not isinstance(date_str, str):
            return False
        release_date = datetime.strptime(date_str, '%Y-%m-%d')
        thirty_days_ago = datetime.now() - timedelta(days=30)
        return release_date >= thirty_days_ago
    except (ValueError, TypeError):
        return False

# Global cache for data
cache = {
    'data': None,
    'last_updated': None,
    'username': None
}

def get_github_stats(username: str, token: str = None) -> Dict[str, Any]:
    """Get comprehensive GitHub statistics."""
    if not validate_username(username):
        log_security_event("INVALID_USERNAME", f"Invalid username attempted: {username}")
        raise ValueError("Invalid GitHub username format")
    
    logger.info(f"Fetching GitHub stats for user: {username}")
    
    try:
        tracker = GitHubVersionTracker(token)
        
        # Get repositories
        repos = tracker.get_user_repos(username, include_forks=False)
        
        releases = []
        packages = []
        languages = {}
        total_commits = 0
        
        for repo in repos:
            repo_owner = repo['owner']['login']
            repo_name = repo['name']
            
            # Get latest release
            release = tracker.get_latest_release(repo_owner, repo_name)
            if release:
                # Convert markdown description to HTML with safe settings
                md = markdown.Markdown(
                    extensions=['nl2br', 'fenced_code', 'codehilite'],
                    extension_configs={
                        'codehilite': {
                            'css_class': 'highlight'
                        }
                    }
                )
                
                if release.description and release.description != "No description":
                    # Truncate if too long but preserve markdown structure
                    description = release.description
                    if len(description) > 1000:
                        # Find a good breaking point
                        truncated = description[:1000]
                        last_newline = truncated.rfind('\n')
                        if last_newline > 800:  # If there's a reasonable break point
                            description = truncated[:last_newline] + "\n\n*[Truncated - see full release notes]*"
                        else:
                            description = truncated + "...\n\n*[Truncated - see full release notes]*"
                    
                    html_description = md.convert(description)
                    # Sanitize HTML to prevent XSS
                    html_description = sanitize_html_content(html_description)
                else:
                    html_description = "<em>No description available</em>"
                
                releases.append({
                    'repo_name': release.repo_name,
                    'latest_version': release.latest_version,
                    'release_date': release.release_date,
                    'release_url': release.release_url,
                    'download_count': release.download_count,
                    'is_prerelease': release.is_prerelease,
                    'description': html_description,
                    'language': release.language,
                    'stars': release.stars,
                    'forks': release.forks
                })
            
            # Get packages
            repo_packages = tracker.get_packages(repo_owner, repo_name)
            for pkg in repo_packages:
                packages.append({
                    'repo_name': pkg.repo_name,
                    'package_type': pkg.package_type,
                    'latest_version': pkg.latest_version,
                    'package_url': pkg.package_url,
                    'downloads': pkg.downloads
                })
            
            # Count languages
            if repo.get('language'):
                lang = repo['language']
                languages[lang] = languages.get(lang, 0) + 1
        
        # Sort all releases by date (most recent first) for better display
        releases.sort(key=lambda x: x['release_date'], reverse=True)
        
        # Calculate advanced stats
        total_stars = sum(r['stars'] for r in releases)
        total_forks = sum(r['forks'] for r in releases)
        total_downloads = sum(r['download_count'] for r in releases)
        
        # Get recent activity (last 30 days)
        recent_releases = [r for r in releases if is_recent_release(r['release_date'])]
        
        # Sort recent releases by date (most recent first)
        recent_releases.sort(key=lambda x: x['release_date'], reverse=True)
        
        # Language distribution
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Project categories
        categories = categorize_projects(releases)
        
        return {
            'username': username,
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_repositories': len(repos),
                'total_releases': len(releases),
                'total_packages': len(packages),
                'total_downloads': total_downloads,
                'total_stars': total_stars,
                'total_forks': total_forks,
                'recent_releases': len(recent_releases),
                'active_languages': len(languages)
            },
            'releases': releases,
            'packages': packages,
            'languages': top_languages,
            'categories': categories,
            'recent_activity': recent_releases[:10]  # Last 10 recent releases
        }
    
    except Exception as e:
        logger.error(f"Error fetching GitHub stats for {username}: {str(e)}")
        log_security_event("API_ERROR", f"GitHub API error for user {username}: {str(e)}")
        raise

def is_recent_release(date_str: str) -> bool:
    """Check if a release is within the last 30 days."""
    try:
        release_date = datetime.strptime(date_str, '%Y-%m-%d')
        thirty_days_ago = datetime.now() - timedelta(days=30)
        return release_date >= thirty_days_ago
    except:
        return False

def categorize_projects(releases: List[Dict]) -> Dict[str, int]:
    """Categorize projects based on language and naming patterns."""
    categories = {
        'Web Development': 0,
        'Data Science': 0,
        'DevOps': 0,
        'Mobile': 0,
        'Desktop': 0,
        'Libraries': 0,
        'Tools': 0,
        'Other': 0
    }
    
    for release in releases:
        lang = (release.get('language') or '').lower()
        name = release.get('repo_name', '').lower()
        
        if any(term in name for term in ['web', 'site', 'html', 'css', 'js']) or lang in ['javascript', 'typescript', 'html', 'css']:
            categories['Web Development'] += 1
        elif any(term in name for term in ['data', 'ml', 'ai', 'analysis']) or lang in ['python', 'r', 'jupyter notebook']:
            categories['Data Science'] += 1
        elif any(term in name for term in ['docker', 'k8s', 'deploy', 'ci', 'cd']) or lang in ['shell', 'dockerfile']:
            categories['DevOps'] += 1
        elif lang in ['swift', 'kotlin', 'java', 'dart']:
            categories['Mobile'] += 1
        elif lang in ['c++', 'c#', 'c', 'rust', 'go']:
            categories['Desktop'] += 1
        elif any(term in name for term in ['lib', 'sdk', 'api', 'framework']):
            categories['Libraries'] += 1
        elif any(term in name for term in ['tool', 'cli', 'util', 'helper']):
            categories['Tools'] += 1
        else:
            categories['Other'] += 1
    
    return {k: v for k, v in categories.items() if v > 0}

def update_cache_async(username: str, token: str = None):
    """Update cache in background."""
    def update():
        try:
            data = get_github_stats(username, token)
            cache['data'] = data
            cache['last_updated'] = datetime.now()
            cache['username'] = username
            logger.info(f"Cache updated for {username}")
        except Exception as e:
            logger.error(f"Error updating cache: {e}")
    
    thread = threading.Thread(target=update)
    thread.daemon = True
    thread.start()

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/api/stats/<username>')
@limiter.limit("30 per minute")  # Rate limiting
def api_stats(username):
    """API endpoint to get GitHub stats with enhanced security."""
    token = os.getenv('GITHUB_TOKEN')
    
    # Validate username format
    if not validate_username(username):
        log_security_event("INVALID_USERNAME", f"Invalid username attempted: {username}")
        return jsonify({'error': 'Invalid username format'}), 400
    
    # Check if we have cached data for this user
    if (cache['data'] and 
        cache['username'] == username and 
        cache['last_updated'] and 
        (datetime.now() - cache['last_updated']).total_seconds() < 86400):  # 24 hours cache
        # Add cache info to response
        response_data = cache['data'].copy()
        response_data['cache_info'] = {
            'cached': True,
            'cache_age_hours': round((datetime.now() - cache['last_updated']).total_seconds() / 3600, 1),
            'next_refresh_hours': round(24 - (datetime.now() - cache['last_updated']).total_seconds() / 3600, 1)
        }
        return jsonify(response_data)
    
    # Update cache in background for next request
    update_cache_async(username, token)
    
    # If no cached data, get it synchronously
    if not cache['data'] or cache['username'] != username:
        try:
            data = get_github_stats(username, token)
            cache['data'] = data
            cache['last_updated'] = datetime.now()
            cache['username'] = username
            data['cache_info'] = {
                'cached': False,
                'cache_age_hours': 0,
                'next_refresh_hours': 24
            }
            return jsonify(data)
        except Exception as e:
            logger.error(f"Error fetching stats: {e}")
            return jsonify({'error': str(e)}), 500
    
    # Return existing cache with info
    response_data = cache['data'].copy()
    response_data['cache_info'] = {
        'cached': True,
        'cache_age_hours': round((datetime.now() - cache['last_updated']).total_seconds() / 3600, 1),
        'next_refresh_hours': round(24 - (datetime.now() - cache['last_updated']).total_seconds() / 3600, 1)
    }
    return jsonify(response_data)

@app.route('/api/refresh/<username>')
@limiter.limit("5 per minute")  # Stricter rate limiting for refresh
def api_refresh(username):
    """Force refresh data for a user with enhanced security."""
    token = os.getenv('GITHUB_TOKEN')
    
    # Validate username format
    if not validate_username(username):
        log_security_event("INVALID_USERNAME", f"Invalid username attempted in refresh: {username}")
        return jsonify({'error': 'Invalid username format'}), 400
    
    try:
        data = get_github_stats(username, token)
        cache['data'] = data
        cache['last_updated'] = datetime.now()
        cache['username'] = username
        logger.info(f"Data refreshed successfully for user: {username}")
        return jsonify({'status': 'success', 'message': 'Data refreshed'})
    except Exception as e:
        logger.error(f"Error refreshing data for {username}: {e}")
        log_security_event("REFRESH_ERROR", f"Refresh error for user {username}: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Unable to refresh data'}), 500

# Error handlers for rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors."""
    log_security_event("RATE_LIMIT_EXCEEDED", f"Rate limit exceeded: {e.description}")
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

@app.errorhandler(404)
def not_found_handler(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error_handler(e):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Use environment variable to control debug mode
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=8080)
