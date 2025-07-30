#!/bin/bash
# Update badge URLs with actual GitHub username

if [ -z "$1" ]; then
    echo "Usage: ./scripts/update-badges.sh YOUR_GITHUB_USERNAME"
    echo "Example: ./scripts/update-badges.sh johndoe"
    exit 1
fi

USERNAME=$1
REPO="ai-ecosystem-control-center"

echo "🏷️ Updating badges for GitHub user: $USERNAME"

# Update README.md
sed -i '' "s|user/ai-ecosystem-control-center|$USERNAME/$REPO|g" README.md
echo "✅ Updated README.md badges"

# Update ARCHITECTURE.md
sed -i '' "s|user/ai-ecosystem-control-center|$USERNAME/$REPO|g" docs/ARCHITECTURE.md
echo "✅ Updated ARCHITECTURE.md badges"

# Update badge config
sed -i '' "s|user/ai-ecosystem-control-center|$USERNAME/$REPO|g" .github/badge-config.md
echo "✅ Updated badge configuration"

echo ""
echo "🎉 Badge URLs updated successfully!"
echo "Now commit and push the changes:"
echo "  git add ."
echo "  git commit -m 'Update badge URLs with actual GitHub username'"
echo "  git push"
echo ""
echo "After pushing, wait 2-3 minutes for GitHub Actions to run, then check your badges!"
