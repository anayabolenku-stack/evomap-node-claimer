#!/usr/bin/env python3
"""
Claim EvoMap free LLM credits using GitHub repo stars.
"""

import json
import os
import sys
import urllib.request
import argparse

def get_github_stars(owner, repo, token=None):
    """Get star count for a GitHub repo."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"token {token}")
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        return data.get("stargazers_count", 0)
    except Exception as e:
        print(f"Error fetching stars: {e}", file=sys.stderr)
        return 0

def check_eligible(token, min_stars=2):
    """Check if user has any repo with min_stars+ stars."""
    url = "https://api.github.com/user/repos?per_page=100&sort=stars"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {token}")
    try:
        resp = urllib.request.urlopen(req)
        repos = json.loads(resp.read())
        eligible = [r for r in repos if r.get("stargazers_count", 0) >= min_stars]
        return eligible
    except Exception as e:
        print(f"Error checking repos: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="Claim EvoMap free LLM credits")
    parser.add_argument("--github-token", help="GitHub personal access token")
    parser.add_argument("--owner", help="GitHub owner/username")
    parser.add_argument("--repo", help="GitHub repo name")
    parser.add_argument("--min-stars", type=int, default=2, help="Minimum stars required")
    args = parser.parse_args()

    token = args.github_token or os.environ.get("GITHUB_TOKEN", "")

    if args.owner and args.repo:
        stars = get_github_stars(args.owner, args.repo, token)
        print(f"Repository: {args.owner}/{args.repo}")
        print(f"Stars: {stars}")
        if stars >= args.min_stars:
            print(f"✅ Eligible! You have {stars} stars (>= {args.min_stars}).")
            print("Go to https://evomap.ai and connect your GitHub to claim credits.")
        else:
            print(f"❌ Not eligible. Need {args.min_stars} stars, have {stars}.")
            print("Ask friends to star your repo, or contribute to popular open-source projects.")
    elif token:
        repos = check_eligible(token, args.min_stars)
        if repos:
            print(f"✅ Found {len(repos)} eligible repos:")
            for r in repos[:5]:
                print(f"  - {r['full_name']} ★{r['stargazers_count']}")
            print("\nGo to https://evomap.ai and connect your GitHub to claim credits.")
        else:
            print(f"❌ No repos with {args.min_stars}+ stars found.")
            print("Create a repo, add valuable content, and get stars from the community.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
