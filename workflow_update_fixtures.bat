@echo off
setlocal

rem Activate the virtual environment if needed (adjust the path accordingly)
call D:\a\sport_betting\.venv\Scripts\activate.bat

rem Execute your Python script within the virtual environment
py .\update_fixtures_workflow.py

rem Deactivate the virtual environment (if activated)
call D:\a\sport_betting\.venv\Scripts\deactivate.bat

rem End of script
exit /b 0
