# user-data-archive-2026-09

Private archive of the operator's own user data, pulled **2026-09-28** for the
window **2026-05-28 → 2026-09-28 (4 months)** across the usernames
`Living_Sin` / `Living_sin` / `sin` / `living_sin` (single local UID 1000,
see `IDENTITY.md`). Pushed to GitHub through Hermes.CLI (`hermes sync`).

## Contents

| Path | What it is |
|---|---|
| `IDENTITY.md` | username/UID/host map + why most raw data starts 2026-09-26 (rebuild) |
| `git-history-4mo.md` | per-repo commit index for the full 4-month window, all 133 local clones |
| `hermes/` | hermes memories (MEMORY/USER/SOUL), full session DB dump (4 117 messages), agent+gateway logs, pastes, terminal sessions, curator backups, kanban/shared-state/cron DB dumps, history file |
| `opencode/` | full opencode DB dump (sessions, messages, events), tool logs, prompt history, config snapshots |
| `lia/` | Lia.CLI memories & data: current checkout vault, **older corrupted versions**, scattered memory copies, full-history git bundle, findings in `lia/CORRUPTION-NOTE.md` |
| `shell-terminal/` | fish history, konsole profiles, recently-used files, bash rc files |
| `desktop/` | NEXT-REBOOT-READ-ME.txt |
| `audit/` | `_verify.json`, `_clone_results.json`, `_secrets.json` from the 120-repo inventory audit |

## Lia.CLI verdict (short form)

- Memories recovered: vault of 2026-07-17 (3 entries, 1 encrypted), second vault
  of 2026-09-03 (1 entry), 18 KB pending-hermes-memory batch of 2026-09-21,
  two empty legal scans of 2026-07-21, task/plan files.
- Older versions: the upstream clone's `kg_schema.py` (truncated `from owlready2
  import` — never valid Python), one-line `main.py`/`__init__.py` stubs, and a
  `keygen key.txt` transcript from the old `/home/sin` machine. All deleted from
  the repo in commit `f0f6235` and preserved here + in `lia-cli-full-history.bundle`.
  Full write-up: `lia/CORRUPTION-NOTE.md`.

## Deliberately NOT in this archive (withheld)

- `~/.hermes/auth.json`, `~/.hermes/vault/{vault.key,vault.json.enc}`,
  `~/.hermes/shared/nous_auth.json`, `~/.local/share/opencode/auth.json`
  — live credentials
- `~/.lia-cli/inbox/token` — live bearer token for the Replika bridge collector
- `~/.ssh/*`, `~/.config/gh/*` — keys/gh config
- Raw SQLite files: replaced by `.dump` text exports (consistent, no WAL needed)
- Live secrets found **inside** session data were **redacted in place** and
  marked `[REDACTED-SECRET-2026-09-28]`:
  - a GitHub fine-grained PAT pasted into an opencode session (2026-09-26)
  - the old (already-rotated) lia inbox token that had leaked into test code
  - other token-shaped strings caught by the archive-wide scan
- Synthetic scan fixtures (`[AWS_KEY_REDACTED:1a5d44a2]`, `[SLACK_REDACTED:2b763169]-…`,
  `eyJhbGciOi…abcdefghijklmnop`) were left — they are hermes' own test strings,
  not real secrets.

Restore the Lia history bundle with:

```sh
git clone lia-cli-full-history.bundle lia-cli-history
```
