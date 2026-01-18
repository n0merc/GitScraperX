import os
import re
import requests
import subprocess
import json
from threading import Thread

class GitScraperX:
    def __init__(self, github_token):
        self.token = github_token
        self.headers = {'Authorization': f'token {self.token}'}
        self.secrets_patterns = {
            'API_KEY': r'[A-Za-z0-9]{32,}',
            'PASSWORD': r'password\s*=\s*["\']([^"\']+)["\']',
            'AWS_ACCESS_KEY': r'AKIA[0-9A-Z]{16}',
            'SSH_PRIVATE_KEY': r'-----BEGIN RSA PRIVATE KEY-----',
        }
    
    def search_repos(self, query, max_repos=50):
        """Search GitHub for repos matching the query."""
        url = f'https://api.github.com/search/repositories?q={query}&per_page={max_repos}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return [repo['clone_url'] for repo in response.json()['items']]
        else:
            print(f"Fuck! Failed to fetch repos: {response.status_code}")
            return []
    
    def clone_repo(self, repo_url, local_path):
        """Clone a repo to a local directory."""
        try:
            subprocess.run(['git', 'clone', repo_url, local_path], check=True)
            print(f"Cloned {repo_url} to {local_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {repo_url}: {e}")
    
    def scan_for_secrets(self, repo_path):
        """Walk through the repo and scan for secrets."""
        findings = []
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for secret_type, pattern in self.secrets_patterns.items():
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                findings.append({
                                    'file': file_path,
                                    'secret_type': secret_type,
                                    'matches': matches[:5]  # Limit to first 5 matches
                                })
                except Exception as e:
                    continue  # Skip binary files or permission errors
        return findings
    
    def run(self, query="password", max_repos=10):
        """Main function to search, clone, and scan."""
        repos = self.search_repos(query, max_repos)
        all_findings = []
        for repo_url in repos:
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            local_path = f'./cloned_repos/{repo_name}'
            self.clone_repo(repo_url, local_path)
            findings = self.scan_for_secrets(local_path)
            all_findings.extend(findings)
        
        # Save results
        with open('findings.json', 'w') as f:
            json.dump(all_findings, f, indent=4)
        print(f"Scan complete. Found {len(all_findings)} potential secrets. Saved to findings.json")

# Usage
if __name__ == "__main__":
    token = "your_github_token_here"  # Get one from GitHub settings
    scraper = GitScraperX(token)
    scraper.run(query="config", max_repos=5)
