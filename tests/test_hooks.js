#!/usr/bin/env node

const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const root = path.resolve(__dirname, "..");
const hook = path.join(root, "hooks", "chief-of-staff-hook.js");

function run(event, pluginData, cwd = root) {
  const result = spawnSync(process.execPath, [hook, event], {
    cwd,
    encoding: "utf8",
    env: { ...process.env, PLUGIN_ROOT: root, PLUGIN_DATA: pluginData },
  });
  assert.strictEqual(result.status, 0, result.stderr);
  return JSON.parse(result.stdout);
}

const temp = fs.mkdtempSync(path.join(os.tmpdir(), "chief-of-staff-hooks-"));
try {
  for (const [event, expected] of [
    ["session", "SessionStart"],
    ["subagent", "SubagentStart"],
  ]) {
    const output = run(event, temp);
    assert.strictEqual(output.systemMessage, "CHIEF OF STAFF:0.4.4");
    assert.strictEqual(output.hookSpecificOutput.hookEventName, expected);
    const context = output.hookSpecificOutput.additionalContext;
    assert.match(context, /85% compression/);
    assert.match(context, /caveman/i);
    assert.match(context, /Technical Assistant Persona/i);
    assert.match(context, /Local configuration: not found/);
  }

  const config = path.join(temp, "chief-of-staff.json");
  fs.writeFileSync(config, '{"release_version":"0.4.4"}\n', "utf8");
  const configured = run("session", temp);
  assert.match(configured.hookSpecificOutput.additionalContext, /Read it before connector/);
  assert.match(configured.hookSpecificOutput.additionalContext, /chief-of-staff\.json/);
  console.log("PASS: SessionStart and SubagentStart hook output validated.");
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}
