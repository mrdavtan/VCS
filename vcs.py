#!/bin/env python3

import sys
import os
from repository import init_repository
from hashnstore import process_file, store_object
from branch import create_branch, get_current_branch, get_branch_commit, switch_branch, list_branches
from tracker import track_changes
from commit import create_commit, get_parent_commit
from hashnstore import hash_content
from utils import get_next_commit, update_working_directory, get_latest_commit_hash

def get_latest_commit_hash(branch_name, repo_name='.vcs'):
    branch_path = os.path.join(repo_name, 'refs', 'heads', branch_name)
    try:
        with open(branch_path, 'r') as f:
            commit_hash = f.read().strip()
            return commit_hash
    except FileNotFoundError:
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python vcs.py <command> [arguments]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'init':
        init_repository()
        print("Initialized empty VCS repository.")
    elif command == 'add':
        if len(sys.argv) < 3:
            print("Usage: python vcs.py add <file>")
            sys.exit(1)
        file_path = sys.argv[2]
        process_file(file_path)
        with open(os.path.join('.vcs', 'stage'), 'a') as f:
            f.write(file_path + '\n')
        print(f"Added file: {file_path}")

    elif command == 'commit':
        if len(sys.argv) < 3:
            print("Usage: python vcs.py commit '<message>'")
            sys.exit(1)
        message = sys.argv[2]
        create_commit(message)
        print(f"Committed with message: {message}")


    elif command == 'add':
        if len(sys.argv) < 3:
            print("Usage: python vcs.py add <file>")
            sys.exit(1)
        file_path = sys.argv[2]
        process_file(file_path)
        with open(os.path.join('.vcs', 'stage'), 'a') as f:
            f.write(file_path + '\n')
        print(f"Added file: {file_path}")

    elif command == 'push':
        if len(sys.argv) < 3:
            print("Usage: python vcs.py push <branch>")
            sys.exit(1)
        branch = sys.argv[2]
        commit_hash = get_branch_commit(branch)
        if commit_hash:
            # Store the commit object
            commit_path = os.path.join('.vcs', 'objects', commit_hash[:2], commit_hash[2:])
            with open(commit_path, 'rb') as f:
                commit_content = f.read()
            store_object(commit_content, repo_name='.vcs')
            print(f"Pushed to branch '{branch}' (commit {commit_hash})")
        else:
            print(f"Branch '{branch}' does not exist or has no commits.")

    elif command == 'checkout':
        if len(sys.argv) < 3:
            print("Usage: python vcs.py checkout <branch> [filename]")
            sys.exit(1)
        branch = sys.argv[2]
        if len(sys.argv) > 3:
            filename = sys.argv[3]
            commit_hash = get_branch_commit(branch)
            if commit_hash:
                # Implement the checkout functionality for a specific file
                print(f"Checked out {filename} from branch: {branch}")
            else:
                print(f"Branch '{branch}' does not exist or has no commits.")
        else:
            if switch_branch(branch):
                print(f"Switched to branch '{branch}'")
            else:
                print(f"Branch '{branch}' does not exist.")

    elif command == 'reset':
        branch_name = get_current_branch()
        if branch_name:
            current_commit = get_branch_commit(branch_name)
            if current_commit:
                parent_commit = get_parent_commit(current_commit)
                if parent_commit:
                    # Update the branch reference to point to the parent commit
                    branch_path = os.path.join('.vcs', 'refs', 'heads', branch_name)
                    with open(branch_path, 'w') as f:
                        f.write(parent_commit)
                    # Update the HEAD reference to point to the parent commit
                    head_path = os.path.join('.vcs', 'HEAD')
                    with open(head_path, 'w') as f:
                        f.write(f'ref: refs/heads/{branch_name}\n')

                    # Retrieve the parent commit object content
                    parent_commit_path = os.path.join('.vcs', 'objects', parent_commit[:2], parent_commit[2:])
                    with open(parent_commit_path, 'rb') as f:
                        parent_commit_content = f.read().decode('utf-8')

                    # Parse the parent commit object content to get the file paths and hashes
                    parent_commit_files = {}
                    lines = parent_commit_content.split('\n')
                    file_section = False
                    for line in lines:
                        if line == "Files:":
                            file_section = True
                        elif file_section:
                            if line:
                                file_path, file_hash = line.split('|')
                                parent_commit_files[file_path] = file_hash

                    # Update the working directory files to match the parent commit
                    for file_path, file_hash in parent_commit_files.items():
                        file_content_path = os.path.join('.vcs', 'objects', file_hash[:2], file_hash[2:])
                        if os.path.exists(file_content_path):
                            with open(file_content_path, 'rb') as f:
                                file_content = f.read()
                            with open(file_path, 'wb') as f:
                                f.write(file_content)
                        else:
                            # If the file doesn't exist in the parent commit, remove it from the working directory
                            if os.path.exists(file_path):
                                os.remove(file_path)

                    print(f"Reset branch '{branch_name}' to commit {parent_commit}")
                else:
                    print(f"No parent commit found for commit {current_commit}. Already at the initial commit.")
            else:
                print(f"Branch '{branch_name}' has no commits.")
        else:
            print("Not currently on any branch.")

    elif command == 'redo':
        current_branch = get_current_branch()
        if current_branch:
            current_commit = get_branch_commit(current_branch)
            next_commit = get_next_commit(current_commit)
            if next_commit:
                # Update the branch reference to point to the next commit
                branch_path = os.path.join('.vcs', 'refs', 'heads', current_branch)
                with open(branch_path, 'w') as f:
                    f.write(next_commit)
                # Update the working directory files to match the next commit
                update_working_directory(next_commit)
                print(f"Moved forward to commit {next_commit}")
            else:
                print("Already at the latest commit.")
        else:
            print("Not currently on any branch.")

    elif command == 'status':
        changes = track_changes()
        branch_name = get_current_branch()

        if branch_name:
            commit_hash = get_latest_commit_hash(branch_name)
            print(f"On branch {branch_name}")
            print(f"Latest commit: {commit_hash}")


            if not any(changes.values()):
                print("Nothing to commit, working tree clean.")
            else:
                if changes['staged']:
                    print("Changes to be committed:")
                    for file in changes['staged']:
                        print(f"  (staged)    {file}")
                if any(files for category, files in changes.items() if category != 'staged'):
                    print("Changes not staged for commit:")
                    for category, files in changes.items():
                        if category != 'staged':
                            for file in files:
                                print(f"  ({category})   {file}")
        else:
            print("Not currently on any branch.")
            print("Changes in the working directory:")
            for category, files in changes.items():
                if category == 'untracked':
                    print("Untracked files:")
                else:
                    print(f"{category.capitalize()}:")
                for file in files:
                    print(f"  {file}")


    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
