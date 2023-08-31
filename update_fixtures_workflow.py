import os
import sys
import logging



if __name__ == "__main__":

    # Configure logging
    print("File:",os.getcwd())
    print("Dirs",os.listdir())
    # Create a StreamHandler to also log to the console
    print("Import...")
    from src.data.download import download_fixtures
    print("Download...")
    download_fixtures(url="https://www.football-data.co.uk/fixtures.csv")
