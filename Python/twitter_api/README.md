# Download all Instagram posts
Download all posts from an Instagram account.

## Run instructions

Install dependencies and create a file called `login_details.txt` with the following contents:
```
username
password
```
Then run the program: `python3 download-all-instagram-posts.py`.
You will be prompted to enter a username, then select a mode.
* CSV mode saves the posts with the filename as a number, and creates a CSV `output/<username>.csv` that matches
each number to the post's caption and the date and time it was posted.
* Caption mode saves the post with the filename as as much of the caption as can fit, and changes the modified date
to the date and time it was posted.

All of that user's posts will then be downloaded into `output/<username>/`.

The list of posts for each user will be cached - 
if there is one available, you will be prompted to choose to either use the cache or get a fresh list of posts.
