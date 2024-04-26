# Version Control System

## Version Control System (VCS)
===================================

![version_control_system](https://github.com/mrdavtan/vcs/assets/21132073/442ecdc5-aa4c-41fb-b5de-9c41b951cf96)


A lightweight and easy-to-use version control system for managing code and text files locally.

## Description
-----------

The Version Control System (VCS) is a command-line tool designed to be operated locally by an LLM while testing and debugging. It provides a set of basic version control operations, following git conventions, allowing you to create commits, switch between branches, and navigate through the commit history.

This tool was made to avoid the situation of an agent sending too many commits unnecessarily by an agent, until the user is ready to push it to a remote repository.

## Features
--------

-   Initialize a new VCS repository
-   Stage and commit changes
-   Create and switch between branches
-   View the commit history and file changes
-   Navigate forward and backward through the commit history
-   Restore previous versions of files

## Installation
------------

To use the VCS, follow these steps:

1.  Clone the repository:
```bash
git clone https://github.com/yourusername/vcs.git
```
2. Navigate to the project directory:
```bash
cd vcs
```

3. Make sure you have Python installed (version 3.6 or higher).

4. You're ready to start using the VCS!

## Usage

```bash
# Initialize a new repository
$ python vcs.py init

# Stage changes
$ python vcs.py add <file>

# Create a commit
$ python vcs.py commit "Commit message"

# View the commit history
$ python vcs.py log

# Create a new branch
$ python vcs.py branch <branch-name>

# Switch to a branch
$ python vcs.py checkout <branch-name>

# Move to the previous commit
$ python vcs.py reset

# Move to the next commit
$ python vcs.py redo

```

For more detailed information and additional commands, please refer to the User Guide.

Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. Make sure to follow the contribution guidelines.

License
This project is licensed under the MIT License.

The Simple VCS was inspired by the need for a lightweight version control system for local development and testing by an LLM. It follows git conventions while providing a simplified interface.

Happy versioning!
