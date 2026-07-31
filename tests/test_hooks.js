#!/usr/bin/env node

const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const root = path.resolve(__dirname, "..");
const hook = path.join(root, "hooks", "chief-of-staff-hook.js");

function runCodex(event, pluginData, cwd, codexHome) {
  const result = spawnSync(process.execPath, [hook, event], {
    cwd,
    encoding: "utf8",
    env: {
      ...process.env,
      PLUGIN_ROOT: root,
      PLUGIN_DATA: pluginData,
      CODEX_HOME: codexHome,
    },
  });
  assert.strictEqual(result.status, 0, result.stderr);
  return JSON.parse(result.stdout);
}

function runClaude(event, cwd = root) {
  const env = { ...process.env, CLAUDE_PLUGIN_ROOT: root };
  delete env.PLUGIN_ROOT;
  delete env.PLUGIN_DATA;
  const result = spawnSync(process.execPath, [hook, event], {
    cwd,
    encoding: "utf8",
    env,
  });
  assert.strictEqual(result.status, 0, result.stderr);
  return result.stdout;
}

const temp = fs.mkdtempSync(path.join(os.tmpdir(), "chief-of-staff-hooks-"));
try {
  const emptyHome = path.join(temp, "home");
  const emptyProject = path.join(temp, "project");
  fs.mkdirSync(emptyHome);
  fs.mkdirSync(emptyProject);
  for (const [event, expected] of [
    ["session", "SessionStart"],
    ["subagent", "SubagentStart"],
  ]) {
    const output = runCodex(event, temp, emptyProject, emptyHome);
    assert.strictEqual(output.systemMessage, "CHIEF OF STAFF:0.5.2");
    assert.strictEqual(output.hookSpecificOutput.hookEventName, expected);
    const context = output.hookSpecificOutput.additionalContext;
    assert.match(context, /85% compression/);
    assert.match(context, /caveman/i);
    assert.match(context, /Technical Assistant Persona/i);
    assert.match(context, /Local configuration: not found/);
  }

  const config = path.join(temp, "chief-of-staff.json");
  fs.writeFileSync(config, '{"release_version":"0.5.2"}\n', "utf8");
  const configured = runCodex("session", temp, emptyProject, emptyHome);
  assert.match(configured.hookSpecificOutput.additionalContext, /Read it before connector/);
  assert.match(configured.hookSpecificOutput.additionalContext, /chief-of-staff\.json/);

  fs.writeFileSync(path.join(emptyProject, "AGENTS.md"), fs.readFileSync(path.join(root, "AGENTS.md")));
  const deduplicated = runCodex("session", temp, emptyProject, emptyHome);
  assert.doesNotMatch(deduplicated.hookSpecificOutput.additionalContext, /85% compression/);
  assert.match(deduplicated.hookSpecificOutput.additionalContext, /Technical Assistant Persona/i);

  const session = runClaude("session");
  assert.match(session, /CODEX CHIEF OF STAFF ACTIVE - v0\.5\.2/);
  assert.match(session, /85% compression/);
  assert.match(session, /Technical Assistant Persona/i);
  assert.match(session, /Local configuration: not found/);

  const subagent = JSON.parse(runClaude("subagent"));
  assert.strictEqual(subagent.hookSpecificOutput.hookEventName, "SubagentStart");
  assert.match(subagent.hookSpecificOutput.additionalContext, /caveman/i);
  console.log("PASS: Codex and Claude Code session and subagent hooks validated.");
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}
