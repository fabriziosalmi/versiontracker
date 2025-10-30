#!/usr/bin/env python3
"""
Quick start script - customize this with your GitHub username and run!

This script provides a simple way to generate GitHub version reports
with minimal configuration. Just set your username and run.
"""

import os
import sys
from version_tracker import GitHubVersionTracker

# 🔧 CUSTOMIZE THESE SETTINGS
YOUR_GITHUB_USERNAME = "your-username-here"  # Replace with your GitHub username
INCLUDE_FORKED_REPOS = False  # Set to True if you want to include forked repositories
OUTPUT_FORMAT = "rich"  # Options: "rich", "table", "json"
SAVE_TO_FILE = None  # Set to a filename like "my_report.txt" to save output

def main():
    """
    Generate your GitHub version report.
    
    This function:
    1. Validates configuration
    2. Sets up GitHub authentication (if available)
    3. Creates tracker instance
    4. Generates and displays/saves the report
    """
    
    # Check if username is configured
    if YOUR_GITHUB_USERNAME == "your-username-here":
        print("❌ Configuration Required!")
        print("=" * 60)
        print("Please edit this script and set YOUR_GITHUB_USERNAME")
        print("to your actual GitHub username.")
        print()
        print("Example:")
        print('  YOUR_GITHUB_USERNAME = "fabriziosalmi"')
        print()
        print(f"File to edit: {__file__}")
        print("=" * 60)
        sys.exit(1)
    
    # Get GitHub token from environment (optional but recommended)
    github_token = os.getenv('GITHUB_TOKEN')
    
    print("🚀 GitHub Version Tracker - Quick Start")
    print("=" * 60)
    print(f"📂 Username: {YOUR_GITHUB_USERNAME}")
    print(f"🍴 Include forks: {INCLUDE_FORKED_REPOS}")
    print(f"📊 Output format: {OUTPUT_FORMAT}")
    
    if not github_token:
        print("⚠️  No GitHub token found")
        print("   Running with default rate limits (60 requests/hour)")
        print()
        print("💡 Tip: Set GITHUB_TOKEN environment variable for higher limits")
        print("   Without token: 60 requests/hour")
        print("   With token: 5,000 requests/hour")
        print()
        print("   To set token:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your token: GITHUB_TOKEN=your_token_here")
        print("   Or: export GITHUB_TOKEN=your_token_here")
    else:
        print("✅ GitHub token found - Higher rate limits enabled")
    
    print("=" * 60)
    print()
    
    # Create tracker
    tracker = GitHubVersionTracker(github_token)
    
    # Generate report
    print(f"📊 Generating report for {YOUR_GITHUB_USERNAME}...")
    print()
    
    if SAVE_TO_FILE:
        # Save to file
        original_stdout = sys.stdout
        try:
            with open(SAVE_TO_FILE, 'w', encoding='utf-8') as f:
                if OUTPUT_FORMAT == 'rich':
                    # For rich format, use table when saving to file
                    # (rich colors don't work well in text files)
                    sys.stdout = f
                    repos = tracker.get_user_repos(YOUR_GITHUB_USERNAME, INCLUDE_FORKED_REPOS)
                    releases = []
                    packages = []
                    
                    for repo in repos:
                        repo_owner = repo['owner']['login']
                        repo_name = repo['name']
                        
                        release = tracker.get_latest_release(repo_owner, repo_name)
                        if release:
                            releases.append(release)
                        
                        repo_packages = tracker.get_packages(repo_owner, repo_name)
                        packages.extend(repo_packages)
                    
                    tracker._display_table_report(releases, packages)
                else:
                    sys.stdout = f
                    tracker.generate_report(YOUR_GITHUB_USERNAME, INCLUDE_FORKED_REPOS, OUTPUT_FORMAT)
        finally:
            sys.stdout = original_stdout
        
        print(f"✅ Report saved successfully!")
        print(f"📄 File: {SAVE_TO_FILE}")
        print(f"📏 Size: {os.path.getsize(SAVE_TO_FILE)} bytes")
    else:
        # Display to console
        tracker.generate_report(YOUR_GITHUB_USERNAME, INCLUDE_FORKED_REPOS, OUTPUT_FORMAT)
    
    print()
    print("=" * 60)
    print("✅ Report generation complete!")
    print()
    print("💡 Next steps:")
    print("   • Try different output formats (rich, table, json)")
    print("   • Use --include-forks to see forked repositories")
    print("   • Set SAVE_TO_FILE to save the report")
    print("   • Launch web interface: python launch_web.py")

if __name__ == "__main__":
    main()
