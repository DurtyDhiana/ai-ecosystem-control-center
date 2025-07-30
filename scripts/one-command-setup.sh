#!/bin/bash
# One-Command GitHub Setup for AI Ecosystem Control Center
# Usage: ./scripts/one-command-setup.sh

set -e

echo "🚀 AI Ecosystem Control Center - One-Command GitHub Setup"
echo "========================================================="

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "📦 Installing GitHub CLI via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install gh
fi

# Authenticate if needed
if ! gh auth status &> /dev/null; then
    echo "🔐 Please authenticate with GitHub..."
    gh auth login
fi

# Create repository
echo "🏗️ Creating repository..."
gh repo create ai-ecosystem-control-center \
    --description "🤖 AI-powered macOS ecosystem for file organization, code monitoring, email intelligence, and health analytics" \
    --public \
    --clone=false

# Initialize and push
echo "📝 Setting up git and pushing code..."
git init
git add .
git commit -m "Initial commit: AI Ecosystem Control Center with real badges and CI pipeline"
git remote add origin https://github.com/DurtyDhiana/ai-ecosystem-control-center.git
git branch -M main
git push -u origin main

# Update badges
echo "🏷️ Updating badges..."
./scripts/update-badges.sh DurtyDhiana
git add .
git commit -m "Update badge URLs for DurtyDhiana/ai-ecosystem-control-center"
git push

echo ""
echo "🎉 COMPLETE! Your repository is live at:"
echo "   https://github.com/DurtyDhiana/ai-ecosystem-control-center"
echo ""
echo "⏱️ Wait 2-3 minutes for GitHub Actions to run, then check your badges!"
