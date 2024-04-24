#!/bin/env python3
# branch.py
# This might need to interact with commits, for example, to create a branch at a specific commit
from commit import create_commit

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



# branch.py
def create_branch(name, start_point='master', repo_name='.yourvcs'):
    """Create a new branch."""
    # Copy the start_point commit hash to the new branch file in refs/heads
    pass

