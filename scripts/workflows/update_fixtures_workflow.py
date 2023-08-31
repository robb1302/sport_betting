import os
import sys
import logging

def find_and_append_module_path():
    current_dir = os.getcwd()
    substring_to_find = 'sport_betting'
    index = current_dir.rfind(substring_to_find)
    
    if index != -1:
        # Extract the directory path up to and including the last "mypath" occurrence
        new_dir = current_dir[:index + (len(substring_to_find))]

        # Change the current working directory to the new directory
        os.chdir(new_dir)
        sys.path.append(new_dir)
        # Verify the new current directory
        print("New current directory:", os.getcwd())
    else:
        print("No 'mypath' found in the current directory")

if __name__ == "__main__":

    # Configure logging
    print("File:",os.getcwd())
    # print("Dirs",os.listdir())
    # Create a StreamHandler to also log to the console
    print("find_and_append_module_path...")
    find_and_append_module_path()
    print("File:",os.getcwd())
    print("Import...")
    from src.data.download import download_fixtures
    print("Download...")
    download_fixtures(url="https://www.football-data.co.uk/fixtures.csv")
