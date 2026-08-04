# {{CLIENT_NAME}} brand voice pipeline

One job: build and operate {{CLIENT_NAME}}'s governed corporate voice.

## Route

| Need | Stage |
|---|---|
| Collect client answers and owner roles | `stages/01_intake/` |
| Inventory sources and claims | `stages/02_evidence/` |
| Define the corporate voice | `stages/03_voice/` |
| Build the full package | `stages/04_package/` |
| Write a requested copy asset | `stages/05_copy/` |
| Record QA and release status | `stages/06_release/` |

Stable rules live in `_shared/`. Blank edit surfaces live in `_templates/`. Each run lives in `runs/` and points to the adopted package version.

Current owner: {{OWNER}}
Created: {{CREATED_DATE}}
