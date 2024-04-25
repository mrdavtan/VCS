# utils.py
import os


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
