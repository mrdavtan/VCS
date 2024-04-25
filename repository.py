#!/bin/env python3

import os
from branch import create_branch

def init_repository(repo_name='.vcs'):
    """Initialize a new repository."""
    os.makedirs(repo_name, exist_ok=True)
    subdirs = ['objects', 'refs/heads']
    for subdir in subdirs:
        os.makedirs(os.path.join(repo_name, subdir), exist_ok=True)
    with open(os.path.join(repo_name, 'HEAD'), 'w') as f:
        f.write('ref: refs/heads/main\n')

    # Create the initial "main" branch
    create_branch('main', repo_name=repo_name)


