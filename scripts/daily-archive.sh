#!/bin/bash

# Info Agent Daily Archive Script
# This script archives daily notes and reports to the archive directory

WORKSPACE="/workspace/projects/workspace-info"
ARCHIVE_DIR="$WORKSPACE/archive"
DATE=$(date +%Y-%m-%d)
ARCHIVE_PATH="$ARCHIVE_DIR/$DATE"

# Create archive directory for today
mkdir -p "$ARCHIVE_PATH/notes"
mkdir -p "$ARCHIVE_PATH/tech"
mkdir -p "$ARCHIVE_PATH/other"

# Copy daily-summary.md if it exists
if [ -f "$WORKSPACE/daily-summary.md" ]; then
    cp "$WORKSPACE/daily-summary.md" "$ARCHIVE_PATH/"
    echo "✓ Archived daily-summary.md"
fi

# Copy any notes files (if they exist in a notes directory or as markdown files)
if [ -d "$WORKSPACE/notes" ]; then
    cp -r "$WORKSPACE/notes/"* "$ARCHIVE_PATH/notes/" 2>/dev/null
    echo "✓ Archived notes"
fi

# Copy any tech files (if they exist in a tech directory)
if [ -d "$WORKSPACE/tech" ]; then
    cp -r "$WORKSPACE/tech/"* "$ARCHIVE_PATH/tech/" 2>/dev/null
    echo "✓ Archived tech files"
fi

# Check for any other markdown files that should be archived
find "$WORKSPACE" -maxdepth 1 -name "*.md" -type f -exec cp {} "$ARCHIVE_PATH/other/" \; 2>/dev/null

# Clean up older than 365 days (keep 1 year of archives)
find "$ARCHIVE_DIR" -type d -mtime +365 -exec rm -rf {} + 2>/dev/null

echo "✅ Archive completed for $DATE"
