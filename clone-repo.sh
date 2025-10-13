#!/bin/bash
# Quick GitHub repository clone helper

if [ -z "$1" ]; then
    echo "Usage: ./clone-repo.sh <repository-url-or-org/repo>"
    echo ""
    echo "Examples:"
    echo "  ./clone-repo.sh https://github.com/user/repo.git"
    echo "  ./clone-repo.sh user/repo"
    echo "  ./clone-repo.sh git@github.com:user/repo.git"
    exit 1
fi

REPO="$1"

# If just org/repo format, convert to HTTPS URL
if [[ ! "$REPO" =~ ^(https|git@) ]]; then
    REPO="https://github.com/${REPO}.git"
fi

# Extract repo name for directory
REPO_NAME=$(basename "$REPO" .git)

echo "=== Cloning GitHub Repository ==="
echo "Repository: $REPO"
echo "Target directory: ./$REPO_NAME"
echo ""

# Clone the repository
git clone "$REPO"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully cloned!"
    echo "📁 Directory: ./$REPO_NAME"
    echo ""
    echo "Next steps:"
    echo "  cd $REPO_NAME"
    echo "  ls -la"
else
    echo ""
    echo "❌ Clone failed. Check:"
    echo "  - Repository URL is correct"
    echo "  - You have access to the repository"
    echo "  - Network connection is working"
fi

