#!/usr/bin/env python3
"""
Quick example script showing how to use the GitHub Version Tracker.
"""

import os
from version_tracker import GitHubVersionTracker

def main():
    # Example usage
    username = "octocat"  # Replace with your GitHub username
    
    # You can set your GitHub token as an environment variable
    # or pass it directly to the GitHubVersionTracker
    token = os.getenv('GITHUB_TOKEN')
    
    # Create tracker instance
    tracker = GitHubVersionTracker(token)
    
    # Generate report with rich formatting
    print("Generating GitHub version report...")
    tracker.generate_report(username, include_forks=False, output_format='rich')

if __name__ == "__main__":
    main()
