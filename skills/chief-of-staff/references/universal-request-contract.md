# Universal request contract

Chief is the only discoverable skill. Apply this contract once to every
non-trivial request, then load only the internal capability contract selected
by the router. Never ask the user to choose a specialist.

## One-pass route

1. **Resolve scope and project.** Use the named project or current workspace.
   If neither establishes a client, stay generic. Client and project records
   are runtime inputs, never reusable skill content.
2. **Classify the task.** Run `scripts/route_request.py` once or apply the same
   capability registry directly when the classification is obvious. Choose one
   primary capability. Add a validator or host capability only when execution
   actually requires it.
3. **Select the contract.** Read only the returned internal contract paths.
   The `generic` fallback is valid for any task that does not need a specialist
   workflow. An unknown category is not a reason to fail.
4. **Verify inputs and authority.** Check required facts, source provenance,
   current permissions, named identities, evidence, and human gates before the
   first irreversible or external action. Treat the user's direct instruction,
   approved plan, approved goal, or full-access instruction as durable
   authorization for all actions plainly inside that scope.
5. **Execute.** Use the fewest tools that can finish the task reliably. Keep
   synthesis in Chief; use deterministic scripts for repeatable retrieval,
   validation, state, and receipts.
6. **Validate.** Check the complete output against the selected contract. Read
   external writes back. Do not convert a component pass into approval of the
   complete deliverable.
7. **Return.** Lead with the finished output or exact hold. For non-trivial
   operational work, end with numbered `Next steps` followed by `Execution
   trace`. Complete every safe authorized step before listing it and list only
   remaining actions or genuine external blockers. Never insert a closing
   summary before the trace. Append a compact execution receipt.

## Plan-scoped authorization

Do not request a new approval for each step of an approved plan. A plan that
includes writing or publishing authorizes the complete in-scope path, including
local edits, uploads, connector record batches, pushes, pull requests, merges,
tags, releases, deployments, and publication. Phrases such as `full access is
on`, `execute`, `finish the plan`, and `do not stop` confirm the same durable
authorization. The owner may steer, narrow, or revoke it while work is in
progress.

Read external state back after writes. If an authorized action fails, determine
whether it succeeded before retrying; an idempotent retry does not require new
approval. Do not confuse a review or acceptance check with permission to
perform the next already-authorized action.

Reconfirm only for a material scope expansion, a new external target or
recipient, an irreversible destructive action that was not included, or a
missing decision that could change the audience, offer, claim, legal position,
rights, payment, clinical treatment, publication, or target. A full-access
instruction does not provide missing credentials or override host and system
safeguards.

## Fail-closed boundaries

Stop with a specific hold when a missing fact could change the audience,
offer, claim, legal position, rights, payment, clinical treatment, publication,
or external target. Do not create a hold solely because an authorized plan has
reached publication, sending, media buying, permissions, destructive work, or
external record writes.

Do not fail closed merely because no specialist route exists. Use the generic
contract, preserve stated constraints, and validate the actual output.

## Receipt

Record:

- resolved scope;
- primary capability;
- internal contracts actually used;
- source and evidence checks;
- tools, apps, or MCP actions actually executed;
- validators and results;
- human gate or external-write authorization;
- final status and limitations.

Reading a contract is not material use. Report a capability as used only when
it changed the workflow, execution, validation, or output.
