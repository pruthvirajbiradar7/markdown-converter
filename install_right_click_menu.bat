@echo off
cd /d "%~dp0"

set "PYTHONW=%~dp0venv\Scripts\pythonw.exe"
set "FILE_SCRIPT=%~dp0run_silent.py"
set "FOLDER_SCRIPT=%~dp0run_folder_silent.py"

echo Installing "Convert to Markdown" right-click menu...
echo.

if not exist "%PYTHONW%" (
    echo ERROR: venv not found. Please run setup.bat first, then try again.
    pause
    exit /b 1
)

REM --- Right-click on any FILE ---
reg add "HKCU\Software\Classes\*\shell\ConvertToMarkdown" /ve /d "Convert to Markdown" /f >nul 2>&1
reg add "HKCU\Software\Classes\*\shell\ConvertToMarkdown\command" /ve /d "\"%PYTHONW%\" \"%FILE_SCRIPT%\" \"%%1\"" /f >nul 2>&1

REM --- Right-click on any FOLDER ---
reg add "HKCU\Software\Classes\Directory\shell\ConvertToMarkdown" /ve /d "Convert to Markdown" /f >nul 2>&1
reg add "HKCU\Software\Classes\Directory\shell\ConvertToMarkdown\command" /ve /d "\"%PYTHONW%\" \"%FOLDER_SCRIPT%\" \"%%V\"" /f >nul 2>&1

if errorlevel 1 (
    echo Something went wrong. Try right-clicking this file and choosing
    echo "Run as administrator", then try again.
) else (
    echo Done.
    echo.
    echo Registered for:
    echo   Files:   right-click any file   -^> "Convert to Markdown"
    echo   Folders: right-click any folder -^> "Convert to Markdown"
    echo.
    echo Python: %PYTHONW%
)
echo.
pause
