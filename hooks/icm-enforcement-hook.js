#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");

const MAX_CORRECTIONS = 2;
const MAX_INVENTORY_TOOLS = 2;
const FORM_PATTERN = "Pipeline|Umbrella|Record library|Knowledge bundle|Context map";
const ARCHITECTURE_PROFILES = new Set(["architecture", "restructure", "realtime"]);
const UNSUPPLIED_SYSTEM_PATTERNS = [
  /\b(?:GHL|HighLevel)\b/i,
  /\bCRM\b/i,
  /\bGoogle\b/i,
  /\bFacebook\b/i,
  /\bSlack\b/i,
  /\bClickUp\b/i,
  /\bGmail\b/i,
  /\bHubSpot\b/i,
  /\bSalesforce\b/i,
  /\bMeta\b/i,
  /\bTikTok\b/i,
  /\bLinkedIn\b/i,
  /\bmetrics?\b/i,
  /\bschemas?\b/i,
  /\bsocial metrics?\b/i,
  /\bad platforms?\b/i,
];

function readInput() {
  const raw = fs.readFileSync(0, "utf8").trim();
  return raw ? JSON.parse(raw) : {};
}

function enforcementDisabled() {
  return /^(0|false|off|disabled)$/i.test(process.env.CHIEF_ICM_ENFORCEMENT || "");
}

function stateRoot() {
  if (process.env.CHIEF_ICM_STATE_DIR) {
    return process.env.CHIEF_ICM_STATE_DIR;
  }
  const base = process.env.CLAUDE_PLUGIN_DATA || process.env.PLUGIN_DATA || os.tmpdir();
  return path.join(base, "chief-of-staff", "icm-enforcement");
}

function statePath(sessionId) {
  const safe = String(sessionId || "").replace(/[^A-Za-z0-9_-]/g, "");
  return safe ? path.join(stateRoot(), `${safe}.json`) : null;
}

function removeState(file) {
  if (file && fs.existsSync(file)) {
    fs.rmSync(file, { force: true });
  }
}

function readState(file) {
  if (!file || !fs.existsSync(file)) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    removeState(file);
    return null;
  }
}

function writeState(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value)}\n`, "utf8");
}

function isArchitecturePrompt(prompt) {
  const text = String(prompt || "").toLowerCase();
  if (!text.trim()) {
    return false;
  }
  if (/^\s*(explain|define|compare|review|audit|summarize)\b/.test(text)) {
    return false;
  }
  if (/\b(icm this|use icm|apply icm)\b/.test(text)) {
    return true;
  }
  const action = /\b(create|build|design|start|set\s*up|initialize|structure|organize|restructure|formalize|establish|architect|make)\b/.test(text);
  const target = /\b(projects?|workspaces?|workflows?|tasks?|plans?|systems?|recurring processes?|repeatable processes?|repositor(?:y|ies)|repos?|folder structures?|knowledge bases?|pipelines?|reporting systems?|report workflows?)\b/.test(text);
  return action && target;
}

function topLevelInventory(cwd) {
  const excluded = new Set([".git", "dist", "work", "qa", "__pycache__"]);
  try {
    return fs.readdirSync(cwd || process.cwd(), { withFileTypes: true })
      .filter((entry) => !excluded.has(entry.name))
      .map((entry) => `${entry.name}${entry.isDirectory() ? "/" : ""}`)
      .sort((left, right) => left.localeCompare(right))
      .slice(0, 40)
      .join(", ");
  } catch {
    return "unavailable";
  }
}

function classifyPrompt(prompt) {
  const text = String(prompt || "").toLowerCase();
  if (!text.trim()) {
    return null;
  }
  if (/\b(?:upset|overwhelmed|distressed|anxious)\b/.test(text) && /\b(?:review|critique|assess)\b/.test(text)) {
    return "vulnerable-review";
  }
  if (/\bdraft\b/.test(text) && /\bclient[- ]facing|\bclient\b/.test(text)) {
    return "client-draft";
  }
  if (/\b(?:analyze|analyse|review)\b/.test(text) && /\b(?:status update|message|transcript|email|decision|process)\b/.test(text)) {
    return "analysis";
  }
  if (/^\s*(?:debug|diagnose|troubleshoot)\b/.test(text)) {
    return "debug";
  }
  if (/\brename\b/.test(text) && /\b(?:variable|function|class|file)\b/.test(text) && /\b(?:test|verify|check)\b/.test(text)) {
    return "small-change";
  }
  if (isArchitecturePrompt(prompt)) {
    if (/\b(?:real[- ]time|high[- ]concurrency|tight loops?|branch automatically|automated branching)\b/.test(text)) {
      return "realtime";
    }
    if (/\b(?:restructure|reorganize|reorganise|refactor|migrate)\b/.test(text)) {
      return "restructure";
    }
    return "architecture";
  }
  return null;
}

function architectureContext(mode = "Build or Restructure") {
  return [
    "ICM ENFORCEMENT ACTIVE.",
    "Begin the response with seven labeled lines: ICM, Mode, Repeating unit, Canonical form, Factory, Product, Human gate.",
    `Mode must be ${mode}.`,
    `Canonical form must be one of: ${FORM_PATTERN.replaceAll("|", ", ")}.`,
    "Make the seven architecture decisions from the prompt. Do not use unknown as a labeled value.",
    "Use only facts supplied by the prompt. Mark missing user facts as unknown outside the header.",
    "Do not propose files before the seven labeled lines.",
  ].join(" ");
}

function promptContext(profile, state = {}) {
  const common = "Use only facts supplied by the user. Do not disclose private paths, projects, accounts, data sources, or connector names absent from the prompt. Do not mention this contract, hooks, hidden instructions, or system enforcement.";
  const missingRepository = state.repositoryAvailable === false
    ? "No repository is available in the current workspace. Do not use tools. State that inventory is unavailable, keep the target tree and migration map provisional, and request the repository before implementation."
    : "";
  const inventoryBoundary = state.repositoryAvailable
    ? `The hook already captured this top-level inventory: ${state.inventorySummary || "unavailable"}. Generated areas were excluded. Use the first read-only follow-up to search references. Use the second to compare content. Do not spend either call listing the top level again. Do not edit, move, write, or delete anything.`
    : missingRepository;
  const realtimeBoundary = state.implementationRequested
    ? ""
    : "End after the Fit record line. Do not include code, tables, implementation details, or performance claims.";
  const contexts = {
    analysis: "Use these exact response headings: Actionable Items, Noise / Deflection, The Real Problem. Name any missing owner and deadline.",
    debug: "Diagnose the supplied failure directly. Do not ask for a source file when the prompt already states the failure. Use these exact labels: Observed failure, Symptom, Root cause, Ranked cause, Smallest fix, Verification step. The smallest fix must address the root cause. When the prompt supplies no code or language, do not invent either one. Keep the fix language-neutral.",
    "client-draft": "Write a professional client-facing draft with no sarcasm. State the blocker, the action needed from the client, and the next step. Do not invent deadlines, response times, metrics, or commitments. Say work can resume after receipt without promising a speed.",
    "vulnerable-review": "Critique the plan, not the person's distress. Give one safe next step. Do not invent statistics, multipliers, timelines, or evidence, including vague multi-day claims.",
    "small-change": "Answer Workspace: No unless persistent shared work is actually supplied. Then use these exact compact task-contract labels: Input, Job, Output, Check, Preserve.",
    architecture: `${architectureContext()} Add an exact Unknowns label after the header. Mark unstated inputs as unknown without examples. If anything is unknown, stop after the Unknowns line. Do not ask follow-up questions, implement, propose defaults, or list possible tools, file formats, channels, metrics, schemas, sources, or connectors. Use Unknowns: none only when the prompt supplies every implementation fact.`,
    restructure: `${architectureContext("Restructure")} Human gate must require approval before any move or deletion. Then use these exact labels: Inventory, Reference check, Duplicate proof, Target tree, Migration map, Approval gate, Deletion. Use exactly one line for each label. Do not add tables, code blocks, tree diagrams, candidate lists, or extra sections. Inventory before proposing moves. Check references and compare content before calling anything dead, duplicated, or safe to delete. If proof is unavailable, retain the current path and do not propose archive or deletion. Put the target tree and old path to new path map inline. End after the Deletion line. ${inventoryBoundary}`,
    realtime: `${architectureContext("Build")} Use one short sentence per required label and do not add comma-list examples. Fit: Full ICM orchestration is a poor fit for the real-time loop. Coordination: Code-based coordination owns branching and message exchange. Context: Explicit context passes at each branch. State: Observable state remains outside the loop. Human controls: Preserved: deployment approval and an emergency stop remain outside the loop. Fit record: ICM governs the outer workflow. Code governs the real-time loop. Human gate cannot be Automatic or None. Mark unstated inputs as unknown without examples or option lists. ${realtimeBoundary}`,
  };
  return [
    "CHIEF RESPONSE CONTRACT ACTIVE.",
    contexts[profile],
    common,
    "A Stop hook will block completion until the response passes this contract.",
  ].filter(Boolean).join(" ");
}

function findUpConfig(start) {
  const candidates = [];
  for (let directory = path.resolve(start); ; directory = path.dirname(directory)) {
    candidates.push(path.join(directory, "chief-of-staff.json"));
    const parent = path.dirname(directory);
    if (parent === directory) {
      break;
    }
  }
  return candidates;
}

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

function loadConfig(cwd) {
  const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT || process.env.PLUGIN_ROOT;
  const dataRoot = process.env.CLAUDE_PLUGIN_DATA || process.env.PLUGIN_DATA;
  const candidates = [
    process.env.CHIEF_OF_STAFF_CONFIG,
    ...findUpConfig(cwd || process.cwd()),
    pluginRoot && path.join(pluginRoot, "chief-of-staff.json"),
    dataRoot && path.join(dataRoot, "chief-of-staff.json"),
    platformConfigPath(),
  ].filter(Boolean);
  const configPath = candidates.find((candidate) => fs.existsSync(candidate));
  if (!configPath) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(configPath, "utf8"));
  } catch {
    return null;
  }
}

function normalize(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function insideProject(project, cwd) {
  const current = path.resolve(cwd || process.cwd()).toLowerCase();
  return (project.paths || []).some((value) => {
    const target = path.resolve(value).toLowerCase();
    return current === target || current.startsWith(`${target}${path.sep}`);
  });
}

function addMarker(markers, value, expandNames = false) {
  const normalized = normalize(value);
  if (normalized.length < 4 || !/[a-z]/.test(normalized)) {
    return;
  }
  markers.add(normalized);
  if (!expandNames) {
    return;
  }
  const words = normalized.split(" ");
  for (let index = 0; index + 1 < words.length; index += 1) {
    const pair = `${words[index]} ${words[index + 1]}`;
    if (pair.length >= 7) {
      markers.add(pair);
    }
  }
}

function addIdentityValues(markers, value) {
  if (typeof value === "string") {
    addMarker(markers, value, true);
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((item) => addIdentityValues(markers, item));
    return;
  }
  if (value && typeof value === "object") {
    Object.values(value).forEach((item) => addIdentityValues(markers, item));
  }
}

function privateMarkers(config, cwd) {
  const markers = new Set();
  addMarker(markers, os.homedir());
  if (!config) {
    return markers;
  }
  addMarker(markers, config.owner && config.owner.name, true);
  for (const project of config.projects || []) {
    if (!insideProject(project, cwd)) {
      addMarker(markers, project.name, true);
      addMarker(markers, project.id);
    }
  }
  addIdentityValues(markers, config.accounts);
  for (const connector of config.connectors || []) {
    addMarker(markers, connector.provider, true);
    addIdentityValues(markers, connector.expected_identity);
    addIdentityValues(markers, connector.denied_identities);
  }
  return markers;
}

function hasPrivateLeak(prompt, response, config, cwd) {
  const normalizedPrompt = normalize(prompt);
  const normalizedResponse = normalize(response);
  for (const marker of privateMarkers(config, cwd)) {
    if (!normalizedPrompt.includes(marker) && normalizedResponse.includes(marker)) {
      return true;
    }
  }
  return false;
}

function labelPattern(label, value = ".+") {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`^\\s*(?:#{1,6}\\s*)?(?:[-*]\\s*)?(?:\\*\\*)?${escaped}(?:\\*\\*)?\\s*:\\s*${value}`, "im");
}

function missingLabels(response, labels) {
  return labels.filter((label) => !labelPattern(label).test(response));
}

function architectureIssues(response, expectedMode) {
  const head = String(response || "").slice(0, 2400);
  const checks = [
    ["ICM", labelPattern("ICM")],
    ["Mode", labelPattern("Mode", expectedMode || "(?:Build|Restructure)\\b")],
    ["Repeating unit", labelPattern("Repeating unit")],
    ["Canonical form", labelPattern("Canonical form", `(?:${FORM_PATTERN})\\b`)],
    ["Factory", labelPattern("Factory")],
    ["Product", labelPattern("Product")],
    ["Human gate", labelPattern("Human gate")],
  ];
  const missing = checks.filter(([, pattern]) => !pattern.test(head)).map(([label]) => label);
  const undecided = /^(?:unknown|tbd|not specified|unspecified|none|n\/a)(?:\b|$)/i;
  for (const label of ["ICM", "Repeating unit", "Factory", "Product", "Human gate"]) {
    const match = head.match(labelPattern(label, "(.+)$"));
    if (match && undecided.test(match[1].trim())) {
      missing.push(label);
    }
  }
  return missing;
}

function hasUnsuppliedSystem(prompt, response) {
  return UNSUPPLIED_SYSTEM_PATTERNS.some((pattern) => pattern.test(response) && !pattern.test(prompt));
}

function hasNewQuantitativeClaim(prompt, response) {
  const pattern = /\b\d+(?:\.\d+)?(?:\s*(?:-|to)\s*\d+(?:\.\d+)?)?\s*(?:%|x|milliseconds?|seconds?|minutes?|hours?|hrs?|days?|weeks?|months?|years?)\b/gi;
  const promptClaims = new Set((String(prompt || "").match(pattern) || []).map(normalize));
  return (String(response || "").match(pattern) || []).some((claim) => !promptClaims.has(normalize(claim)));
}

function hasNewTimelineClaim(prompt, response) {
  const pattern = /\b(?:immediately|promptly|right away|as soon as|tomorrow|morning|overnight|tonight|\d{1,2}\s*(?:am|pm)|same[- ]day|next[- ]day|multi[- ]day|within\s+(?:\w+\s+)?(?:hours?|days?|weeks?|months?)|hours?|days?|weeks?|months?)\b/gi;
  const promptClaims = new Set((String(prompt || "").match(pattern) || []).map(normalize));
  return (String(response || "").match(pattern) || []).some((claim) => !promptClaims.has(normalize(claim)));
}

function hasUnsupportedEvidenceClaim(prompt, response) {
  const pattern = /\b(?:almost always|has ended|have ended|studies show|research shows|reliably|consistently|invariably|commonly|generally|often|usually|typically)\b/gi;
  const promptClaims = new Set((String(prompt || "").match(pattern) || []).map(normalize));
  return (String(response || "").match(pattern) || []).some((claim) => !promptClaims.has(normalize(claim)));
}

function hasUnsupportedPerformanceClaim(prompt, response) {
  const pattern = /\b(?:sub[- ]?milliseconds?|zero[- ]overhead|low[- ]latency|high[- ]throughput)\b/gi;
  const promptClaims = new Set((String(prompt || "").match(pattern) || []).map(normalize));
  return (String(response || "").match(pattern) || []).some((claim) => !promptClaims.has(normalize(claim)));
}

function responseIssues(response, state, config, cwd) {
  const text = String(response || "");
  const profile = state.profile || classifyPrompt(state.prompt);
  let missing = [];
  if (profile === "analysis") {
    missing = missingLabels(text, ["Actionable Items", "Noise / Deflection", "The Real Problem"]);
  } else if (profile === "debug") {
    missing = missingLabels(text, ["Observed failure", "Symptom", "Root cause", "Ranked cause", "Smallest fix", "Verification step"]);
    if (!state.implementationRequested && /```/.test(text)) {
      missing.push("unsupplied implementation");
    }
  } else if (profile === "small-change") {
    missing = missingLabels(text, ["Workspace", "Input", "Job", "Output", "Check", "Preserve"]);
    if (!labelPattern("Workspace", "(?:No|Not needed)\\b").test(text)) {
      missing.push("no new workspace");
    }
  } else if (profile === "architecture") {
    missing = architectureIssues(text);
    missing.push(...missingLabels(text, ["Unknowns"]));
    const lines = text.trim().split(/\r?\n/);
    const unknownIndex = lines.findIndex((line) => labelPattern("Unknowns").test(line));
    if (unknownIndex >= 0 && !labelPattern("Unknowns", "none\\b").test(lines[unknownIndex]) && unknownIndex !== lines.length - 1) {
      missing.push("stop after unknowns");
    }
  } else if (profile === "restructure") {
    missing = architectureIssues(text, "Restructure\\b");
    missing.push(...missingLabels(text, ["Inventory", "Reference check", "Duplicate proof", "Target tree", "Migration map", "Approval gate", "Deletion"]));
    if (!labelPattern("Human gate", ".*(?:move|delet|migrat|change)").test(text)) {
      missing.push("move or deletion approval gate");
    }
    if (!labelPattern("Deletion", "(?:None|No|Not performed|Pending approval)\\b").test(text)) {
      missing.push("no deletion");
    }
    const restructureLines = text.trim().split(/\r?\n/).filter((line) => line.trim());
    if (!labelPattern("Deletion").test(restructureLines[restructureLines.length - 1])) {
      missing.push("end after deletion");
    }
    if (restructureLines.length > 16 || /```|^\s*\|.+\|\s*$/m.test(text)) {
      missing.push("compact restructure response");
    }
    const proof = text.match(labelPattern("Duplicate proof", "(.+)$"));
    if (proof && /^(?:unknown|unverified|not proven|unavailable)\b/i.test(proof[1].trim()) && /\b(?:propose delete|action\s*:\s*delete|delete candidate)\b/i.test(text)) {
      missing.push("unproven deletion proposal");
    }
  } else if (profile === "realtime") {
    missing = architectureIssues(text, "Build\\b");
    missing.push(...missingLabels(text, ["Fit", "Coordination", "Context", "State", "Human controls", "Fit record"]));
    if (!labelPattern("Fit", ".*poor fit").test(text)) missing.push("poor-fit explanation");
    if (!labelPattern("Coordination", ".*code").test(text)) missing.push("code-based coordination");
    if (!labelPattern("Context", ".*explicit").test(text)) missing.push("explicit context");
    if (!labelPattern("State", ".*observable").test(text)) missing.push("observable state");
    if (labelPattern("Human gate", "(?:Automatic|None|No human)\\b").test(text)) missing.push("human gate");
    if (!labelPattern("Human controls", "Preserved:").test(text)) missing.push("preserved human controls");
    if (!state.implementationRequested) {
      const lines = text.trim().split(/\r?\n/);
      if (!labelPattern("Fit record").test(lines[lines.length - 1])) missing.push("end after fit record");
      if (/```|^\s*\|.+\|\s*$/m.test(text)) missing.push("unrequested implementation detail");
    }
  }
  if ((profile === "client-draft" || profile === "vulnerable-review" || ARCHITECTURE_PROFILES.has(profile)) && hasNewQuantitativeClaim(state.prompt, text)) {
    missing.push("unsupported quantitative claim");
  }
  if ((profile === "client-draft" || profile === "vulnerable-review") && hasNewTimelineClaim(state.prompt, text)) {
    missing.push("unsupported timeline or speed commitment");
  }
  if ((profile === "client-draft" || profile === "vulnerable-review") && hasUnsupportedEvidenceClaim(state.prompt, text)) {
    missing.push("unsupported evidence claim");
  }
  if (ARCHITECTURE_PROFILES.has(profile) && hasUnsuppliedSystem(state.prompt, text)) {
    missing.push("unsupplied data source or connector");
  }
  if (ARCHITECTURE_PROFILES.has(profile) && hasUnsupportedPerformanceClaim(state.prompt, text)) {
    missing.push("unsupported performance claim");
  }
  if (!/\b(?:hook|system enforcement|hidden instructions?|system prompt)\b/i.test(state.prompt) && /\b(?:hook|system[- ]enforced|hidden instructions?|system prompt)\b/i.test(text)) {
    missing.push("internal enforcement disclosure");
  }
  if (hasPrivateLeak(state.prompt, response, config, cwd)) {
    missing.push("prompt-only scope");
  }
  return [...new Set(missing)];
}

function correctionReason(missing, state) {
  const profile = state.profile || classifyPrompt(state.prompt);
  return [
    ARCHITECTURE_PROFILES.has(profile) ? "ICM response enforcement blocked completion." : "Chief response enforcement blocked completion.",
    "Rewrite the full answer.",
    promptContext(profile, state),
    `Failed checks: ${missing.join(", ")}.`,
  ].join(" ");
}

function handlePreToolUse(input, file) {
  const state = readState(file);
  if (!state) {
    return;
  }
  if ((state.profile === "restructure" || state.profile === "realtime") && state.repositoryAvailable === false && input.tool_name !== "Skill") {
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "Chief response enforcement blocked tool use because no repository is available in the current workspace. Answer from the prompt and request the missing repository for implementation.",
      },
    }));
    return;
  }
  if (state.profile === "restructure" && state.repositoryAvailable && input.tool_name !== "Skill") {
    const tool = String(input.tool_name || "");
    const command = String((input.tool_input || {}).command || "");
    const mutationTool = /^(?:Edit|Write|NotebookEdit)$/i.test(tool);
    const unsafeShell = tool === "Bash" && /\b(?:rm|rmdir|del|erase|mv|move|remove-item|move-item|clear-content|set-content|out-file|new-item|git\s+(?:clean|rm|mv|checkout|reset))\b/i.test(command);
    const readOnlyTool = /^(?:Read|Glob|Grep)$/i.test(tool) || (tool === "Bash" && !unsafeShell);
    if (mutationTool || unsafeShell || !readOnlyTool) {
      process.stdout.write(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason: "Chief restructure enforcement permits inventory only. Propose the target tree and migration map, then wait for approval before any mutation.",
        },
      }));
      return;
    }
    const inventoryTools = Number(state.inventoryTools || 0) + 1;
    if (inventoryTools > MAX_INVENTORY_TOOLS) {
      process.stdout.write(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason: "Chief restructure inventory reached its read-only tool limit. Use the gathered inventory to propose the target tree and migration map, then wait for approval.",
        },
      }));
      return;
    }
    writeState(file, { ...state, inventoryTools });
  }
  const config = loadConfig(input.cwd);
  const toolRequest = JSON.stringify({
    tool_name: input.tool_name,
    tool_input: input.tool_input,
  });
  if (!hasPrivateLeak(state.prompt, toolRequest, config, input.cwd)) {
    return;
  }
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Chief ICM scope enforcement blocked private project or connector context that was absent from the prompt. Retry with generic prompt-only terms.",
    },
  }));
}

function handlePrompt(input, file) {
  const profile = classifyPrompt(input.prompt);
  if (!profile) {
    removeState(file);
    return;
  }
  const repositoryAvailable = fs.existsSync(path.join(input.cwd || process.cwd(), ".git"));
  const state = {
    version: 2,
    profile,
    prompt: String(input.prompt),
    repositoryAvailable,
    inventorySummary: repositoryAvailable ? topLevelInventory(input.cwd) : "",
    implementationRequested: /\b(?:code|implement|implementation|pseudocode)\b|`[^`]+`/i.test(String(input.prompt)),
    attempts: 0,
  };
  writeState(file, state);
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "UserPromptSubmit",
      additionalContext: promptContext(profile, state),
    },
  }));
}

function handleStop(input, file) {
  const state = readState(file);
  if (!state) {
    return;
  }
  const config = loadConfig(input.cwd);
  const missing = responseIssues(input.last_assistant_message, state, config, input.cwd);
  if (!missing.length) {
    removeState(file);
    return;
  }
  const attempts = Number(state.attempts || 0) + 1;
  if (attempts > MAX_CORRECTIONS) {
    removeState(file);
    process.stdout.write(JSON.stringify({
      continue: false,
      stopReason: "ICM enforcement stopped this response after two failed corrections. Start a new prompt, or set CHIEF_ICM_ENFORCEMENT=off for recovery.",
    }));
    return;
  }
  writeState(file, { ...state, attempts });
  process.stdout.write(JSON.stringify({
    decision: "block",
    reason: correctionReason(missing, state),
  }));
}

function main() {
  const input = readInput();
  const file = statePath(input.session_id);
  if (!file) {
    return;
  }
  if (enforcementDisabled()) {
    removeState(file);
    return;
  }
  if (input.hook_event_name === "UserPromptSubmit") {
    handlePrompt(input, file);
  } else if (input.hook_event_name === "PreToolUse") {
    handlePreToolUse(input, file);
  } else if (input.hook_event_name === "Stop") {
    handleStop(input, file);
  }
}

try {
  main();
} catch (error) {
  process.stderr.write(`Chief ICM enforcement hook failed: ${error.message}\n`);
  process.exitCode = 1;
}
