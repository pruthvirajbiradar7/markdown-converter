@echo off
echo Removing right-click menus...
reg delete "HKCU\Software\Classes\*\shell\ConvertToMarkdown" /f >nul 2>&1
reg delete "HKCU\Software\Classes\Directory\shell\ConvertToMarkdown" /f >nul 2>&1
reg delete "HKCU\Software\Classes\SystemFileAssociations\.md\shell\ConvertToWord" /f >nul 2>&1
echo Done. All menu entries removed.
echo.
pause
