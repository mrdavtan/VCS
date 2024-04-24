#!/bin/env python3
# commit.py
import time
import os
from hashnstore import store_object

def create_commit(message, author="Author <email>", repo_name='.vcs'):
    """Create a commit object and update the current branch reference."""
    # Get the current branch
    head_path = os.path.join(repo_name, 'HEAD')
    with open(head_path, 'r') as f:
        current_branch = f.read().strip()

    # Create the commit object
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    commit_content = f"Commit by: {author}\nDate: {timestamp}\n\n{message}"
    commit_hash = store_object(commit_content.encode('utf-8'), repo_name)

    # Update the branch reference to point to the new commit
    branch_path = os.path.join(repo_name, current_branch)
    with open(branch_path, 'w') as f:
        f.write(commit_hash)

