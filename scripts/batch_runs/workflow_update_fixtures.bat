@echo off
setlocal

rem Execute your Python scripts within the virtual environment
py .\scripts\provide_data\download_fixtures.py 
py .\scripts\make_predictions\deploy_results.py 

rem End of script
exit /b 0
