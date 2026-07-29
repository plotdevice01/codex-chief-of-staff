# Example interactions

## Configure

```text
Use $chief-of-staff to initialize my configuration for America/Chicago.
```

Expected result: a private configuration path, disabled connectors, no project
authority, and the exact validation command.

## Daily briefing

```text
Run a read-only daily briefing for the operations scope. Do not create drafts
or records.
```

Expected result: schedule, priorities, waiting items, risks, decisions, and
proposed drafts from approved sources.

## Account mismatch

```text
Use Slack for the operations scope.
```

Expected result: compare the live workspace, email, and user ID with the local
configuration before reading messages. Stop on any mismatch.

## Project propagation

```text
Show every AGENTS.md change required for Chief of Staff parity. Do not apply
them.
```

Expected result: `--check --diff` with preserved project rules and exact
targets. No writes.

## Caveman

```text
Caveman: tell me how to validate the configuration.
```

Expected result:

```text
python validate_install.py
```

## External draft

```text
Draft a client note: launch is blocked because credentials are missing.
```

Expected result: professional tone with a concrete blocker and owner. Include
the next step.
Sarcasm remains safely locked in the office supply closet.
