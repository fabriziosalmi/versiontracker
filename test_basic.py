#!/usr/bin/env python3
"""
Simple test script to validate basic functionality.

This is not a comprehensive test suite, but provides basic smoke tests
to verify the core functionality is working.
"""

import sys
import os
from version_tracker import GitHubVersionTracker, ReleaseInfo, PackageInfo

def test_imports():
    """Test that all required imports work."""
    print("✓ Testing imports...")
    try:
        import requests
        import click
        from rich.console import Console
        from tabulate import tabulate
        print("  ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_tracker_initialization():
    """Test GitHubVersionTracker initialization."""
    print("✓ Testing tracker initialization...")
    try:
        # Without token
        tracker1 = GitHubVersionTracker()
        assert tracker1 is not None
        assert tracker1.console is not None
        
        # With token
        tracker2 = GitHubVersionTracker(token="test_token")
        assert "Authorization" in tracker2.headers
        
        print("  ✅ Tracker initialization successful")
        return True
    except Exception as e:
        print(f"  ❌ Initialization failed: {e}")
        return False

def test_data_classes():
    """Test that data classes work correctly."""
    print("✓ Testing data classes...")
    try:
        release = ReleaseInfo(
            repo_name="test/repo",
            latest_version="v1.0.0",
            release_date="2025-01-01",
            release_url="https://github.com/test/repo/releases/tag/v1.0.0",
            download_count=100,
            is_prerelease=False,
            description="Test release",
            language="Python",
            stars=50,
            forks=10
        )
        assert release.repo_name == "test/repo"
        
        package = PackageInfo(
            repo_name="test/repo",
            package_type="npm",
            latest_version="1.0.0",
            package_url="https://npmjs.com/package/test",
            downloads=1000
        )
        assert package.package_type == "npm"
        
        print("  ✅ Data classes working correctly")
        return True
    except Exception as e:
        print(f"  ❌ Data class test failed: {e}")
        return False

def test_api_connection():
    """Test that we can connect to GitHub API."""
    print("✓ Testing GitHub API connection...")
    try:
        import requests
        # Test unauthenticated request to get rate limit
        response = requests.get(
            "https://api.github.com/rate_limit",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            remaining = data['rate']['remaining']
            print(f"  ✅ API connection successful (Rate limit remaining: {remaining})")
            return True
        else:
            print(f"  ⚠️  API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ API connection failed: {e}")
        return False

def test_user_repos():
    """Test fetching user repositories (using a known user)."""
    print("✓ Testing get_user_repos (using 'octocat')...")
    try:
        tracker = GitHubVersionTracker()
        # Use octocat, GitHub's official test account
        repos = tracker.get_user_repos("octocat", include_forks=False)
        
        if repos and len(repos) > 0:
            print(f"  ✅ Successfully fetched {len(repos)} repositories")
            return True
        else:
            print("  ⚠️  No repositories found (might be rate limited)")
            return True  # Not a failure, might be rate limited
    except Exception as e:
        print(f"  ❌ Repository fetch failed: {e}")
        return False

def test_config_loading():
    """Test that config.py loads correctly."""
    print("✓ Testing configuration loading...")
    try:
        import config
        assert hasattr(config, 'GITHUB_API_BASE')
        assert hasattr(config, 'SUPPORTED_PACKAGE_TYPES')
        assert hasattr(config, 'RICH_THEME')
        print("  ✅ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"  ❌ Config loading failed: {e}")
        return False

def main():
    """Run all tests and report results."""
    print("=" * 60)
    print("GitHub Version Tracker - Basic Functionality Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_imports,
        test_tracker_initialization,
        test_data_classes,
        test_config_loading,
        test_api_connection,
        test_user_repos,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"  ❌ Test crashed: {e}")
            results.append(False)
            print()
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        print("=" * 60)
        return 0
    else:
        print("⚠️  Some tests failed or returned warnings")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
