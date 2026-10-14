@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

rem ============================================================
rem PLUZ-AllStar.bat -- the full PLUZ-ps5 pipeline in one shot:
rem   check -> fetch -> update -> pkg -> ffpfsc -> validate -> git add/commit/push
rem
rem Stops immediately on the first failing step. Non-destructive
rem up through validate (those steps only write manifests/logs);
rem the git step is the only one that touches the remote, and it
rem only runs if every step before it succeeded.
rem
rem Tool locations come from .env (see .env.example) via pluz-env.bat.
rem ============================================================

call "%~dp0pluz-env.bat"
set "COMMIT_MSG=auto: PLUZ-AllStar pipeline run"

"%PY%" --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python not found. Set PLUZ_PY_DIR or PLUZ_PYTHON in .env.
    exit /b 1
)
"%GIT%" --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Git not found. Set PLUZ_GIT_DIR or PLUZ_GIT in .env.
    exit /b 1
)

echo.
echo ==================== [1/7] pluz-check ====================
"%PY%" "core\pluz_check.py"
if errorlevel 1 (
    echo.
    echo [FAIL] pluz-check reported problems -- fix them before AllStar can continue.
    exit /b 1
)

echo.
echo ==================== [2/7] pluz-fetch ====================
"%PY%" "core\pluz_fetch.py" --apply
if errorlevel 1 (
    echo.
    echo [FAIL] pluz-fetch failed.
    exit /b 1
)

echo.
echo ==================== [3/7] pluz-update ====================
"%PY%" "core\pluz_update.py"
if errorlevel 1 (
    echo.
    echo [FAIL] pluz-update failed -- manifests were not fully regenerated.
    exit /b 1
)

echo.
echo ==================== [4/7] pluz-pkg ====================
"%PY%" "core\pluz_pkg.py"
if errorlevel 1 (
    echo.
    echo [FAIL] pluz-pkg failed -- PKG manifest was not fully regenerated.
    exit /b 1
)

echo.
echo ==================== [5/7] pluz-ffpfsc ====================
"%PY%" "core\pluz_ffpfsc.py"
if errorlevel 1 (
    echo.
    echo [FAIL] pluz-ffpfsc failed -- ffpfsc manifest was not fully regenerated.
    exit /b 1
)

echo.
echo ==================== [6/7] pluz-validate ====================
"%PY%" "core\pluz_validate.py"
if errorlevel 1 (
    echo.
    echo [FAIL] pluz-validate found problems -- not pushing a bad state.
    exit /b 1
)

echo.
echo ==================== [7/7] git add / commit / push ====================
"%GIT%" add -A
if errorlevel 1 (
    echo [FAIL] git add failed.
    exit /b 1
)

"%GIT%" diff --cached --quiet
if not errorlevel 1 (
    echo Nothing changed -- skipping commit/push.
    goto :done
)

"%GIT%" commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo [FAIL] git commit failed -- see output above.
    exit /b 1
)

"%GIT%" push
if errorlevel 1 (
    echo [FAIL] git push failed -- committed locally but not pushed. Check your remote/auth and push manually.
    exit /b 1
)

echo Pushed.

:done
echo.
echo ==================== AllStar complete -- all steps passed ====================
exit /b 0
