#!/bin/env python3

import os
import time
from hashnstore import store_object
from tracker import track_changes

def create_commit(message, author="Author <email>", repo_name='.vcs'):
    """Create a commit object and update the current branch reference."""
    # Get the current branch
    head_path = os.path.join(repo_name, 'HEAD')
    with open(head_path, 'r') as f:
        current_branch = f.read().strip()

    # Get the tracked changes
    changes = track_changes(repo_name)

    # Create the commit object content
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    commit_content = f"Commit by: {author}\nDate: {timestamp}\n\nMessage: {message}\n\nChanges:\n"

    # Add the changes to the commit content
    for category, files in changes.items():
        commit_content += f"\n{category.capitalize()}:\n"
        for file in files:
            commit_content += f"  {file}\n"

    # Store the commit object
    commit_hash = store_object(commit_content.encode('utf-8'), repo_name)

    # Update the branch reference to point to the new commit
    branch_path = os.path.join(repo_name, current_branch)
    with open(branch_path, 'w') as f:
        f.write(commit_hash)

    return commit_hash
