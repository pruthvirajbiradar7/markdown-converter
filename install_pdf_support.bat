@echo off
cd /d "%~dp0"
echo.
echo Installing PDF support (pymupdf)...
if not exist "venv\Scripts\pip.exe" ( echo ERROR: Run setup.bat first. & pause & exit /b 1 )
venv\Scripts\pip install pymupdf -q
venv\Scripts\python.exe -c "import fitz; print('  pymupdf', fitz.version[0], '- OK')"
echo.
echo Done. PDF conversion is now enabled.
echo.
pause
