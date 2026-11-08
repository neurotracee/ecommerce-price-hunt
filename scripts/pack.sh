#!/usr/bin/env bash
# 只打包，不联网、不推送。用法: bash scripts/pack.sh [version]
set -euo pipefail
cd "$(dirname "$0")/.."
if command -v python >/dev/null 2>&1; then PY=python; else PY=python3; fi
"$PY" scripts/pack.py "${1:-}"
