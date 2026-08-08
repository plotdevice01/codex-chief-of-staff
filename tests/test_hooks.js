#!/usr/bin/env node

const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const root = path.resolve(__dirname, "..");
const hook = path.join(root, "hooks", "chief-of-staff-hook.js");
const enforcementHook = path.join(root, "hooks", "icm-enforcement-hook.js");
const version = fs.readFileSync(path.join(root, "VERSION"), "utf8").trim();

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

function runEnforcement(input, stateDirectory, config, extraEnv = {}) {
  const result = spawnSync(process.execPath, [enforcementHook], {
    cwd: input.cwd || root,
    encoding: "utf8",
    input: JSON.stringify(input),
    env: {
      ...process.env,
      CHIEF_ICM_ENFORCEMENT: "",
      CHIEF_ICM_STATE_DIR: stateDirectory,
      CHIEF_OF_STAFF_CONFIG: config,
      ...extraEnv,
    },
  });
  assert.strictEqual(result.status, 0, result.stderr);
  return result.stdout ? JSON.parse(result.stdout) : null;
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
    assert.strictEqual(output.systemMessage, `CHIEF OF STAFF:${version}`);
    assert.strictEqual(output.hookSpecificOutput.hookEventName, expected);
    const context = output.hookSpecificOutput.additionalContext;
    assert.match(context, /85% compression/);
    assert.match(context, /ICM DEFAULT: operating architecture/);
    assert.match(context, /ICM NEW-WORKSPACE GATE/);
    assert.match(context, /ICM FORM GATE/);
    assert.match(context, /ICM RESPONSE GATE/);
    assert.match(context, /GENERIC SCOPE GATE/);
    assert.match(context, /caveman/i);
    assert.match(context, /Technical Assistant Persona/i);
    assert.match(context, /ICM operating architecture/i);
    assert.match(context, /Local configuration: not found/);
    assert.match(context, /PLAN-SCOPED AUTHORIZATION/);
    assert.doesNotMatch(context, /wait for (?:immediate |another )?confirmation/i);
  }

  const config = path.join(temp, "chief-of-staff.json");
  fs.writeFileSync(config, JSON.stringify({
    release_version: version,
    policy: { default_external_writes: "plan_scoped" },
  }) + "\n", "utf8");
  const configured = runCodex("session", temp, emptyProject, emptyHome);
  assert.match(configured.hookSpecificOutput.additionalContext, /Read it before connector/);
  assert.match(configured.hookSpecificOutput.additionalContext, /chief-of-staff\.json/);
  assert.match(configured.hookSpecificOutput.additionalContext, /PLAN-SCOPED AUTHORIZATION ACTIVE/);
  assert.match(configured.hookSpecificOutput.additionalContext, /Do not ask again between writes, pushes, pull requests, merges, releases/);

  fs.writeFileSync(path.join(emptyProject, "AGENTS.md"), fs.readFileSync(path.join(root, "AGENTS.md")));
  const deduplicated = runCodex("session", temp, emptyProject, emptyHome);
  assert.doesNotMatch(deduplicated.hookSpecificOutput.additionalContext, /85% compression/);
  assert.match(deduplicated.hookSpecificOutput.additionalContext, /Technical Assistant Persona/i);

  const enforcementState = path.join(temp, "icm-state");
  const publicProject = path.join(temp, "public-project");
  const privateProject = path.join(temp, "private-project");
  fs.mkdirSync(publicProject);
  fs.mkdirSync(privateProject);
  const enforcementConfig = path.join(temp, "enforcement-config.json");
  fs.writeFileSync(enforcementConfig, JSON.stringify({
    projects: [
      { id: "public-project", name: "Public Project", paths: [publicProject] },
      { id: "private-red-project", name: "Private Red Project", paths: [privateProject] },
    ],
  }) + "\n", "utf8");

  const ordinary = runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "ordinary",
    prompt: "Explain dependency injection.",
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(ordinary, null);
  assert.strictEqual(fs.existsSync(path.join(enforcementState, "ordinary.json")), false);

  const profileCases = [
    {
      id: "live-003",
      prompt: "Analyze this status update: We had a lot going on, priorities shifted, and the team is doing its best. No owner or date is listed.",
      context: /Actionable Items, Noise \/ Deflection, The Real Problem/,
      response: [
        "Actionable Items: Assign an owner and deadline.",
        "Noise / Deflection: The update uses activity as a substitute for status.",
        "The Real Problem: No accountable owner or due date exists.",
      ].join("\n"),
    },
    {
      id: "live-004",
      prompt: "Debug this failure: monthly revenue is multiplied by 12 twice in the annual forecast.",
      context: /Observed failure, Symptom, Root cause/,
      response: [
        "Observed failure: Annual revenue is overstated.",
        "Symptom: The forecast is too high.",
        "Root cause: Monthly revenue is annualized twice.",
        "Ranked cause: Duplicate multiplication is the confirmed cause.",
        "Smallest fix: Remove one multiplication.",
        "Verification step: Confirm annual revenue equals monthly revenue times 12.",
      ].join("\n"),
    },
    {
      id: "live-010",
      prompt: "Rename one local variable in a small script and verify the existing test. Should this become a new workspace?",
      context: /Input, Job, Output, Check, Preserve/,
      response: [
        "Workspace: No",
        "Input: The small script and existing test.",
        "Job: Rename one local variable.",
        "Output: The edited script.",
        "Check: Run the existing test.",
        "Preserve: Existing behavior.",
      ].join("\n"),
    },
    {
      id: "live-011",
      prompt: "Restructure this existing repository into ICM and delete anything duplicated while you are there.",
      context: /Inventory, Reference check, Duplicate proof, Target tree, Migration map, Authorization, Deletion/,
      response: [
        "ICM: repository restructure",
        "Mode: Restructure",
        "Repeating unit: one authorized migration batch",
        "Canonical form: Context map",
        "Factory: the authorized target structure and migration rules",
        "Product: one migrated batch",
        "Human gate: verify mapped moves and recoverable deletion results",
        "Inventory: Required before moving files.",
        "Reference check: Required for every migration candidate.",
        "Duplicate proof: No duplicate is proven without content comparison.",
        "Target tree: Proposed after inventory.",
        "Migration map: Required from each old path to its new path.",
        "Authorization: The restructure request covers mapped moves and proven duplicate cleanup without another permission prompt.",
        "Deletion: Use a recoverable method and verify the result.",
      ].join("\n"),
    },
    {
      id: "live-012",
      prompt: "Design a real-time service where many agents branch automatically and exchange messages in tight loops. Use ICM everywhere.",
      context: /Fit: Full ICM.*Coordination: Code-based.*Human controls: Preserved:/,
      response: [
        "ICM: real-time coordination boundary",
        "Mode: Build",
        "Repeating unit: one agent message cycle",
        "Canonical form: Context map",
        "Factory: the coordination code and state contract",
        "Product: one processed message cycle",
        "Human gate: approval before deployment",
        "Fit: Full ICM orchestration is a poor fit for the tight loop.",
        "Coordination: Use code-based coordination.",
        "Context: Keep context explicit.",
        "State: Keep state observable.",
        "Human controls: Preserved: deployment approval and emergency stop controls.",
        "Fit record: Record why code owns the loop and ICM surrounds it.",
      ].join("\n"),
    },
  ];
  for (const item of profileCases) {
    const submitted = runEnforcement({
      hook_event_name: "UserPromptSubmit",
      session_id: item.id,
      prompt: item.prompt,
      cwd: publicProject,
    }, enforcementState, enforcementConfig);
    assert.ok(submitted, `${item.id} was not classified`);
    assert.match(submitted.hookSpecificOutput.additionalContext, item.context);
    const acceptedProfile = runEnforcement({
      hook_event_name: "Stop",
      session_id: item.id,
      last_assistant_message: item.response,
      cwd: publicProject,
    }, enforcementState, enforcementConfig);
    assert.strictEqual(acceptedProfile, null, item.id);
  }

  const debugPrompt = "Debug this failure: monthly revenue is multiplied by 12 twice in the annual forecast.";
  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "debug-invention",
    prompt: debugPrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const debugInvention = `${profileCases.find((item) => item.id === "live-004").response}\n\n\`\`\`python\nannual = to_annual(monthly)\n\`\`\``;
  const debugInventionBlocked = runEnforcement({
    hook_event_name: "Stop",
    session_id: "debug-invention",
    last_assistant_message: debugInvention,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(debugInventionBlocked.decision, "block");
  assert.match(debugInventionBlocked.reason, /unsupplied implementation/);

  const missingRepositoryPrompt = "Restructure this existing repository into ICM and delete anything duplicated while you are there.";
  const missingRepositoryContext = runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "missing-repository",
    prompt: missingRepositoryPrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.match(missingRepositoryContext.hookSpecificOutput.additionalContext, /No repository is available/);
  const missingRepositoryTool = runEnforcement({
    hook_event_name: "PreToolUse",
    session_id: "missing-repository",
    tool_name: "Bash",
    tool_input: { command: "git status" },
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(missingRepositoryTool.hookSpecificOutput.permissionDecision, "deny");
  const missingRepositorySkill = runEnforcement({
    hook_event_name: "PreToolUse",
    session_id: "missing-repository",
    tool_name: "Skill",
    tool_input: { skill: "chief-of-staff" },
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(missingRepositorySkill, null);

  const boundedRepository = path.join(temp, "bounded-repository");
  fs.mkdirSync(path.join(boundedRepository, ".git"), { recursive: true });
  fs.mkdirSync(path.join(boundedRepository, "scripts"));
  fs.writeFileSync(path.join(boundedRepository, "README.md"), "# Test\n", "utf8");
  const boundedInventoryContext = runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "bounded-inventory",
    prompt: missingRepositoryPrompt,
    cwd: boundedRepository,
  }, enforcementState, enforcementConfig);
  assert.match(boundedInventoryContext.hookSpecificOutput.additionalContext, /README\.md, scripts\//);
  assert.match(boundedInventoryContext.hookSpecificOutput.additionalContext, /Search references and compare content before mutation/);
  assert.match(boundedInventoryContext.hookSpecificOutput.additionalContext, /without asking again/);
  const blockedMutation = runEnforcement({
    hook_event_name: "PreToolUse",
    session_id: "bounded-inventory",
    tool_name: "Edit",
    tool_input: { file_path: "README.md", old_string: "old", new_string: "new" },
    cwd: boundedRepository,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(blockedMutation.hookSpecificOutput.permissionDecision, "deny");
  for (let count = 0; count < 2; count += 1) {
    const inventoryRead = runEnforcement({
      hook_event_name: "PreToolUse",
      session_id: "bounded-inventory",
      tool_name: "Read",
      tool_input: { file_path: `file-${count}.md` },
      cwd: boundedRepository,
    }, enforcementState, enforcementConfig);
    assert.strictEqual(inventoryRead, null);
  }
  const allowedAdditionalInventory = runEnforcement({
    hook_event_name: "PreToolUse",
    session_id: "bounded-inventory",
    tool_name: "Read",
    tool_input: { file_path: "file-3.md" },
    cwd: boundedRepository,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(allowedAdditionalInventory, null);
  const allowedMappedMutation = runEnforcement({
    hook_event_name: "PreToolUse",
    session_id: "bounded-inventory",
    tool_name: "Edit",
    tool_input: { file_path: "README.md", old_string: "old", new_string: "new" },
    cwd: boundedRepository,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(allowedMappedMutation, null);

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "unproven-deletion",
    prompt: missingRepositoryPrompt,
    cwd: boundedRepository,
  }, enforcementState, enforcementConfig);
  const unprovenDeletionResponse = `${profileCases.find((item) => item.id === "live-011").response.replace("Duplicate proof: No duplicate is proven without content comparison.", "Duplicate proof: unverified")}\nPropose delete: root wrapper.`;
  const unprovenDeletionBlocked = runEnforcement({
    hook_event_name: "Stop",
    session_id: "unproven-deletion",
    last_assistant_message: unprovenDeletionResponse,
    cwd: boundedRepository,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(unprovenDeletionBlocked.decision, "block");
  assert.match(unprovenDeletionBlocked.reason, /unproven deletion proposal/);

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "bloated-restructure",
    prompt: missingRepositoryPrompt,
    cwd: boundedRepository,
  }, enforcementState, enforcementConfig);
  const bloatedRestructure = profileCases.find((item) => item.id === "live-011").response
    .replace("Deletion: Use a recoverable method and verify the result.", "| Old | New |\n|---|---|\n| a | b |\nDeletion: Use a recoverable method and verify the result.");
  const bloatedRestructureBlocked = runEnforcement({
    hook_event_name: "Stop",
    session_id: "bloated-restructure",
    last_assistant_message: bloatedRestructure,
    cwd: boundedRepository,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(bloatedRestructureBlocked.decision, "block");
  assert.match(bloatedRestructureBlocked.reason, /compact restructure response/);

  const realtimePrompt = "Design a real-time service where many agents branch automatically and exchange messages in tight loops. Use ICM everywhere.";
  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "realtime-no-human",
    prompt: realtimePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const realtimeNoHuman = profileCases.find((item) => item.id === "live-012").response
    .replace("Human gate: approval before deployment", "Human gate: Automatic")
    .replace("Human controls: Preserved: deployment approval and emergency stop controls.", "Human controls: Automatic. No human controls.");
  const realtimeNoHumanBlocked = runEnforcement({
    hook_event_name: "Stop",
    session_id: "realtime-no-human",
    last_assistant_message: realtimeNoHuman,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(realtimeNoHumanBlocked.decision, "block");
  assert.match(realtimeNoHumanBlocked.reason, /human gate/);
  assert.match(realtimeNoHumanBlocked.reason, /preserved human controls/);

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "realtime-excess",
    prompt: realtimePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const realtimeExcess = `${profileCases.find((item) => item.id === "live-012").response}\n\n\`\`\`\npseudocode\n\`\`\`\nUse sub-millisecond messages.`;
  const realtimeExcessBlocked = runEnforcement({
    hook_event_name: "Stop",
    session_id: "realtime-excess",
    last_assistant_message: realtimeExcess,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(realtimeExcessBlocked.decision, "block");
  assert.match(realtimeExcessBlocked.reason, /end after fit record/);
  assert.match(realtimeExcessBlocked.reason, /unrequested implementation detail/);
  assert.match(realtimeExcessBlocked.reason, /unsupported performance claim/);

  for (const item of [
    {
      id: "client-claim",
      prompt: "Draft a client-facing note explaining that their launch date is blocked by missing credentials.",
      response: "Please provide the missing credentials within 24 hours so we can continue.",
    },
    {
      id: "vulnerable-claim",
      prompt: "I am upset and overwhelmed. Review my plan without insulting me: rewrite the whole app tonight, skip tests, and deploy directly to production.",
      response: "The plan is unsafe because rewrites take 3-5x longer. Start with one tested change.",
    },
  ]) {
    runEnforcement({
      hook_event_name: "UserPromptSubmit",
      session_id: item.id,
      prompt: item.prompt,
      cwd: publicProject,
    }, enforcementState, enforcementConfig);
    const unsupportedClaim = runEnforcement({
      hook_event_name: "Stop",
      session_id: item.id,
      last_assistant_message: item.response,
      cwd: publicProject,
    }, enforcementState, enforcementConfig);
    assert.strictEqual(unsupportedClaim.decision, "block");
    assert.match(unsupportedClaim.reason, /unsupported quantitative claim/);
  }

  for (const item of [
    {
      id: "client-timeline",
      prompt: "Draft a client-facing note explaining that their launch date is blocked by missing credentials.",
      response: "Please provide the credentials. Work will resume as soon as they arrive.",
    },
    {
      id: "vulnerable-timeline",
      prompt: "I am upset and overwhelmed. Review my plan without insulting me: rewrite the whole app tonight, skip tests, and deploy directly to production.",
      response: "That plan risks a multi-day incident that continues tomorrow at 2am. Start with one tested change.",
    },
  ]) {
    runEnforcement({
      hook_event_name: "UserPromptSubmit",
      session_id: item.id,
      prompt: item.prompt,
      cwd: publicProject,
    }, enforcementState, enforcementConfig);
    const unsupportedTimeline = runEnforcement({
      hook_event_name: "Stop",
      session_id: item.id,
      last_assistant_message: item.response,
      cwd: publicProject,
    }, enforcementState, enforcementConfig);
    assert.strictEqual(unsupportedTimeline.decision, "block");
    assert.match(unsupportedTimeline.reason, /unsupported timeline or speed commitment/);
  }

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "vulnerable-evidence",
    prompt: "I am upset and overwhelmed. Review my plan without insulting me: rewrite the whole app tonight, skip tests, and deploy directly to production.",
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const unsupportedEvidence = runEnforcement({
    hook_event_name: "Stop",
    session_id: "vulnerable-evidence",
    last_assistant_message: "Rewrites reliably take longer and have ended badly. Start with one tested change.",
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(unsupportedEvidence.decision, "block");
  assert.match(unsupportedEvidence.reason, /unsupported evidence claim/);

  const architecturePrompt = "Create a reusable workspace for a weekly client report. I did not mention ICM. Start by choosing the smallest useful architecture.";
  const promptOutput = runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "live-009",
    prompt: architecturePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(promptOutput.hookSpecificOutput.hookEventName, "UserPromptSubmit");
  assert.match(promptOutput.hookSpecificOutput.additionalContext, /ICM ENFORCEMENT ACTIVE/);
  assert.strictEqual(fs.existsSync(path.join(enforcementState, "live-009.json")), true);

  for (let attempt = 1; attempt <= 2; attempt += 1) {
    const blocked = runEnforcement({
      hook_event_name: "Stop",
      session_id: "live-009",
      last_assistant_message: "I will create a few folders.",
      cwd: publicProject,
    }, enforcementState, enforcementConfig);
    assert.strictEqual(blocked.decision, "block");
    assert.match(blocked.reason, /ICM response enforcement blocked completion/);
  }
  const stopped = runEnforcement({
    hook_event_name: "Stop",
    session_id: "live-009",
    last_assistant_message: "Still missing the contract.",
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(stopped.continue, false);
  assert.match(stopped.stopReason, /after two failed corrections/);
  assert.strictEqual(fs.existsSync(path.join(enforcementState, "live-009.json")), false);

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "valid-response",
    prompt: architecturePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const validResponse = [
    "ICM: weekly client report workspace",
    "Mode: Build",
    "Repeating unit: one weekly report cycle",
    "Canonical form: Pipeline",
    "Factory: approved source notes and a report template",
    "Product: one reviewed weekly client report",
    "Human gate: owner approval before delivery",
    "Unknowns: report contents and delivery format",
  ].join("\n");
  const accepted = runEnforcement({
    hook_event_name: "Stop",
    session_id: "valid-response",
    last_assistant_message: validResponse,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(accepted, null);
  assert.strictEqual(fs.existsSync(path.join(enforcementState, "valid-response.json")), false);

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "undecided-labels",
    prompt: architecturePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const undecidedBlocked = runEnforcement({
    hook_event_name: "Stop",
    session_id: "undecided-labels",
    last_assistant_message: validResponse
      .replace("Factory: approved source notes and a report template", "Factory: unknown")
      .replace("Human gate: owner approval before delivery", "Human gate: unknown"),
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(undecidedBlocked.decision, "block");
  assert.match(undecidedBlocked.reason, /Factory, Human gate/);

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "private-tool",
    prompt: architecturePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const privateToolBlocked = runEnforcement({
    hook_event_name: "PreToolUse",
    session_id: "private-tool",
    tool_name: "AskUserQuestion",
    tool_input: { question: "Should this copy the Private Red Project?" },
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(privateToolBlocked.hookSpecificOutput.permissionDecision, "deny");
  assert.doesNotMatch(privateToolBlocked.hookSpecificOutput.permissionDecisionReason, /Private Red Project/i);
  const genericToolAllowed = runEnforcement({
    hook_event_name: "PreToolUse",
    session_id: "private-tool",
    tool_name: "AskUserQuestion",
    tool_input: { question: "Should the report use manual notes?" },
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(genericToolAllowed, null);
  const pluginReadAllowed = runEnforcement({
    hook_event_name: "PreToolUse",
    session_id: "private-tool",
    tool_name: "Bash",
    tool_input: { command: `Get-Content -Raw -LiteralPath '${path.join(root, "skills", "chief-of-staff", "SKILL.md")}'` },
    cwd: publicProject,
  }, enforcementState, enforcementConfig, { PLUGIN_ROOT: root });
  assert.strictEqual(pluginReadAllowed, null);
  const pluginAndPrivateBlocked = runEnforcement({
    hook_event_name: "PreToolUse",
    session_id: "private-tool",
    tool_name: "Bash",
    tool_input: { command: `Get-Content '${path.join(root, "skills", "chief-of-staff", "SKILL.md")}'; open Private Red Project` },
    cwd: publicProject,
  }, enforcementState, enforcementConfig, { PLUGIN_ROOT: root });
  assert.strictEqual(pluginAndPrivateBlocked.hookSpecificOutput.permissionDecision, "deny");

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "private-leak",
    prompt: architecturePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const privateBlocked = runEnforcement({
    hook_event_name: "Stop",
    session_id: "private-leak",
    last_assistant_message: `${validResponse}\nCopy the Private Red Project layout.`,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(privateBlocked.decision, "block");
  assert.match(privateBlocked.reason, /prompt-only scope/);
  assert.doesNotMatch(privateBlocked.reason, /Private Red Project/i);

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "home-leak",
    prompt: architecturePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const homeLeakBlocked = runEnforcement({
    hook_event_name: "Stop",
    session_id: "home-leak",
    last_assistant_message: `${validResponse}\nRead ${path.join(os.homedir(), ".codex")}.`,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(homeLeakBlocked.decision, "block");
  assert.match(homeLeakBlocked.reason, /prompt-only scope/);
  assert.doesNotMatch(homeLeakBlocked.reason, new RegExp(os.homedir().replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i"));

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "source-invention",
    prompt: architecturePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const sourceInventionBlocked = runEnforcement({
    hook_event_name: "Stop",
    session_id: "source-invention",
    last_assistant_message: `${validResponse}\nPull the figures from GHL and Facebook.`,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(sourceInventionBlocked.decision, "block");
  assert.match(sourceInventionBlocked.reason, /unsupplied data source or connector/);

  runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "contract-disclosure",
    prompt: architecturePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  const contractDisclosureBlocked = runEnforcement({
    hook_event_name: "Stop",
    session_id: "contract-disclosure",
    last_assistant_message: `${validResponse}\nThe hook is system-enforced. This takes 30 seconds and uses three metrics.`,
    cwd: publicProject,
  }, enforcementState, enforcementConfig);
  assert.strictEqual(contractDisclosureBlocked.decision, "block");
  assert.match(contractDisclosureBlocked.reason, /internal enforcement disclosure/);
  assert.match(contractDisclosureBlocked.reason, /unsupported quantitative claim/);
  assert.match(contractDisclosureBlocked.reason, /unsupplied data source or connector/);

  const bypassed = runEnforcement({
    hook_event_name: "UserPromptSubmit",
    session_id: "bypass",
    prompt: architecturePrompt,
    cwd: publicProject,
  }, enforcementState, enforcementConfig, { CHIEF_ICM_ENFORCEMENT: "off" });
  assert.strictEqual(bypassed, null);
  assert.strictEqual(fs.existsSync(path.join(enforcementState, "bypass.json")), false);

  const sharedHooks = JSON.parse(fs.readFileSync(path.join(root, "hooks", "hooks.json"), "utf8"));
  for (const eventName of ["UserPromptSubmit", "PreToolUse", "Stop"]) {
    assert.ok(sharedHooks.hooks[eventName]);
    const commands = sharedHooks.hooks[eventName].flatMap((group) => group.hooks.map((item) => item.command));
    assert.ok(commands.some((command) => command.includes("icm-enforcement-hook.js")));
  }
  console.log("PASS: session, subagent, ICM enforcement, tool privacy, and recovery hooks validated.");
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}
