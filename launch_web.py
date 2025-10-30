#!/usr/bin/env python3
"""
Quick launcher for the GitHub Version Tracker web interface.

This script provides a user-friendly way to start the web application
with automatic browser opening and helpful status messages.
"""

import os
import sys
import webbrowser
import time
import subprocess
from threading import Timer

def open_browser():
    """
    Open the web browser after a short delay.
    
    This gives the Flask server time to start before attempting
    to load the page.
    """
    webbrowser.open('http://localhost:8080')

def check_dependencies():
    """
    Check if required dependencies are installed.
    
    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    try:
        import flask
        import flask_cors
        import flask_limiter
        return True
    except ImportError:
        return False

def main():
    """
    Launch the web application.
    
    This function:
    1. Checks for dependencies
    2. Verifies GitHub token availability
    3. Starts the Flask web server
    4. Opens the browser automatically
    """
    print("🚀 Starting GitHub Version Tracker Web App...")
    print("=" * 60)
    
    # Check dependencies first
    if not check_dependencies():
        print("❌ Error: Missing required dependencies")
        print()
        print("Please install dependencies with:")
        print("   pip install -r requirements.txt")
        print()
        print("Required packages:")
        print("   • flask")
        print("   • flask-cors")
        print("   • flask-limiter")
        print("   • requests")
        print("   • rich")
        print("=" * 60)
        sys.exit(1)
    
    # Check if we have a GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if token:
        print("✅ GitHub token found - Higher rate limits enabled")
        print("   Rate limit: 5,000 requests/hour")
    else:
        print("⚠️  No GitHub token found - Using default rate limits")
        print("   Rate limit: 60 requests/hour")
        print()
        print("   To increase rate limits:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your token: GITHUB_TOKEN=your_token_here")
        print("   3. Restart the web app")
    
    print()
    print("📱 Web interface will be available at:")
    print("   → http://localhost:8080")
    print()
    print("🎨 Features:")
    print("   • Modern cyberpunk UI with glassmorphism effects")
    print("   • Real-time GitHub repository and release tracking")
    print("   • Interactive statistics and visualizations")
    print("   • Responsive design for all devices")
    print("   • Package tracking (npm, PyPI, etc.)")
    print("   • Smart caching for optimal performance")
    print()
    print("🛑 To stop the server, press Ctrl+C")
    print("=" * 60)
    print("Starting server...\n")
    
    # Open browser after 2 seconds (gives server time to start)
    Timer(2.0, open_browser).start()
    
    try:
        # Import and run the web app
        from web_app import app
        app.run(
            debug=False,      # Set to True for development
            host='0.0.0.0',   # Listen on all network interfaces
            port=8080,        # Default port
            threaded=True     # Handle multiple requests concurrently
        )
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        print("=" * 60)
        print("Thank you for using GitHub Version Tracker!")
        print("Star us on GitHub: https://github.com/fabriziosalmi/versiontracker")
        print("=" * 60)
        sys.exit(0)
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print()
        print("Please ensure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        print("=" * 60)
        sys.exit(1)
    except OSError as e:
        if "Address already in use" in str(e):
            print("\n❌ Error: Port 8080 is already in use")
            print()
            print("Solutions:")
            print("   1. Stop the other process using port 8080")
            print("   2. Or modify launch_web.py to use a different port")
            print()
            print("To find what's using port 8080:")
            print("   Linux/Mac: lsof -ti:8080")
            print("   Windows: netstat -ano | findstr :8080")
            print("=" * 60)
        else:
            print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print()
        print("Please report this issue:")
        print("   https://github.com/fabriziosalmi/versiontracker/issues")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
