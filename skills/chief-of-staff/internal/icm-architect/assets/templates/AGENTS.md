# {Workspace name}

{One sentence describing this workspace and its final output.}

This workspace uses ICM. Folders carry sequence, hierarchy scopes context, and
files carry state. Put each explanation in that folder's `CONTEXT.md`.

## Where things live

| Folder | Purpose |
|---|---|
| `stages/` | Pipeline stages in execution order |
| `_shared/` | Stable factory rules and references |
| `_templates/` | Blank starters copied for new work |
| `setup/` | One-time factory configuration |

## Route the task

| Current need | Read next | Stop when |
|---|---|---|
| Start a run | `stages/01_.../CONTEXT.md` | Human reads its output |
| Continue approved work | Next numbered stage contract | Human reads its output |
| Report status | `CONTEXT.md`, then `stages/*/output/` | Existing artifacts are reported |
| Configure a user | `setup/questionnaire.md` | Answers are written to `_shared/` |

Do not load the whole workspace. Read only the current contract, its named
references, and its working inputs. Nothing advances until the named human
check passes.
