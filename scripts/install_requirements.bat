@echo off

REM Check if venv exists and create if not
IF NOT EXIST venv (
  python -m venv venv
  echo Created virtual environment 'venv'
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Check if requirements.txt exists and install requirements
IF EXIST requirements.txt (
  pip install -r requirements.txt
  echo Installed requirements from requirements.txt
) ELSE (
  echo requirements.txt not found. Please create it or install packages manually.
)
