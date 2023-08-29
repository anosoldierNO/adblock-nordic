#!/usr/bin/env python3
""""
This code first imports the following modules:

os for file handling
requests for downloading files from the internet
github for interacting with GitHub repositories
The code then defines the following constants:

REPO_OWNER: The GitHub username of the owner of the repository where the hosts file will be uploaded
REPO_NAME: The name of the repository where the hosts file will be uploaded
REPO_BRANCH: The name of the branch in the repository where the hosts file will be uploaded
ACCESS_TOKEN: A GitHub access token with the necessary permissions to upload files to the repository
url_list: A list of URLs of hosts files that will be downloaded and combined
The code then defines the following functions:

combine_hosts(): This function downloads the hosts files from the URLs in url_list and combines them into a single file. 
The combined file is then written to a file named hosts.
upload_to_github(): This function uploads the file named hosts to the GitHub repository specified by the constants
REPO_OWNER, REPO_NAME, and REPO_BRANCH. The file is uploaded with the commit message Merged hosts file.
The code then calls the combine_hosts() function. 
The combine_hosts() function downloads the hosts files from the URLs in url_list and combines them into a single file. 
The combined file is then written to a file named hosts.

Finally, the code calls the upload_to_github() function. The upload_to_github() function uploads the file named hosts - 
to the GitHub repository specified by the constants REPO_OWNER, REPO_NAME, and REPO_BRANCH. 
The file is uploaded with the commit message Merged hosts file.

In summary, this code downloads three hosts files from the internet, combines them into a single file, 
and then uploads the combined file to a GitHub repository.
""""


import os
import requests
from github import Github, GithubObject

# GitHub repository information
REPO_OWNER = 'GithubUsername'
REPO_NAME = 'github-reponame'
REPO_BRANCH = 'main'

# GitHub access token (requires repo permissions)
ACCESS_TOKEN = 'your_github_access_token'

# List of URLs to download hosts files from
url_list = [
    'https://someonewhocares.org/hosts/zero/hosts',
    'https://winhelp2002.mvps.org/hosts.txt',
    'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'
]

# Download and combine hosts files
def combine_hosts():
    combined_hosts = ''

    # ... (same as your existing code)

    # Write combined_hosts string to a file
    with open('hosts', 'w') as f:
        f.write(combined_hosts)

    # Upload file to GitHub
    upload_to_github('hosts', 'Merged hosts file')

# ... (same as your existing code)

# Upload file to GitHub
def upload_to_github(file_path, commit_message):
    try:
        # Authenticate with GitHub using access token
        g = Github(ACCESS_TOKEN)

        # Get repository and branch
        repo = g.get_user(REPO_OWNER).get_repo(REPO_NAME)
        branch = repo.get_branch(REPO_BRANCH)

        # Create a new blob with the file content
        with open(file_path, 'rb') as f:
            data = f.read()
        blob = repo.create_git_blob(data, 'utf-8')

        # Get the current tree and append the new blob to it
        tree = repo.get_git_tree(branch.commit.sha, recursive=True)
        element = GithubObject.GithubObject({
            'path': file_path,
            'mode': '100644',
            'type': 'blob',
            'sha': blob.sha
        })
        new_tree = repo.create_git_tree([element], base_tree=tree)

        # Create a new commit with the updated tree
        commit = repo.create_git_commit(
            commit_message,
            new_tree,
            [branch.commit],
            author={
                'name': 'GitHub Action',
                'email': 'anosoldierno@proton.me'
            },
            committer={
                'name': 'GitHub Action',
                'email': 'anosoldierno@proton.me'
            }
        )

        # Update the branch reference to point to the new commit
        branch.edit(commit.sha)
        
        print('File uploaded and committed successfully!')
    except Exception as e:
        print('Failed to upload to GitHub:', str(e))

# Call the function to combine and upload hosts files
combine_hosts()
