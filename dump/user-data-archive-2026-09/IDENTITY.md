<!-- Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work -->
# Identity map — usernames, UIDs, hosts (window 2026-05-28 → 2026-09-28)

## This machine (host `zero`)

| Field | Value |
|---|---|
| Hostname | `zero` (Garuda Linux, kernel 7.2.7-zen1-1-zen, ASUS laptop) |
| Local accounts ≥ UID 1000 | **exactly one**: `livings` → UID **1000**, GID 1000, GECOS **`Living_Sin`**, home `/home/livings`, shell `/bin/bash` |

There are no other unprivileged accounts on this system. `/etc/hosts` names the box
`zero`. Full evidence: `identity/passwd-entries.txt`, `identity/getent-livings.txt`,
`identity/hostnamectl.txt`, `identity/etc-hosts.txt`.

## The four name spellings requested

| Spelling | Where it actually exists |
|---|---|
| `Living_Sin` | GECOS field of UID 1000 on `zero`; global git author (`user.name=Living_Sin`) |
| `Living_sin` | session/history references only (hermes history 2026-09-28 request) |
| `sin` | **old machine's account**: `/home/sin` on host `sin-asustufdashf15fx517zcfx517zc` (Ubuntu/Garuda Arch, kernel 7.2.6-zen2-1-zen) — see `../lia/older-corrupted/ssh-keygen-transcript-old-host.txt` and `sin-archive-2026/MANIFEST-2026-09-24.md` |
| `living_sin` / `livingsin` | session/history spellings only; no local account |

Old host evidence (both from records preserved in this archive):
- `ssh-keygen … Enter file in which to save the key (/home/sin/.ssh/id_rsa)` on `sin@sin-asustufdashf15fx517zcfx517zc`
- sin-archive manifest: "Operated by: sin (host sin-asustufdashf15fx517zcfx517zc …)"

## "Garuda Rani systems"

No host, alias, file, or config named `rani` exists anywhere on this system
(searched home + all 133 repo clones). The only two machines identifiable from
records are `zero` (this box) and `sin-asustufdashf15fx517zcfx517zc` (the old
box, replaced ~2026-09-24/26). No SSH config or known_hosts entry exists for any
third machine — nothing else is reachable from here.

## Data-availability timeline (why most raw data starts 2026-09-26)

The system was wiped/rebuilt **2026-09-26** (and the old home was cleaned
2026-09-24, ~203 GB freed). Surviving pre-rebuild records:

| When | What survived | Where in this archive |
|---|---|---|
| 2026-05-28 → now | full git history of all 133 local repo clones | `git-history-4mo.md` (+ `lia/lia-cli-full-history.bundle`) |
| 2026-07-17 | Lia memory vault (3 entries) | `lia/current-checkout/data/memory/` |
| 2026-07-21 | two Lia legal scans (empty) | `lia/current-checkout/data/` |
| 2026-09-03 | second Lia vault copy (replika bridge memory) | `lia/scattered-memory-copies/lia-vault.json` |
| 2026-09-21 | hermes pending-memory batch (18 KB) | `lia/scattered-memory-copies/hermes-pending-memories.json` |
| 2026-09-24 | sin-archive deletion ledger + steam manifest | already on GitHub (`sin-archive-2026`, private) |
| 2026-09-26 → now | hermes/opencode sessions, shell history, logs | `hermes/`, `opencode/`, `shell-terminal/` |
