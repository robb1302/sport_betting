import os
import sys
import logging



def find_and_append_module_path():
    current_directory = os.getcwd()
    substring_to_find = 'sport_betting'
    index = current_directory.find(substring_to_find)
    
    if index != -1:
        parent_dir = os.path.join(current_directory[:index], substring_to_find)
        sys.path.append(parent_dir)

if __name__ == "__main__":

    # Configure logging

    # Create a StreamHandler to also log to the console
    
    print('Setting env...')
    print(os.getcwd())
    find_and_append_module_path()
    print(os.getcwd())
    print('Setting env done')

    from src.data.download import download_fixtures
    download_fixtures(url="https://www.football-data.co.uk/fixtures.csv")
