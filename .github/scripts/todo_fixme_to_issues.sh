#!/bin/bash

# Script to find TODO/FIXME comments and create GitHub issues
# Usage: ./todo_fixme_to_issues.sh <KEYWORD> <LABEL>
# Example: ./todo_fixme_to_issues.sh TODO enhancement

KEYWORD=$1
LABEL=$2

if [ -z "$KEYWORD" ] || [ -z "$LABEL" ]; then
    echo "Usage: $0 <KEYWORD> <LABEL>"
    exit 1
fi

# Find all files with the keyword, excluding certain directories
grep -r "$KEYWORD:" --include="*.py" --include="*.lua" --include="*.js" --include="*.md" | while IFS= read -r line; do
    # Extract file, line number, and comment
    file=$(echo "$line" | cut -d: -f1)
    line_num=$(echo "$line" | cut -d: -f2)
    comment=$(echo "$line" | cut -d: -f3- | sed "s/.*$KEYWORD: *//" | sed 's/^[[:space:]]*//')
    context=$(sed -n "$((line_num+10))p" "$file" 2>/dev/null || echo "Could not retrieve context")

    # Skip if comment is empty
    if [ -z "$comment" ]; then
        continue
    fi
    
    # Create issue title and body
    title="[$KEYWORD] $comment"
    body="Found in \`$file\` at line $line_num:

\`\`\`
$context
\`\`\`

"
    
    # Check if issue already exists
    existing=$(gh issue list --search "$title" --json title --jq '.[].title' | grep -F "$title" || true)
    
    if [ -z "$existing" ]; then
        echo "Creating issue: $title"
        gh issue create --title "$title" --body "$body" --label "$LABEL"
    else
        echo "Issue already exists: $title"
    fi
done
