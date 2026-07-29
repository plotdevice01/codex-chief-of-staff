#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");

const VERSION = "0.4.0";
const event = process.argv[2] === "subagent" ? "SubagentStart" : "SessionStart";
const pluginRoot = process.env.PLUGIN_ROOT || process.env.CLAUDE_PLUGIN_ROOT || path.resolve(__dirname, "..");

function platformConfigPath() {
  if (process.env.XDG_CONFIG_HOME) {
    return path.join(process.env.XDG_CONFIG_HOME, "codex-chief-of-staff", "chief-of-staff.json");
  }
  if (process.platform === "win32") {
    const appData = process.env.APPDATA || path.join(os.homedir(), "AppData", "Roaming");
    return path.join(appData, "codex-chief-of-staff", "chief-of-staff.json");
  }
  return path.join(os.homedir(), ".config", "codex-chief-of-staff", "chief-of-staff.json");
}

function resolveConfigPath() {
  const candidates = [
    process.env.CHIEF_OF_STAFF_CONFIG,
    path.join(process.cwd(), "chief-of-staff.json"),
    path.join(pluginRoot, "chief-of-staff.json"),
    process.env.PLUGIN_DATA && path.join(process.env.PLUGIN_DATA, "chief-of-staff.json"),
    process.env.CLAUDE_PLUGIN_DATA && path.join(process.env.CLAUDE_PLUGIN_DATA, "chief-of-staff.json"),
    platformConfigPath(),
  ].filter(Boolean);
  return candidates.find((candidate) => fs.existsSync(candidate)) || null;
}

function readRequired(relativePath) {
  return fs.readFileSync(path.join(pluginRoot, relativePath), "utf8").replace(/^\uFEFF/, "").trim();
}

function emit() {
  const configPath = resolveConfigPath();
  const configStatus = configPath
    ? `Local configuration: ${configPath}. Read it before connector or registered-project work.`
    : "Local configuration: not found. Keep generic behavior active; do not access connectors or assume project authority.";
  const context = [
    `CODEX CHIEF OF STAFF ACTIVE - v${VERSION}`,
    readRequired("AGENTS.md"),
    readRequired(path.join("persona", "technical-assistant-persona.txt")),
    configStatus,
  ].join("\n\n");

  if (process.env.PLUGIN_DATA) {
    process.stdout.write(JSON.stringify({
      systemMessage: `CHIEF OF STAFF:${VERSION}`,
      hookSpecificOutput: {
        hookEventName: event,
        additionalContext: context,
      },
    }));
    return;
  }

  if (event === "SubagentStart") {
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: event,
        additionalContext: context,
      },
    }));
    return;
  }

  process.stdout.write(context);
}

try {
  emit();
} catch (error) {
  process.stderr.write(`Chief of Staff hook failed: ${error.message}\n`);
  process.exitCode = 1;
}
