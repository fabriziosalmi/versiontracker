#!/usr/bin/env python3
"""
Quick example script showing how to use the GitHub Version Tracker.

This example demonstrates basic usage of the GitHubVersionTracker class
to generate a formatted report for a GitHub user.
"""

import os
from version_tracker import GitHubVersionTracker

def main():
    """
    Main function demonstrating basic usage.
    
    This example:
    1. Retrieves GitHub token from environment (optional)
    2. Creates a tracker instance
    3. Generates a rich-formatted report for a user
    """
    # Example usage - replace with your GitHub username
    username = "octocat"  # GitHub's official mascot account
    
    # Get GitHub token from environment variable (optional but recommended)
    # Set with: export GITHUB_TOKEN=your_token_here
    # Or create a .env file with: GITHUB_TOKEN=your_token_here
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        print("⚠️  No GITHUB_TOKEN found in environment")
        print("   Running without authentication (60 requests/hour limit)")
        print("   Set GITHUB_TOKEN for 5,000 requests/hour\n")
    
    # Create tracker instance with optional token
    tracker = GitHubVersionTracker(token)
    
    # Generate report with rich formatting (colored output with tables)
    print(f"📊 Generating GitHub version report for '{username}'...")
    print("=" * 60)
    
    tracker.generate_report(
        username=username,
        include_forks=False,  # Set to True to include forked repositories
        output_format='rich'   # Options: 'rich', 'table', 'json'
    )
    
    print("\n" + "=" * 60)
    print("💡 Tip: Try with your own username!")
    print(f"   python {__file__} --username YOUR_USERNAME")

if __name__ == "__main__":
    main()
