@echo off
cd /d "%~dp0"
echo.
echo ============================================================
echo  Markdown Converter - Test
echo ============================================================
echo.
if not exist "venv\Scripts\python.exe" ( echo ERROR: Run setup.bat first. & pause & exit /b 1 )
echo ^<h1^>Test Heading^</h1^>^<p^>Hello from the converter.^</p^> > "%TEMP%\mdconvert_test.html"
echo Testing conversion...
venv\Scripts\python.exe mdconvert.py "%TEMP%\mdconvert_test.html" -o "%TEMP%"
if exist "%TEMP%\mdconvert_test.md" (
    echo.
    echo SUCCESS - Conversion is working. Output:
    echo.
    type "%TEMP%\mdconvert_test.md"
    echo.
    echo ============================================================
    echo  Right-click any file or folder and choose
    echo  "Convert to Markdown".
    echo ============================================================
) else (
    echo FAILED. Check %TEMP%\mdconvert_log.txt for details.
)
echo.
pause
