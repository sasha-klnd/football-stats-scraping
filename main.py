from  scrapes import *
import requests

def main():
    # Call some of the scraping methods here

    df = pd.read_csv('ga-sota-psxg.csv')

    print(df.tail())

    pass

if __name__ == "__main__":
    main()