@echo off
setlocal

rem Path to the virtual environment
set VENV_PATH=C:\Users\Robert\Documents\Projekte\dev\sport_betting\.venv

rem Activate the virtual environment
call "%VENV_PATH%\Scripts\activate"

rem Execute your Python scripts within the virtual environment
py .\scripts\provide_data\download_fixtures.py 
py .\scripts\make_predictions\deploy_results.py 

rem Deactivate the virtual environment when done with Python scripts
call "%VENV_PATH%\Scripts\deactivate"

rem Push 'updates.csv' to the 'main' branch in your Git repository
cd "C:\Users\Robert\Documents\Projekte\dev\sport_betting\data\results\"

rem Add 'updates.csv' to the Git staging area
git add results.csv

rem Commit the changes
git commit -m "Add results.csv"

rem Push the changes to the 'main' branch
git push origin main

rem End of script
exit /b 0
