@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "RC=0"

rem ============================================================
rem PLUZ-AllStar.bat -- the whole PLUZ5 pipeline in one shot:
rem   sync -> check -> fetch -> update -> pkg -> ffpfsc -> validate -> commit/push
rem
rem Stops at the first failing step and says which one. The window
rem stays open at the end when you double-click this file.
rem Tool locations and repo name come from .env (see .env.example).
rem ============================================================

call "%~dp0pluz-env.bat"
if not defined GH_BRANCH set "GH_BRANCH=main"
set "COMMIT_MSG=auto: PLUZ-AllStar pipeline run"

"%PY%" --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python not found. Set PLUZ_PY_DIR or PLUZ_PYTHON in .env.
    set "RC=1"
    goto :end
)
"%GIT%" --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Git not found. Set PLUZ_GIT_DIR or PLUZ_GIT in .env.
    set "RC=1"
    goto :end
)
echo Python: %PY%
echo Git:    %GIT%

echo.
echo ==================== [0/7] sync with GitHub ====================
"%GIT%" rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    if not defined GH_USER (
        echo [FAIL] This folder is not a git repo and GH_USER / GH_REPO are not set in .env.
        set "RC=1"
        goto :end
    )
    echo This folder is not a git repo yet. Connecting it to https://github.com/%GH_USER%/%GH_REPO%
    "%GIT%" init -b %GH_BRANCH%
    "%GIT%" remote add origin https://github.com/%GH_USER%/%GH_REPO%.git
    "%GIT%" fetch origin
    "%GIT%" reset origin/%GH_BRANCH% >nul 2>&1
)
"%GIT%" remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [FAIL] No remote named origin. Run: git remote add origin https://github.com/%GH_USER%/%GH_REPO%.git
    set "RC=1"
    goto :end
)
set "GHAUTH="
for /f "delims=" %%H in ('"%PY%" "core\pluz_ghauth.py"') do set "GHAUTH=%%H"
if defined GHAUTH (echo Signing in to GitHub with GH_TOKEN from .env) else (echo No GH_TOKEN in .env - git will use its own saved login or ask you to sign in)
set "NOHELP="
if defined GHAUTH set "NOHELP=-c credential.helper="
"%GIT%" %NOHELP% -c "http.extraheader=%GHAUTH%" pull --rebase --autostash origin %GH_BRANCH%
if errorlevel 1 echo [WARN] Could not pull the latest from GitHub - continuing. If the push fails at the end, send me this window's text.

call :step "[1/7] pluz-check" pluz_check.py || goto :end
call :step "[2/7] pluz-fetch" pluz_fetch.py --apply || goto :end
call :step "[3/7] pluz-update" pluz_update.py || goto :end
call :step "[4/7] pluz-pkg" pluz_pkg.py || goto :end
call :step "[5/7] pluz-ffpfsc" pluz_ffpfsc.py || goto :end
call :step "[6/7] pluz-validate" pluz_validate.py || goto :end

echo.
echo ==================== [7/7] git add / commit / push ====================
"%GIT%" add -A
if errorlevel 1 (
    echo [FAIL] git add failed.
    set "RC=1"
    goto :end
)
set "GITCFG="
set "HAVEID="
for /f "delims=" %%N in ('"%GIT%" config user.name 2^>nul') do set "HAVEID=1"
if not defined HAVEID set "GITCFG=-c user.name=%GH_USER% -c user.email=%GH_USER%@users.noreply.github.com"
"%GIT%" diff --cached --quiet
if errorlevel 1 (
    "%GIT%" %GITCFG% commit -m "%COMMIT_MSG%"
    if errorlevel 1 (
        echo [FAIL] git commit failed - see the text above.
        set "RC=1"
        goto :end
    )
) else (
    echo Nothing new to commit - pushing any earlier commits that are still waiting.
)
"%GIT%" %NOHELP% -c "http.extraheader=%GHAUTH%" push -u origin %GH_BRANCH%
if errorlevel 1 (
    echo [FAIL] git push failed - committed locally but not pushed.
    echo        Check that GH_TOKEN in .env is a valid token with access to %GH_REPO% (Contents: read and write).
    set "RC=1"
    goto :end
)
echo Pushed.
goto :end

:step
echo.
echo ==================== %~1 ====================
"%PY%" "core\%~2" %~3
if errorlevel 1 (
    echo.
    echo [FAIL] %~1 failed - stopping. The newest file in the logs folder has the details.
    exit /b 1
)
exit /b 0

:end
echo.
if "%RC%"=="0" (echo ==================== AllStar finished ====================) else (echo ==================== AllStar STOPPED - see the [FAIL] line above ====================)
echo "%cmdcmdline%" | find /i "%~nx0" >nul && pause
exit /b %RC%
