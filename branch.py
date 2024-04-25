#!/bin/env python3
import os

def create_branch(name, start_point=None, repo_name='.vcs'):
    """Create a new branch."""
    branch_path = os.path.join(repo_name, 'refs', 'heads', name)

    if start_point:
        # Copy the start_point commit hash to the new branch file
        with open(branch_path, 'w') as f:
            f.write(start_point)
    else:
        # Create an empty branch file
        with open(branch_path, 'w') as f:
            f.write('')

def get_branch_commit(branch_name, repo_name='.vcs'):
    """Get the commit hash of the specified branch."""
    branch_path = os.path.join(repo_name, 'refs', 'heads', branch_name)

    try:
        with open(branch_path, 'r') as f:
            commit_hash = f.read().strip()
            return commit_hash
    except FileNotFoundError:
        return None

def get_current_branch(repo_name='.vcs'):
    """Get the name of the current branch."""
    head_path = os.path.join(repo_name, 'HEAD')

    try:
        with open(head_path, 'r') as f:
            head_content = f.read().strip()

        if head_content.startswith('ref: '):
            ref_path = head_content[5:]
            branch_name = os.path.basename(ref_path)
            return branch_name
        else:
            return None
    except FileNotFoundError:
        return None

def switch_branch(branch_name, repo_name='.vcs'):
    """Switch to the specified branch."""
    branch_path = os.path.join(repo_name, 'refs', 'heads', branch_name)

    if os.path.exists(branch_path):
        head_path = os.path.join(repo_name, 'HEAD')
        with open(head_path, 'w') as f:
            f.write(f'ref: refs/heads/{branch_name}\n')
        return True
    else:
        return False

def list_branches(repo_name='.vcs'):
    """List all branches in the repository."""
    branch_dir = os.path.join(repo_name, 'refs', 'heads')

    branches = []
    for root, dirs, files in os.walk(branch_dir):
        for file in files:
            branch_name = os.path.relpath(os.path.join(root, file), branch_dir)
            branches.append(branch_name)

    return branches
