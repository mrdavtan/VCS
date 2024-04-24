from repository import init_repository
from hashnstore import process_file
from branch import create_branch
from commit import create_commit
from tracker import track_changes


# Initialize a new repository
init_repository()

# Process the test file and store its content
process_file('test.txt')

# Create a new branch (optional)
create_branch('new_branch')

# Create a commit
create_commit('Initial commit', author='davtan <mrdavtan@protonmail.com')

# Track changes in the working directory
track_changes()
