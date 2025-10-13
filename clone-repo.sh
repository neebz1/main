#!/bin/bash
# Quick GitHub repository cloner

if [ -z "$1" ]; then
    echo "Usage: ./clone-repo.sh <github-url-or-user/repo>"
    echo ""
    echo "Examples:"
    echo "  ./clone-repo.sh https://github.com/user/repo.git"
    echo "  ./clone-repo.sh user/repo"
    echo "  ./clone-repo.sh user/repo main"
    echo ""
    exit 1
fi

REPO="$1"
BRANCH="${2:-main}"

# If it's just "user/repo", convert to full GitHub URL
if [[ ! "$REPO" =~ ^https?:// ]] && [[ "$REPO" =~ ^[^/]+/[^/]+$ ]]; then
    REPO="https://github.com/${REPO}.git"
fi

# Extract repo name for directory
REPO_NAME=$(basename "$REPO" .git)

echo "=== Cloning Repository ==="
echo "Repo: $REPO"
echo "Branch: $BRANCH"
echo "Target: $REPO_NAME"
echo ""

# Clone the repo
if [ -n "$BRANCH" ]; then
    git clone -b "$BRANCH" "$REPO"
else
    git clone "$REPO"
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully cloned to: $(pwd)/$REPO_NAME"
    echo ""
    echo "Next steps:"
    echo "  cd $REPO_NAME"
    echo "  ls -la"
else
    echo ""
    echo "❌ Clone failed. Check the URL and try again."
    exit 1
fi

