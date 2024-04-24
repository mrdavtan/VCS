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
        f.write('refs/heads/master\n')

    # Create the initial "master" branch
    create_branch('master', repo_name=repo_name)
