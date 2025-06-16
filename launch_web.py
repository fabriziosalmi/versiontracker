#!/usr/bin/env python3
"""
Quick launcher for the GitHub Version Tracker web interface.
"""

import os
import sys
import webbrowser
import time
import subprocess
from threading import Timer

def open_browser():
    """Open the web browser after a short delay."""
    webbrowser.open('http://localhost:8080')

def main():
    """Launch the web application."""
    print("🚀 Starting GitHub Version Tracker Web App...")
    print("=" * 50)
    
    # Check if we have a GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if token:
        print("✅ GitHub token found - Higher rate limits enabled")
    else:
        print("⚠️  No GitHub token found - Using default rate limits")
        print("   Set GITHUB_TOKEN environment variable for better performance")
    
    print("\n📱 Web interface will be available at:")
    print("   http://localhost:8080")
    print("\n🔥 Features:")
    print("   • Modern cyberpunk UI with glassmorphism effects")
    print("   • Real-time GitHub repository and release tracking")
    print("   • Interactive statistics and visualizations")
    print("   • Responsive design for all devices")
    print("   • Package tracking (npm, PyPI, etc.)")
    
    print("\n" + "=" * 50)
    print("Starting server...")
    
    # Open browser after 2 seconds
    Timer(2.0, open_browser).start()
    
    try:
        # Import and run the web app
        from web_app import app
        app.run(debug=False, host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        sys.exit(0)
    except ImportError:
        print("❌ Error: Missing dependencies. Please run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting web app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
