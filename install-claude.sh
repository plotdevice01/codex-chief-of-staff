#!/usr/bin/env sh
set -eu

scope="${1:-user}"
case "$scope" in
  user|project|local) ;;
  *) echo "Usage: ./install-claude.sh [user|project|local]" >&2; exit 2 ;;
esac

command -v claude >/dev/null 2>&1 || {
  echo "Claude Code is not installed or is not on PATH." >&2
  exit 1
}

marketplaces="$(claude plugin marketplace list --json)"
installed="$(claude plugin list --json)"

for entry in \
  "ponytail|DietrichGebert/ponytail|ponytail@ponytail" \
  "ai-sloppy-copy|plotdevice01/ai-sloppy-copy|ai-sloppy-copy@ai-sloppy-copy" \
  "brand-voice-factory|plotdevice01/brand-voice-factory|brand-voice-factory@brand-voice-factory" \
  "crafty-carousels-skill|plotdevice01/crafty-carousels-skill|crafty-carousels@crafty-carousels-skill" \
  "codex-chief-of-staff|plotdevice01/codex-chief-of-staff|chief-of-staff@codex-chief-of-staff"
do
  marketplace="${entry%%|*}"
  rest="${entry#*|}"
  repository="${rest%%|*}"
  plugin="${rest#*|}"
  force_install=false

  if [ "$plugin" = "ai-sloppy-copy@ai-sloppy-copy" ] &&
     printf '%s' "$installed" | grep -Fq "$plugin" &&
     printf '%s' "$installed" | grep -Eq '"version"[[:space:]]*:[[:space:]]*"2\.2\.6"'; then
    claude plugin uninstall "$plugin"
    force_install=true
  fi

  if printf '%s' "$marketplaces" | grep -Fq "\"$marketplace\""; then
    claude plugin marketplace update "$marketplace"
  else
    claude plugin marketplace add "$repository"
  fi

  if [ "$force_install" = false ] && printf '%s' "$installed" | grep -Fq "$plugin"; then
    claude plugin update "$plugin"
  else
    claude plugin install "$plugin" --scope "$scope"
  fi
done

claude plugin list --json
printf "PASS: Chief of Staff stack installed for Claude Code at scope '%s'.\n" "$scope"
printf "Next: start Claude Code, run /reload-plugins, review /hooks, then start a fresh session.\n"
