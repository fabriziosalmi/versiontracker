#!/usr/bin/env python3
"""
GitHub Version Tracker
A tool to generate reports of latest published versions across GitHub repositories.
"""

import os
import requests
import json
import base64
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from tabulate import tabulate
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import click

@dataclass
class ReleaseInfo:
    """Data class for repository release information."""
    repo_name: str
    latest_version: str
    release_date: str
    release_url: str
    download_count: int
    is_prerelease: bool
    description: str
    language: str
    stars: int
    forks: int

@dataclass
class PackageInfo:
    """Data class for package information."""
    repo_name: str
    package_type: str
    latest_version: str
    package_url: str
    downloads: int

class GitHubVersionTracker:
    """Main class for tracking GitHub repository versions."""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Version-Tracker'
        }
        if token:
            self.headers['Authorization'] = f'token {token}'
        
        self.console = Console()
    
    def get_user_repos(self, username: str, include_forks: bool = False) -> List[Dict[str, Any]]:
        """Get all repositories for a user."""
        repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f"https://api.github.com/users/{username}/repos"
            params = {
                'page': page,
                'per_page': per_page,
                'sort': 'updated',
                'direction': 'desc'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                self.console.print(f"[red]Error fetching repositories: {response.status_code}[/red]")
                break
            
            page_repos = response.json()
            if not page_repos:
                break
            
            if not include_forks:
                page_repos = [repo for repo in page_repos if not repo['fork']]
            
            repos.extend(page_repos)
            page += 1
            
            # GitHub API pagination limit
            if len(page_repos) < per_page:
                break
        
        return repos
    
    def get_latest_release(self, repo_owner: str, repo_name: str) -> Optional[ReleaseInfo]:
        """Get the latest release for a repository."""
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            return None
        
        release_data = response.json()
        
        # Calculate total download count
        download_count = sum(asset.get('download_count', 0) for asset in release_data.get('assets', []))
        
        # Get repository info
        repo_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        repo_response = requests.get(repo_url, headers=self.headers)
        repo_info = repo_response.json() if repo_response.status_code == 200 else {}
        
        return ReleaseInfo(
            repo_name=f"{repo_owner}/{repo_name}",
            latest_version=release_data.get('tag_name', 'N/A'),
            release_date=self._format_date(release_data.get('published_at')),
            release_url=release_data.get('html_url', ''),
            download_count=download_count,
            is_prerelease=release_data.get('prerelease', False),
            description=release_data.get('body', '') or 'No description',
            language=repo_info.get('language') or 'Unknown',
            stars=repo_info.get('stargazers_count', 0),
            forks=repo_info.get('forks_count', 0)
        )
    
    def get_packages(self, repo_owner: str, repo_name: str) -> List[PackageInfo]:
        """Get packages for a repository."""
        packages = []
        
        # Check for npm packages
        npm_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/package.json"
        npm_response = requests.get(npm_url, headers=self.headers)
        
        if npm_response.status_code == 200:
            try:
                # Get package.json content
                content = base64.b64decode(npm_response.json()['content']).decode('utf-8')
                package_data = json.loads(content)
                package_name = package_data.get('name')
                
                if package_name:
                    # Try to get npm package info
                    npm_api_url = f"https://registry.npmjs.org/{package_name}"
                    npm_pkg_response = requests.get(npm_api_url)
                    
                    if npm_pkg_response.status_code == 200:
                        npm_data = npm_pkg_response.json()
                        latest_version = npm_data.get('dist-tags', {}).get('latest', 'Unknown')
                        
                        packages.append(PackageInfo(
                            repo_name=f"{repo_owner}/{repo_name}",
                            package_type="npm",
                            latest_version=latest_version,
                            package_url=f"https://www.npmjs.com/package/{package_name}",
                            downloads=0  # Would need additional API call to get download stats
                        ))
            except Exception:
                pass
        
        # Check for Python packages (setup.py, pyproject.toml)
        python_files = ['setup.py', 'pyproject.toml', 'setup.cfg']
        for file in python_files:
            py_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file}"
            py_response = requests.get(py_url, headers=self.headers)
            
            if py_response.status_code == 200:
                try:
                    # Try to get package name from the file
                    package_name = None
                    
                    if file == 'setup.py':
                        # Try to extract package name from setup.py
                        content = base64.b64decode(py_response.json()['content']).decode('utf-8')
                        # Simple regex to find name parameter
                        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                        if name_match:
                            package_name = name_match.group(1)
                    
                    elif file == 'pyproject.toml':
                        # Try to extract package name from pyproject.toml
                        content = base64.b64decode(py_response.json()['content']).decode('utf-8')
                        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                        if name_match:
                            package_name = name_match.group(1)
                    
                    if package_name:
                        # Try to get PyPI package info
                        pypi_url = f"https://pypi.org/pypi/{package_name}/json"
                        pypi_response = requests.get(pypi_url)
                        
                        if pypi_response.status_code == 200:
                            pypi_data = pypi_response.json()
                            latest_version = pypi_data.get('info', {}).get('version', 'Unknown')
                            
                            packages.append(PackageInfo(
                                repo_name=f"{repo_owner}/{repo_name}",
                                package_type="python",
                                latest_version=latest_version,
                                package_url=f"https://pypi.org/project/{package_name}/",
                                downloads=0
                            ))
                        else:
                            # Fallback if PyPI lookup fails
                            packages.append(PackageInfo(
                                repo_name=f"{repo_owner}/{repo_name}",
                                package_type="python",
                                latest_version="Unknown",
                                package_url=f"https://github.com/{repo_owner}/{repo_name}",
                                downloads=0
                            ))
                    else:
                        # Fallback if we can't extract package name
                        packages.append(PackageInfo(
                            repo_name=f"{repo_owner}/{repo_name}",
                            package_type="python",
                            latest_version="Unknown",
                            package_url=f"https://github.com/{repo_owner}/{repo_name}",
                            downloads=0
                        ))
                        
                except Exception:
                    # Fallback on any error
                    packages.append(PackageInfo(
                        repo_name=f"{repo_owner}/{repo_name}",
                        package_type="python",
                        latest_version="Unknown",
                        package_url=f"https://github.com/{repo_owner}/{repo_name}",
                        downloads=0
                    ))
                break
        
        return packages
    
    def _format_date(self, date_str: str) -> str:
        """Format ISO date string to readable format."""
        if not date_str:
            return "Unknown"
        
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')
        except Exception:
            return date_str
    
    def generate_report(self, username: str, include_forks: bool = False, output_format: str = 'table') -> None:
        """Generate a comprehensive version report."""
        self.console.print(f"[bold blue]Fetching repositories for {username}...[/bold blue]")
        
        repos = self.get_user_repos(username, include_forks)
        
        if not repos:
            self.console.print("[red]No repositories found or error occurred.[/red]")
            return
        
        self.console.print(f"[green]Found {len(repos)} repositories. Checking for releases...[/green]")
        
        releases = []
        packages = []
        
        for repo in repos:
            repo_owner = repo['owner']['login']
            repo_name = repo['name']
            
            # Get latest release
            release = self.get_latest_release(repo_owner, repo_name)
            if release:
                releases.append(release)
            
            # Get packages
            repo_packages = self.get_packages(repo_owner, repo_name)
            packages.extend(repo_packages)
        
        # Display results
        if output_format == 'rich':
            self._display_rich_report(releases, packages, username)
        elif output_format == 'json':
            self._display_json_report(releases, packages)
        else:
            self._display_table_report(releases, packages)
    
    def _display_rich_report(self, releases: List[ReleaseInfo], packages: List[PackageInfo], username: str) -> None:
        """Display report using Rich formatting."""
        
        # Summary panel
        total_downloads = sum(r.download_count for r in releases)
        total_stars = sum(r.stars for r in releases)
        total_forks = sum(r.forks for r in releases)
        
        summary_text = f"""
[bold]Total Repositories with Releases:[/bold] {len(releases)}
[bold]Total Download Count:[/bold] {total_downloads:,}
[bold]Total Stars:[/bold] {total_stars:,}
[bold]Total Forks:[/bold] {total_forks:,}
[bold]Report Generated:[/bold] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        self.console.print(Panel(summary_text, title=f"GitHub Version Report - {username}", border_style="blue"))
        
        if releases:
            # Releases table
            table = Table(title="Latest Releases", show_header=True, header_style="bold magenta")
            table.add_column("Repository", style="cyan", no_wrap=True)
            table.add_column("Version", style="green")
            table.add_column("Release Date", style="yellow")
            table.add_column("Language", style="blue")
            table.add_column("Stars", justify="right", style="gold1")
            table.add_column("Downloads", justify="right", style="green")
            table.add_column("Pre-release", justify="center")
            
            for release in sorted(releases, key=lambda x: x.stars, reverse=True):
                prerelease = "✓" if release.is_prerelease else ""
                table.add_row(
                    release.repo_name,
                    release.latest_version,
                    release.release_date,
                    release.language or "Unknown",
                    str(release.stars),
                    str(release.download_count),
                    prerelease
                )
            
            self.console.print(table)
        
        if packages:
            # Packages table
            pkg_table = Table(title="Published Packages", show_header=True, header_style="bold cyan")
            pkg_table.add_column("Repository", style="cyan")
            pkg_table.add_column("Package Type", style="magenta")
            pkg_table.add_column("Latest Version", style="green")
            pkg_table.add_column("Package URL", style="blue")
            
            for package in packages:
                pkg_table.add_row(
                    package.repo_name,
                    package.package_type,
                    package.latest_version,
                    package.package_url
                )
            
            self.console.print(pkg_table)
    
    def _display_table_report(self, releases: List[ReleaseInfo], packages: List[PackageInfo]) -> None:
        """Display report using simple tables."""
        
        if releases:
            print("\n" + "="*80)
            print("LATEST RELEASES")
            print("="*80)
            
            headers = ["Repository", "Version", "Date", "Language", "Stars", "Downloads", "Pre-release"]
            rows = []
            
            for release in sorted(releases, key=lambda x: x.stars, reverse=True):
                rows.append([
                    release.repo_name,
                    release.latest_version,
                    release.release_date,
                    release.language or "Unknown",
                    release.stars,
                    release.download_count,
                    "Yes" if release.is_prerelease else "No"
                ])
            
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        
        if packages:
            print("\n" + "="*80)
            print("PUBLISHED PACKAGES")
            print("="*80)
            
            headers = ["Repository", "Type", "Version", "URL"]
            rows = []
            
            for package in packages:
                rows.append([
                    package.repo_name,
                    package.package_type,
                    package.latest_version,
                    package.package_url
                ])
            
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        
        # Summary
        total_downloads = sum(r.download_count for r in releases)
        total_stars = sum(r.stars for r in releases)
        
        print(f"\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        print(f"Repositories with releases: {len(releases)}")
        print(f"Published packages: {len(packages)}")
        print(f"Total download count: {total_downloads:,}")
        print(f"Total stars: {total_stars:,}")
    
    def _display_json_report(self, releases: List[ReleaseInfo], packages: List[PackageInfo]) -> None:
        """Display report in JSON format."""
        
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_releases": len(releases),
                "total_packages": len(packages),
                "total_downloads": sum(r.download_count for r in releases),
                "total_stars": sum(r.stars for r in releases),
                "total_forks": sum(r.forks for r in releases)
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
        
        print(json.dumps(report_data, indent=2))

@click.command()
@click.option('--username', '-u', required=True, help='GitHub username to analyze')
@click.option('--token', '-t', help='GitHub personal access token (optional, for higher rate limits)')
@click.option('--include-forks', '-f', is_flag=True, help='Include forked repositories')
@click.option('--format', '-F', type=click.Choice(['table', 'rich', 'json']), default='rich', help='Output format')
@click.option('--save', '-s', help='Save report to file')
def main(username: str, token: str, include_forks: bool, format: str, save: str):
    """Generate a GitHub version report for a user's repositories."""
    
    # Load token from environment if not provided
    if not token:
        token = os.getenv('GITHUB_TOKEN')
    
    tracker = GitHubVersionTracker(token)
    
    if save:
        # Redirect output to file
        import sys
        original_stdout = sys.stdout
        with open(save, 'w') as f:
            if format == 'rich':
                # For rich format, we'll use table format when saving to file
                sys.stdout = f
                repos = tracker.get_user_repos(username, include_forks)
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
                tracker.generate_report(username, include_forks, format)
        
        sys.stdout = original_stdout
        print(f"Report saved to {save}")
    else:
        tracker.generate_report(username, include_forks, format)

if __name__ == "__main__":
    main()
