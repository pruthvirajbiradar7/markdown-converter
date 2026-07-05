@echo off
cd /d "%~dp0"
echo.
echo ============================================================
echo  Markdown Converter - Setup
echo  Running from: %CD%
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.12+ from https://www.python.org/downloads/
    echo IMPORTANT: tick "Add python.exe to PATH" during install.
    pause & exit /b 1
)

echo Python found:
python --version
echo.

python -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python version too old. Need 3.10+. Install Python 3.13 from python.org
    pause & exit /b 1
)

echo Python version OK.
echo.
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 ( echo ERROR: venv creation failed. & pause & exit /b 1 )

echo Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip -q 2>nul

echo Installing dependencies (about a minute)...
venv\Scripts\pip install -r requirements.txt -q
if errorlevel 1 ( echo ERROR: Install failed. Check internet connection. & pause & exit /b 1 )

echo.
echo Verifying packages...
venv\Scripts\python.exe -c "from markitdown import MarkItDown; print('  markitdown OK')"
venv\Scripts\python.exe -c "import fitz; print('  pymupdf OK')"
venv\Scripts\python.exe -c "import pytesseract; print('  pytesseract OK')"
venv\Scripts\python.exe -c "from PIL import Image; print('  pillow OK')"
echo.
echo ============================================================
echo  Setup complete.
echo  Next: double-click install_right_click_menu.bat
echo ============================================================
echo.
pause
