#!/bin/bash
# Git History Cleanup Script
# Removes deleted files from git history
# WARNING: This rewrites history. Use with caution.

set -e

echo "⚠️  WARNING: This script will rewrite git history!"
echo "⚠️  Make sure you have a backup and are on a feature branch!"
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# Files to remove from history
FILES_TO_REMOVE=(
    ".cursorignore"
    "CORE_INTERFACES_REPORT.md"
    "GIT_DIFF_HISTORY.txt"
    ".cursor/rules/"
)

echo "Cleaning git history..."

# Use git filter-repo if available, otherwise use filter-branch
if command -v git-filter-repo &> /dev/null; then
    echo "Using git-filter-repo..."
    for file in "${FILES_TO_REMOVE[@]}"; do
        echo "Removing: $file"
        git filter-repo --path "$file" --invert-paths --force
    done
else
    echo "Using git filter-branch (git-filter-repo not found)..."
    echo "Consider installing git-filter-repo for better performance:"
    echo "  pip install git-filter-repo"
    echo ""

    # Create filter script
    FILTER_SCRIPT=$(mktemp)
    cat > "$FILTER_SCRIPT" << 'EOF'
#!/bin/bash
# Remove specified files from history
for file in "${FILES_TO_REMOVE[@]}"; do
    git rm --cached --ignore-unmatch "$file" || true
done
EOF

    chmod +x "$FILTER_SCRIPT"

    # Apply filter to all branches
    git filter-branch --force --index-filter \
        "bash -c 'for f in .cursorignore CORE_INTERFACES_REPORT.md GIT_DIFF_HISTORY.txt; do git rm --cached --ignore-unmatch \"\$f\" 2>/dev/null || true; done; git rm -rf --cached --ignore-unmatch .cursor/rules/ 2>/dev/null || true'" \
        --prune-empty --tag-name-filter cat -- --all

    rm "$FILTER_SCRIPT"
fi

echo ""
echo "✅ Git history cleaned!"
echo ""
echo "Next steps:"
echo "1. Review the changes: git log --all --oneline"
echo "2. If satisfied, force push (if on feature branch):"
echo "   git push --force-with-lease origin <branch-name>"
echo ""
echo "⚠️  If on main/master, create a new branch first!"
