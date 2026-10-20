<!-- Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work -->
# zero-scratch-archive

Archive of excess / leftover material from machine **zero** (Garuda Linux, user `livings`),
consolidated on 2026-10-10 for future reference. Local copies were removed after this
repo was verified pushed.

Nothing here is live or imported by any running service. Active material was deliberately
**excluded** — see "Excluded" below.

## Contents (`dump/`)

| Path | What it is |
|------|------------|
| `_audit-archive/` | Repo clone/verify results, `_secrets.json` scan report, notes archive, `dream-engine-backup-20261001.tar.gz` |
| `_healer-junk-backup-20260928/` | `junk-files.tgz` from the 2026-09-28 cleanup |
| `_provenance/` | `README.md` describing the provenance tooling (code lives in the `provenance` repo) |
| `host-audit-20260929/` | Host audit write-up (`AUDIT.md`) |
| `later-work/` | Placeholder scratch repo |
| `sin-archive-2026/` | Steam manifests + configs snapshot |
| `user-data-archive-2026-09/` | User-data dump: opencode + hermes session DBs/logs, lia, shell, identity, desktop, audit |
| `root-__pycache__/` | Compiled caches of `hermes-containment.py` and `send-torch.py` |

## Excluded (live / not junk)

- `~/var/` — live `coordination-server.service` state (logs + `agent-credentials.json`)
- `~/honeypot/` — live `nyan-honeypot.service` guard (request log)
- `~/.var/` — Flatpak per-app data (browser integration hosts)
- `~/provenance/` — active private repo (security tooling)
- `Projects/_inventory/` — scratch working copies (kept in place)

## Sanitisation

OpenSSH/RSA private-key blocks found in the dumped session logs were replaced with
`[REDACTED PRIVATE KEY]` before pushing.
