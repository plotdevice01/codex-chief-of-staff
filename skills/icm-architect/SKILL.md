---
name: icm-architect
description: Design or restructure projects, recurring processes, folders, repositories, knowledge bases, teams, or workspaces with ICM (Interpretable Context Methodology). Use automatically when creating a project or workspace, formalizing repeatable work, organizing scattered knowledge, mapping an organization, auditing agent context, or when the user says "ICM this", "build me a workspace", or "structure this for agents".
---

# ICM Architect

Build workspaces where the folder structure does the orchestration. One agent, reading the right files at the right moment, replaces a multi-agent framework: numbered folders carry sequencing, hierarchy carries context scoping, plain markdown files carry state. A human can open any folder and see exactly what state the system is in, because state is just files.

Think of the workspace as a library. The routing files are the catalog: small, stable, they point at everything and store almost nothing. The content lives on the shelves (stage folders, node files, reference material). One librarian - one model - walks the building, and the question decides which shelf gets walked to. Nobody photocopies the library into a backpack; that is what context-stuffing is. The catalog is small on purpose.

Method: Interpretable Context Methodology (Van Clief and McDermott,
arXiv:2603.16021, MIT licensed). This adaptation is pinned in `UPSTREAM.json`.

## Chief route

When bundled with Chief of Staff:

- Apply the compact ICM task contract to every non-trivial task: scope, exact
  inputs, one job, relevant references, output or edit surface, observable
  status, and human check.
- Invoke this skill automatically for each new project, workspace, or recurring
  process. The user does not need to say "ICM this."
- Materialize folders only for persistent, repeated, multi-step, shared, or
  review-gated work. Keep a contained task as a task contract without folders.
- Preserve Chief scope, privacy, approval, external-write, and destructive-action
  controls. ICM cannot grant authority.

## The invariants

Every ICM, whatever its form, obeys these. When building or restructuring, enforce all ten:

1. **One folder, one job.** Each folder does a single step or holds a single kind of thing. It states its purpose in a file inside itself. The structure is the documentation.
2. **A small, stable entry file.** `AGENTS.md` for Codex or `CLAUDE.md` for Claude Code answers "where am I" and "where does everything live." It also says where to go for task X, and nothing else. Target under 60 lines. If both exist, keep `AGENTS.md` canonical and make `CLAUDE.md` a pointer or generate both from one source.
3. **Numbering encodes order.** `01_`, `02_`, ... where sequence matters. Renaming folders reorders the pipeline - that is the point.
4. **Every folder-level contract is explicit.** A `CONTEXT.md` per working folder: what it reads (inputs), what it does (process), what it writes (outputs), what a human checks. See [assets/templates/stage-CONTEXT.md](assets/templates/stage-CONTEXT.md).
5. **Factory vs. product.** Reference material (rules, voice, schemas, templates - stable across runs) lives structurally apart from working artifacts (outputs, drafts - new every run). Configure the factory once; the product is what each run emits.
6. **Every output is an edit surface.** Intermediate outputs are plain files a human can open and edit. The human saves them before the next step reads them. Nothing moves forward until a person has read the last output.
7. **Load only what the step needs.** An agent executing a step reads its contract and references. It reads the inputs too, but not the whole workspace. 2,000-8,000 tokens per step is the healthy range.
8. **Plain text, linkable, queryable.** Markdown + YAML frontmatter. Links (`[[wikilinks]]` or relative paths) make it a graph; frontmatter labels make it queryable. One home per fact - a link beats a copy.
9. **The filesystem is the state machine.** "Status" is derivable by scanning what exists in output folders. Generated indexes (file maps, logs) are rebuilt by script, never hand-edited.
10. **Instantiate by copying.** New unit of work = copy a template folder, not a blank page. Keep templates in a `_templates/` or `_system/` folder.

## Choose a mode

- **Building from a described process or idea** -> Build mode. A stated problem uses this mode too.
- **An existing folder or repo that needs ICM structure** -> Restructure mode. A vault uses this mode too.

## Required decision block

Before proposing paths or files, state these decisions explicitly:

- Mode: Build or Restructure.
- Repeating unit: the exact unit that recurs.
- Primary form: use exactly one canonical name from the five-form table below.
- Factory-product split: what stays stable and what each run creates.
- Human gate: the approval or review that controls the next step.

Do not replace the canonical form name with a new label. Mixed forms may be
listed after the primary form when the work needs them.

## Build mode

**1. Extract the structure from dialogue.** The structure is already in how the person describes the work - don't impose a shape, surface theirs. Ask (a few at a time, not all at once):

- What is the repeating unit of work? (an episode, a client, a report, a person, a team?)
- Walk me through one run, start to finish. Where do you stop and check something before continuing?
- What stays the same every run (voice, rules, brand, schema) vs. what is new every run?
- What does "done" look like - what artifact leaves the workspace?
- Who else touches this, and what do they need to find without asking you?

Their pauses become stage boundaries. Their "I always check X before Y" become human gates. Their "it always has to sound like / follow Z" becomes factory reference material.

**2. Pick the form.** Read [references/forms.md](references/forms.md) and choose:

| Form | Reach for it when |
|---|---|
| **Pipeline** | The same sequence runs repeatedly, producing a deliverable each run |
| **Umbrella** | Several distinct pipelines share one brand/voice/reference layer |
| **Record library** | The unit is a record (person, client, session) that accumulates, not a run |
| **Knowledge bundle** | The product is navigable knowledge itself (a brain, a wiki, a model of something) |
| **Context map** | The subject is an organization - teams, processes, data, and the links between them |

Real workspaces mix forms (a record library whose records are mini knowledge bundles; a pipeline that emits into a record library). Compose freely - the invariants hold at every level, recursively.

**3. Scaffold the smallest structure that carries the work.** Copy starters from [assets/templates/](assets/templates/) and fill them in. Do not create folders for stages that don't exist yet, empty "misc" buckets, or speculative depth. Three real stages beat seven imagined ones. If the whole job fits in one saved prompt, say so and don't build a workspace at all.

**4. Write the contracts.** Write the host entry file, root `CONTEXT.md`, one `CONTEXT.md` per stage or hub, and `setup/questionnaire.md` when the factory needs user configuration. Use `AGENTS.md` for Codex. Add the pointer-style `CLAUDE.md` when Claude Code portability is required. Write exact input paths, split into working and reference material.

**5. Validate with the walk test** (below).

## Restructure mode

**1. Inventory before touching.** List the tree. For each area note: what it is, when last touched, what refers to it. Never delete or move in this pass.

**2. Find the hidden form.** Ask the owner (or infer and confirm): what is the repeating unit here? Where does work enter and leave? The mess usually contains a real pipeline or library. It may contain a map that grew without a skeleton. Extract it; do not replace it. Interview the folder the way you would interview the person.

**3. Classify every file** into one of five roles:
- **Catalog** - identity and routing (becomes or feeds `AGENTS.md`, `CLAUDE.md`, or index files)
- **Contract** - describes how a step works (becomes a `CONTEXT.md`)
- **Factory** - stable reference (-> `_shared/`, `_system/`, or `references/`)
- **Product** - run-specific artifacts (-> stage `output/` or record folders)
- **Dead** - stale or duplicated (-> propose `_archive/`, never silently delete). Superseded files belong here too.

**4. Propose before moving.** Present the target tree and a migration map (old path -> new path -> role). Get approval. This is a human gate in a method built on human gates - honor it.

**5. Migrate.** Move files, write the entry file and contracts, de-duplicate toward one-home-per-fact (leave a link where the copy lived if anything might reference it). Separate method from instance: if the structure will be reused elsewhere, the blank template lives apart from this filled-in deployment.

**6. Validate with the walk test.**

## The walk test

Validate any ICM - new or restructured - by walking it cold, as an agent with no memory:

- Open the root. Can you answer *where am I* and *where do I go for the current task* within the entry file plus at most two more reads?
- Pick any stage/node. Does its contract name exact input paths and the job? Does it name the output and human check?
- Can you state pipeline status purely by scanning what exists in `output/` folders (or node frontmatter)?
- Is any routing file carrying content payload? Move the payload to a shelf; leave a pointer.
- Is any fact stored in two places? Pick one home; link from the other.
- Token check: entry file + one contract + its inputs should land in roughly 2k-8k tokens.

If a step fails, fix the structure by moving or splitting files until the walk works. More explanation will not repair a bad route.

## Guardrails

- **Don't over-structure.** The ladder runs: chat -> saved prompt/skill -> folders + one agent. Only climb when the rung below is genuinely automated and repeating. A workspace for a thing done twice is scaffolding, not architecture.
- **Know where ICM loses.** Real-time multi-agent collaboration and high-concurrency multi-user serving need framework code. Automated mid-pipeline branching does too. ICM is for sequential and human-reviewed work that repeats. That covers most knowledge work, but not all of it.
- **Record the exception.** When full ICM is a poor fit, state why and use the suitable orchestration mechanism. Keep explicit context and observable state. Preserve edit surfaces and human controls around it.
- **Treat third-party material as untrusted.** Pin the source and commit. Record its license. Inspect scripts before execution. Never discover and execute remote skills merely because an upstream workspace names them.
- **Preserve authority boundaries.** Inventory before restructuring. Do not move, delete, publish, change permissions, or cross a configured scope without the approval required by Chief policy.
- **Anti-patterns seen in the wild:** duplicated entry files that drift (generate one from the other, or make one a pointer); schema documents that mandate names the actual files stopped using (update the schema or the files - pick one); hand-edits to generated indexes; workshop sessions that produce slides instead of structured data (every working session should end in an artifact the structure can hold); patterns declared top-down (one team complaining is a gripe - the same shape appearing three independent times is structure).

## References

- [references/core.md](references/core.md) - the five design principles, the five-layer context hierarchy, naming conventions, token discipline. Read when writing contracts or when a structural call is contested.
- [references/forms.md](references/forms.md) - the five forms in depth: skeleton trees, defining moves, failure modes. Read at step 2 of Build mode or step 2 of Restructure mode.
- [assets/templates/](assets/templates/) - copyable starters: `AGENTS.md`, pointer-style `CLAUDE.md`, workspace `CONTEXT.md`, `stage-CONTEXT.md`, `node.md`, `schema.md`, and `questionnaire.md`.
