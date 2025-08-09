@echo off
echo Closing Brave Browser...
taskkill /F /IM brave.exe >nul 2>&1
echo Brave closed successfully.
pause