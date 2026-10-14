#!/usr/bin/env bash
# pluz-allstar.sh -- Arch/Linux companion to PLUZ-AllStar.bat.
# Same pipeline: check -> fetch -> update -> pkg -> ffpfsc -> validate -> git add/commit/push,
# stopping immediately on the first failing step.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
. ./pluz-env.sh

COMMIT_MSG="auto: PLUZ-AllStar pipeline run"

run_step() {
    local label="$1"; shift
    echo
    echo "==================== ${label} ===================="
    "$@"
    local rc=$?
    if [ "$rc" -ne 0 ]; then
        echo
        echo "[FAIL] ${label} failed (exit ${rc}) -- stopping."
        exit 1
    fi
}

run_step "[1/7] pluz-check"    "$PY" "core/pluz_check.py"
run_step "[2/7] pluz-fetch"    "$PY" "core/pluz_fetch.py" --apply
run_step "[3/7] pluz-update"   "$PY" "core/pluz_update.py"
run_step "[4/7] pluz-pkg"      "$PY" "core/pluz_pkg.py"
run_step "[5/7] pluz-ffpfsc"  "$PY" "core/pluz_ffpfsc.py"
run_step "[6/7] pluz-validate" "$PY" "core/pluz_validate.py"

echo
echo "==================== [7/7] git add / commit / push ===================="
"$GIT" add -A
if ! "$GIT" diff --cached --quiet; then
    if ! "$GIT" commit -m "$COMMIT_MSG"; then
        echo "[FAIL] git commit failed -- see output above."
        exit 1
    fi
    if ! "$GIT" push; then
        echo "[FAIL] git push failed -- committed locally but not pushed. Check your remote/auth and push manually."
        exit 1
    fi
    echo "Pushed."
else
    echo "Nothing changed -- skipping commit/push."
fi

echo
echo "==================== AllStar complete -- all steps passed ===================="
exit 0
