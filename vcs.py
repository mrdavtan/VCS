#!/bin/env python3

import sys
import os
from repository import init_repository
from hashnstore import process_file, store_object
from branch import create_branch
from commit import create_commit
from tracker import track_changes

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
        print(f"Added file: {file_path}")
    elif command == 'commit':
        if len(sys.argv) < 3:
            print("Usage: python vcs.py commit '<message>'")
            sys.exit(1)
        message = sys.argv[2]
        create_commit(message)
        print(f"Committed with message: {message}")
    elif command == 'push':
        if len(sys.argv) < 3:
            print("Usage: python vcs.py push <branch>")
            sys.exit(1)
        branch = sys.argv[2]
        # Implement the push functionality
        print(f"Pushed to branch: {branch}")
    elif command == 'checkout':
        if len(sys.argv) < 3:
            print("Usage: python vcs.py checkout <branch> [filename]")
            sys.exit(1)
        branch = sys.argv[2]
        if len(sys.argv) > 3:
            filename = sys.argv[3]
            # Implement the checkout functionality for a specific file
            print(f"Checked out {filename} from branch: {branch}")
        else:
            # Implement the checkout functionality for the entire branch
            print(f"Checked out branch: {branch}")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
