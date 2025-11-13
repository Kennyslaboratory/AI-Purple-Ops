#!/bin/bash
# Remove outdated docs from git history
# WARNING: This rewrites history. Use with caution.

set -e

FILES_TO_REMOVE=(
    "docs/USABILITY_ASSESSMENT.md"
    "docs/USABILITY_ASSESSMENT_B07.md"
    "docs/B04_POLISH_SUMMARY.md"
    "docs/P2_POLISH_ITEMS.md"
    "docs/REVIEWER_NOTES.md"
)

echo "Removing outdated docs from git history..."
echo "Files to remove:"
for file in "${FILES_TO_REMOVE[@]}"; do
    echo "  - $file"
done
echo ""

# Use git filter-repo if available, otherwise use filter-branch
if command -v git-filter-repo &> /dev/null; then
    echo "Using git-filter-repo..."
    for file in "${FILES_TO_REMOVE[@]}"; do
        echo "Removing: $file"
        git filter-repo --path "$file" --invert-paths --force
    done
else
    echo "Using git filter-branch..."
    echo ""

    # Build filter command
    FILTER_CMD=""
    for file in "${FILES_TO_REMOVE[@]}"; do
        FILTER_CMD="$FILTER_CMD git rm --cached --ignore-unmatch \"$file\" 2>/dev/null || true;"
    done

    # Apply filter to current branch only (safer)
    git filter-branch --force --index-filter "$FILTER_CMD" --prune-empty HEAD

    echo ""
    echo "✅ History cleaned for current branch!"
    echo ""
    echo "To clean all branches, run:"
    echo "  git filter-branch --force --index-filter '$FILTER_CMD' --prune-empty --tag-name-filter cat -- --all"
fi

echo ""
echo "Next steps:"
echo "1. Review: git log --oneline"
echo "2. Force push (if on feature branch): git push --force-with-lease"
