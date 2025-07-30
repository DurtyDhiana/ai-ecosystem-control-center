#!/bin/bash
# GitHub API Automation Script (Alternative to GitHub CLI)
# Creates repository using GitHub REST API

set -e

# Configuration
GITHUB_USERNAME="DurtyDhiana"
REPO_NAME="ai-ecosystem-control-center"
REPO_DESCRIPTION="🤖 AI-powered macOS ecosystem for file organization, code monitoring, email intelligence, and health analytics"

echo "🚀 GitHub API Repository Creation"
echo "================================="

# Check if GitHub token exists
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN environment variable not set."
    echo ""
    echo "To create a token:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Select scopes: repo, workflow, admin:repo_hook"
    echo "4. Copy the token and run:"
    echo "   export GITHUB_TOKEN='your_token_here'"
    echo ""
    exit 1
fi

# Create repository using GitHub API
echo "🏗️ Creating repository via GitHub API..."

RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/github_response.json \
    -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/user/repos \
    -d "{
        \"name\": \"$REPO_NAME\",
        \"description\": \"$REPO_DESCRIPTION\",
        \"private\": false,
        \"auto_init\": false,
        \"has_issues\": true,
        \"has_projects\": true,
        \"has_wiki\": true
    }")

HTTP_CODE="${RESPONSE: -3}"

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ Repository created successfully!"
    REPO_URL=$(cat /tmp/github_response.json | python3 -c "import sys, json; print(json.load(sys.stdin)['html_url'])")
    echo "🔗 Repository URL: $REPO_URL"
elif [ "$HTTP_CODE" = "422" ]; then
    echo "⚠️ Repository already exists. Continuing with existing repository..."
else
    echo "❌ Failed to create repository. HTTP Code: $HTTP_CODE"
    echo "Response:"
    cat /tmp/github_response.json
    exit 1
fi

# Continue with git setup
echo "📝 Setting up git repository..."
git init
git add .
git commit -m "Initial commit: AI Ecosystem Control Center with real badges and CI pipeline"
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
git branch -M main
git push -u origin main

# Update badges
echo "🏷️ Updating badges..."
./scripts/update-badges.sh "$GITHUB_USERNAME"
git add .
git commit -m "Update badge URLs for $GITHUB_USERNAME/$REPO_NAME"
git push

echo ""
echo "🎉 Repository setup complete!"
echo "🔗 https://github.com/$GITHUB_USERNAME/$REPO_NAME"

# Clean up
rm -f /tmp/github_response.json
