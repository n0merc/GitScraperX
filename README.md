# GitScraperX 

**Automated GitHub Repository Scanner for Secrets & Vulnerabilities**

GitScraperX is a powerful Python tool that automatically clones public GitHub repositories, scans them for sensitive information (API keys, passwords, tokens, etc.), and identifies potential code vulnerabilities. Perfect for red team operations, bug bounty hunters, and security researchers.

>  **WARNING**: This tool is for authorized security testing and educational purposes only. Unauthorized use against repositories you don't own is illegal and unethical. The developers are not responsible for misuse.

## Features 

- **Mass Repository Cloning**: Clone multiple repositories based on search queries
- **Secret Detection**: Regex-based scanning for:
  - API Keys (AWS, Google, etc.)
  - Passwords in configuration files
  - Private keys (SSH, RSA)
  - Authentication tokens
- **Basic Vulnerability Scanning**: Identify common code patterns that could lead to security issues
- **Multi-threaded Operations**: Faster scanning through parallel processing
- **JSON/HTML Reports**: Export findings for further analysis

## Installation 

### Prerequisites
- Python 3.8+
- Git installed on your system
- GitHub Personal Access Token (with `repo` scope)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/GitScraperX.git
cd GitScraperX

# Install dependencies
pip install -r requirements.txt

# Set up your GitHub token
export GITHUB_TOKEN="your_personal_access_token_here"
# Or create a config.py file with your token
```

## Usage 

### Basic Usage
```python
from git_scraperx import GitScraperX

# Initialize with your GitHub token
scraper = GitScraperX("your_github_token")

# Search for repositories containing "config" and scan them
scraper.run(query="config", max_repos=10)
```

### Command Line Interface
```bash
# Scan for repositories with "password" in their name/description
python git_scraperx.py --query password --max-repos 20

# Specify output format
python git_scraperx.py --query api_key --format html --output results.html

# Use custom regex patterns
python git_scraperx.py --query config --patterns custom_patterns.json
```

### Advanced Configuration
Create a `config.json` file:
```json
{
  "github_token": "your_token_here",
  "default_query": "password OR secret OR key",
  "max_repos": 50,
  "output_format": "json",
  "custom_patterns": {
    "CUSTOM_SECRET": "your_regex_here"
  }
}
```

## Example Output 

```json
[
  {
    "repository": "https://github.com/example/vulnerable-app",
    "file": "/config/database.yml",
    "secret_type": "PASSWORD",
    "matches": ["db_password: 'SuperSecret123!'"],
    "line_number": 42,
    "severity": "HIGH"
  },
  {
    "repository": "https://github.com/example/api-service",
    "file": "/src/main.py",
    "secret_type": "API_KEY",
    "matches": ["api_key='AKIAIOSFODNN7EXAMPLE'"],
    "line_number": 15,
    "severity": "CRITICAL"
  }
]
```

## Detection Patterns 

GitScraperX comes with built-in patterns for:
- AWS Access Keys (`AKIA[0-9A-Z]{16}`)
- GitHub Tokens (`ghp_[0-9a-zA-Z]{36}`)
- Google API Keys (`AIza[0-9A-Za-z\\-_]{35}`)
- Private Key Headers (`-----BEGIN RSA PRIVATE KEY-----`)
- Database connection strings
- Hardcoded credentials in configuration files

## Contributing 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Legal Disclaimer 

This tool is provided for **educational and authorized testing purposes only**. The user assumes all responsibility for any actions taken using this tool. Scanning repositories without explicit permission may violate:
- GitHub's Terms of Service
- Computer Fraud and Abuse Act (CFAA)
- Various international laws

**USE AT YOUR OWN RISK.**

## License 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 

Found a bug? Have a feature request? Open an issue or reach out:
- Telegram: n0merc UE

---
