#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");

const VERSION = "2.1.1";
const event = process.argv[2] === "subagent" ? "SubagentStart" : "SessionStart";
const pluginRoot = process.env.PLUGIN_ROOT || path.resolve(__dirname, "..");
const SHARED_CONTRACT = "<!-- SHARED-BEHAVIOR-CONTRACT:START -->";

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
    platformConfigPath(),
  ].filter(Boolean);
  return candidates.find((candidate) => fs.existsSync(candidate)) || null;
}

function readRequired(relativePath) {
  return fs.readFileSync(path.join(pluginRoot, relativePath), "utf8").replace(/^\uFEFF/, "").trim();
}

function instructionFile(directory) {
  for (const name of ["AGENTS.override.md", "AGENTS.md"]) {
    const candidate = path.join(directory, name);
    if (fs.existsSync(candidate) && fs.readFileSync(candidate, "utf8").trim()) {
      return candidate;
    }
  }
  return null;
}

function projectInstructionFiles() {
  const current = process.cwd();
  let root = current;
  for (let directory = current; ; directory = path.dirname(directory)) {
    if (fs.existsSync(path.join(directory, ".git"))) {
      root = directory;
      break;
    }
    const parent = path.dirname(directory);
    if (parent === directory) {
      break;
    }
  }
  const directories = [];
  for (let directory = current; ; directory = path.dirname(directory)) {
    directories.push(directory);
    if (directory === root) {
      break;
    }
  }
  return directories.reverse().map(instructionFile).filter(Boolean);
}

function codexAlreadyLoadedContract() {
  const codexHome = process.env.CODEX_HOME || path.join(os.homedir(), ".codex");
  const files = [instructionFile(codexHome), ...projectInstructionFiles()].filter(Boolean);
  return files.some((file) => fs.readFileSync(file, "utf8").includes(SHARED_CONTRACT));
}

function emit() {
  const configPath = resolveConfigPath();
  const configStatus = configPath
    ? `Local configuration: ${configPath}. Read it before connector or registered-project work.`
    : "Local configuration: not found. Keep generic behavior active; do not access connectors or assume project authority.";
  const icmGates = [
    "ICM DEFAULT: operating architecture for non-trivial work. The communication default remains separate.",
    "ICM NEW-WORKSPACE GATE: before proposing files, say ICM and state the repeating unit. State the selected form and factory-product split. Name the human gate.",
    "ICM FORM GATE: use one canonical form name from Chief's internal ICM Architect workflow. Do not invent a sixth form label.",
    "ICM RESPONSE GATE: for every new project, workspace, or recurring process, the first architecture block must name ICM, mode, repeating unit, one canonical form, factory, product, and human gate. Do not propose files before those fields. Use only prompt facts; mark missing inputs unknown.",
    "GENERIC SCOPE GATE: when no registered project is named, do not load or use client facts from configuration or memory. Do not suggest those facts or connector details. Stay generic.",
  ];
  const contextParts = [`CODEX CHIEF OF STAFF ACTIVE - v${VERSION}`];
  if (!process.env.PLUGIN_DATA || !codexAlreadyLoadedContract()) {
    contextParts.push(readRequired("AGENTS.md"));
  }
  contextParts.push(
    readRequired(path.join("persona", "technical-assistant-persona.txt")),
    configStatus,
    ...icmGates,
  );
  const context = contextParts.join("\n\n");

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
