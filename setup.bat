@echo off

:: Check if virtual environment already exists
IF NOT EXIST "venv" (
    python -m venv venv
    echo Created virtual environment.
) ELSE (
    echo virtual environment already exists.
)

:: Activate virtual environment 
call venv\Scripts\activate.bat

:: Install requirements
pip install -r requirements.txt

echo installed dependencies.
