# Status note — 2026-09-28 ~13:45 MST

Written so you can walk away and resume cold. Nothing is mid-edit; no partial
state. Everything below is either done-and-verified or waiting on **your**
sudo password.

## 1. PAM / admin lockdown — APPLIED, core paths verified

Ran at 13:32 and 13:33 (you ran it twice; second run created a second backup dir).
Backups: `/root/pam-faillock-backup-20260928-133257` and `-133401`.

Verified PASS (read-only, by me):
- `/etc/pam.d/su` and `su-l`: `pam_rootok` + `pam_wheel required` **before** the
  password prompt + `pam_faillock` preauth/authfail/authsucc. Files identical.
- `unlock_time = 900`, `deny = 10`.
- `access.conf`: `+ root`, `+ livings`, `- ALL` (currently duplicated — harmless).
- `system-auth`: no `nullok`.
- `wheel` and `shield-admin`: only `livings`.
- No interactive account other than `livings`.
- polkit catch-all gate installed: `/etc/polkit-1/rules.d/00-operator-only.rules`.
- `admin-guard.timer` enabled, hourly, last run `status=0/SUCCESS`.
- pam_faillock is live: `/run/faillock/livings` record file was created by your
  real `sudo` auth.

### To finish (one command, needs sudo)
```
sudo bash /home/livings/pam-faillock-lockdown.sh
```
It is now idempotent and additionally fixes 3 things:
1. `dir = /var/lib/faillock` in `faillock.conf` — right now Arch's pam_faillock
   defaults to `/var/run/faillock` (tmpfs), so **failure counters are wiped on
   reboot**. This is the only real remaining security gap.
2. dedupes `access.conf`.
3. reinstalls the **fixed** `admin-guard.sh` and corrected unit files.

### Then verify
```
sudo bash /home/livings/pam-verify.sh
```
Expect all PASS. Known false alarms in the current verifier output, ignore them:
- `/etc/pam.d/sudo has no pam_faillock` — it includes `system-auth`, which has it
  (verifier does not follow includes yet).
- `polkit operator gate missing` — `/etc/polkit-1/rules.d` is `0750 root:polkitd`,
  so non-root cannot stat it. The file is there.
- `guard reports N DRIFT` — from the **old** buggy guard still installed.

### Manual items only you can do (need your password)
- `sudo -v`
- `su - livings` (must work)
- one deliberately WRONG password at su/sudo/SDDM, then `faillock --user livings`
  (expect counter +1), then correct password (expect reset).
- clear a test lockout: `sudo faillock --user livings --reset`

### Rollback (the checklist's flat `cp -a` line was wrong — use this)
```
sudo bash /home/livings/pam-rollback.sh            # plan only, changes nothing
sudo bash /home/livings/pam-rollback.sh --apply    # per-path restore
```

### Files
- `/home/livings/pam-faillock-lockdown.sh` (12 sections, idempotent)
- `/home/livings/admin-guard.sh` (hourly guard; `--dry-run` works without root)
- `/home/livings/pam-verify.sh` (read-only PASS/FAIL report)
- `/home/livings/pam-rollback.sh` (per-path restore + full stop)

## 2. Hermes — nothing is exposed right now

- `hermes-gateway.service` (user unit) active since 12:41, `status=0/SUCCESS`.
- **No messaging platforms enabled** (`platforms: {}`, "No messaging platforms
  enabled", "Channel directory built: 0 target(s)").
- No `.env`, no relay creds, `pairing/` empty, no `*_ALLOW_ALL_USERS` in the
  running process env, **no network listener** owned by hermes.
- Control socket `/home/livings/.hermes/gateway.sock` inside a `0700` dir.
- Source confirmed fail-closed: with no allowlist, authorization falls through to
  `_env_truthy("GATEWAY_ALLOW_ALL_USERS")` = deny.
- No unauthorized/denied/pairing events anywhere in the logs. The only matches
  were `tools.url_safety` correctly blocking a 127.0.0.1 request (SSRF guard
  working).

So no one is currently reaching hermes. Remaining hardening (all user-level, no
sudo needed, NOT yet done):
- `chmod -R go-rwx /home/livings/.hermes` (19 files are 0644, 14 dirs 0755;
  harmless today because the parent is 0700, but tighten it).
- systemd drop-in for the gateway unit: `UMask=0077`, `NoNewPrivileges`,
  `PrivateTmp`, `RestrictSUIDSGID`, `LockPersonality`, `ProtectKernelTunables`,
  `ProtectControlGroups`, `ProtectKernelModules`, `RestrictRealtime`.
- Write fail-closed `GATEWAY_ALLOW_ALL_USERS=false` + per-platform
  `<P>_ALLOW_ALL_USERS=false` into `~/.hermes/.env`.
- Same for opencode's own state: `~/.local/share/opencode`,
  `~/.config/opencode`, `~/.local/state/opencode` — not yet checked/locked.
- Add hermes exposure checks to `admin-guard.sh` (truthy ALLOW_ALL in .env or the
  gateway's `/proc/<pid>/environ` → neutralize + log; non-loopback hermes
  listener → log DRIFT).

### "Fix hermes" — what is actually broken
Nothing structural. Two error classes in `logs/errors.log`, both upstream:
- 14× `ERROR chat_completion_helpers: Streaming failed before delivery: Provider
  returned an empty response` + `APIError` retries — provider-side (nous
  `inference-api.nousresearch.com`). Retry logic already exists; nothing local
  to fix.
- 1× `WARNING cli: Terminal I/O broken (clear_screen) — freezing UI paints
  (#81521)` — known upstream TUI guard; it self-limits. If this is the symptom
  you are actually seeing, the workaround is `hermes --cli` instead of `--tui`,
  or launching via konsole. Tell me the symptom and I will target it.
- Nothing patched inside `/opt/hermes-agent` (vendored app) — no symptom was
  specific enough to justify a fork.

## 3. Your input/output vs other devs — audit result

Scanned every local git repo for tracked *and* historical transcript/log/secret
files (`.hermes/`, `agent.log`, `errors.log`, `gateway.log`, `.hermes_history`,
`sessions/`, `transcript`, `conversation`, `kanban.db`, `auth.json`,
`config.yaml`, `.opencode`, `messages.json`, `.env`, `chat_history`):

**0 hits in HEAD and 0 in history, across every repo checked.** Nothing of yours
has been committed or pushed. (Scan covered ~50 local repos before you aborted
it; 130 repos exist on GitHub. I can finish the remainder on request.)

## 4. Repo visibility — needs your decision, nothing changed yet

Rule you gave: security-minded repos private; only games and bugfixes public.

Security-minded repos are **already PRIVATE** — verified: `hermes-blood`,
`zen-hardening`, `lin-antimalware`, `shield-kitty`, `shield-kitty-forensics`,
`sin-archive-2026`, `work-automation`, `lia-cli`, `business-health-monitor`,
`business-debug-wrappers`, `buildlog`, `himalaya-bot`, `living-sin-*`,
`faucet-logins`, `web-bug-reports`, `wildhearts-linux-fixes`,
`once-human-linux-fixes`, `steam-linux-optimizations`, `waydroid-issues`.

**15 PUBLIC repos that are not games or bugfixes** → candidates to make private:
- clearly not games/bugfixes: `bch-faucet-web` (crypto faucet web app),
  `voynich-occult-corpus`, `garuda-tools-fresh`, `firedragon-flatpak-fresh`,
  `gaming-engineer-kb`
- game-adjacent but tooling/meta, your call: `gaming-portfolio`,
  `gaming-unified`, `loz-ocarina-mq`, `ringworld-redux`, `skyrim-ai-overhaul`,
  `skyrim-mod-packages`, `soh-masterquest-build`, `te-bonfire`,
  `The-Elder-Scrolls-Elsewhyr`, `The-Elder-Scrolls-Elsweyr`

**7 PRIVATE repos that are games/bugfixes** → candidates to publish, but I will
not publish anything without your explicit go (that is the disclosure direction):
`helldivers2-bugfixes`, `helldivers2-patched`, `non-steam-games`,
`once-human-linux-fixes`, `steam-linux-optimizations`, `waydroid-issues`,
`wildhearts-linux-fixes`

## 5. Still owed to you from earlier
- The crash-rebuild to-do list (restore `crypto-bot` + `bch-faucet-backup`
  checkouts, `bhm-self-watchdog.service` inactive, miner/faucet blockers,
  `business-health-monitor` `then then` syntax bug, archived lia corruption).
- Fleet-deployment questions (scope; DOGE address; RVN node route; BCH wallet;
  Polsia PayPal; sudo-dependent changes).
- Your stated agent policy is now implemented as: only `root` + `livings` are
  admin, your agents run under your authentication, unattended agent commands go
  through the scoped drop-in `/etc/sudoers.d/50-agent-scope` (template inactive,
  no root password stored anywhere).
