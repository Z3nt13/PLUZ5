@echo off
cd /d "%~dp0"
call "%~dp0pluz-env.bat"
"%PY%" "core\pluz_migrate.py" %*
