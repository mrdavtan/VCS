# utils.py
import os
from commit import create_commit, get_parent_commit

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
            commit_hash = os.path.join(root[-2:], file)
            commit_objects.append((commit_hash, commit_content))

    # Find the current commit index
    current_index = None
    for index, (hash, content) in enumerate(commit_objects):
        if hash == commit_hash:
            current_index = index
            break

    # Get the next commit hash
    if current_index is not None and current_index < len(commit_objects) - 1:
        next_commit_hash = commit_objects[current_index + 1][0]
        return next_commit_hash

    return None

def update_working_directory(commit_hash, repo_name='.vcs'):
    """Update the working directory files based on the given commit hash."""
    commit_path = os.path.join(repo_name, 'objects', commit_hash[:2], commit_hash[2:])
    with open(commit_path, 'rb') as f:
        commit_content = f.read().decode('utf-8')

    lines = commit_content.split('\n')
    file_section = False
    for line in lines:
        if line == "Files:":
            file_section = True
        elif file_section:
            if line:
                file_path, file_hash = line.split('|')
                file_content_path = os.path.join(repo_name, 'objects', file_hash[:2], file_hash[2:])
                with open(file_content_path, 'rb') as f:
                    file_content = f.read()
                with open(file_path, 'wb') as f:
                    f.write(file_content)

def get_latest_commit_hash(branch_name, repo_name='.vcs'):
    """Get the latest commit hash of the specified branch."""
    branch_path = os.path.join(repo_name, 'refs', 'heads', branch_name)
    try:
        with open(branch_path, 'r') as f:
            commit_hash = f.read().strip()
            return commit_hash
    except FileNotFoundError:
        return None
