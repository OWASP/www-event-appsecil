@echo off
setlocal
rem Refresh the user PATH so a newly installed Ruby can be found.
for /f "tokens=2,*" %%A in ('reg query HKCU\Environment /v Path 2^>nul') do set "PATH=%%B;%PATH%"
where ruby.exe >nul 2>nul
if errorlevel 1 (
    echo Ruby was not found. Install Ruby and enable its Add to PATH option.
    exit /b 1
)
ruby.exe "%~dp0_tools\preview.rb" %*
exit /b %errorlevel%
