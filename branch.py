#!/bin/env python3
# branch.py
# This might need to interact with commits, for example, to create a branch at a specific commit
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

def create_branch(name, start_point=None, repo_name='.vcs'):
    """Create a new branch."""
    branch_path = os.path.join(repo_name, 'refs', 'heads', name)

    if start_point:
        # Copy the start_point commit hash to the new branch file in refs/heads
        with open(branch_path, 'w') as f:
            f.write(start_point)
    else:
        # Create an empty branch file
        with open(branch_path, 'w') as f:
            f.write('')