#!/usr/bin/env bash
cd "$(dirname "${BASH_SOURCE[0]}")"
. ./pluz-env.sh
"$PY" "core/pluz_merge.py" "$@"
