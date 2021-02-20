# Usage
	- python run.py

# Python Version (important!)
- Python 3.8.6 (specifically needed for tensorflow 2)
* **pyenv** is built to manage python versions
* To make sure we're all using the same version, issue: pyenv global 3.8.6
* Note: a different package may be required to do this on Windows

# Package dependencies
Before installing, create a new virtual environment.
* python -m venv /path/to/virtual/environ/folder
	- creates virtual environment in specified location with specified name
	- e.g., name of the virtual environment for above command would be 'folder'
* pip install -r requirements.txt
	-  installs all project package requirements listed in requirements.txt:

# Github Flow
- Github flow docs: https://guides.github.com/introduction/flow/
	
Example: we have a new page to add for user uploads.

The flow follows these steps:
1) git checkout -b upload-page
	- This command simultaneously creates a new branch and switches into it.
	- The branch names should always be descriptive of the feature they are for.
2) You do some work on the `upload-page` branch, and are ready to commit them.
	- git add <files_to_be_committed>
	- git commit -m "message describing the commit changes"
	- git push origin upload-page
3) At this point, our feater branch 'upload-page' is one commit ahead of the 'main' branch,
   and is ready to be merged back into main. However, what if there has been recent changes to main?
   The simple answer is to perform a `git pull origin main` while on the `upload-page` branch to 
   pull in any recent changes that have been merged to master while we've been working on our feature branch.
4) Now it's finally time to merge our changes back into master, which will be done using a Pull Request (PR).
   To do this, navigate to the repository in the browser, select the branch where the pull request is being
   made from, change to the  `Pull Requests` tab, and click `Compare and pull request`. This will open the request, 
   and allow you to attach notes.
5) Lastly, all we need to do is *wait for one (1) other team member to review our changes*. This is critical 
   to ensuring that the changes are good, tested, and ready for deployment!
