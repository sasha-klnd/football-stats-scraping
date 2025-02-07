# Setting up the environment
Create a python virtual environment using `python -m venv env`
Install all the necessary packages with `pip install -r requirements.txt`

# Setting up a Chromium Driver
Some scraping methods use a Chromium Driver with Selenium. 
If you don't already have a Chromium Driver downloaded, you can [do it here](https://developer.chrome.com/docs/chromedriver/downloads.).

Extract the contents of the .zip folder and remember the directory you save it to.
In the repository folder, create a new text file called `DRIVERPATH.txt`, and on the first line paste the file path to driver.