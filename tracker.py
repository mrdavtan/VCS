#!/bin/env python3

import os
from hashnstore import hash_content, store_object

def track_changes(repo_name='.vcs'):
    """Track file changes in the working directory."""
    # Get the last commit hash
    head_path = os.path.join(repo_name, 'HEAD')
    with open(head_path, 'r') as f:
        current_branch = f.read().strip()
    branch_path = os.path.join(repo_name, current_branch)
    with open(branch_path, 'r') as f:
        last_commit_hash = f.read().strip()

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

    # Track file changes
    changes = {
        'added': [],
        'modified': [],
        'deleted': []
    }

    # Compare the current state of files to the last commit
    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.startswith(repo_name):
                continue  # Skip files in the repository directory

            with open(file_path, 'rb') as f:
                content = f.read()
            current_hash = hash_content(content)

            if file_path not in last_commit_files:
                changes['added'].append(file_path)
            elif current_hash != last_commit_files[file_path]:
                changes['modified'].append(file_path)

    # Check for deleted files
    for file_path in last_commit_files:
        if not os.path.exists(file_path):
            changes['deleted'].append(file_path)

    return changes


