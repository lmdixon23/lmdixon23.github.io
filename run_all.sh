#!/usr/bin/env bash
set -euo pipefail

PY=python3
"$PY" -c "" 2>/dev/null || PY=python
"$PY" -c "" 2>/dev/null || { echo "No working Python interpreter found"; exit 1; }

printf '%s\n' '== Canonical-file integrity =='
"$PY" scripts/verify_sha256_manifest.py

printf '%s\n' '== Static-site structure =='
"$PY" scripts/verify_site.py

printf '%s\n' '== Final canonical-file integrity =='
"$PY" scripts/verify_sha256_manifest.py

printf '%s\n' 'VERDICT: SITE VERIFIED'
