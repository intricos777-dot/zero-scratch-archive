<!-- Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work -->
# Reconstruction To-Do — what was lost or never ported in the machine rebuild

Compiled 2026-09-26 by mining every session store and Git repository on this
host. Evidence for each item is cited so you can verify rather than trust.

## How this was reconstructed, and what the limits are

**Session logs cover only today.** The Hermes store (`~/.hermes/state.db`)
has exactly 1 session; OpenCode (`~/.local/share/opencode/opencode.db`) has
exactly 2. Every one starts 2026-09-26, the day of the rebuild. I searched
both databases for the old hostname, "sentinel", "watchman" and "bchn" — all
zero hits. There are no older databases anywhere on the filesystem, no
`/home/sin` home directory, and no other agent profiles.

So there is **no session history from the previous machine to scan.** The
reconstruction below is built from the other surviving record: the git history
of 120 repositories, plus `sin-archive-2026`, which is a self-describing
ledger of the last cleanup on the old host.

**Caveat on scope.** I can enumerate what the old system *referenced to* and
what is missing now. I cannot prove a component ever ran, only that its code
exists in git while its deployed form is absent from this machine.

## The old system, from the archive ledger

`sin-archive-2026/MANIFEST-2026-09-24.md` records a cleanup on 2026-09-24:

- Host: `sin-asustufdashf15fx517zcfx517zc`, Garuda/Arch, kernel 7.2.6-zen2-1-zen
- Freed ~203G; root went from 95% full to 51%
- "Sentinel posture: 15/15 integrity anchors intact, watchman active,
  34 listeners baselined, no tripwire events"
- One outstanding warning: `ANTHROPIC_API_KEY` ambient in the environment
- Kernel here is 7.2.7-zen1-1-zen — **this is a different machine, not the
  same host restored.**

## PRIORITY 1 — Blocked, needs your sudo password

These are the two I have already built and verified but cannot install:

- [ ] **Install the single-admin faillock policy.**
      `sudo ~/Projects/zen-hardening/install-faillock-admin.sh`
      Until this runs, live `/etc/security/faillock.conf` has no
      `admin_group`, so you are **not** exempt from your own lockout policy,
      and live `unlock_time` is 30s against the repo's 1800s.

- [ ] **Install USB device admission control.**
      `sudo ~/Projects/shield-kitty/device-blacklist/install.sh`
      First sighting quarantines and notifies; second permanently bans.
      Root hubs and HID devices are exempt so you cannot lock yourself out.

## PRIORITY 2 — Whole subsystems that did not come across

The BDE patrol suite and the security shell wrappers exist in git but were
**never checked out** on this machine. Nothing from them is running.

- [ ] **Check out and re-point the BDE integrity patrol.**
      `hermes-security-scripts/scripts/bde-system-integrity-patrol.sh` writes
      to `/home/sin/.hermes/logs/...` and runs
      `/home/sin/Projects/space-edge-network/security/bde/patrols/system_patrol_scheduler.py`.
      The patrol code itself is intact in
      `space-edge-network/security/bde/patrols/` (adb_patrol, github_scanner,
      integrity_patrol, scheduler, system_patrol_scheduler). Only the wiring
      and the deploy are missing.

- [ ] **Re-establish the "15/15 integrity anchors" baseline.**
      The old host ended cleanup with 15 anchors verified and a watchman
      active. On this machine the only monitoring unit running is
      `shield-kitty-watch.service`. There is no watchman, no sentinel
      posture, and no anchor set. What those 15 anchors were is not recorded
      anywhere I could find — this needs your recollection.

- [ ] **Re-create the per-agent secure/self-heal wrappers.**
      `hermes-security-scripts/scripts/` contains 11 wrappers that all predate
      this machine: `hermes-secure.sh`, `lia-secure.sh`, `opencode-secure.sh`,
      `opencode-self-heal.sh`, `supercode-secure.sh`,
      `supercode-self-heal.sh`, `polsia-secure.sh`,
      `lin-antimalware-self-heal.sh`, `bde-system-integrity-patrol.sh`, and a
      `shield-kitty/` subdir. None are deployed here.

- [ ] **Rebuild the 34-listener baseline.**
      This machine currently has 4 listeners. The old baseline of 34 is not
      documented, so it cannot be reconstructed from artifacts — it would
      have to be re-derived from what you intend to run.

## PRIORITY 3 — Path drift: 72 of 120 repos hardcode the old account

This is the largest and most mechanical problem. `grep` for `/home/sin`
matches in **72 repos**. The active account here is `livings`, so every one
of those paths is dead on this box.

Worst offenders by file count: `zen-healer` (240), `ringworld-redux` (108),
`gaming-unified` (26), `security-audit-2026` (17), `offline-agents` (16),
`work-automation` (15), `twilight-elysium` (15), `bde-security-biometrics`
(12), `business-health-monitor` (11).

Deployable units that would fail immediately if installed as-is:

- [ ] `business-health-monitor` — 4 `.service` files with
      `ExecStart=/home/sin/...` (I fixed these in the working checkout to use
      `%h` + `User=livings`, but that is **not pushed**, and the deployed
      units on this machine are still the old ones.)
- [ ] `crypto-bot` — `crypto-bot-api.service` and `crypto-bot.service` both
      point at `/home/sin/finance/crypto-bot` and `/home/sin/Projects/crypto-bot`
      (note: the two units disagree with each other on the path).
- [ ] `work-automation` — `agent-launcher.service` hardcodes
      `/home/sin/work-automation` for WorkingDirectory, ExecStart, and both
      log paths.
- [ ] `zen-healer` — `zen-healer.service` and `zen-healer-watchdog.service`
      run from `/home/sin/zen/ai-healer/`.

Suggested approach: a repo-wide pass replacing `/home/sin` with
`${HOME}` / `%h` plus an explicit `User=` in every system unit (a system unit
using `%h` without `User=` expands to `/root`, which is its own bug class).
I already hit and fixed that trap in `business-health-monitor`.

## PRIORITY 4 — Not checked out locally, may be needed

Present in git, absent as working checkouts on this machine:

`hermes-security-scripts`, `space-edge-network`, `security-audit-2026`,
`code-theft-evidence`, `work-automation`, `crypto-bot`, `zen-healer`,
`aerovora-industries`.

Tell me which of these you still consider live and I will clone and rebuild
them properly.

## PRIORITY 5 — Deliberately deleted on the old host; decide before restoring

The 2026-09-24 ledger deleted these on purpose. They are absent now, and
mostly that is correct — flagging so the decision is yours, not an oversight.

- [ ] **`~/.bitcoin-cash/wallets` — this one matters.**
      The ledger explicitly lists it under "Kept (not archived, not deleted):
      retained per operator decision" and "never uploaded anywhere." It is
      **not on this machine.** `bchn.service` is inactive and
      `~/.bitcoin-cash` does not exist. If those wallets hold funds, they are
      on the old disk or in a backup — nothing here can recover them.
      **Please confirm you have them backed up somewhere.**
- [ ] `~/.local/share/Steam` (222G) — deleted by choice. The 64 owned-game
      AppIDs survive in `sin-archive-2026/steam-manifest/`, so the library can
      be reconstructed precisely if you want it back.
- [ ] `~/shader-backup-20260918-162219` (9G) — stale cache, config preserved
      in the archive repo.
- [ ] `~/zen-suite-bootable.iso` (0.3G) — rebuildable via the zen-suite
      pipeline. Note the archive holds only its SHA-256 prefix, not the ISO.
- [ ] `~/Games/{epic-games-store,ea-app,ubisoft-connect}` — launcher caches.
- [ ] `~/Desktop/games` (16.8G Skyrim + Oblivion .7z) — retained by operator
      decision on the old host, also absent here.

## Housekeeping found along the way

- [ ] **`node_modules/` is committed in 3 repos** — `coordination-server`,
      `himalaya-exchange`, `lia-groq-bridge`. This is what put dotenv's
      placeholder keys into git history in the first place. Untrack them and
      add `.gitignore`.
- [ ] `crypto-dashboard/.env` is tracked and ungitignored. Harmless today (it
      holds only two `localhost:4123` URLs) but it is the wrong pattern.
- [ ] `~/.config/gh/token.clean` **no longer exists** — the directory is now
      empty. My notes recorded a working token there. Anything that depended
      on it (including my earlier API-based checks) needs it restored.
- [ ] The bde-security-biometrics history rewrite and the lia-cli collector
      are **committed locally but not pushed**. Until force-pushed, the old
      collector token is still retrievable from GitHub history even though the
      running service rejects it.

## Not actionable, for the record

- No firewall is active on this machine in a way that matches the old
  "34 listeners baselined" posture. OpenCode is currently mid-work on a
  `workstation.xml` firewalld zone and has hit a real Arch packaging bug
  (`fail2ban.service` declares `PartOf=iptables.service firewalld.service`, so
  restarting firewalld plans a fail2ban restart in the same transaction that
  stops it). I will verify its result when it finishes rather than
  duplicating the work.
- The old host's `ANTHROPIC_API_KEY` warning was environmental and does not
  carry over.
