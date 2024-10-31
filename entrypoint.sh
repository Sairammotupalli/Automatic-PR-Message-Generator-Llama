#!/bin/sh -l

# Check if llama3_api environment variable is set
if [ -z "llama3_api" ]; then
  echo "Error: llama3_api environment variable is not set."
  exit 1
fi

# Fetch the pull request diff and generate the PR body
gh pr diff >> pr_diff.txt
python main.py pr_diff.txt --output-file pr_body.txt

# Update the pull request with the generated body
gh pr edit -F pr_body.txt
