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
If you don't already have a Chromium Driver downloaded, you can [do it here](https://googlechromelabs.github.io/chrome-for-testing/).

Your installation of Chrome needs to match the version of the Chromium Driver. The easiest way to ensure this is to open the Settings page in Chrome, go to About Chrome, and check for any updates. Once Chrome is up to date, go to the above link and download the Chromium Driver for your system with the same version.

Extract the contents of the .zip folder to whichever directory you prefer on your system.
In the repository folder, create a new text file called `DRIVERPATH.txt`, and on the first line paste the file path to folder you just extracted.

# Scraping Methods

All the scraping methods are found in the `scrapes.py` file. 

The `fotmob_prem_gk_urls` method will create a text file `fotmob_prem_gk_urls.txt` in the repository folder containing the URLs to the 20 Premier League goalkeeper stats pages on FotMob. Originally this method was combined with `fotmob_prem_gk_stats`, but it was needlessly long to scrape every goalkeeper URL every time you wanted to fetch the most recent stats. Now, you can run this method just once to establish the URLs file.

The `fotmob_prem_gk_stats` method will use the `fotmob_prem_gk_urls.txt` to scrape the stats for each goalkeeper URL. It will create a new CSV file `fotmob_prem_gk_stats.csv` in the repository folder, which can easily be converted into a DataFrame for further manipulation.