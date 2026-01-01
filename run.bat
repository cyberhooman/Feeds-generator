@echo off
cd /d "%~dp0"
echo ==================================================
echo      INSTAGRAM FEED GENERATOR LAUNCHER
echo ==================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python from python.org and try again.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b
)

:: Check if Streamlit is installed
echo Checking requirements...
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Streamlit is not installed. Installing now...
    pip install streamlit
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Streamlit.
        pause
        exit /b
    )
    echo Streamlit installed successfully.
)

echo Starting the application...
echo Keep this window OPEN. If browser doesn't open, go to http://127.0.0.1:8501
python -m streamlit run main.py --server.port 8501 --server.address 127.0.0.1 --browser.gatherUsageStats false
pause