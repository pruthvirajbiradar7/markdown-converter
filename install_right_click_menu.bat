@echo off
cd /d "%~dp0"

set "PYTHONW=%~dp0venv\Scripts\pythonw.exe"
set "FILE_SCRIPT=%~dp0run_silent.py"
set "FOLDER_SCRIPT=%~dp0run_folder_silent.py"
set "MD_TO_WORD_SCRIPT=%~dp0run_md_to_word_silent.py"

echo Installing right-click menus...
echo.

if not exist "%PYTHONW%" (
    echo ERROR: venv not found. Please run setup.bat first, then try again.
    pause
    exit /b 1
)

REM --- Any FILE: "Convert to Markdown" ---
reg add "HKCU\Software\Classes\*\shell\ConvertToMarkdown" /ve /d "Convert to Markdown" /f >nul 2>&1
reg add "HKCU\Software\Classes\*\shell\ConvertToMarkdown\command" /ve /d "\"%PYTHONW%\" \"%FILE_SCRIPT%\" \"%%1\"" /f >nul 2>&1

REM --- Any FOLDER: "Convert to Markdown" ---
reg add "HKCU\Software\Classes\Directory\shell\ConvertToMarkdown" /ve /d "Convert to Markdown" /f >nul 2>&1
reg add "HKCU\Software\Classes\Directory\shell\ConvertToMarkdown\command" /ve /d "\"%PYTHONW%\" \"%FOLDER_SCRIPT%\" \"%%V\"" /f >nul 2>&1

REM --- .md FILES ONLY: "Convert to Word" ---
reg add "HKCU\Software\Classes\SystemFileAssociations\.md\shell\ConvertToWord" /ve /d "Convert to Word" /f >nul 2>&1
reg add "HKCU\Software\Classes\SystemFileAssociations\.md\shell\ConvertToWord\command" /ve /d "\"%PYTHONW%\" \"%MD_TO_WORD_SCRIPT%\" \"%%1\"" /f >nul 2>&1

if errorlevel 1 (
    echo Something went wrong. Try right-clicking this file and choosing
    echo "Run as administrator", then try again.
) else (
    echo Done.
    echo.
    echo Registered:
    echo   Any file    -^> right-click -^> "Convert to Markdown"
    echo   Any folder  -^> right-click -^> "Convert to Markdown"
    echo   .md files   -^> right-click -^> "Convert to Word"
    echo.
    echo Python: %PYTHONW%
)
echo.
pause
