# Setting up the environment
Install all the necessary dependencies for this project:
``` 
# Initializes and activate a new virtual environment
python -m venv env
.\env\Scripts\activate

# Install packages
pip install -r requirements.txt
```

# Setting up a Chromium Driver
Some scraping methods use a Chromium Driver with Selenium. 
If you don't already have a Chromium Driver downloaded, you can [do it here](https://developer.chrome.com/docs/chromedriver/downloads).

Extract the contents of the .zip folder.
In the repository folder, create a new text file called `DRIVERPATH.txt`, and on the first line paste the file path to folder you just extracted.