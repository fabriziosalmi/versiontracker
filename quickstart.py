#!/usr/bin/env python3
"""
Quick start script - customize this with your GitHub username and run!
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
    """Generate your GitHub version report."""
    
    # Check if username is configured
    if YOUR_GITHUB_USERNAME == "your-username-here":
        print("❌ Please edit this script and set YOUR_GITHUB_USERNAME to your actual GitHub username!")
        print("   Edit the line: YOUR_GITHUB_USERNAME = \"your-username-here\"")
        sys.exit(1)
    
    # Get GitHub token from environment (optional but recommended)
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("💡 Tip: Set GITHUB_TOKEN environment variable for higher API rate limits")
        print("   Without token: 60 requests/hour")
        print("   With token: 5,000 requests/hour")
        print()
    
    # Create tracker
    tracker = GitHubVersionTracker(github_token)
    
    # Generate report
    print(f"🚀 Generating GitHub version report for {YOUR_GITHUB_USERNAME}...")
    print()
    
    if SAVE_TO_FILE:
        # Save to file
        original_stdout = sys.stdout
        with open(SAVE_TO_FILE, 'w') as f:
            if OUTPUT_FORMAT == 'rich':
                # For rich format, use table when saving to file
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
        
        sys.stdout = original_stdout
        print(f"📄 Report saved to: {SAVE_TO_FILE}")
    else:
        # Display to console
        tracker.generate_report(YOUR_GITHUB_USERNAME, INCLUDE_FORKED_REPOS, OUTPUT_FORMAT)

if __name__ == "__main__":
    main()
