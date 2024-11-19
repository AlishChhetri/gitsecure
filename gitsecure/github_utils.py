import requests
from urllib.parse import urlparse
from typing import Any, Dict


class SecurityStatus:
    """Class to check security features of a GitHub repository."""

    def __init__(self, token: str):
        if not token:
            raise ValueError(
                "GitHub token not found. Please set GITHUB_TOKEN environment variable."
            )
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        self.base_url = "https://api.github.com"

    def parse_github_url(self, url: str) -> tuple:
        """Extract owner and repo name from GitHub URL."""
        path = urlparse(url).path.strip("/")
        parts = path.split("/")
        if len(parts) < 2:
            raise ValueError("Invalid GitHub URL format")
        return parts[0], parts[1]

    def get(self, url: str):
        """Make a GET request to the GitHub API."""
        return requests.get(url, headers=self.headers)

    def check_security_policy(self, owner: str, repo: str) -> Dict[str, Any]:
        """Check if repository has a security policy file."""
        urls = [
            f"{self.base_url}/repos/{owner}/{repo}/contents/SECURITY.md",
            f"{self.base_url}/repos/{owner}/{repo}/contents/.github/SECURITY.md",
        ]
        for url in urls:
            if self.get(url).status_code == 200:
                return {"exists": True}
        return {"exists": False}

    def check_dependabot_alerts(self, owner: str, repo: str) -> Dict[str, Any]:
        """Check Dependabot alerts status."""
        url = f"{self.base_url}/repos/{owner}/{repo}/vulnerability-alerts"
        return {"enabled": self.get(url).status_code == 204}

    def check_code_scanning(self, owner: str, repo: str) -> Dict[str, Any]:
        """Check if code scanning is enabled."""
        url = f"{self.base_url}/repos/{owner}/{repo}/code-scanning/analyses"
        return {"enabled": self.get(url).status_code != 404}
