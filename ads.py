#!/usr/bin/env python3

"""
This script is a powerful ad-blocking solution that combines several sources into one,
providing you with the most comprehensive protection against unwanted ads and pop-ups.
By merging these sources, we have created a single, easy-to-use script that offers
the best ad-blocking experience for our users.

**Block the Noise!**

Say goodbye to annoying ads and hello to a cleaner, faster browsing experience with
adblock-nordic by anosoldierNO. This repository contains a custom-made adblock list
with entries for Nordic countries, built to help you block unwanted ads on your devices.
By using this list with adblocker software like Pihole, you can enjoy a safer,
more enjoyable browsing experience without any distractions. Don't let ads slow you down –
take control of your online experience today with adblock-nordic.

**Copyright Information**

This adblock list is an open-source project and is licensed under the MIT License.

(c) 2023 anosoldierNO

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

**Standard Information**

This is the adblock-nordic repository by anosoldierNO. It contains a custom-made
adblock list with entries for Nordic countries.

Check out anosoldierNO's Github profile for more information and updates:
https://github.com/anosoldierNO

You can use this list with adblocker software like Pihole to prevent ads from appearing
on your devices. Not only will this enhance your browsing experience, but it will also
protect you from malicious ads that could potentially harm your device.
"""


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
