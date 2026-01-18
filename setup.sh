#!/bin/bash
# GitScraperX Setup Script
# Run this fucking thing to get started

echo "Setting up GitScraperX..."
echo ""

# Check Python version
python3 --version || { echo "Python3 not installed. Install it first, dumbass."; exit 1; }

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p cloned_repos results reports

# Create config template
cat > config.example.py << 'EOF'
# GitScraperX Configuration
# Rename this to config.py and add your token

GITHUB_TOKEN = "your_personal_access_token_here"
MAX_REPOS = 50
OUTPUT_FORMAT = "json"
CUSTOM_PATTERNS = {
    # Add your custom regex patterns here
}
EOF

echo ""
echo "Setup complete! Now:"
echo "1. Get a GitHub token from https://github.com/settings/tokens"
echo "2. Copy config.example.py to config.py"
echo "3. Add your token to config.py"
echo "4. Run: python git_scraperx.py --help"
echo ""
echo "enjoy!"
