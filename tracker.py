#!/bin/env python3
import os
from hashnstore import hash_content

def track_changes(repo_name='.vcs'):
    """Track file changes in the working directory."""
    # Get the last commit hash
    head_path = os.path.join(repo_name, 'HEAD')
    with open(head_path, 'r') as f:
        current_branch = f.read().strip()
    branch_path = os.path.join(repo_name, current_branch)

    try:
        with open(branch_path, 'r') as f:
            last_commit_hash = f.read().strip()
    except FileNotFoundError:
        # If the branch file doesn't exist, assume no previous commits
        last_commit_hash = None

    if last_commit_hash:
        # Load the last commit object
        last_commit_path = os.path.join(repo_name, 'objects', last_commit_hash[:2], last_commit_hash[2:])
        with open(last_commit_path, 'rb') as f:
            last_commit_content = f.read().decode('utf-8')

        # Parse the last commit object to get the file hashes
        last_commit_lines = last_commit_content.split('\n')
        last_commit_files = {}
        for line in last_commit_lines:
            if line.startswith('file:'):
                file_path, file_hash = line[5:].split(' ')
                last_commit_files[file_path] = file_hash
    else:
        last_commit_files = {}

    # Track file changes
    changes = {
        'staged': [],
        'modified': [],
        'deleted': [],
        'untracked': []
    }

    # Compare the current state of files to the last commit
    for root, dirs, files in os.walk('.'):
        # Exclude the VCS directory and other unrelated directories
        dirs[:] = [d for d in dirs if d not in [repo_name, '.git', '__pycache__']]

        for file in files:
            file_path = os.path.join(root, file)

            # Exclude specific files and directories
            excluded_files = [
                'branch.py', 'hashnstore.py', '__init__.py', 'repository.py',
                'vcs.py', 'commit.py', 'tracker.py', 'README.md'
            ]
            if any(file_path.endswith(excluded_file) for excluded_file in excluded_files):
                continue

            with open(file_path, 'rb') as f:
                content = f.read()
            current_hash = hash_content(content)

            if file_path not in last_commit_files:
                changes['untracked'].append(file_path)
            elif current_hash != last_commit_files[file_path]:
                changes['modified'].append(file_path)
            else:
                # File is unchanged and already committed
                pass

    # Check for deleted files
    for file_path in last_commit_files:
        if not os.path.exists(file_path):
            changes['deleted'].append(file_path)

    # Get the list of staged files
    stage_file_path = os.path.join(repo_name, 'stage')
    if os.path.exists(stage_file_path):
        with open(stage_file_path, 'r') as f:
            staged_files = [line.strip() for line in f.readlines()]
        changes['staged'] = staged_files

    return changes


