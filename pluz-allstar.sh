#!/usr/bin/env bash
# pluz-allstar.sh -- Linux/Mac companion to PLUZ-AllStar.bat.
# sync -> check -> fetch -> update -> pkg -> ffpfsc -> validate -> commit/push.
# Stops at the first failing step. Repo name and tool paths come from .env.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
. ./pluz-env.sh
GH_USER="${GH_USER:-$(sed -n 's/^GH_USER=//p' .env 2>/dev/null | head -1 | tr -d '"' | tr -d "'")}"
GH_REPO="${GH_REPO:-$(sed -n 's/^GH_REPO=//p' .env 2>/dev/null | head -1 | tr -d '"' | tr -d "'")}"
GH_BRANCH="${GH_BRANCH:-$(sed -n 's/^GH_BRANCH=//p' .env 2>/dev/null | head -1 | tr -d '"' | tr -d "'")}"
GH_BRANCH="${GH_BRANCH:-main}"
COMMIT_MSG="auto: PLUZ-AllStar pipeline run"

fail() { echo; echo "[FAIL] $1"; exit 1; }

run_step() {
    local label="$1"; shift
    echo; echo "==================== ${label} ===================="
    "$@" || fail "${label} failed -- stopping. The newest file in logs/ has the details."
}

echo; echo "==================== [0/7] sync with GitHub ===================="
if ! "$GIT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    [ -n "$GH_USER" ] && [ -n "$GH_REPO" ] || fail "Not a git repo and GH_USER / GH_REPO are not set in .env."
    echo "This folder is not a git repo yet. Connecting it to https://github.com/$GH_USER/$GH_REPO"
    "$GIT" init -b "$GH_BRANCH"
    "$GIT" remote add origin "https://github.com/$GH_USER/$GH_REPO.git"
    "$GIT" fetch origin
    "$GIT" reset "origin/$GH_BRANCH" >/dev/null 2>&1 || true
fi
"$GIT" remote get-url origin >/dev/null 2>&1 || fail "No remote named origin."
GHAUTH="$("$PY" core/pluz_ghauth.py)"
NOHELP=(); [ -n "$GHAUTH" ] && NOHELP=(-c "credential.helper=")
"$GIT" "${NOHELP[@]}" -c "http.extraheader=$GHAUTH" pull --rebase --autostash origin "$GH_BRANCH" || echo "[WARN] Could not pull the latest from GitHub -- continuing."

run_step "[1/7] pluz-check"    "$PY" core/pluz_check.py
run_step "[2/7] pluz-fetch"    "$PY" core/pluz_fetch.py --apply
run_step "[3/7] pluz-update"   "$PY" core/pluz_update.py
run_step "[4/7] pluz-pkg"      "$PY" core/pluz_pkg.py
run_step "[5/7] pluz-ffpfsc"   "$PY" core/pluz_ffpfsc.py
run_step "[6/7] pluz-validate" "$PY" core/pluz_validate.py

echo; echo "==================== [7/7] git add / commit / push ===================="
"$GIT" add -A || fail "git add failed."
if "$GIT" diff --cached --quiet; then
    echo "Nothing new to commit -- pushing any earlier commits that are still waiting."
else
    CFG=()
    [ -n "$("$GIT" config user.name 2>/dev/null)" ] || CFG=(-c "user.name=$GH_USER" -c "user.email=$GH_USER@users.noreply.github.com")
    "$GIT" "${CFG[@]}" commit -m "$COMMIT_MSG" || fail "git commit failed."
fi
"$GIT" "${NOHELP[@]}" -c "http.extraheader=$GHAUTH" push -u origin "$GH_BRANCH" || fail "git push failed -- check GH_TOKEN in .env (Contents: read and write)."
echo "Pushed."
echo; echo "==================== AllStar finished ===================="
