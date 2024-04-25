#!/bin/env python3

import os
import time
from hashnstore import store_object, hash_content
from tracker import track_changes
from branch import get_branch_commit


def create_commit(message, author="Author <email>", repo_name='.vcs'):
    """Create a commit object and update the current branch reference."""
    # Get the current branch
    head_path = os.path.join(repo_name, 'HEAD')
    with open(head_path, 'r') as f:
        current_branch = f.read().strip()

    # Extract the branch name from the reference
    branch_name = current_branch.split('/')[-1]

    # Get the parent commit hash
    parent_commit = get_branch_commit(branch_name, repo_name)

    # Get the tracked changes
    changes = track_changes(repo_name)

    # Create the commit object content
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    commit_content = f"Commit by: {author}\nDate: {timestamp}\n"
    if parent_commit:
        commit_content += f"Parent: {parent_commit}\n"
    commit_content += f"\nMessage: {message}\n\nChanges:\n"

    # Add the changes to the commit content
    for category, files in changes.items():
        commit_content += f"\n{category.capitalize()}:\n"
        for file in files:
            commit_content += f"  {file}\n"

    commit_content += "\nFiles:\n"
    for category, files in changes.items():
        for file in files:
            with open(file, 'rb') as f:
                file_content = f.read()
            file_hash = hash_content(file_content)
            commit_content += f"{file}|{file_hash}\n"

    # Store the commit object
    commit_hash = store_object(commit_content.encode('utf-8'), repo_name)

    # Get the next commit hash
    next_commit_hash = get_next_commit(commit_hash, repo_name)
    if next_commit_hash:
        commit_content += f"\nNext: {next_commit_hash}\n"
        commit_hash = store_object(commit_content.encode('utf-8'), repo_name)

    # Update the branch reference to point to the new commit
    branch_path = os.path.join(repo_name, 'refs', 'heads', branch_name)
    with open(branch_path, 'w') as f:
        f.write(commit_hash)

    # Update the HEAD reference to point to the current branch
    head_path = os.path.join(repo_name, 'HEAD')
    with open(head_path, 'w') as f:
        f.write(f'ref: refs/heads/{branch_name}\n')

    # Store the committed files based on their content hash
    for category, files in changes.items():
        for file in files:
            with open(file, 'rb') as f:
                file_content = f.read()
            file_hash = hash_content(file_content)
            commit_file_path = os.path.join(repo_name, 'objects', file_hash[:2], file_hash[2:])
            commit_file_dir = os.path.dirname(commit_file_path)
            if not os.path.exists(commit_file_dir):
                os.makedirs(commit_file_dir)
            with open(commit_file_path, 'wb') as dst_file:
                dst_file.write(file_content)

    # Update the stage file with the newly staged files
    stage_file_path = os.path.join(repo_name, 'stage')
    with open(stage_file_path, 'w') as f:
        for category, files in changes.items():
            if category != 'staged':
                for file in files:
                    f.write(file + '\n')

    print(f"Created commit: {commit_hash}")
    print(f"Parent commit: {parent_commit}")
    print(f"Next commit: {next_commit_hash}")

    return commit_hash

def get_next_commit(commit_hash, repo_name='.vcs'):
    """Get the next commit hash based on the current commit."""
    # Get all commit objects
    commit_objects = []
    objects_dir = os.path.join(repo_name, 'objects')
    for root, dirs, files in os.walk(objects_dir):
        for file in files:
            commit_path = os.path.join(root, file)
            with open(commit_path, 'rb') as f:
                commit_content = f.read().decode('utf-8')
            full_commit_hash = os.path.join(root, file)
            commit_objects.append((full_commit_hash, commit_content))

    # Find the current commit index
    current_index = None
    for index, (hash, content) in enumerate(commit_objects):
        if hash == os.path.join(repo_name, 'objects', commit_hash[:2], commit_hash[2:]):
            current_index = index
            break

    # Check if the current commit has a next commit hash in its metadata
    if current_index is not None:
        current_commit_content = commit_objects[current_index][1]
        lines = current_commit_content.split('\n')
        for line in lines:
            if line.startswith('Next: '):
                next_commit_hash = line[6:].strip()
                print(f"Next commit hash from metadata: {next_commit_hash}")
                return next_commit_hash

    # If no next commit hash found in metadata, get the next commit hash based on the index
    if current_index is not None and current_index < len(commit_objects) - 1:
        next_commit_hash = commit_objects[current_index + 1][0]
        print(f"Next commit hash from index: {next_commit_hash}")
        return next_commit_hash

    print("No next commit found")
    return None

def get_parent_commit(commit_hash, repo_name='.vcs'):
    """Get the parent commit hash of the specified commit."""
    commit_path = os.path.join(repo_name, 'objects', commit_hash[:2], commit_hash[2:])
    try:
        with open(commit_path, 'rb') as f:
            commit_content = f.read().decode('utf-8')
        lines = commit_content.split('\n')
        for line in lines:
            if line.startswith('Parent: '):
                return line[8:].strip()
    except FileNotFoundError:
        return None
    return None



