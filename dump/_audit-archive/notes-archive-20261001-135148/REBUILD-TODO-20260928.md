<!-- Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work -->
# Current To-Do — updated 2026-09-28 17:10 MST

Supersedes `REBUILD-TODO-20260928.md`. That file's GitHub-push blocker and its
path-drift numbers were both stale — corrected below with what was actually
found and verified this session.

## Fixed and verified this session

- [DONE] **`bhm-self-watchdog` was silently dead.** It watched
  `business-health-monitor.service`, which does not exist (the real unit is
  `business-health.service`), so it had *zero* journal entries — enabled but
  never having run. It also watched a `Type=oneshot` service that is correctly
  inactive between runs, so a fixed version would have restart-looped forever.
  Now watches `business-health.timer` and runs one scan on failure. Active.
- [DONE] **The business-health "self-healer" was writing junk into your repos
  every night.** Two independent bugs:
  1. `scan_all()` walked `Projects/<category>/<repo>`, but `Projects` is flat.
     The extra level made it treat each repo's *subdirectories* as separate
     repos, so it healed `hermes-blood/alacritty`, `zen-hardening/systemd`, etc.
  2. `heal_issue()` ran `git add -A && git commit` unattended (committing its
     own output) and fabricated stub `README.md` / `.gitignore` files.

  Fixed both; healing is now report-only except `git checkout -- .`.
  Removed 67 junk files (63 untracked + 4 it had committed), tarballed first to
  `~/Projects/_healer-junk-backup-20260928/junk-files.tgz`.
  The two `auto: daily maintenance` commits only *added* files — no real work
  was lost. Verified a `--cron` run now creates **0** files.
  Scan visits 18 real repos (was 200+ bogus paths); issue count 417 → 34.
- [DONE] **4 failed user units → 0.** All were cosmetic, each with its own
  cause: `autorandr` ×2 (exits 1 by design on Wayland, and no profiles are
  configured anyway), `libinput-gestures@autostart` (duplicate of the
  `libinput-gestures.service` that is already active), `snapper-tools-check`
  (its `grep -q .snapshots /proc/cmdline` guard cannot match this box's
  subvolume layout; `snapper-tools --autostart` itself exits 0 when run).
  Masked at user level — no sudo needed.
- [DONE] **`component-resource-director` enabled and running** (was installed,
  disabled, never started — todo item E16). It works: currently applying
  `hermes-gateway.service` CPUWeight=300, MemoryHigh≈642Mi.
  Still logs the known IOWeight warning; that needs the root io-controller
  delegation and is unchanged.
- [DONE] **`bde-security-biometrics`: 2157 tracked `.venv` files removed** from
  git (files kept on disk). Every one had `/home/sin/workspace/...` baked into
  its shebangs and activate scripts — 2157 tracked dead paths. Pushed.
- [DONE] **`install-bde.sh` dead path fixed.** `BDE_DIR` was hardcoded to
  `/home/sin/workspace/bde-security-biometrics`, so the installer could never
  find its own sources. Now resolved from `${BASH_SOURCE[0]}`; all four PAM
  install sources verified to resolve. Pushed.
- [DONE] **`lia-cli` sweep-coordinator dead path fixed** —
  `CRYPTO_BOT` was `/home/sin/...`, so every sweep returned "Faucet CLI not
  found". Now `join(homedir(), ...)`. `tsc --noEmit` passes. Pushed;
  `lia-inbox-collector` verified still active, NRestarts=0, port 4124 listening.

## Stale todo items — closed, no action needed

- ~~A2 / B1: "no GitHub token, nothing can be pushed"~~ — `gh` **is**
  authenticated (`intricos777-dot`, scopes repo/workflow/gist, keyring). Push
  over HTTPS works; `gh auth setup-git` is now done. The `bde` commit the old
  todo called unpushed was already pushed.
- ~~B2: untrack `node_modules` in coordination-server / himalaya-exchange /
  lia-groq-bridge~~ — already done; 0 tracked `node_modules` files, all three
  have a `.gitignore`.
- ~~D13/D14: "72 of 120 repos hardcode /home/sin"~~ — overstated. Measured
  across all top-level checkouts: **108 refs in 31 files across 9 repos**, and
  **zero** in any systemd unit file except comments. The rest are in
  `user-data-archive-2026-09` and `code-theft-evidence` (historical records —
  correctly left alone) or are already-fixed comments.
- ~~The `business-health-monitor` `then then` syntax bug~~ — not present. The
  earlier "syntax error" was `bash -n` being run against a `.py` file.

## Still open — needs you

1. [ ] **BCH wallet backup** (todo A1). Unchanged and still the only item where
   delay can cost money. `~/.bitcoin-cash` does not exist here; the 2026-09-24
   ledger records those wallets as retained and never uploaded.
2. [ ] **SSH key** — `ssh -T git@github.com` is still rejected. HTTPS push
   works, so this only matters if you want SSH remotes. Register a key at
   github.com/settings/keys.
3. [ ] **Which unchecked-out repos are still live** (todo A3). Blocks deploying
   the 11 secure/self-heal wrappers from `hermes-security-scripts` and wiring
   the BDE integrity patrol.
4. [ ] **15/15 anchor set** (todo A4) — old host's anchors unrecoverable.
5. [ ] **Repo visibility decisions** (Desktop `PAM-HERMES-STATUS.md` §4): 15
   public repos that are not games/bugfixes, and 7 private repos that are.
   Per your standing rule the security-minded ones are already private.
6. [ ] **Listener baseline re-derive** (todo C12). 12 listeners, 4 LAN-exposed:
   `kdeconnectd` on `*:1716`, Steam on `*:27036` (both TCP+UDP on 0.0.0.0).

## Needs your sudo password — no workaround

- `sudo bash /home/livings/pam-faillock-lockdown.sh` — the one real remaining
  security gap is that Arch's pam_faillock defaults `dir=/run/faillock`
  (tmpfs), so **failure counters are wiped on reboot**. Then
  `sudo bash /home/livings/pam-verify.sh`.
- Solo miner rig (Desktop `NEXT-REBOOT-READ-ME.txt`): needs a valid DOGE
  address, an RVN node route, and `sudo install-solo-miners.sh --daemons`.
  Nothing in that rig is running; rebooting is safe.
- IOWeight no-op in the director — one root change, documented in the
  director README.
