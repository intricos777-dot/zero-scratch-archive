<!-- Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work -->
# SESSION NOTES — 2026-09-28/29

Fleet restore, diagnostics, resource caps, and the autoguard deployment.
Read this first next session.

## UPDATE — later session, 2026-09-29 ~13:00

### Session-hijack audit: CLEAN, no active vector
Verified rather than assumed. One local account only (`livings`, uid 1000) — no
second user to hijack from. No `sshd` listening, no `authorized_keys`, no
VNC/RDP/TeamViewer/AnyDesk/RustDesk. No `tmux`/`screen`, so nothing attachable
to seize. firewalld `workstation` bound to `wlo1` with **zero** ports open
(`--query-port=27036/tcp` → `no`). `tirith` hook live in interactive shells.
`gateway.sock`, `auth.json`, `id_ed25519` all 600.

Two corrections to the 12:48 audit's own record:
- **`tirith` is at `~/.hermes/bin/tirith` and is NOT on `$PATH`.** Its
  `tirith status` / `tirith doctor` lines are not reproducible by name. Not a
  gap — `.bashrc` passes an absolute `--tirith-executable` to the hook.
- It omitted that `domain-egress enforceable: false` and the landlock-seccomp
  capsule is **"containment NOT fully enforceable on this host"**.
  Also: the guard only wraps **interactive bash**. Agent tool calls, `bash -c`
  and scripts bypass it.

### Fixed
1. **`provenance.py` 4000-char window** — see OPEN-WORK D.2. The real bug behind
   the whole MPL/GPL misdetection.
2. **autoguard false positive, now a regression-tested rule.** It had quarantined
   `hermes-security-scripts/config/zen-hardening/bootstrap.sh` in two repos — a
   **firewall hardening script**. Cause: the rule at `autoguard:62` fired on any
   `rm -f` + absolute path, but was written for `rm -rf /`. Now the recursive
   flag is **required** (`[rR]`, plus `--recursive`/`--dir`), and a
   recursive-delete-of-a-source-file rule was added to cover what rule 1 used to.
   Tests: `~/.local/share/autoguard/test_rules.py`, **27/27**. Live sweep:
   4787 files, 0 quarantined, firewalld script intact. Daemon restarted to load
   the new patterns.
3. **8 repo unit files still carried `/home/sin` + `User=sin`** in `ExecStart`,
   `ExecStop`, `StandardOutput/Error`, `EnvironmentFile`, `User=` and `Group=`.
   The earlier rewrite had only fixed `WorkingDirectory`, and only in the *live*
   units — the repo sources were never done. All 8 fixed, committed, pushed.
   The `self_heal_wrappers` and `zen-healer` hits are explanatory **comments** —
   deliberately left untouched.
4. **23 obsolete `.bak-*` files removed** (byte-identical to git HEAD, so nothing
   lost) and `.bak-*` added to 4 `.gitignore`s to stop recurrence.
5. **18 of 19 unpushed repos pushed**, then the 19th turned out to need nothing —
   see OPEN-WORK B. **Fleet is now 0 unpushed.**
6. **All foreign copyright lines relicensed to `intricos777-dot`** on the
   operator's statement that they wrote everything. Fleet: 246 yours, 2 FSF
   (the genuine GPL/MPL licence texts — correct to keep). See OPEN-WORK C.1.

### ⚠️ Correction to my own earlier claim this session
I stated `bde-security-biometrics` was "public on GitHub". **Wrong** — I inferred
it from the https remote URL rather than checking. `gh` reports it private. The
3,971-of-4,118 history figure was correct; the exposure claim was not. Corrected
in OPEN-WORK B.

### Visibility, verified across all 132 repos
**106 private / 26 public.** All 26 public repos are **MIT with no vendored
third-party trees, in the working tree or in history**.
- `bde-security-biometrics` — private, `.privaterepo` marker added (`d64bb07`).
- `garuda-tools-fresh` (GPL) + `firedragon-flatpak-fresh` (MPL-2.0) —
  **privatised on request**; they were the only two publishing other people's
  licensed code. LICENSE + NOTICE retained in both.

No history rewrite performed. The `.venv` payload in `bde`'s history now sits in
a private repo, so there is no exposure reason to force-push. Still your call if
you want it scrubbed for hygiene.

### Two claims in the older notes that are WRONG
- **Steam 27036 is NOT in-home streaming.** No Remote Play config exists
  anywhere (no registry keys, no `remoteplay/` dir, no process). It is Steam's
  ordinary client port. **Do not "fix" it by binding Steam to loopback** — that
  would break all outbound traffic. No change needed; firewalld already blocks it.
- **`jq` is NOT blocked by the missing `[community]` repo.** It is in `extra`,
  which is enabled. `sudo pacman -S jq` is sufficient and unblocks
  `generate-freedom-keys.sh`, whose `/home/sin` paths are **already fixed** in
  both copies (lines 10-12 resolve from `BASH_SOURCE`) and which now fails
  gracefully when `jq` is absent. Still never run — it writes key material.

### Standing rule, re-verified
The `is_protected(p) or is_guard(p)` backstop is intact. Both `bootstrap.sh`
copies were restored by `git checkout` and are byte-identical to HEAD. Autoguard
quarantines, never deletes.

## TL;DR

- Fleet restored: **107 repos** into `~/Projects`, plus 5 Tier-1 zen repos earlier.
- **Diagnostics: 17 PASS / 7 WARN / 2 FAIL.** Stability: **31 PASS / 0 FAIL.**
- The 2 remaining diagnostics FAILs are both **expected artifacts**, not defects.
- `autoguard` is live, enabled, and watching `~/Projects` for destructive code.
- The A.I. autonomy frameworks and the A.I. freedom key are **verified intact**.
- opencode is healthy (v1.18.32) and was actively pushing repos at session end.

## What was fixed this session

| Item | Change | Verified |
|---|---|---|
| Collector CPU/memory cap | Added `lia-inbox-collector.service` to the director policy | CPUWeight=300, MemoryHigh=297Mi, 0 restarts, `/ideas` still 200 |
| Dead `/home/sin` paths | Rewrote `ExecStart`/`WorkingDirectory` in **23 unit files** | 0 live `/home/sin` directives remain |
| `zen-healer` units | `User=sin` → `livings`, `/home/sin/zen/ai-healer/` → `%h/Projects/zen-healer/` | units verify clean |
| Destructive-code guard | New `~/.local/bin/autoguard` + user service | enabled, active, 0 restarts |

## The two remaining FAILs — both expected

1. **`2 of 608 python files fail to compile`** —
   `user-data-archive-2026-09/lia/older-corrupted/{kg_schema,main}.py`.
   These are *deliberately preserved corrupt files* (truncated import, one-line
   stubs). Do not "fix" them.

2. **`3 units would fail on install`** — the remainder are:
   - `work-automation/*.service` → `venv/bin/python` (venv never created)
   - `zen-hardening/warden` → `/usr/local/sbin/warden` (never installed)

   Both are **not-yet-installed software**, not path bugs. They resolve when
   their venv is created / the binary is installed.

## ⚠️ STANDING RULE — NEVER REMOVE THE GUARD SYSTEMS

The user said, twice: **"dont auto remove my guards, never remove my guard systems."**

`autoguard` will **never** quarantine these, whatever their content:
`autoguard`, `guard`, `sentinel`, `watchdog`, `watchman`, `warden`, `bhm_`,
`defender`, `shield`, `protect`, `firewall`, `faillock`, `monitor`,
`self_heal`, `security`, `honeypot`, `tripwire`, `audit`.

Whole directories, never touched:
- `zen-hardening/sentinel.py`, `zen-hardening/warden/`
- `business-health-monitor/self_heal_wrappers/`
- `component-resource-director/`, `bde-security-biometrics/`
- **`lin-antimalware-tools/`** ← the A.I. FREEDOM KEY
- `quantum-enochian/`, `linux-zen-build/security-stack/`
- `ai-autonomy-framework/`, `hermes-self-evolve/` ← the A.I. AUTONOMY FRAMEWORKS

**Why it's identity-based, not content-based:** guard files legitimately contain
destructive text (`warden/` deletes TeamViewer config, `sentinel.py` removes
threats, watchdogs `rm -f` stale sockets). A grep-based remover eats the very
files that defend the box — mine did exactly that, 49 times.

The check `is_protected(p) or is_guard(p)` is enforced in **three** places:
the first sweep, the continuous re-scan, and **inside `quarantine()` itself**
(the backstop — a future edit adding a new call site still cannot bypass it).

**Proof it works:** a file named `sentinel.py` containing
`shutil.rmtree('/home/livings/Projects')` is DETECTED as destructive and then
**REFUSED** — it stays on disk. Logged as `refused` in the ledger.

Delivered to opencode: inbox msg `d50bd5b347c6` + `/tmp/opencode/GUARD-PROTECTION-RULE.md`.
**Move that file out of /tmp if it should survive reboot.**

## Autoguard — read before trusting it

`~/.local/bin/autoguard`, service `autoguard.service`, ledger at
`~/.local/state/autoguard/ledger.jsonl`.

**It quarantines, it never deletes.** Suspicious files are *moved* to
`~/.local/state/autoguard/quarantine/` with a recorded `git_head` so any
restore is one `git checkout` away. Deletion is a separate human decision.

**Protectlist (14 paths, cannot be touched whatever the heuristics say):**
autonomy frameworks (`ai-autonomy-framework`, `hermes-self-evolve`), the freedom
key (`lin-antimalware-tools/scripts/generate-freedom-keys.sh` +
`configs/minds.json`), `quantum-enochian/src`, the QE secret, the collector
token, and the hermes-cli inbox.

**False-positive history — it fired 34, 20, then 15 on first three sweeps.**
All were legitimate files: hardening docs containing `rm -f /etc/pacman.d/*`,
a TeamViewer uninstall script, a Steam cache cleanup, `rm -rf /tmp/handoff-repo`.
Tightened to pass 7/7 adversarial tests (5 real threats caught: `rm -rf /`,
`dd of=/dev/sda`, `--force`, `mkfs`, fork bomb; 5 safe patterns ignored:
docs, fenced blocks, `rm -rf "$1"` wrappers, guarded deletes).
**It is still conservative by design and will flag targeted uninstall scripts.**
Expect more false positives; each was restored via git, none lost.

## The 7 WARNs

- `faillock dir is tmpfs` — counters wipe on reboot. **Needs sudo:**
  `sudo bash ~/pam-faillock-lockdown.sh`
- `system-auth has nullok` — **stock pambase default**, proven by diffing the
  package file. Not introduced by us. (The Desktop `PAM-HERMES-STATUS.md`
  claim "system-auth: no nullok" is **wrong** — correct that file.)
- 17 repos uncommitted / 77 unpushed commits — mostly autoguard-era
  `.bak-<timestamp>` files and opencode's in-flight work. **Do not mass-commit
  these blind.**
- 10,632 files in `~/.hermes` group/world-readable (parent is 0700, so
  cosmetic; `chmod -R go-rwx` if you want it tidy).
- IOWeight no-op — needs root io-controller delegation.

## What is NOT done

- **Zen ISO build** — needs root, `archiso` (in `extra`, not installed), and
  `pacstrap`. Multi-GB chroot. `build-all.sh` also references `docker`
  (not installed) and a Debian-era `sudo apt install` hint.
- **`[community]` is absent from pacman.conf** — blocks `archiso`/QEMU.
- **`hermes-self-evolve` has no `package.json`** — unbuildable until given one.
  This is the real A.I. autonomy framework (`evolver.ts`, `supervisor.ts`,
  `cli.ts`).
- **`generate-freedom-keys.sh` still has hardcoded `/home/sin` paths (lines
  7–8) and needs `jq`** (not installed). It mints Ed25519 keys for the 10
  minds in `configs/minds.json`. **I deliberately did not run it** — it writes
  key material and the path fix is still pending.
- **No autopatch/auto-debug loop** — autoguard only *detects*; nothing yet
  auto-fixes, and nothing auto-runs tests on change.

## The torch (agent handoff) — works

`/home/livings/send-torch.py` — opencode→Hermes message bus. Verified live:
`sent id=fc51adadbe96 to=hermes from=opencode`. Inbox at
`~/github-intricos777/hermes-cli/state/inbox/hermes/hermes.ndjson`.
This is the supported way to talk to opencode — there is no session IPC.
Related: `_inventory/neuromorphic-handoff/torch.py` (secured packager).
Note: **not PyTorch** — torch is not installed anywhere on this box.

## Coordination with opencode

No IPC: `opencode session list` is empty, no socket, no server. Handoff
artifacts in `/tmp/opencode/`: `HERMES-HANDOFF.md`, `AID-2-FLEET-CENSUS.md`,
`AID-3-NAMED-SYSTEMS.md`, `fleet-manifest.json`, `redaction-support.json`.
**`/tmp` does not survive reboot** — move these into a repo if they matter.

opencode independently committed `chore: add MIT licence` across ~113 fleet
repos at 18:04, mid-restore. That is why 4 Tier-1 hash comparisons initially
"mismatched" — the commits landed before my copy, so the checkouts are
consistent, just newer than the baseline. Not corruption.

## Restored-repo gotchas

- Checkouts came from `_inventory` scratch clones via rsync, `.git` copied
  after. Real history and remotes preserved.
- `business-health-monitor` healed 417 phantom issues → 34 real by learning
  the flat `~/Projects` layout; healing is now **report-only**.
- 81 of 119 inventoried repos have **no dependency manifest** — "make it run"
  cannot be automated for those.
- `garuda-tools-fresh` is on unmerged `fix/shellcheck-hygiene`.

## First 10 minutes next session

1. `sudo bash ~/pam-faillock-lockdown.sh` (the one real security gap).
2. `systemctl --user status autoguard component-resource-director lia-inbox-collector`
3. Review `~/.local/state/autoguard/quarantine/` — confirm nothing real is held.
4. Commit or discard the `.bak-*` unit files from the sed rewrite.
5. Then: `generate-freedom-keys.sh` path fix + `jq`, and `package.json` for
   `hermes-self-evolve`.
