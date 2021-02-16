# Usage
	- python run.py

# Package dependencies
	- Before installing, create a new virtual environment for this project
		* Python venv docs: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
	- Python 3.8.6
		* This version specifically needed for Tensorflow
		* Use pyenv or similar to manage Python versions
	- Flask
	- flask-wtf
	- email_validator
	- Pillow
	- flask-mail

# Github Flow
	- Github flow docs: https://guides.github.com/introduction/flow/
	
	Example: we have a new page to add for user uploads.

	The flow follows these steps:
		1) `git checkout -b upload-page`
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
		   made from, and click `Compare and pull request`. This will open the request, where you can make notes.
		5) Lastly, all we need to do is *wait for one (1) other team member to review our changes*. This is critical 
		   to ensuring that the changes are good, tested, and ready for deployment!
		   

# TODO
	- get rid of bootstrap href's --> make all links internal and self contained
