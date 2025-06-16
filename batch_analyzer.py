#!/usr/bin/env python3
"""
Advanced example showing batch processing and custom reporting.
"""

import os
import json
from datetime import datetime
from version_tracker import GitHubVersionTracker

def analyze_multiple_users(usernames: list, output_dir: str = "reports"):
    """Analyze multiple GitHub users and save individual reports."""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get GitHub token
    token = os.getenv('GITHUB_TOKEN')
    tracker = GitHubVersionTracker(token)
    
    all_reports = {}
    
    for username in usernames:
        print(f"\n🔍 Analyzing {username}...")
        
        try:
            # Get repositories
            repos = tracker.get_user_repos(username, include_forks=False)
            
            releases = []
            packages = []
            
            for repo in repos:
                repo_owner = repo['owner']['login']
                repo_name = repo['name']
                
                # Get latest release
                release = tracker.get_latest_release(repo_owner, repo_name)
                if release:
                    releases.append(release)
                
                # Get packages
                repo_packages = tracker.get_packages(repo_owner, repo_name)
                packages.extend(repo_packages)
            
            # Create report data
            report_data = {
                "username": username,
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_repositories": len(repos),
                    "total_releases": len(releases),
                    "total_packages": len(packages),
                    "total_downloads": sum(r.download_count for r in releases),
                    "total_stars": sum(r.stars for r in releases),
                    "total_forks": sum(r.forks for r in releases),
                    "most_popular_language": get_most_popular_language(releases),
                    "most_starred_repo": get_most_starred_repo(releases)
                },
                "releases": [
                    {
                        "repo_name": r.repo_name,
                        "latest_version": r.latest_version,
                        "release_date": r.release_date,
                        "release_url": r.release_url,
                        "download_count": r.download_count,
                        "is_prerelease": r.is_prerelease,
                        "description": r.description,
                        "language": r.language,
                        "stars": r.stars,
                        "forks": r.forks
                    } for r in releases
                ],
                "packages": [
                    {
                        "repo_name": p.repo_name,
                        "package_type": p.package_type,
                        "latest_version": p.latest_version,
                        "package_url": p.package_url,
                        "downloads": p.downloads
                    } for p in packages
                ]
            }
            
            all_reports[username] = report_data
            
            # Save individual report
            filename = f"{output_dir}/{username}_report.json"
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"✅ Report saved: {filename}")
            print(f"   Repositories: {len(repos)}, Releases: {len(releases)}, Packages: {len(packages)}")
            
        except Exception as e:
            print(f"❌ Error analyzing {username}: {e}")
            continue
    
    # Save combined report
    combined_filename = f"{output_dir}/combined_report.json"
    with open(combined_filename, 'w') as f:
        json.dump(all_reports, f, indent=2)
    
    print(f"\n📊 Combined report saved: {combined_filename}")
    
    # Generate summary
    generate_summary_report(all_reports, output_dir)

def get_most_popular_language(releases):
    """Get the most popular programming language from releases."""
    if not releases:
        return "Unknown"
    
    language_counts = {}
    for release in releases:
        lang = release.language or "Unknown"
        language_counts[lang] = language_counts.get(lang, 0) + 1
    
    return max(language_counts, key=language_counts.get)

def get_most_starred_repo(releases):
    """Get the repository with the most stars."""
    if not releases:
        return "None"
    
    most_starred = max(releases, key=lambda r: r.stars)
    return f"{most_starred.repo_name} ({most_starred.stars} stars)"

def generate_summary_report(all_reports: dict, output_dir: str):
    """Generate a summary report across all users."""
    
    total_repos = sum(report['summary']['total_repositories'] for report in all_reports.values())
    total_releases = sum(report['summary']['total_releases'] for report in all_reports.values())
    total_packages = sum(report['summary']['total_packages'] for report in all_reports.values())
    total_downloads = sum(report['summary']['total_downloads'] for report in all_reports.values())
    total_stars = sum(report['summary']['total_stars'] for report in all_reports.values())
    
    summary_data = {
        "generated_at": datetime.now().isoformat(),
        "total_users_analyzed": len(all_reports),
        "aggregated_stats": {
            "total_repositories": total_repos,
            "total_releases": total_releases,
            "total_packages": total_packages,
            "total_downloads": total_downloads,
            "total_stars": total_stars
        },
        "user_summaries": {
            username: report['summary'] for username, report in all_reports.items()
        }
    }
    
    filename = f"{output_dir}/summary_report.json"
    with open(filename, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f"📈 Summary report saved: {filename}")
    
    # Print summary to console
    print(f"\n" + "="*60)
    print("BATCH ANALYSIS SUMMARY")
    print("="*60)
    print(f"Users analyzed: {len(all_reports)}")
    print(f"Total repositories: {total_repos}")
    print(f"Total releases: {total_releases}")
    print(f"Total packages: {total_packages}")
    print(f"Total downloads: {total_downloads:,}")
    print(f"Total stars: {total_stars:,}")
    print("="*60)

def main():
    """Example usage of batch analysis."""
    
    # Example: analyze multiple GitHub users
    # Replace with actual usernames you want to analyze
    usernames = [
        "octocat",
        # Add more usernames here
        # "username1",
        # "username2",
    ]
    
    print("🚀 Starting batch GitHub analysis...")
    analyze_multiple_users(usernames)

if __name__ == "__main__":
    main()
