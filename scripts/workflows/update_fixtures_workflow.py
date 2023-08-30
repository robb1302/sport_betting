import os
import sys
import logging



if __name__ == "__main__":

    # Configure logging
    print(os.getcwd())
    # Create a StreamHandler to also log to the console
    
    from src.data.download import download_fixtures
    download_fixtures(url="https://www.football-data.co.uk/fixtures.csv")
