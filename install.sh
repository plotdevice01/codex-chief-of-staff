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

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required to stage the repository-owned install package." >&2
  exit 1
fi

if [[ -n "${CODEX_HOME:-}" ]]; then
  CODEX_HOME_PATH="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$CODEX_HOME")"
else
  CODEX_HOME_PATH="$(python3 -c 'import pathlib; print((pathlib.Path.home()/".codex").resolve())')"
fi
INSTALL_SOURCE="$REPO_ROOT/.install/codex-chief-of-staff"
CACHE_ROOT="$CODEX_HOME_PATH/plugins/cache/codex-chief-of-staff/chief-of-staff"

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

run_allow_failure() {
  printf '%q ' "$@"
  printf '\n'
  if [[ "$DRY_RUN" == false ]]; then
    "$@" || true
  fi
}

remove_chief_path() {
  local target="$1"
  local expected="$2"
  local resolved_target resolved_expected
  resolved_target="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve())' "$target")"
  resolved_expected="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve())' "$expected")"
  if [[ "$resolved_target" != "$resolved_expected" ]]; then
    echo "Refusing to remove unexpected path: $resolved_target" >&2
    exit 1
  fi
  if [[ -e "$resolved_target" ]]; then
    printf 'REMOVE %s\n' "$resolved_target"
    if [[ "$DRY_RUN" == false ]]; then
      rm -rf -- "$resolved_target"
    fi
  fi
}

if [[ "$UNINSTALL" == true ]]; then
  run_allow_failure codex plugin remove "$PLUGIN_ID"
  run_allow_failure codex plugin marketplace remove "$MARKETPLACE"
  remove_chief_path "$CACHE_ROOT" "$CACHE_ROOT"
  remove_chief_path "$INSTALL_SOURCE" "$INSTALL_SOURCE"
  echo "Chief of Staff and its cache removed. Local configuration retained."
  exit 0
fi

run_allow_failure codex plugin remove "$PLUGIN_ID"
run_allow_failure codex plugin marketplace remove "$MARKETPLACE"
remove_chief_path "$CACHE_ROOT" "$CACHE_ROOT"
remove_chief_path "$INSTALL_SOURCE" "$INSTALL_SOURCE"
run python3 "$REPO_ROOT/scripts/stage_install.py" --output "$INSTALL_SOURCE"
run codex plugin marketplace add "$INSTALL_SOURCE"
run codex plugin add "$PLUGIN_ID"

if [[ "$SKIP_CONFIG" == false ]]; then
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
fi

echo "Chief of Staff installed from a clean repository-owned staging package. Old Chief cache removed."
echo "Restart Codex, review and trust the Chief of Staff hooks, then start a new task. All internal workflows are bundled."
