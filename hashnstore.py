#!/usr/bin/env python3
import hashlib
import os
import sys

def hash_content(content):
    """Generate a SHA-1 hash for the given content."""
    sha1 = hashlib.sha1()
    sha1.update(content)
    return sha1.hexdigest()

def store_object(content, repo_name='.vcs'):
    """Store a content object in the repository."""
    hash_id = hash_content(content)
    subdir = hash_id[:2]
    filename = hash_id[2:]
    object_path = os.path.join(repo_name, 'objects', subdir)
    os.makedirs(object_path, exist_ok=True)
    with open(os.path.join(object_path, filename), 'wb') as f:  # Open as binary to write
        f.write(content)
    return hash_id

def process_file(file_path, repo_name='.vcs'):
    """Reads file content, hashes, and stores it using provided VCS functions."""
    with open(file_path, 'rb') as f:  # Open as binary to read
        content = f.read()
        store_object(content, repo_name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py <file1> [file2] ...")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        process_file(file_path)

