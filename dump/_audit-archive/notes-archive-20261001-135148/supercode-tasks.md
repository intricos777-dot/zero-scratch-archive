<!-- Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work -->
# Supercode Task List (handoff from Lia.CLI sync, 2026-08-09)

Supervisor: lia-cli · Master plan: `~/Projects/lia-cli/tasks/active-plan.json` · Machine-readable: `supercode-tasks.json`
Work together with the hermes kanban board (`hermes kanban ls`) and opencode (`opencode-task-work`).

## 1. void-supercode-local — PRIORITY HIGH (do this first)
You are the local (Void) supercode. `supercode init` must start an interactive session using OUR version.

- `~/Projects/lia-cli/tasks/supercode-tasks.json` is your source of truth.
- Wrapper: `/home/sin/.hermes/scripts/supercode` (policy-gated via lin-antimalware bridge: python3 `from tools.bridge import request` → `supercode`/`integrity.read`).
- Config: `/home/sin/.config/supercode/{cli-config.json,settings.json}`.
- [ ] vs-1: Make the wrapper run our version so `supercode init` works
- [ ] vs-2: Fix lin-antimalware policy bridge authorization for `supercode` `integrity.read`
- [ ] vs-3: Verify `supercode init` starts an interactive session end to end

## 2. twilight-elysium — publish as own private repo
- [ ] te-1: Remove `engines/twilight-elysium` from `~/Projects/gaming-unified` (currently UNTRACKED, subtree deletion is safe; standalone copy exists at `~/Projects/twilight-elysium`)
- [ ] te-2: Publish `~/Projects/twilight-elysium` as its own PRIVATE GitHub repository

## 3. spacecraft-blueprint-simulator — continue GA pipeline
- [ ] sbs-1: Ingest real reference data instead of hardcoded lists
- [ ] sbs-2: Add convergence detection so GA stops early
- [ ] sbs-3: Generate Markdown design reports for best blueprints (target `blueprints/best`, currently missing)
- [ ] sbs-4: Push best blueprints and reports to GitHub automatically