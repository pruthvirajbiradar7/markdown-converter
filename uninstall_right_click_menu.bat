@echo off
echo Removing "Convert to Markdown" right-click menu...
reg delete "HKCU\Software\Classes\*\shell\ConvertToMarkdown" /f >nul 2>&1
reg delete "HKCU\Software\Classes\Directory\shell\ConvertToMarkdown" /f >nul 2>&1
echo Done. File and folder menu entries have been removed.
echo.
pause
