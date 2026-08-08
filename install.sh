#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ID="chief-of-staff@codex-chief-of-staff"
MARKETPLACE="codex-chief-of-staff"
DRY_RUN=false
UPGRADE=false
UNINSTALL=false
SKIP_CONFIG=false
OWNER="Your Name"
TIMEZONE="Etc/UTC"

usage() {
  cat <<'EOF'
Usage: ./install.sh [--dry-run] [--upgrade] [--uninstall] [--skip-config]
                    [--owner NAME] [--timezone IANA_TIMEZONE]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --upgrade) UPGRADE=true; shift ;;
    --uninstall) UNINSTALL=true; shift ;;
    --skip-config) SKIP_CONFIG=true; shift ;;
    --owner) OWNER="${2:?--owner requires a value}"; shift 2 ;;
    --timezone) TIMEZONE="${2:?--timezone requires a value}"; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

run() {
  printf '%q ' "$@"
  printf '\n'
  if [[ "$DRY_RUN" == false ]]; then
    "$@"
  fi
}

if [[ "$UNINSTALL" == true ]]; then
  run codex plugin remove "$PLUGIN_ID"
  run codex plugin marketplace remove "$MARKETPLACE"
  echo "Chief of Staff removed. Local configuration retained."
  exit 0
fi

run codex plugin marketplace add "$REPO_ROOT"
run codex plugin add "$PLUGIN_ID"

if [[ "$SKIP_CONFIG" == false ]]; then
  if command -v python3 >/dev/null 2>&1; then
    if [[ "$DRY_RUN" == true ]]; then
      run python3 "$REPO_ROOT/scripts/configure.py" init --owner "$OWNER" --timezone "$TIMEZONE"
    else
      set +e
      python3 "$REPO_ROOT/scripts/configure.py" init --owner "$OWNER" --timezone "$TIMEZONE"
      status=$?
      set -e
      if [[ $status -ne 0 && $status -ne 2 ]]; then
        exit "$status"
      fi
    fi
  else
    echo "WARN: Python 3 was not found. Plugin installed; configuration was not initialized." >&2
  fi
fi

echo "Restart Codex, review and trust the Chief of Staff hooks, then start a new task. All internal workflows are bundled."
