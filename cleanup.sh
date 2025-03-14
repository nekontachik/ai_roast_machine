#!/bin/bash
# Cleanup script for AI Roast Machine
# Removes temporary files and directories that shouldn't be committed to version control

echo "🧹 Cleaning up AI Roast Machine..."

# Remove compiled Python files and __pycache__ directories
echo "Removing compiled Python files and __pycache__ directories..."
find . -name "*.pyc" -o -name "__pycache__" | xargs rm -rf

# Remove system files
echo "Removing system files..."
find . -name ".DS_Store" | xargs rm -rf

# Remove pytest cache
echo "Removing pytest cache..."
find . -name ".pytest_cache" | xargs rm -rf

# Remove mypy cache
echo "Removing mypy cache..."
find . -name ".mypy_cache" | xargs rm -rf

# Check for sensitive files
echo "Checking for sensitive files..."
if [ -f ".env" ]; then
    echo "⚠️  Warning: .env file exists and contains sensitive information."
    echo "    This file is excluded from version control, but make sure it doesn't contain any hardcoded credentials."
fi

# Check for large files
echo "Checking for large files (>5MB)..."
large_files=$(find . -type f -size +5M | grep -v "venv" | grep -v ".git")
if [ -n "$large_files" ]; then
    echo "⚠️  Warning: Large files found that might not be suitable for version control:"
    echo "$large_files"
fi

echo "✅ Cleanup complete!"
echo "Run 'python run_tests.py' to make sure everything is working properly." 