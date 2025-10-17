#!/usr/bin/env python3
"""
Top 20 GitHub Repositories Finder
Find and display the most popular GitHub repositories

Features:
- Search for top repositories by stars
- Filter by language
- Display key metrics (stars, forks, description)
- Easy-to-use CLI interface
"""

import requests
import sys
import os
from typing import List, Dict, Optional
from datetime import datetime


# Curated list of top GitHub repositories (fallback/offline mode)
TOP_REPOS_CURATED = [
    {"full_name": "freeCodeCamp/freeCodeCamp", "stargazers_count": 400000, "forks_count": 37000, 
     "description": "freeCodeCamp.org's open-source codebase and curriculum. Learn to code for free.", 
     "language": "TypeScript", "html_url": "https://github.com/freeCodeCamp/freeCodeCamp"},
    
    {"full_name": "996icu/996.ICU", "stargazers_count": 269000, "forks_count": 21000,
     "description": "Repo for counting stars and contributing. Press F to pay respect to glorious developers.",
     "language": "Rust", "html_url": "https://github.com/996icu/996.ICU"},
    
    {"full_name": "facebook/react", "stargazers_count": 228000, "forks_count": 46000,
     "description": "The library for web and native user interfaces",
     "language": "JavaScript", "html_url": "https://github.com/facebook/react"},
    
    {"full_name": "vuejs/vue", "stargazers_count": 207000, "forks_count": 33000,
     "description": "This is the repo for Vue 2. For Vue 3, go to https://github.com/vuejs/core",
     "language": "TypeScript", "html_url": "https://github.com/vuejs/vue"},
    
    {"full_name": "tensorflow/tensorflow", "stargazers_count": 186000, "forks_count": 74000,
     "description": "An Open Source Machine Learning Framework for Everyone",
     "language": "C++", "html_url": "https://github.com/tensorflow/tensorflow"},
    
    {"full_name": "twbs/bootstrap", "stargazers_count": 170000, "forks_count": 78000,
     "description": "The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web.",
     "language": "JavaScript", "html_url": "https://github.com/twbs/bootstrap"},
    
    {"full_name": "microsoft/vscode", "stargazers_count": 163000, "forks_count": 29000,
     "description": "Visual Studio Code",
     "language": "TypeScript", "html_url": "https://github.com/microsoft/vscode"},
    
    {"full_name": "torvalds/linux", "stargazers_count": 180000, "forks_count": 53000,
     "description": "Linux kernel source tree",
     "language": "C", "html_url": "https://github.com/torvalds/linux"},
    
    {"full_name": "ohmyzsh/ohmyzsh", "stargazers_count": 173000, "forks_count": 25000,
     "description": "🙃 A delightful community-driven (with 2,300+ contributors) framework for managing your zsh configuration.",
     "language": "Shell", "html_url": "https://github.com/ohmyzsh/ohmyzsh"},
    
    {"full_name": "flutter/flutter", "stargazers_count": 165000, "forks_count": 27000,
     "description": "Flutter makes it easy and fast to build beautiful apps for mobile and beyond",
     "language": "Dart", "html_url": "https://github.com/flutter/flutter"},
    
    {"full_name": "golang/go", "stargazers_count": 123000, "forks_count": 17000,
     "description": "The Go programming language",
     "language": "Go", "html_url": "https://github.com/golang/go"},
    
    {"full_name": "nodejs/node", "stargazers_count": 107000, "forks_count": 29000,
     "description": "Node.js JavaScript runtime ✨🐢🚀✨",
     "language": "JavaScript", "html_url": "https://github.com/nodejs/node"},
    
    {"full_name": "denoland/deno", "stargazers_count": 95000, "forks_count": 5200,
     "description": "A modern runtime for JavaScript and TypeScript.",
     "language": "Rust", "html_url": "https://github.com/denoland/deno"},
    
    {"full_name": "rust-lang/rust", "stargazers_count": 97000, "forks_count": 12000,
     "description": "Empowering everyone to build reliable and efficient software.",
     "language": "Rust", "html_url": "https://github.com/rust-lang/rust"},
    
    {"full_name": "electron/electron", "stargazers_count": 114000, "forks_count": 15000,
     "description": "Build cross-platform desktop apps with JavaScript, HTML, and CSS",
     "language": "C++", "html_url": "https://github.com/electron/electron"},
    
    {"full_name": "kubernetes/kubernetes", "stargazers_count": 110000, "forks_count": 39000,
     "description": "Production-Grade Container Orchestration",
     "language": "Go", "html_url": "https://github.com/kubernetes/kubernetes"},
    
    {"full_name": "axios/axios", "stargazers_count": 105000, "forks_count": 10000,
     "description": "Promise based HTTP client for the browser and node.js",
     "language": "JavaScript", "html_url": "https://github.com/axios/axios"},
    
    {"full_name": "vercel/next.js", "stargazers_count": 125000, "forks_count": 27000,
     "description": "The React Framework",
     "language": "JavaScript", "html_url": "https://github.com/vercel/next.js"},
    
    {"full_name": "python/cpython", "stargazers_count": 62000, "forks_count": 30000,
     "description": "The Python programming language",
     "language": "Python", "html_url": "https://github.com/python/cpython"},
    
    {"full_name": "django/django", "stargazers_count": 79000, "forks_count": 31000,
     "description": "The Web framework for perfectionists with deadlines.",
     "language": "Python", "html_url": "https://github.com/django/django"},
]


class GitHubTopRepos:
    """Find and display top GitHub repositories"""
    
    def __init__(self, token: Optional[str] = None):
        self.base_url = "https://api.github.com/search/repositories"
        self.token = token
        self.headers = {}
        if token:
            self.headers["Authorization"] = f"token {token}"
        
    def fetch_top_repos(
        self, 
        count: int = 20,
        language: Optional[str] = None,
        sort_by: str = "stars",
        offline: bool = False
    ) -> List[Dict]:
        """
        Fetch top GitHub repositories
        
        Args:
            count: Number of repositories to fetch (default: 20)
            language: Filter by programming language (optional)
            sort_by: Sort criteria (stars, forks, updated)
            offline: Use curated list instead of API (default: False)
            
        Returns:
            List of repository data dictionaries
        """
        # Use curated list if offline mode
        if offline:
            repos = TOP_REPOS_CURATED.copy()
            if language:
                repos = [r for r in repos if r.get("language", "").lower() == language.lower()]
            return repos[:count]
        
        # Build query
        query = "stars:>1000"  # Only repos with significant stars
        if language:
            query += f" language:{language}"
            
        # API parameters
        params = {
            "q": query,
            "sort": sort_by,
            "order": "desc",
            "per_page": min(count, 100)  # GitHub API limit
        }
        
        try:
            response = requests.get(
                self.base_url, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            return data.get("items", [])[:count]
            
        except requests.RequestException as e:
            print(f"Error fetching repositories: {e}", file=sys.stderr)
            print("\n💡 Tip: GitHub API has rate limits. You can:", file=sys.stderr)
            print("   1. Wait a few minutes and try again", file=sys.stderr)
            print("   2. Set GITHUB_TOKEN environment variable with a personal access token", file=sys.stderr)
            print("   3. Use the default curated list (add --offline flag)\n", file=sys.stderr)
            return []
    
    def display_repos(self, repos: List[Dict], detailed: bool = False):
        """
        Display repositories in a formatted way
        
        Args:
            repos: List of repository data
            detailed: Show detailed information
        """
        if not repos:
            print("No repositories found.")
            return
            
        print("\n" + "="*80)
        print(f"🌟 TOP {len(repos)} GITHUB REPOSITORIES 🌟".center(80))
        print("="*80 + "\n")
        
        for idx, repo in enumerate(repos, 1):
            # Basic info
            name = repo.get("full_name", "Unknown")
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            description = repo.get("description", "No description")
            language = repo.get("language", "Unknown")
            url = repo.get("html_url", "")
            
            # Format output
            print(f"{idx}. {name}")
            print(f"   ⭐ Stars: {stars:,} | 🍴 Forks: {forks:,} | 💻 Language: {language}")
            
            if description:
                # Truncate long descriptions
                desc = description[:120] + "..." if len(description) > 120 else description
                print(f"   📝 {desc}")
            
            print(f"   🔗 {url}")
            
            if detailed:
                issues = repo.get("open_issues_count", 0)
                watchers = repo.get("watchers_count", 0)
                created = repo.get("created_at", "")
                updated = repo.get("updated_at", "")
                
                print(f"   📊 Issues: {issues} | 👀 Watchers: {watchers}")
                if created:
                    created_date = created.split("T")[0]
                    print(f"   📅 Created: {created_date}")
                if updated:
                    updated_date = updated.split("T")[0]
                    print(f"   🔄 Updated: {updated_date}")
            
            print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Find and display top GitHub repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get top 20 repositories
  python top20_github_repos.py
  
  # Get top 10 Python repositories
  python top20_github_repos.py -c 10 -l python
  
  # Get top 30 JavaScript repos with details
  python top20_github_repos.py -c 30 -l javascript -d
  
  # Sort by forks instead of stars
  python top20_github_repos.py -s forks
        """
    )
    
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=20,
        help="Number of repositories to display (default: 20)"
    )
    
    parser.add_argument(
        "-l", "--language",
        type=str,
        help="Filter by programming language (e.g., python, javascript, go)"
    )
    
    parser.add_argument(
        "-s", "--sort",
        type=str,
        choices=["stars", "forks", "updated"],
        default="stars",
        help="Sort criteria (default: stars)"
    )
    
    parser.add_argument(
        "-d", "--detailed",
        action="store_true",
        help="Show detailed information"
    )
    
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use curated list instead of GitHub API (no rate limits)"
    )
    
    args = parser.parse_args()
    
    # Get GitHub token from environment if available
    github_token = os.environ.get("GITHUB_TOKEN")
    
    # Create finder instance
    finder = GitHubTopRepos(token=github_token)
    
    # Fetch repositories
    print(f"🔍 Fetching top {args.count} GitHub repositories...")
    if args.offline:
        print(f"   Mode: Offline (curated list)")
    if args.language:
        print(f"   Filtering by language: {args.language}")
    if not args.offline:
        print(f"   Sorting by: {args.sort}")
    print()
    
    repos = finder.fetch_top_repos(
        count=args.count,
        language=args.language,
        sort_by=args.sort,
        offline=args.offline
    )
    
    # Display results
    if repos:
        # Fix the display call to pass count
        finder.display_repos(repos, detailed=args.detailed)
        print("="*80)
        print(f"✅ Found {len(repos)} repositories")
    else:
        print("❌ No repositories found or error occurred")
        sys.exit(1)


if __name__ == "__main__":
    main()
