# ICM conformance

Chief of Staff v2.1.1 retains the v2.1.0 Interpretable Context Methodology as its default
operating architecture. The compact task contract applies to every non-trivial
task. Full workspace files appear only when the work needs persistent structure.

## Source contract

Use sources in this order:

1. Van Clief and McDermott, arXiv:2603.16021, for method intent.
2. `RinDig/icm-architect` at the commit recorded in
   `skills/chief-of-staff/internal/icm-architect/UPSTREAM.json` for Chief's
   internal build and restructure workflow.
3. Chief rules for Codex routing, scope, privacy, approval, validation, and
   release behavior.

The vendored skill retains its MIT license. Chief additions do not weaken the
source method or claim that proposed research features are complete.

## Method mapping

| ICM requirement | Chief implementation | Evidence |
|---|---|---|
| One stage or folder, one job | Task kernel and stage contracts | `scripts/validate_icm.py` |
| Plain text interface | Markdown, JSON, YAML, and file paths | Repository scan |
| Layered context loading | Exact task inputs and selective skill references | Persona contract and ICM tests |
| Every output is an edit surface | Named output plus human check | Contract validation |
| Configure factory, not product | `skills/`, `persona/`, `docs/` apart from `dist/` and `qa/` | Root `CONTEXT.md` |
| Layer 0 identity | Root `AGENTS.md` | Entry validation |
| Layer 1 routing | Root `CONTEXT.md` | Line and route checks |
| Layer 2 control point | Folder `CONTEXT.md` contracts | Required heading checks |
| Layer 3 references | Named stable source files | Exact input paths |
| Layer 4 working artifacts | Source edits, stage outputs, `dist/`, and `qa/` | Release contracts |
| Human review gates | Contract checks and Chief approval policy | Static and live scenarios |
| Cold-agent navigation | Entry file plus no more than two reads | Workspace fixture test |
| Typical 2,000 to 8,000 tokens | Budget estimator and measured live tasks | ICM tests and acceptance evidence |

## Chief extensions

- Apply a compact ICM task contract to all non-trivial work.
- Invoke ICM Architect automatically for each new project or workspace. Apply
  it to recurring processes too.
- On Codex, enforce the seven-line architecture header through supported prompt
  and lifecycle hooks. Permit two correction cycles, then stop with a recovery path.
- Apply the prompt-only privacy boundary before each tool request and again at
  final response.
- Use `AGENTS.md` as the canonical Codex Layer 0 file.
- Require scope and privacy controls. Require migration and destructive-action
  controls. External-write and publication approvals remain human gates.
- Pin third-party source and license before bundling or executing it.

These are Chief controls built on ICM. They are not attributed to the paper.

## Materialization rule

Use a task contract without new folders for contained work. Create an ICM
workspace when work persists or repeats. Multi-step, shared and review-gated
work may need one too. Record the reason when full ICM is bypassed for real-time
agent coordination or high concurrency. Do the same for automated branching.

The rule keeps ICM universal as an operating test without violating its own
instruction to avoid irrelevant context and ceremonial scaffolding.

The deterministic hook is an enforcement boundary for architecture responses,
not a replacement for the compact task kernel. It does not create folders or
authorize external actions. Human approval remains the gate for material work.

## Research boundary

The paper discusses incremental recompilation and semantic provenance. It also
describes cross-stage verification and markdown breakpoints. Learning from
repeated edits is another future direction. v2.1.0 may use verified pieces, but it
does not claim those research directions as complete capabilities.
