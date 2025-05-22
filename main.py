from  scrapes import *
import time

def main():
    # Call some of the scraping methods here

    start = time.time()

    transfermarkt_mls_transfers()

    print(f"----- Program Execution Time: {time.time() - start} -----")

if __name__ == "__main__":
    main()