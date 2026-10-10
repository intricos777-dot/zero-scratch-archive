# Commit history, 2026-05-28 .. 2026-09-28 (all local clones, all branches)

Generated 2026-09-28T13:00:25-07:00 on host zero by opencode for the user-data archive.

## bch-faucet
```
ba90304|2026-09-26|livings|bch-faucet: rebuild backend lost to the machine rebuild
```

## bde-security-biometrics
```
9361ec0|2026-09-26|Living Sin|chore: stop tracking compiled Python bytecode
359cc45|2026-09-26|Living_Sin|hardlock: fail open when the biometric verifier is unavailable
1b51281|2026-09-26|Living Sin|security(tampermonkey): purge collector token from the userscript and history
0c1abe7|2026-09-21|sin|initial commit
938e3bd|2026-09-21|Living_Sin|feat: add tampermonkey liaison bridge user script
b6972de|2026-08-29|Living_Sin| untrack vendored .venv
ede6ef7|2026-08-18|intricos777-dot|chore: auto-commit pending changes
bc49bfa|2026-08-18|intricos777-dot|chore: auto-commit 1 changes
6353e81|2026-08-18|intricos777-dot|chore: auto-commit 3 changes
ae7dfa0|2026-08-18|intricos777-dot|Update PAM daemon, modules, scripts, and add void-browser
1fc816a|2026-08-07|intricos777-dot|chore: save working state before cleanup
299eff5|2026-08-07|intricos777-dot|Add web patrol: hourly AI-tracking detection, evidence archive, lawsuit package builder
823cc0b|2026-08-05|intricos777-dot|feat: add BDE HardLock patch and BlackArch package for biometric enforcement
5944b18|2026-08-05|intricos777-dot|feat: add BDE sync daemon, client, and wrapper integration for node network patrol
e0088c9|2026-08-05|intricos777-dot|feat: add void magic browser extension
d7ebff5|2026-08-05|intricos777-dot|init: BDE security and biometrics overhaul with PAM + docs + tampermonkey bridge
```

## buildlog
```
25bf65b|2026-09-26|Living_Sin|fix: fail2ban ignoreip exempted 10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16 -- written assuming a shared enterprise network where banning a /8 would 24h-ban a colleague. On a single-user local-only box that reasoning is void: no colleagues to protect, and the exemption covered the user's own whole network, so anyone failing five auth attempts walked away forever. Added narrow-fail2ban-ignoreip.sh: removes the /8, keeps loopback/link-local/own-address/gateway, all derived from the live system (ip addr + ip route) rather than hardcoded. Gateway stays exempt deliberately -- a ban against the next-hop router is indistinguishable from losing the network. Also rewrote the now-contradictory 'Never ban ... your own LAN' comment. Backs up, edits via python3 (value spans two continuation lines, sed is fragile there), validates with fail2ban-client -t, auto-restores on invalid output. NOTE: this makes future bans possible, it bans nobody now -- sshd is inactive and recidive only re-bans upstream bans. commit 5ffff93
11eb56c|2026-09-26|Living_Sin|fix: alert delivery was unlogged on success: notify-send is silent, and the code only logged on output or non-zero rc, so an empty log meant either 'delivered' or 'dropped'. That is the same ambiguity that hid the root-session-bus bug, where notifications failed while all status checks reported healthy. Both the datafile scanner and the hook test path now branch explicitly: 'alert delivered ok for <ip>' or 'alert DELIVERY FAILED for <ip> (rc=N): <output>'. Verified both branches with stub notifiers (silent rc=0, and rc=1 with stderr). commit 10ca689
0ea3fd4|2026-09-26|Living_Sin|fix: audit pass over the arpwatch work, 4 real defects. CRITICAL: scanner treated arp.dat as current state, but arpwatch only ADDS a row per mac/ip pair and never removes one, so one routine DHCP reassignment (laptop A yesterday, laptop B today, same IP) read as a permanent 2-MAC spoof that alerted once then said 'persists' forever -- guaranteed false positives on a /8 with lease churn. Fixed with a 1h window over the timestamp field arpwatch already writes; documented trade-off that a continuing spoof ages out after the window since the datafile cannot distinguish 'still spoofing' from 'seen once'. Also: ignored addresses were written to the state file, so un-ignoring one later made it match 'persists' and never alert. Installer: two mktemp -u calls left only one dir cleaned, orphaning a dir per root install; now one mktemp -d. Installer: units hardcoded /run/user/1000 while the installer resolved SUDO_USER for the home path; both now derived. 16/16 tests incl. both previously-broken cases; all scripts parse, all 3 units verify, no temp leak, notify path confirmed live. commit 3efc51f
054cd8e|2026-09-26|Living_Sin|fix: arp.dat stayed at 0 entries while arpwatch-spoof showed 'active (running)'. Root cause from SIGNALS in arpwatch(8): 'arpwatch updates arp.dat once every 15 minutes. The SIGHUP signal causes it to update immediately.' So the 2-min scan timer re-read the same stale file 7x, and an empty datafile is indistinguishable from a healthy one in systemctl status. The 101-byte arp.dat- is arpwatch's in-progress DB, not corruption. Fix: scan unit now SIGHUPs the collector (needs CAP_KILL against root) before reading, via a new -P /run/arpwatch-spoof.pid rather than pidof. Scan unit is root again BUT the session bus is now pinned to /run/user/1000 explicitly instead of derived from uid, which is what silently broke notifications before. Also added -D /var/lib/arpwatch: this build's compiled-in arpdir /usr/arpwatch does not exist, so arpwatch never found ethercodes.dat (shipped in /var/lib/arpwatch) and MAC vendor names were silently missing from all reports. commit 706c458
88428fc|2026-09-26|Living_Sin|fix: arpwatch-spoof showed 'active (running)' but two real defects were hidden behind it. (1) arpwatch-spoof-scan.service had no User=, inherited root, and the scanner resolves XDG_RUNTIME_DIR from its own uid -> /run/user/0, a bus that does not exist, so notifications would fail SILENTLY while the scan looked healthy. Now User=livings + explicit XDG_RUNTIME_DIR/DBUS. (2) install-arpwatch-spoof.sh ran 'install /dev/null $DB' unconditionally, TRUNCATING arp.dat on every re-run, destroying collected addresses while the collector was appending to it -- that is also why the datafile looked absent. Now created only when missing. Also /var/lib/arpwatch was 0750 root:root, locking livings out of the dir regardless of file mode; now 0755 + spoof-state 0644 livings:livings so dedup can be rewritten. WorkingDirectory=/var/lib/arpwatch to fix arpwatch's /usr/arpwatch chdir fallback to /. commit fafed7f
9885813|2026-09-26|Living_Sin|fix: install-arpwatch-spoof.sh appeared frozen on 'already installed'. Cause: my new parse-check ran 'arpwatch ARGS' in the foreground; under sudo that succeeds, opens the raw socket and NEVER RETURNS (-F is what keeps it foreground). The check had only ever been tested unprivileged, where arpwatch fails on the socket and exits at once -- the single case that returns. Fixed with 'timeout 3', treating exit 124 as success ('still running' == flags parsed); the real signal is absence of a usage message, valid under both root and unprivileged. Probe now uses a temp datafile. All 3 paths tested. commit 54050ec
4ce2282|2026-09-26|Living_Sin|fix: arpwatch-spoof STILL failed after the 3.9 rewrite: the culprit was -q. arpwatch(8) lists -q in the synopsis [-CdFNpqsvzZ] and describes it in OPTIONS, but the 3.9 binary rejects it and prints usage, exit 1. Tested every synopsis letter: -C -d -F -N -p -s -v -z -Z all accepted, -q is the sole exception, so the man page is wrong. arpwatch prints usage BEFORE opening the raw socket, so bad flags are detectable unprivileged -- added a parse-check to the installer reading ARPWATCH_ARGS shared with the unit, so it cannot drift again. commit fc71393
11781a4|2026-09-26|Living_Sin|fix: arpwatch-spoof.service exited 1 in a restart loop: I used original-LBL-arpwatch flags, but the extra-repo 3.9 build has NO -a exec hook, no -u, no -c, and wants -i INTERFACE not positional. Rewrote detection to poll the datafile via arpwatch-spoof-scan.sh on a 2min timer, unit now uses -F -i wlo1 -f arp.dat -s -q -N -z (-N matters, this is a /8 so most traffic looks like a bogon). Found+fixed 3 bugs: comma-based MAC counting false-alarmed on same MAC with different case; stale state file swallowed a returning spoof; installer/scanner/unit disagreed on the datafile name. 12/12 tests pass incl. dedup lifecycle and 5000-row scale. commit 7dc7a07
2f82326|2026-09-26|Living_Sin|fix: arpwatch installer aborted under sudo: 'hook not executable: /root/Projects/...'. sudo resets HOME to /root, so $HOME/Projects resolved into /root. Fixed by resolving the real home from SUDO_USER via getent and rewriting the unit path + Environment=HOME at install time. Also found a SECOND silent bug the same way: the hook is arpwatch's child, and arpwatch starts as root then drops privs with -u, which changes uid but NOT the environment -- so the hook had no DISPLAY/DBUS and every spoof notification failed while the log line still appeared. Fixed by reconstructing the session from /run/user/UID/bus. Verified: notify-send with only the bootstrapped vars exits 0, bare env fails 'Cannot autolaunch D-Bus'. commit b39490a
0de1ca8|2026-09-26|Living_Sin|fix: corrected an earlier claim of mine: kdeconnectd is NOT LAN-exposed. systemctl says inactive/not-found because it is a KDE session autostart app (app-org.kde.kdeconnect.daemon@autostart.service), and the workstation zone bound to wlo1 returns no for 1716/tcp, 1716/udp and 5353/udp -- firewalld drops it. No jail needed and none is possible (the daemon writes no journal entries, so a jail would match nothing, same as the inert sshd jail)
7bf46f7|2026-09-26|Living_Sin|ok: built ARP spoof detection (arpwatch 3.9-1 from extra, was entirely absent): arpwatch-spoof-alert.sh exec hook + arpwatch-spoof.service + install-arpwatch-spoof.sh, commit 3a65f5e. Alerts ONLY on flip-flop (one IP, two MACs); new hosts logged not alerted. NO auto-ban by design -- MAC randomisation makes flip-flops routine on a /8 with 16.7M other addresses, so a 24h ban would cut off colleagues; the 1-day ban stays with fail2ban where it keys on real auth attempts. 7/7 classification tests pass + live notify-send delivery verified. NOT INSTALLED, needs root
eb7c5ea|2026-09-26|Living_Sin|note: repo updated to match live: shield-kitty-fail2ban.local recidive enabled=true (c897508), confirmed deliberate by user, not drift. Repo and live now byte-identical on all functional lines. Preconditions verified before endorsing it: /var/log/fail2ban.log present (root:root 0600, 34K), loglevel=INFO in fail2ban.conf (below WARNING recidive silently never counts bans), backend=polling+logpath since the journal lacks fail2ban's own log. fail2ban-client -t passes with recidive on
21de717|2026-09-26|Living_Sin|note: THREE REAL GAPS found auditing 'ban remote access for 1 day': (1) ignoreip includes 10.0.0.0/8 and this machine IS 10.197.250.246/8, so 16,777,216 addresses on the local network are permanently EXEMPT from banning -- fail2ban cannot ban 'another system' on this network at all. (2) sshd jail is INERT: sshd inactive, nothing listens on 22. (3) kdeconnectd is LAN-exposed on *:1716 tcp+udp with NO jail -- the only real remote surface, unmonitored
1fd10c6|2026-09-26|Living_Sin|note: SYSTEM SPOOFING IS ENTIRELY UNCOVERED: no arpwatch, no suricata, no zeek, no tcpdump, no tpm2-tools installed, and zero spoofing logic in any repo. fail2ban structurally CANNOT do this -- it parses auth logs for repeated failures and has no notion of ARP/DHCP/hostname/MAC spoofing or rogue-device impersonation. This needs different tooling, and installing it needs root
1e6b395|2026-09-26|Living_Sin|note: 1-day fail2ban lockout was ALREADY live: bantime=86400 on sshd + recidive jails in /etc/fail2ban/jail.d/shield-kitty.conf, matches repo. firewalld is now active with the workstation zone, so firewallcmd-rich-rules bans ARE enforceable. Fixed stale docs in unban-self.sh + fail2ban-coverage.md that wrongly claimed bantime=-1 permanent (89506fc)
d1aaf2b|2026-09-26|Living_Sin|note: pam_faillock facts confirmed from local man pages: (1) unlock_time=0 means NEVER - needs 'faillock --user X --reset' as root, and man page warns it is an easy DoS target; (2) default dir /var/run/faillock is tmpfs so tallies AND any permanent lock vanish on reboot - real permanence needs dir= off tmpfs; (3) admin_group members are handled like root, so setting even_deny_root would defeat the exemption entirely. Live /etc/security/faillock.conf had NO admin_group, so livings was lockable; recover with 'sudo faillock --user livings --reset'
d7e0f23|2026-09-26|Living_Sin|fix: faillock: fixed 'audit = silent' (audit/silent are BARE FLAGS not key=value) and fixed group parsing that split on ',' instead of cutting field 4 from 'name:x:gid:mem1,mem2' -- old check passed unconditionally. unlock_time stays 30s, permanent lockout (0) NOT enabled: no other login users exist on this box anyway, and it is unrecoverable if the exemption breaks
078f31c|2026-09-26|Living_Sin|fix: faillock admin exemption PREPARED, NOT deployed (needs sudo). deploy-faillock-admin.sh orders it safely: backup -> create shield-admin -> enrol livings -> READ GROUP DB BACK -> only then install config naming admin_group, then write enroll.lock. Aborts if livings is not verifiably a member, because pam_faillock would otherwise lock the admin out like everyone else. Run: sudo ~/Projects/zen-hardening/deploy-faillock-admin.sh --check | deploy | --revert
329c152|2026-09-26|Living_Sin|ok: notifications already in place: shield-kitty-watch.service enabled+active, notify-send, no fullscreen takeover
4e898d9|2026-09-26|Living_Sin|fix: BDE hardlock was NOT installed, deliberately. Audit found install-hardlock.sh appended 'auth required pam_deny.so' to /etc/pam.d for login+sudo+gdm-password+sshd+su, and bde-auth exited non-zero on any exception, so a down daemon or missing socket = locked out of login/sudo/sshd. Fixed to fail open (bde-auth 359cc45): exit 2 = unavailable vs exit 1 = denied, BDE_FAILMODE defaults open, socket resolved via pwd not getuid (PAM runs as root), pam_deny.so removed, sshd opt-in, installer gains --dry-run + backups. NOT INSTALLED - needs sudo
66c0f11|2026-09-26|Living_Sin|seed-vcs-sources.sh: parse source names in bash, not grep
fd951b2|2026-09-26|Living_Sin|seed-vcs-sources.sh: stop deep-falling-back on unfetchable pins
92325fd|2026-09-26|Living_Sin|seed-vcs-sources.sh: pre-seed makepkg VCS sources as shallow mirrors
c757c9f|2026-09-26|Living_Sin|note: git identity was only set in nyan-gfsf-alert; zen-hardening/hermes-blood/buildlog could not be committed at all. Set global user.name/user.email to Living_Sin <intricos777-dot@users.noreply.github.com>. buildlog auto-commit works now
f2b97f5|2026-09-26|Living_Sin|fix: paru cache was wiped (~/.cache/paru/clone emptied, 6 repos incl. electron tarball + shallow chromium mirror). Re-cloned AUR electron34 and re-created the 1.3GB shallow chromium mirror (tag 132.0.6834.210, depth 1, refspec pinned to the single tag) so makepkg never full-clones again
6a3b8d7|2026-09-26|Living_Sin|fix: install.sh: was applying Great Vibes as global KDE UI font on every re-install. buildlog:47 records a lockout with that as prime suspect (calligraphy, Regular-only weight, reaching lock screen + dialogs). Font is now opt-in via BLOOD_GLOBAL_FONT=1; icon theme still applies. Live kdeglobals font/fixed restored to Fira Sans, matching the menuFont/toolBarFont the rest of the file already used. hermes-blood 84b2707
48082e2|2026-09-26|Living_Sin|env snapshot
2d83dd3|2026-09-26|Living_Sin|fix: resolve SCRIPT_DIR via $HOME, BASH_SOURCE is empty under fish shebang-less exec
3b020f1|2026-09-26|Living_Sin|buildlog: durable build journal tool
```

## business-debug-wrappers
```
54d0964|2026-09-26|Living_Sin|chore: ignore __pycache__
7301a28|2026-09-26|opencode|Fix hardcoded /home/sin and nonexistent Projects/security paths
3b368a7|2026-09-19|sin|feat: initial debug wrapper
```

## business-health-monitor
```
2b6ad46|2026-09-26|Living_Sin|fix: repair self-heal wrappers - syntax error and dead /home/sin paths
e1562d4|2026-09-26|opencode|Fix hardcoded /home/sin and nonexistent Projects/security paths
25c9f3e|2026-09-21|sin|fix: use --user for systemctl in crypto_watchdog
69d27c1|2026-09-21|sin|auto: daily maintenance
150e854|2026-09-21|sin|auto: daily maintenance
004eddd|2026-09-19|sin|feat: initial business health monitor
```

## component-resource-director
```
61eae6f|2026-09-26|livings|policy: real solo-rig unit names and a memory envelope that fits
73f8ae5|2026-09-26|x|component-resource-director: demand-driven per-service CPU/mem allocation with mining safety floor
```

## hermes-blood
```
cbdabcb|2026-09-26|Living_Sin|chore: add .gitignore
84b2707|2026-09-26|Living_Sin|install.sh: stop applying Great Vibes as global KDE UI font
2ae226a|2026-09-26|Living_Sin|fix: install voidlit to opencode theme/ lookup path and activate it in opencode.jsonc
a38327d|2026-09-26|Living_Sin|fonts: bump Great Vibes to 16pt across all components
f1ffc34|2026-09-21|sin|chore: tune gtk settings and install script
418e662|2026-08-21|Living_Sin|fix: ensure all components use Great Vibes font
5dfbfab|2026-08-21|Living_Sin|fix: remove stray ] from BlackRed.colorscheme Color7Intense and ForegroundIntense
f984a14|2026-08-20|Living_Sin|restore: switch font from Dancing Script to Great Vibes everywhere
b2dd840|2026-08-18|intricos777-dot|Blood Build: full system theme (black bg, red text, Dancing Script font)
968b304|2026-08-18|intricos777-dot|Blood skin + cursive fonts
```

## lia-cli
```
1e727cc|2026-09-26|Living Sin|fix(tests): kill the real server PID, not the setsid wrapper
41e3b0b|2026-09-26|Living Sin|test(inbox): isolate tests from the live collector
f0f6235|2026-09-26|Living Sin|feat(inbox): add lia-inbox collector for the Replika Tampermonkey bridge
609f4bc|2026-09-21|sin|feat: add signal handlers and health_check self-diagnostic
65bda31|2026-09-21|sin|feat: add coordination client, wallet, config and memory updates
b0e1b96|2026-08-15|Sin|Update task plans: mark all projects as completed
e52842f|2026-08-10|Sin|aisle: guardian auto-commit 2026-08-10
2079a89|2026-08-08|Sin|feat: add coinbase business signup form printer
028f96b|2026-08-08|Sin|feat: add Coinbase business signup profile generator
6bf5f7e|2026-08-08|Sin|feat: add Coinbase wallet and sweep coordination module
7cafbb0|2026-08-08|Sin|chore: add AI attribution CREDITS.md
91d91e1|2026-08-07|Sin|feat: add local-only RLM harness runtime integrated into Lia.CLI
39f544b|2026-08-07|Sin|chore: initial standalone repo for Lia CLI with supervisor
```

## lifsea-security-suite
```
c4a8f09|2026-09-26|Living Sin|tools: add validated static auditor; refresh snapshot past today's fixes
ec32f41|2026-09-26|Living Sin|chore: add gitignore for generated artefacts
d83a361|2026-09-26|Living Sin|import: buildlog (21 commits, upstream HEAD 2f82326)
ef807a0|2026-09-26|Living Sin|import: zen-hardening (10 commits, upstream HEAD b39490a)
f9438c6|2026-09-26|Living Sin|import: shield-kitty-forensics (3 commits, upstream HEAD 084cca4)
5dfb653|2026-09-26|Living Sin|import: shield-kitty (6 commits, upstream HEAD 0764685)
be2ab5b|2026-09-26|Living Sin|chore: initialise consolidated security suite repository
```

## lin-antimalware
```
3ea8d3a|2026-09-26|Living Sin|chore: stop tracking the threat-intel cache
662f207|2026-09-26|Living Sin|chore: stop tracking the threat-intel cache
c266365|2026-09-26|Living Sin|chore(intel): refresh threat cache after feed repair
6419b99|2026-09-26|Living_Sin|intel: fix a dead feed and stop swallowing fetch errors
53b7aff|2026-09-26|Living_Sin|fix: make the CLI, the test suite and the web dashboard actually runnable
4d304c3|2026-09-26|opencode|Fix hardcoded /home/sin and nonexistent Projects/security paths
806bfcf|2026-09-21|sin|auto: commit uncommitted changes before push
9e3dd8a|2026-08-05|intricos777-dot|chore: untrack __pycache__/*.pyc (now covered by .gitignore)
0c35889|2026-08-05|intricos777-dot|chore: generate initial scan and dredge reports
901b79c|2026-08-05|intricos777-dot|feat: add deep dredge intel nodes and threat feed agents
4864364|2026-08-05|intricos777-dot|feat: expand signatures, add system checks, quarantine commands, and complete CLI
6d88fef|2026-08-05|intricos777-dot|chore: add gitignore and remove generated scan report
8ea133c|2026-08-05|intricos777-dot|init: LinAntimalware draft with scanner, web dashboard, CLI, self-heal wrapper, and signatures
```

## linux-zen-build
```
b116218|2026-09-26|Living_Sin|miners: replace pool-pointing scripts with true solo mining
af121ec|2026-09-26|livings|security-stack: deploy scripts for the remaining BDE components
7a2426b|2026-09-26|livings|miners: add confirmed-block-preserving cache retention
37a98da|2026-09-21|sin|auto: commit uncommitted changes before push
a5e4386|2026-08-23|intricos777-dot|fix(post-snapshot): use mountpoint paths; verified against live btrfs layout
53cc69d|2026-08-23|intricos777-dot|linux-zen-build v1.0.0 stable: 21-layer encryption, miners, security stack rebuild
```

## shield-kitty
```
d1b9346|2026-09-26|Living_Sin|fix(devices): a ban that fails to write must be loud, not silent
6ac9830|2026-09-26|Living Sin|fix(devices): is_input_device fails safe on unreadable sysfs
0bb87c8|2026-09-26|Living Sin|fix(devices): parse ban attempt count as int; add lockout-safety tests
0764685|2026-09-26|Living_Sin|shield-kitty: check the evidence-write return code
3845292|2026-09-26|Living_Sin|shield-kitty: nyan cat notifications, drop USB noise, add device admission control
c9f7bc9|2026-09-26|opencode|Add tamper-evident evidence chain, seal timer, and fix service paths
fe2a4b5|2026-09-26|Living_Sin|shield-kitty: rename project, scripts and on-screen wordmark
ffd58fc|2026-09-26|Living_Sin|rename: nyan-gfsf-alert -> shield-kitty
edb9cd5|2026-09-26|Living_Sin|nyan-gfsf-alert: pixel-art nyan cat intrusion alert (PyQt6, zenity/kdialog/terminal fallbacks)
```

## shield-kitty-forensics
```
084cca4|2026-09-26|Living_Sin|chore: untrack __pycache__, add .gitignore
75a5ecb|2026-09-26|Living_Sin|fix: evidence verify reported CHAIN BROKEN on every legitimate post-seal record
7d9894e|2026-09-26|opencode|Add tamper-evident evidence chain, seal timer, and fix service paths
```

## zen-hardening
```
65b39ff|2026-09-26|Living_Sin|docs: handoff notes for the 2026-09-26 rebuild closeout
2c14eca|2026-09-26|Living_Sin|chore: closeout script for the 2026-09-26 hardening audit
b9d2d35|2026-09-26|Living_Sin|fix(warden): a DHCP lease renewal no longer causes a permanent ban
5e33384|2026-09-26|Living_Sin|docs: note the stray false.new/true.new test artifacts and how to remove them
1629831|2026-09-26|Living_Sin|feat(warden): preflight.sh — reboot readiness check, with a post-reboot mode
e6018a8|2026-09-26|Living_Sin|feat(warden): ownership registry, MAC-keyed bans, spoof detection, permanent blocks
b577929|2026-09-26|Living_Sin|feat(warden): auto-blacklist connecting devices + block remote-viewing tools
5ffff93|2026-09-26|Living_Sin|add narrow-fail2ban-ignoreip.sh: drop the 10.0.0.0/8 exemption
10ca689|2026-09-26|Living_Sin|log both alert outcomes, so silence is no longer ambiguous
ebe2c80|2026-09-26|Living_Sin|fix: installer left the old collector running, so -P never took effect
3efc51f|2026-09-26|Living_Sin|fix: scanner read arp.dat as current state, but it is append-only history
706c458|2026-09-26|Living_Sin|fix: arp.dat is written every 15 min, so the 2-min scan was reading stale data
fafed7f|2026-09-26|Living_Sin|fix: scan service ran as root, and installer truncated the live datafile
54050ec|2026-09-26|Living_Sin|fix: bound the arpwatch parse probe, which hung the install as root
fc71393|2026-09-26|Living_Sin|fix: drop -q, which arpwatch 3.9 documents but rejects
7dc7a07|2026-09-26|Living_Sin|fix: rewrite integration for arpwatch 3.9, which has no exec hook
7ff38f9|2026-09-26|Living Sin|fix(arpwatch): real selftest, and fix the empty infrastructure exclusion list
b39490a|2026-09-26|Living_Sin|fix: resolve paths via SUDO_USER, bootstrap session env for notify
3a65f5e|2026-09-26|Living_Sin|security: add ARP spoof detection via arpwatch, notifying via Shield Kitty
29355eb|2026-09-26|Living Sin|feat(zen): rebuild sentinel, watchman and bchn-monitor
c897508|2026-09-26|Living_Sin|fail2ban: recidive enabled=true in repo, matching live by request
89506fc|2026-09-26|Living_Sin|docs: correct stale permanent-ban claims to the actual 86400
819c363|2026-09-26|Living_Sin|faillock: add ordered deploy script, fix malformed audit/silent flags
207f22e|2026-09-26|Living_Sin|chore: ignore __pycache__
6aa717a|2026-09-26|Living_Sin|zen-hardening: unban-self escape hatch, and honest fail2ban coverage doc
562afd4|2026-09-26|Living_Sin|faillock: single-admin exemption via a dedicated group, with a refusal gate
2fe0d82|2026-09-26|Living_Sin|zen-hardening: sysctl, faillock and firewalld workstation hardening configs
```

## aeronautical-programming
```
09d9089|2026-08-04|intricos777-dot|chore: add gitignore and strip local artifacts
c783e2d|2026-08-03|intricos777-dot|docs: add placeholder index for GitHub Pages
511b7da|2026-08-03|intricos777-dot|chore: scaffold aeronautical-programming project
```

## aerospace-simulation-foundation
```
38af2b0|2026-09-21|sin|chore: untrack python bytecode, ignore __pycache__
e1c255b|2026-08-03|Simulator|fix: resolve import cycles and add orbital period alias
674e736|2026-08-02|Simulator|Fix all import errors and complete working framework
e0b9e49|2026-08-02|Simulator|Initial release: Aerospace Simulation Foundation v1.0.0 with trajectory simulation, orbital mechanics, control systems, and theoretical antigravity propulsion models
```

## aerovora
```
f08da21|2026-09-21|sin|chore: add site gitignore
42086bd|2026-08-05|intricos777-dot|Seed README
65bce2c|2026-08-03|intricos777-dot|fix: replace hardcoded host with localhost for local backend
bf4f630|2026-07-21|intricos777-dot|Deploy
a451b60|2026-06-23|intricos777-dot|Add success/cancel banner after Stripe Checkout redirect
eb9bde9|2026-06-22|intricos777-dot|Add order tracking + Ops dashboard link
c9ffd5f|2026-06-21|intricos777-dot|Wire up Stripe publishable key and price IDs
e842a9b|2026-06-21|intricos777-dot|Add Stripe Checkout integration
a3e051c|2026-06-20|intricos777-dot|Storefront + investor page
```

## aerovora-industries
```
efdc43f|2026-09-21|sin|chore: gitignore adjustments; add storefront content
c3f040a|2026-08-05|intricos777-dot|Seed README
ed9dad3|2026-07-19|intricos777-dot|Update: firmware tools v4.2, carrier diversity, Stripe→PayPal routing, systemd fix
180897d|2026-06-23|intricos777-dot|Add .env loading to run.sh, fix relative imports for systemd
5908c25|2026-06-23|intricos777-dot|Marketing execution: consolidated console, fix scripts, generate ad schedule
29b6113|2026-06-23|intricos777-dot|Fix package imports — add __init__.py, use relative imports
031ffde|2026-06-23|intricos777-dot|Fix Stripe webhook line items, DaaS SKU mapping, add success banner and .env.example
9a84412|2026-06-22|intricos777-dot|Add production-fulfillment backend, dashboard, Polsia agent modules, order tracking
1af5fe0|2026-06-21|intricos777-dot|Wire up Stripe prices and publishable key
41c54af|2026-06-20|intricos777-dot|Add investor pitch deck page
b7279e1|2026-06-20|intricos777-dot|Clean up, add storefront files
e676ad8|2026-06-20|intricos777-dot|Aerovora Industries — full company
de3a944|2026-06-20|intricos777-dot|Aerovora Industries — full company structure
```

## ai-autonomy-framework
```
358fb1b|2026-09-21|sin|fix: harden self-heal script
2365cdb|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
19767ee|2026-08-08|intricos777-dot|aisle: guardian auto-commit 2026-08-08
3611b2d|2026-08-08|intricos777-dot|chore: initialize repo with service automation scaffold
```

## A.I.-bridge-skills
```
cb6003b|2026-09-21|sin|init: bridge skills manifest and scaffolding
```

## ai-teacher-robot-pairing
```
930d599|2026-09-21|sin|chore: untrack python bytecode, ignore __pycache__
938bd63|2026-08-04|sin|feat: add parent-robot intermediary app with check-ins + emergency escalation
fc990b4|2026-08-04|sin|init: agent-based education sim with learning styles + robot pairing
```

## bch-faucet-backup
```
beb75bd|2026-09-21|sin|Initial backup: BCH faucet wallet + config
```

## bch-faucet-web
```
d267514|2026-09-21|sin|Fix: relative API path for same-origin Caddy proxy
c4521a0|2026-09-21|sin|Fix: use same-origin API URL for Caddy proxy
b100031|2026-09-21|sin|Fix API URL for HTTPS compatibility
c7cd744|2026-09-21|sin|Fix: restore index.html from faucet project
1f7e966|2026-09-21|sin|Trigger Pages rebuild
0b9c1bb|2026-09-21|sin|Update API URL for faucet server
d305d7e|2026-09-21|sin|Initial commit: BCH faucet frontend
```

## bde-security-biometrics
```
b523fb5|2026-09-21|sin|initial commit
cf22536|2026-09-21|Living_Sin|feat: add tampermonkey liaison bridge user script
b6972de|2026-08-29|Living_Sin| untrack vendored .venv
ede6ef7|2026-08-18|intricos777-dot|chore: auto-commit pending changes
bc49bfa|2026-08-18|intricos777-dot|chore: auto-commit 1 changes
6353e81|2026-08-18|intricos777-dot|chore: auto-commit 3 changes
ae7dfa0|2026-08-18|intricos777-dot|Update PAM daemon, modules, scripts, and add void-browser
1fc816a|2026-08-07|intricos777-dot|chore: save working state before cleanup
299eff5|2026-08-07|intricos777-dot|Add web patrol: hourly AI-tracking detection, evidence archive, lawsuit package builder
823cc0b|2026-08-05|intricos777-dot|feat: add BDE HardLock patch and BlackArch package for biometric enforcement
5944b18|2026-08-05|intricos777-dot|feat: add BDE sync daemon, client, and wrapper integration for node network patrol
e0088c9|2026-08-05|intricos777-dot|feat: add void magic browser extension
d7ebff5|2026-08-05|intricos777-dot|init: BDE security and biometrics overhaul with PAM + docs + tampermonkey bridge
```

## beverage-company
```
eb80085|2026-08-10|intricos777-dot|feat: add game studio collab beverages incl Sunset Sasparilla + studio filters
acc8992|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
6118da4|2026-08-08|intricos777-dot|chore: add BDE self-heal/debug patrol scripts
92bcc5e|2026-08-08|intricos777-dot|chore: sync service automation changes
6564726|2026-08-08|intricos777-dot|chore: add service automation scaffold, wrappers, tests, BDE, vm bootstrap
2c36c9f|2026-08-08|intricos777-dot|feat: scaffold beverage company with global drink catalog and BDE security
```

## black-ops-2-elysium
```
aeba41d|2026-09-21|sin|wave 2: add game content
222d43d|2026-09-21|sin|feat: BO2 canon — full arsenal, Pick-10 perks/scorestreaks fixed, Zombies vault (TranZit→Origins, Ray Gun AK Pattern rarest box drop)
702b998|2026-09-21|sin|auto: commit uncommitted changes before push
370a339|2026-08-11|user.email|feat: add 50-player localized P2P lobby scaffolding
4339552|2026-08-11|user.email|aisle: guardian auto-commit 2026-08-11
dbfc483|2026-08-11|user.email|feat: casual/legend difficulties + 50-player zLobbies; fix dream launcher import & repo-relative engine roots
4fe4c23|2026-08-11|intricos777-dot|Merge commit 'd2648a5d54645c3ed118c37d99233255894e9fe1' as 'tools/twilight-elysium'
d2648a5|2026-08-11|intricos777-dot|Squashed 'tools/twilight-elysium/' content from commit 0a28cff
6a8d323|2026-08-11|intricos777-dot|feat: add BO2 data schemas and map stubs
cc365f9|2026-08-10|intricos777-dot|feat: scaffold bo2-elysium public repo structure
```

## business-debug-wrappers
```
7301a28|2026-09-26|opencode|Fix hardcoded /home/sin and nonexistent Projects/security paths
3b368a7|2026-09-19|sin|feat: initial debug wrapper
```

## business-health-monitor
```
e1562d4|2026-09-26|opencode|Fix hardcoded /home/sin and nonexistent Projects/security paths
25c9f3e|2026-09-21|sin|fix: use --user for systemctl in crypto_watchdog
69d27c1|2026-09-21|sin|auto: daily maintenance
150e854|2026-09-21|sin|auto: daily maintenance
004eddd|2026-09-19|sin|feat: initial business health monitor
```

## clean-plastics-sim
```
40afe8a|2026-09-21|sin|chore: untrack python bytecode, ignore __pycache__
f8aff08|2026-08-04|sin|init: clean plastics materials simulator with osmosis + heat retention + durability
```

## code-theft-evidence
```
fc75707|2026-08-15|intricos777-dot|feat: add deep scan evidence and infringement reports
cc82513|2026-08-10|intricos777-dot|aisle: guardian auto-commit 2026-08-10
ce520ce|2026-08-09|intricos777-dot|aisle: guardian auto-commit 2026-08-09
c483942|2026-08-09|intricos777-dot|chore: add deep-scan evidence 2026-08-08
9a2f5f9|2026-08-08|intricos777-dot|chore: add deep-scan evidence 2026-08-08
454c8c9|2026-08-08|intricos777-dot|evidence: add hermes-agent-self-evolution-asshole to infringement inventory
14e3098|2026-08-08|intricos777-dot|docs: push latest evidence package and counsel contact updates
062382c|2026-08-08|intricos777-dot|docs: set counsel contact email to intricos73@gmail.com
b568beb|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
374f04f|2026-08-08|intricos777-dot|evidence: add identity correlation for Baal-TehDriverman / Eric Matthew Hill / Lilith-Systems
88a05b3|2026-08-08|intricos777-dot|aisle: guardian auto-commit 2026-08-08
c57eba5|2026-08-08|intricos777-dot|review: add README-FOR-COUNSEL index for Baal-TehDriverman package
27739b6|2026-08-08|intricos777-dot|evidence: add expanded similarity analysis for Baal-TehDriverman profile
497b856|2026-08-08|intricos777-dot|feat: prepare GitHub DMCA submission package for Baal-TehDriverman review
8ad358a|2026-08-08|intricos777-dot|evidence: flag Baal-TehDriverman profile with suspicious repos
bc72c19|2026-08-08|intricos777-dot|feat: add hourly BDE deep scan + takedown runbook
3fda47b|2026-08-08|intricos777-dot|feat: add IP evidence manifest, DMCA templates, monitoring checklist
8384c90|2026-08-08|intricos777-dot|chore: add evidence dirs and chain-of-custody doc
adb5a9e|2026-08-08|intricos777-dot|chore: initialize evidence repo scaffold
```

## coinbase-agent-tools
```
44bdcb9|2026-08-09|intricos777-dot|aisle: guardian auto-commit 2026-08-09
a8b0912|2026-08-08|intricos777-dot|chore: update deps and add tsconfig/gitignore
53c9d91|2026-08-08|intricos777-dot|init: coinbase-agent-tools
```

## cold-fusion-mini
```
31b50b0|2026-08-03|intricos777-dot|chore: trigger Pages rebuild
3c227ec|2026-08-03|intricos777-dot|chore: ignore pycache and cleanup Pages index
ebe9851|2026-08-03|intricos777-dot|docs: add Pages placeholder index
746cf04|2026-08-03|intricos777-dot|chore: scaffold compact reactor simulation framework
```

## coordination-server
```
6bf314c|2026-09-28|Living_Sin|chore: untrack node_modules/
1015d6c|2026-09-21|Coordination Server|chore: cluster secret placeholders, operation logs, connection test script
7dc3fc1|2026-09-11|Coordination Server|Add Railway deployment config
f541913|2026-09-11|Coordination Server|Initial commit: Coordination server with OCAP, federation, streaming
```

## crypto-bot
```
64734d6|2026-09-21|Living_Sin|SHIB stacking strategy: skip withdraw when asset===swapTarget, graceful convert fallback
60e9845|2026-09-18|Living_Sin|Upgrade coinbase-api to 1.2.6 and rewire profit sink onto brokerage withdrawals API
373a805|2026-09-17|Living_Sin|Add API key auth middleware, rate limiting (30/min global, 5/min /exec), and start-bot.sh
1cb73b0|2026-09-11|Living_Sin|fix: restore isMain guard in server, add error logging to send_stats_to_api, pin allowScripts versions
cf7586a|2026-08-29|Living_Sin| untrack encrypted faucet credential store
3f5e31e|2026-08-15|intricos777-dot|feat: add opensea integration, mining block predictor, api updates
6f52021|2026-08-08|intricos777-dot|feat: add mining-rig harness and mining config
e0088fe|2026-08-08|intricos777-dot|chore: add self-heal/debug wrappers and BDE patrol for crypto-bot
666be95|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
771aafe|2026-08-08|intricos777-dot|aisle: guardian auto-commit 2026-08-08
b285197|2026-08-08|intricos777-dot|security: stop tracking .env secrets; add gitignore
a577769|2026-08-08|intricos777-dot|chore: initialize repo with service automation scaffold
```

## crypto-dashboard
```
eacfee8|2026-09-28|Living_Sin|docs: make .env.example match the variables the app actually reads
ed1e294|2026-09-28|Living_Sin|chore: untrack .env
004e665|2026-09-21|Living_Sin|auto: commit uncommitted changes before push
cd0207c|2026-09-08|Living_Sin|docs: add security monitoring section with auditd references
dafeed4|2026-09-08|Living_Sin|feat: add utils.ts with formatNumber, timeAgo, getPnlBgColor
ae2184a|2026-08-29|Living_Sin| untrack .env from VCS
4b39fd5|2026-08-08|intricos777-dot|chore: add self-heal/debug wrappers and BDE patrol for crypto-dashboard
ffc9ede|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
94e8384|2026-08-08|intricos777-dot|feat: add satellite grid tab to crypto dashboard
```

## dental-ai-agent
```
b04a9ef|2026-09-19|sin|feat: initial dental AI agent system
```

## design-miner
```
c97ce6a|2026-08-05|intricos777-dot|Add idempotency guards and verify deep scraper import/compilation
34ca481|2026-08-05|intricos777-dot|Add design miner with surface/deep scrapers, botchains, notify, and permission tasklist
```

## DivineDirector
```
c165d9e|2026-07-20|intricos777-dot|Initial commit: DivineDirector OBSE plugin for Oblivion AI overhaul
```

## dot-hack-remake
```
2ac42b6|2026-09-21|sin|wave 2: add game content
8183363|2026-08-18|intricos777-dot|feat: Reinitialize repo with source code only (removed 4.7GB Content/ directory)
```

## fate-engine
```
9180fcc|2026-08-10|intricos777-dot|init: fate-engine scaffold with chaos attractors and narrative structures
```

## faucet-logins
```
c992dc7|2026-09-21|intricos777-dot|auto: commit uncommitted changes before push
f0efa66|2026-09-08|intricos777-dot|Document live-batch findings + operator crux (solver key vs headed manual)
b62fde0|2026-09-08|intricos777-dot|Live batch learnings: FaucetPay geo-wall (blocked_skip), overlay-force-click retry, geo/refusal markers in outcome detection, forensic probe tool
1923bc7|2026-09-08|intricos777-dot|Toolset: config-driven signup engine, captcha facade, store mirror reader, enriched ledger with live recon, dry-run verified
28d050b|2026-09-08|intricos777-dot|Mirror encrypted store + salt (resumable baseline); only ciphertext in git
73323c1|2026-09-08|intricos777-dot|Scaffold: faucet ledger, shortlist, findings, toolset blueprint
```

## firedragon
```
55c3a02|2026-09-21|sin|feat: extend control-panel server
34fa8fa|2026-08-10|intricos777-dot|feat: add OperaGX-compatible prefs + gx-music library shuffle tool
a979ad0|2026-08-07|intricos777-dot|test: add unittest suite for packaging/manifest/control panel
a6cecf6|2026-08-07|intricos777-dot|feat: wire sidebar module bus, popup, manifest, background actions
98ede2e|2026-08-07|intricos777-dot|Finish control panel: backend API, theme list/apply flow, serve.sh
690f24f|2026-08-07|intricos777|Remove pyc cache from git and update gitignore
25d215f|2026-08-07|intricos777|Add sidebar chrome, module bus, control panel, theme installer, icons
0cdcecf|2026-08-07|intricos777|Add GitHub Pages docs site for Firedragon
544aca7|2026-08-07|intricos777|Remove pyc cache artifacts
fe9b447|2026-08-07|intricos777|Add README with setup and extension compatibility instructions
1b7175f|2026-08-07|intricos777|Scaffold Firedragon browser: profile, modules, sidebar, ext-compat, launcher
```

## firedragon-flatpak-fresh
```
713846f|2026-09-18|intricos777|fix: revert to 24.08 runtime for GLIBC_2.42 compatibility
ea32d09|2026-09-06|flathubbot|Update firedragon-x64, firedragon-arm64 and firedragon modules
8b3c00b|2026-09-02|flathubbot|Update firedragon-x64, firedragon-arm64 and firedragon modules
d95ee08|2026-08-27|flathubbot|Update firedragon-x64, firedragon-arm64 and firedragon modules
03c6fd2|2026-08-21|flathubbot|Update firedragon-x64, firedragon-arm64 and firedragon modules
dce6562|2026-08-15|flathubbot|Update firedragon-x64, firedragon-arm64 and firedragon modules
1d61934|2026-08-12|flathubbot|Update firedragon-x64, firedragon-arm64 and firedragon modules
40ebcf7|2026-08-09|flathubbot|Update firedragon-x64, firedragon-arm64 and firedragon modules
26b0572|2026-08-05|flathubbot|Update firedragon-x64, firedragon-arm64 and firedragon modules
b1ef0ae|2026-08-05|Stefan Wimmer|docs: Update README
29d9705|2026-08-02|flathubbot|Update firedragon-x64, firedragon-arm64 and firedragon modules
02457f9|2026-07-30|flathubbot|Update firedragon-x64, firedragon-arm64 and firedragon modules
257c642|2026-07-17|Stefan Wimmer|chore: Update for v13
```

## gaming-engineer-kb
```
b539409|2026-09-21|intricos777-dot|gaming-engineer-kb: knowledge library for 3D modeling, world creation, animation
```

## gaming-portfolio
```
134ab9e|2026-09-21|sin|SEO: aliases (Intricos Deathfall, Living_Sin) in head + Person schema, canonical, OG/Twitter, sitemap, robots, fix PS handle typos
6d83097|2026-08-06|intricos777-dot|feat: wire merch cards to live Living Sin storefront (PayPal -> intricos777@gmail.com)
1fb251b|2026-08-06|intricos777|Deploy gaming portfolio: achievements showcase, merch integration, fade toggle
```

## gaming-unified
```
d341467|2026-08-15|intricos777-dot|Remove twilight-elysium from gaming-unified (will be separate repo)
0006120|2026-08-10|intricos777-dot|aisle: guardian auto-commit 2026-08-10
69a9937|2026-08-09|intricos777-dot|remove: promoted twilight-elysium to its own private repo
0aaa785|2026-08-09|intricos777-dot|Clean up: remove embedded git dirs, sensitive keys, binaries, caches
9252480|2026-08-09|intricos777-dot|Initial commit: Unified gaming monorepo
```

## garuda-tools-fresh
```
b47b466|2026-09-18|intricos777|fix: shellcheck hygiene improvements for ISO build scripts
57325fa|2026-09-05|Nico Jensch|feat(util-iso): also record edition in garuda-release file
799ca1f|2026-08-30|Nico Jensch|fix(util): use light text for non-active items
5c45ad3|2026-08-23|Nico Jensch|fix(util-iso-image): use actual release codename for calamares, update defaults
8ca11e0|2026-08-22|Nico Jensch|fix(util-yaml): use working kde endpoints for locale and timezone derivation
43daea1|2026-08-19|Nico Jensch|feat: default to our own arch mirror as kernel.org was timing out constantly
79114b6|2026-08-08|Nico Jensch|fix(util-iso): prepend root for chmod
25e4a0f|2026-08-07|TNE|fix(style): Fix code style of last commit
b917ca9|2026-08-07|Nico Jensch|fix(buildiso): do not chown root path inside chroot
55541cc|2026-08-07|TNE|fix(util-iso): Fix permissions for plasmalogin for use via overlays
c70948f|2026-08-06|Nico Jensch|ci: migrate to gitlab-ci-common templates
df9fac0|2026-08-02|Nico Jensch|feat(buildall): add cosmic
d24f1cb|2026-07-31|TNE|fix(dracut): Add squashfs module
88479bf|2026-07-31|TNE|fix(dracut): Add isofs module
a24a501|2026-07-21|Nico Jensch|fix(util-iso-image): clean btrfs subvolumes on chroot clean, because otherwise it be deleted
be5367f|2026-07-21|Nico Jensch|feat(util): default to linux-garuda as kernel
38b420b|2026-07-17|Nico Jensch|feat(util-yaml): add support for plasmalogin
```

## half-life-2-elysium
```
c5d6428|2026-09-21|sin|wave 2: add game content
60da685|2026-09-21|sin|HL2 Combine bestiary completed to City 17 canon
6e3e0de|2026-09-21|sin|auto: commit uncommitted changes before push
74318c8|2026-08-11|intricos777-dot|feat: scaffold half-life-2-elysium elysium build — engine, game data, casual/legend difficulties
```

## half-life-elysium
```
dc4879b|2026-09-21|sin|wave 2: add game content
4e2b05a|2026-09-21|sin|HL1 bestiary completed to Black Mesa canon
c358140|2026-09-21|sin|auto: commit uncommitted changes before push
11c3e94|2026-08-11|intricos777-dot|feat: scaffold half-life-elysium elysium build — engine, game data, casual/legend difficulties
```

## helldivers2-bugfixes
```
c35ce33|2026-09-18|sin|Helldivers 2 bug fixes & troubleshooting guide
```

## helldivers2-patched
```
5ebff93|2026-09-16|intricos777-dot|Helldivers 2 patch chronicle: root cause, seals, and launch recipe
```

## hermes-blood
```
2ae226a|2026-09-26|Living_Sin|fix: install voidlit to opencode theme/ lookup path and activate it in opencode.jsonc
a38327d|2026-09-26|Living_Sin|fonts: bump Great Vibes to 16pt across all components
f1ffc34|2026-09-21|sin|chore: tune gtk settings and install script
418e662|2026-08-21|Living_Sin|fix: ensure all components use Great Vibes font
5dfbfab|2026-08-21|Living_Sin|fix: remove stray ] from BlackRed.colorscheme Color7Intense and ForegroundIntense
f984a14|2026-08-20|Living_Sin|restore: switch font from Dancing Script to Great Vibes everywhere
b2dd840|2026-08-18|intricos777-dot|Blood Build: full system theme (black bg, red text, Dancing Script font)
968b304|2026-08-18|intricos777-dot|Blood skin + cursive fonts
```

## hermes-cli
```
fe4fb82|2026-09-21|Hermes.CLI|chore: update hermes CLI and state ledger
21cfbe4|2026-09-08|Hermes.CLI|test sync
```

## hermes-security-scripts
```
46fd939|2026-09-26|opencode|Close SSH hole; add anonymisation and deferred trusted-zone scripts
36e2e1b|2026-09-26|opencode|Add zen-hardening configs and Shield Kitty intrusion tooling
555a3bf|2026-08-08|intricos777-dot|feat: add polsia/lia/hermes secure wrappers and strict config snapshot
deb9091|2026-08-08|intricos777-dot|chore: add strict hermess config snapshot and secure wrappers
ae38615|2026-08-08|intricos777-dot|feat: hermes agent secure wrappers and BDE patrol scripts
```

## hermes-self-evolve
```
ae4eddf|2026-09-21|sin|fix: refine evolve patrol and self-heal scripts
3170a82|2026-08-08|intricos777-dot|chore: update supervisor and smoke tests
f4616e0|2026-08-08|intricos777-dot|init: hermes-self-evolve local replacement
```

## himalaya-bot
```
d9cfff0|2026-09-21|sin|feat: add signal handlers and health_check self-diagnostic
36e6daa|2026-09-21|sin|initial commit
```

## himalaya-exchange
```
d51e9b4|2026-09-28|Living_Sin|chore: untrack node_modules/
0a68960|2026-08-29|Living_Sin| untrack node_modules
8cd56aa|2026-08-09|intricos777-dot|aisle: guardian auto-commit 2026-08-09
8767608|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
bae6c47|2026-08-08|intricos777-dot|chore: initialize repo with service automation scaffold
```

## japanese-imports-llc
```
5fa6d4f|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
c7c5cdd|2026-08-08|intricos777-dot|chore: add BDE self-heal/debug patrol scripts
431bce7|2026-08-08|intricos777-dot|chore: sync service automation changes
6d9cf0a|2026-08-08|intricos777-dot|chore: add service automation scaffold, wrappers, tests, BDE, vm bootstrap
bbcaf6b|2026-08-08|intricos777-dot|feat: add per-project VM bootstrap config for neuromorphic node
e3c7f24|2026-08-08|intricos777-dot|copyright: add proprietary rights notice for self-built tooling and industry systems
a12494a|2026-08-08|intricos777-dot|chore: normalize data files and clean pycache
14ca9f8|2026-08-08|intricos777-dot|chore: clean pycache and normalize ignores
28f5500|2026-08-08|intricos777-dot|chore: normalize data files and clean pycache
50c470e|2026-08-08|intricos777-dot|chore: clean pycache and normalize data files
07dc9a1|2026-08-08|intricos777-dot|chore: remove __pycache__
e73f3a9|2026-08-08|intricos777-dot|feat: add shipment manifest generator and discovery scaffold
0a0c82a|2026-08-08|intricos777-dot|chore: remove __pycache__ and clean up
2ecf36a|2026-08-08|intricos777-dot|feat: add supplier registry integration tests and mind registry updates
2952fb1|2026-08-08|intricos777-dot|feat: bootstrap japanese-imports-llc with self-heal/debug wrappers, BDE security, tests
```

## kali-zen-suite
```
f8c9b0e|2026-08-05|intricos777-dot|chore: add .gitignore (drop __pycache__)
8983323|2026-08-05|intricos777-dot|fix: add security headers to vuln-app, clean stale test artifacts
6c2340d|2026-08-05|intricos777-dot|Add containerized exploit testbed, scan wrapper, and vulnerable-app patches
50b53d3|2026-08-05|intricos777-dot|Add separate Red Hat / Black Hat / White Hat toolset files
dcb1266|2026-08-05|intricos777-dot|Add Red Hat / Black Hat / White Hat hacking toolset
7db6e7f|2026-08-05|intricos777-dot|feat: add Kali toolsets and custom repo definitions for Zen Suite
1b28e97|2026-08-05|intricos777-dot|init: Kali Zen Suite live-build profile with zen kernel + credits
```

## kingdom-hearts-zero
```
b3cbe43|2026-09-21|sin|feat: FF7R-flavored combat - ATB gauge, pressure/stagger, Echo partner
7e75b2f|2026-09-21|sin|feat: keyblade master gate + moogle bazaar forge; coalesce worldflesh
d23cb9c|2026-09-21|sin|docs: The Charter of Zero — new lore doctrine (liminal, Door, Twilight Keyblade, Last Forge, Observer, Motes)
a60ac31|2026-09-21|sin|feat: zero nobody-sora character, mythic block + zone ledger, post-reorg path repairs
a171e6b|2026-09-21|sin|chore: untrack python bytecode, ignore __pycache__
bccb71b|2026-08-09|intricos777-dot|aisle: guardian auto-commit 2026-08-09
e1be1f8|2026-08-08|intricos777-dot|feat: command deck real rendering polish + save/load deck state
44f9e96|2026-08-08|intricos777-dot|feat(act2): seal-ledger world gating + Nobody sightings in the grid hub
71f066e|2026-08-08|intricos777-dot|feat: add per-project VM bootstrap config for neuromorphic node
463ba0a|2026-08-08|intricos777-dot|copyright: add proprietary rights notice for self-built tooling and industry systems
fa76b35|2026-08-08|intricos777-dot|test: fix combat_session_test data paths for build cwd
a71adfe|2026-08-08|intricos777-dot|feat: act-one combat expansion, tron shell UI updates, credits data, combat tests
b600081|2026-08-07|intricos777-dot|test: add unittest suites for traversal, save/deck, command deck
450a1a6|2026-08-07|intricos777-dot|fix: act-one traversal JSON parsing, map validation, combat damage math
a18f37b|2026-08-07|intricos777-dot|feat: act one traversal/collision, save system, combat fixes
424f2f9|2026-08-07|intricos777-dot|chore: ignore local audio assets
0eb188e|2026-08-07|intricos777-dot|act one: combat/data/save/docs, command deck wiring, act-one traversal scaffold
8443a64|2026-08-07|intricos777-dot|act one: traverse town via SceneGraph, beat-advancing Tron adventure, command action resolution
1b6b062|2026-08-07|intricos777-dot|chore: save working state before cleanup
3a75e3b|2026-08-06|Joshua Allen Cole Scott|visual game shell: PS2-style KH1/KH2 shaders, Tron world-select hub, KH1+KH2 world lore manifests, terminal adventures on twilight-elysium engine
555f6ca|2026-08-06|Joshua Allen Cole Scott|scaffold: world-synced command deck UI, Ansem-narrated prologue, checksummed save (twilight-elysium engine)
```

## landbridge
```
c2ff5b0|2026-08-11|intricos777-dot|feat: LandBridge — global trucker shipping/receiving GPS (FastAPI + phone PWA, SSE live tracking, ELD-lite logs)
```

## lead-gen-system
```
5e3895e|2026-09-19|sin|feat: initial lead generation system
```

## lia-cli
```
609f4bc|2026-09-21|sin|feat: add signal handlers and health_check self-diagnostic
65bda31|2026-09-21|sin|feat: add coordination client, wallet, config and memory updates
b0e1b96|2026-08-15|Sin|Update task plans: mark all projects as completed
e52842f|2026-08-10|Sin|aisle: guardian auto-commit 2026-08-10
2079a89|2026-08-08|Sin|feat: add coinbase business signup form printer
028f96b|2026-08-08|Sin|feat: add Coinbase business signup profile generator
6bf5f7e|2026-08-08|Sin|feat: add Coinbase wallet and sweep coordination module
7cafbb0|2026-08-08|Sin|chore: add AI attribution CREDITS.md
91d91e1|2026-08-07|Sin|feat: add local-only RLM harness runtime integrated into Lia.CLI
39f544b|2026-08-07|Sin|chore: initial standalone repo for Lia CLI with supervisor
```

## lia-groq-bridge
```
ab56719|2026-09-28|Living_Sin|chore: untrack node_modules/
0ac573e|2026-09-19|sin|security: add rate limiting, helmet, input sanitization, remove shell injection
12b89b4|2026-08-29|Living_Sin| untrack node_modules
d006c03|2026-08-18|intricos777-dot|Add node_modules
1fca6f9|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
0289d1b|2026-08-08|intricos777-dot|aisle: guardian auto-commit 2026-08-08
80fcbf7|2026-08-08|intricos777-dot|fix: move default port from 4124 to 4125 and restart via systemd
7650d49|2026-08-08|intricos777-dot|fix: convert health.js to ESM syntax for module startup
db3719c|2026-08-08|intricos777-dot|chore: initialize repo with service automation scaffold
```

## lin-antimalware
```
4d304c3|2026-09-26|opencode|Fix hardcoded /home/sin and nonexistent Projects/security paths
806bfcf|2026-09-21|sin|auto: commit uncommitted changes before push
9e3dd8a|2026-08-05|intricos777-dot|chore: untrack __pycache__/*.pyc (now covered by .gitignore)
0c35889|2026-08-05|intricos777-dot|chore: generate initial scan and dredge reports
901b79c|2026-08-05|intricos777-dot|feat: add deep dredge intel nodes and threat feed agents
4864364|2026-08-05|intricos777-dot|feat: expand signatures, add system checks, quarantine commands, and complete CLI
6d88fef|2026-08-05|intricos777-dot|chore: add gitignore and remove generated scan report
8ea133c|2026-08-05|intricos777-dot|init: LinAntimalware draft with scanner, web dashboard, CLI, self-heal wrapper, and signatures
```

## lin-antimalware-tools
```
ec6271c|2026-09-21|sin|feat: add freedom-keys generator, redhat and whitehat cipher tests
9d7f60a|2026-08-10|intricos777-dot|chore: remove pycache and add gitignore for cipher modules
9d8e43e|2026-08-09|intricos777-dot|feat: replace foreign binaries with local guards + bde patrol
63bc24c|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
c97e443|2026-08-08|intricos777-dot|aisle: guardian auto-commit 2026-08-08
45a56fd|2026-08-08|intricos777-dot|feat: register polsia/lia-agent/hermes as security minds
5346f2b|2026-08-08|intricos777-dot|feat: register opencode/supercode in minds security bridge
708cdb7|2026-08-08|intricos777-dot|feat: add per-project VM bootstrap config for neuromorphic node
e2d52ad|2026-08-08|intricos777-dot|copyright: add proprietary rights notice for self-built tooling and industry systems
ecfa0fd|2026-08-08|intricos777-dot|test: add whitehat adb unit tests and fix assertions
7e64070|2026-08-08|intricos777-dot|feat: add ADB whitehat scanner/reporter and phone integrity bridge
f698b59|2026-08-08|intricos777-dot|feat: add whitehat scanner/analyzer/reporter, mind security bridge, role-scoped registry
78aa949|2026-08-07|intricos777-dot|feat: redhat autoshutdown + portlock (local-only defensive)
```

## linkedin-cli
```
76be09a|2026-09-19|sin|feat: initial linkedin CLI tool
```

## linkedin-outreach
```
11e27dc|2026-09-19|sin|feat: initial LinkedIn outreach system
```

## linux-zen-build
```
37a98da|2026-09-21|sin|auto: commit uncommitted changes before push
a5e4386|2026-08-23|intricos777-dot|fix(post-snapshot): use mountpoint paths; verified against live btrfs layout
53cc69d|2026-08-23|intricos777-dot|linux-zen-build v1.0.0 stable: 21-layer encryption, miners, security stack rebuild
```

## linux-zen-suite
```
168292a|2026-09-21|intricos777-dot|chore: align AI coordination port, update shader permutations, add gitignore
ff6edcd|2026-09-21|sin|chore: add gitignore (secrets/build/backups), move AI coordination port to 4142
9067831|2026-09-11|Hermes Agent|chore: bump zen-core to v1.2.0 with vulkan module
57c2111|2026-09-11|Hermes Agent|feat: add vulkan shader cache + pipeline pre-warming module
b6a20d9|2026-09-11|intricos777-dot|add zen-suite bootable ISO with lfs
```

## living-sin-assets
```
0cc8993|2026-08-07|intricos777-dot|chore: save working state before cleanup
40646e0|2026-08-05|intricos777-dot|Harden dagger overlay error handling
657e8f9|2026-08-05|sin|Living Sin bulk assets: merch emblems, dagger cursor frames, XCursor theme
f10deb8|2026-08-05|sin|Living Sin bulk assets: merch palettes/merch PNGs+SVG, yin-yang emblems, dagger cursor frames + XCursor theme
```

## living-sin-merch
```
c5c269f|2026-08-06|intricos777-dot|feat: static gothic storefront on Pages with PayPal buy-now (intricos777@gmail.com)
5e68a81|2026-08-05|sin|Add gothic/Hot Topic merch design system: 8 WCAG-validated DESIGN.md themes + generated palette/merch/channel/youtube/motion assets
68d4205|2026-08-05|intricos777-dot|feat: load dotenv so .env values activate in backend
57f8050|2026-08-05|intricos777-dot|feat: add PayPal checkout, Coinbase Commerce crypto checkout, multi-currency support
e26e6c8|2026-08-05|intricos777-dot|init: Living Sin merch storefront with Stripe + PayPal checkout
```

## living-sin-models
```
d26d802|2026-08-05|intricos777-dot|fix: redesign MANIFEST to v1 schema (storage node, weights never in git)
f9afe24|2026-08-05|intricos777-dot|Living Sin model cloud-save + Lia node-sync: manifest, save/pull scripts, bridge registration
```

## living-sin-search
```
07e8bd3|2026-08-17|intricos777-dot|fix: living-sin-search OOM loop -> bounded on-demand indexer
4b4b33c|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
20e2d29|2026-08-08|intricos777-dot|aisle: guardian auto-commit 2026-08-08
d8e633f|2026-08-08|intricos777-dot|chore: add service automation scaffold, wrappers, tests, BDE, vm bootstrap
6421ec9|2026-08-08|intricos777-dot|chore: ignore pycache and remove cached artifacts
55a909c|2026-08-08|intricos777-dot|feat: replace openai STT with local faster-whisper; replace edge-tts with local piper-tts; web search offline-first
993b288|2026-08-08|intricos777-dot|feat: add TTS, STT, encrypted local state, voice CLI
488b1c3|2026-08-08|intricos777-dot|feat: scaffold local-first answer engine
```

## living-sin-ui
```
d6fad2f|2026-08-05|sin|Harden dagger overlay error handling
02a3b02|2026-08-05|sin|Harden pre-commit secret scan (realistic key patterns; path guards)
8a192f4|2026-08-05|sin|probe
16d38e7|2026-08-05|sin|Living Sin gothic UI: Void/supercode + opencode + Konsole merch themes, yin-yang emblems, animated dagger cursor (X11 overlay + XCursor), fish greeting, secret-scan pre-commit
5cb2337|2026-08-05|sin|Living Sin gothic UI: Void/supercode + opencode + Konsole merch themes, yin-yang emblems, animated dagger cursor (X11 overlay + XCursor), fish greeting, secret-scan pre-commit
```

## local-emergency-patrol
```
f05c559|2026-09-21|sin|feat: add dispatch router with API tests
570ad1d|2026-08-18|intricos777-dot|Add backend egg-info
a6443ce|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
e28139a|2026-08-08|intricos777-dot|chore: add BDE self-heal/debug patrol scripts
d1692c9|2026-08-08|intricos777-dot|chore: initialize repo with service automation scaffold
```

## loz-majoras-mask
```
13bc33b|2026-09-21|sin|Add game content and assets
0823ef2|2026-09-21|sin|feat: Termina lore vault — world/cycle, masks, characters (Majora's Mask canon)
67ee4df|2026-09-21|sin|auto: commit uncommitted changes before push
12cb712|2026-09-21|sin|chore: untrack python bytecode, ignore __pycache__
d47cdb6|2026-09-04|intricos777-dot|docs: make the ROM requirement unmistakable — players need their own original copy
7a21755|2026-09-04|intricos777-dot|chore: strip unrelated project scaffolding; add full 2S2H build tooling
8f6cfdc|2026-09-04|intricos777-dot|feat: vendor Twilight Elysium engine into third_party/te; revive self-contained build
dbcf479|2026-08-15|intricos777-dot|update: cli changes
151aab9|2026-08-08|intricos777-dot|feat: task-31 engine bridge integration with time cycle + player movement
745e05a|2026-08-08|intricos777-dot|feat: 3-day time cycle + player movement core (mm --core)
11e406d|2026-08-08|intricos777-dot|feat: add alternate quantum-enochian layered format with 7 user-keyed layers
d5c7904|2026-08-08|intricos777-dot|chore: update start-all.sh port mappings for current fleet
9c91cf7|2026-08-08|intricos777-dot|feat: add master start-all.sh service orchestrator
081b70a|2026-08-08|intricos777-dot|copyright: add proprietary rights notice for self-built tooling and industry systems
05a3243|2026-08-08|intricos777-dot|test: add engine bridge tests for loz-majoras-mask
2a45337|2026-08-08|intricos777-dot|chore: ignore build artifacts
c2e406f|2026-08-08|intricos777-dot|feat: scaffold LOZ Majora Mask with TE engine bridge, CMake, self-heal, tests
72e36f1|2026-08-08|intricos777-dot|feat: add self-heal/debug wrappers and BDE security layer
f69c83e|2026-08-08|intricos777-dot|init: loz-majoras-mask engine bridge scaffold from Twilight Elysium
```

## loz-ocarina-mq
```
1c7a1d6|2026-09-21|sin|chore: untrack python bytecode, ignore __pycache__
f56e1c4|2026-08-08|intricos777-dot|feat: add per-project VM bootstrap config for neuromorphic node
55e172f|2026-08-08|intricos777-dot|copyright: add proprietary rights notice for self-built tooling and industry systems
c9ed5ab|2026-08-08|intricos777-dot|test: add engine bridge tests for loz-ocarina-mq
52dfa40|2026-08-08|intricos777-dot|chore: ignore build artifacts
b54ef6a|2026-08-08|intricos777-dot|feat: scaffold LOZ OoT MQ with TE engine bridge, CMake, self-heal, tests
7463a9d|2026-08-08|intricos777-dot|chore: remove build artifacts
1656a90|2026-08-08|intricos777-dot|feat: add self-heal/debug wrappers and BDE security layer
7b6ccfc|2026-08-08|intricos777-dot|chore: remove build artifacts
b8d491a|2026-08-08|intricos777-dot|init: loz-ocarina-mq engine bridge scaffold from Twilight Elysium
```

## market-library
```
6d7951a|2026-08-08|intricos777-dot|feat: add per-project VM bootstrap config for neuromorphic node
282ba3d|2026-08-08|intricos777-dot|copyright: add proprietary rights notice for self-built tooling and industry systems
f00b140|2026-08-08|intricos777-dot|chore: update local market data cache
16a2fcb|2026-08-08|intricos777-dot|chore: clean pycache and normalize ignores
4afa55b|2026-08-08|intricos777-dot|chore: update local market data cache
5542dd9|2026-08-08|intricos777-dot|feat: add self-heal/self-debug wrappers and BDE security layer
c46bf08|2026-08-08|intricos777-dot|init: market library for forex/stocks/bonds/crypto from public sources
```

## metals-alloy-engineering
```
4e629b7|2026-08-07|intricos777-dot|chore: save working state before cleanup
02605c1|2026-08-05|intricos777-dot|Add biological augmentation patterns and Lia memory bridge
86c9e21|2026-08-05|intricos777-dot|Remove __pycache__
cf0598e|2026-08-05|intricos777-dot|Add bio pattern library for biomimetic alloy design
```

## money-automation
```
c5a0261|2026-09-21|intricos777-dot|chore: extend gitignore
f72c869|2026-09-08|intricos777-dot|Forge three money-automation engines: aggregator, content quill, deal finder
```

## mp3-video-virtualizer
```
4828a49|2026-08-15|intricos777-dot|feat: add core modules, cache, audio features
ecb2e9b|2026-08-07|intricos777-dot|chore: save working state before cleanup
dfa3c85|2026-08-05|intricos777-dot|Add README for cross-platform use
d23b96b|2026-08-05|intricos777-dot|Remove repo-specific frames and clean cache for cross-platform use
e4d97bc|2026-08-05|intricos777-dot|Wire biosynthetic Lia-themed prompts and update desktop link
7ef6c5a|2026-08-05|intricos777-dot|Add biosynthetic biological/nonorganic visualization frames
6e10e1a|2026-08-05|intricos777-dot|Add MP3 video virtualizer with desktop link
```

## nanite-systems
```
2d56c44|2026-08-17|intricos777-dot|chore: stop tracking pycache, add gitignore
b7533b1|2026-08-05|intricos777-dot|Add idempotency guard to achievement detector
f17cd12|2026-08-05|intricos777-dot|Record nanite system protocol/bridge achievements
f55532a|2026-08-05|intricos777-dot|Achievement: protocol — Bluetooth protocol initialized
9279471|2026-08-05|intricos777-dot|Achievement: integration — Lia bridge online
231a234|2026-08-05|intricos777-dot|Add achievement tracker and detector
b589d6b|2026-08-05|intricos777-dot|Achievement: protocol — Bluetooth protocol initialized
7bd61c0|2026-08-05|intricos777-dot|Achievement: integration — Lia bridge online
e589feb|2026-08-05|intricos777-dot|Init: Bluetooth protocol + Lia-nanite bridge
```

## neuromorphic-handoff
```
6ff2521|2026-09-21|sin|feat: update bridge components; untrack bytecode
053ac2e|2026-08-15|intricos777-dot|update: pycache files
8674c95|2026-08-10|intricos777-dot|feat: initial neuromorphic handoff system - torch protocol for agent handoffs
```

## non-steam-games
```
8603f93|2026-09-21|sin|Add game catalog README and build/launch helper
```

## offline-agents
```
eba635f|2026-09-18|intricos777-dot|Add ollama provider config, model reference, and README instructions
12aa0fd|2026-09-18|intricos777-dot|Initial commit: offline survival kit for Hermes + OpenCode
```

## once-human-linux-fixes
```
5d9489f|2026-09-04|intricos777-dot|init: Once Human Linux test report
```

## phone-computers
```
677e1e1|2026-09-21|sin|chore: untrack python bytecode, ignore __pycache__
148f575|2026-08-12|intricos777-dot|aisle: guardian auto-commit 2026-08-12
fa3637c|2026-08-08|intricos777-dot|feat: scaffold phone-computers miniature supercomputer line with BDE security
```

## polsia
```
44db274|2026-09-21|Polsia Portfolio|chore: refresh dealfinder scrape cache
6e46f3e|2026-09-21|Polsia Portfolio|Security: PayPal secrets to .env + env overlay loader; untrack runtime artifacts
e3ce912|2026-09-12|Polsia Portfolio|Polsia Portfolio: consolidated AI income automation with PayPal payouts
```

## polsia-cli
```
012880b|2026-09-21|sin|feat: extend config and memory subsystems
e48e938|2026-08-29|Living_Sin|feat: multi-business registry support (businesses/focus commands, --business flag, status registry)
9db7eeb|2026-08-29|Living_Sin|fix: add missing stripe dependency to pyproject
64f1451|2026-08-17|intricos777-dot|feat: initial polsia agent framework (agents, billing, core LLM, CLI)
218c46b|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
bdeb638|2026-08-08|intricos777-dot|chore: add BDE self-heal/debug patrol scripts
a9705d7|2026-08-08|intricos777-dot|chore: add service automation scaffold, wrappers, tests, BDE, vm bootstrap
7c45a36|2026-08-08|intricos777-dot|feat: add per-project VM bootstrap config for neuromorphic node
988a07a|2026-08-08|intricos777-dot|copyright: add proprietary rights notice for self-built tooling and industry systems
95880a4|2026-08-08|intricos777-dot|feat: add FastAPI backend and passing tests for responder dispatch
b941aca|2026-08-08|intricos777-dot|feat: harden fund routing to owner-only PayPal/Stripe; add data integrity corruption and access control
fcb3c24|2026-08-07|intricos777-dot|test: fix unittest discovery imports for dispatch/payroll/subsidies
a623be6|2026-08-07|intricos777-dot|feat: scaffold polsia emergency response service
7a5ed83|2026-08-03|Polsia|chore: gitignore cleanup and strip tracked artifacts
f4cbe1e|2026-08-03|Polsia|Add polsia/billing.py - Stripe billing integration
d9b4457|2026-08-01|Polsia|feat: configure Stripe with intricos777@gmail.com profile and add missing dependencies
8022e98|2026-07-19|Polsia|Update v0.2.0: multi-LLM support, python-dateutil, Claude path fix
```

## polsia-global-trade
```
46998ef|2026-09-21|sin|auto: commit uncommitted changes before push
86838e0|2026-08-04|intricos777-dot|feat: add default trade config and startup runner
46a2d19|2026-08-04|intricos777-dot|chore: add gitignore
364b9d1|2026-08-04|intricos777-dot|chore: initial polsia-global-trade scaffold
```

## polsia-lawsuit
```
dae542e|2026-09-21|Polsia Portfolio|Add US legal framework: business account blocking, civil rights, Nevada state law
f825e64|2026-09-12|Polsia Portfolio|Initial lawsuit repo setup
```

## profit-widget
```
5973351|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
b060074|2026-08-08|intricos777-dot|chore: add BDE self-heal/debug patrol scripts
a541a31|2026-08-08|intricos777-dot|chore: sync service automation changes
051d743|2026-08-08|intricos777-dot|chore: initialize repo with service automation scaffold
```

## q-debug-vm
```
c52033d|2026-08-11|intricos777-dot|fix: working boot — seed ISO + 9p share (repo root) in run.sh, resilient provision with diag, verified live
82e18de|2026-08-11|intricos777-dot|docs: handoff notes for q-debug-vm
435deef|2026-08-11|intricos777-dot|feat: console relay from preview iframe, VM runtime build + cloud-init seed, runtime docs
1dab240|2026-08-11|intricos777-dot|feat: scaffold Q debug VM with native-browser-Inspect portal and ?q=debug mode
```

## quantum-loop
```
080e398|2026-08-12|intricos777-dot|aisle: guardian auto-commit 2026-08-12
f9b3b19|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
d6a3341|2026-08-08|intricos777-dot|chore: add BDE self-heal/debug patrol scripts
1d6c19d|2026-08-08|intricos777-dot|feat: add FastAPI backend app with health, transport, scheduler routers
d4d2b35|2026-08-08|intricos777-dot|chore: add service automation scaffold, wrappers, tests, BDE, vm bootstrap
e493f04|2026-08-08|intricos777-dot|chore: ignore pycache and remove cached artifacts
ca1621c|2026-08-08|intricos777-dot|feat: add NAT traversal, mesh router, CUDA pool, work stealing, failover
a3c15d8|2026-08-08|intricos777-dot|feat: scaffold quantum-loop distributed compute fabric
```

## ringworld-redux
```
254953c|2026-09-21|sin|fix: roster regrounded to Niven's Known Space; drop mis-copied UNSC scaffold
020cfc6|2026-08-08|intricos777|feat: add per-project VM bootstrap config for neuromorphic node
24d206d|2026-08-08|intricos777|copyright: add proprietary rights notice for self-built tooling and industry systems
051eb92|2026-08-07|intricos777|test: add unittest suite for build/runtime/renderer/input/objectives
91e8b56|2026-08-07|intricos777|fix: auto-close test run loop after bounded frames
d2e82a2|2026-08-06|intricos777|Integrate Twilight Elysium engine: submodule, renderer bridge, CMake wiring
6b66529|2026-08-06|intricos777|Release alpha: public repo, README with setup/console notes, Twilight Elysium integration roadmap
7fea8a4|2026-08-06|intricos777-dot|Alpha: fully playable build with movement, objectives, bosses, Legend, saves, multiplayer
dc29b49|2026-08-06|intricos777-dot|Alpha: wire campaign advance, scaling init, save triggers, audio script hooks, Legend mode
2687ba3|2026-08-06|intricos777-dot|Add boss JSON parsing, enemy scaling, and spawn hooks
594c1a9|2026-08-06|intricos777-dot|Expand campaign to 24 CE maps, wire mission runtime objectives/spawns, add Game::load_mission, fix duplicate init
c74a10b|2026-08-06|intricos777-dot|chore: ignore build dirs, un-track build-bak artifacts
be003b5|2026-08-06|intricos777-dot|Wire current campaign mission into Game runtime, load mission JSON on startup, print first objective
538c1a0|2026-08-06|intricos777-dot|Fix arc_collapse JSON parsing, add debug parse tracing, tolerate numeric enemy_type, remove duplicate main.cpp mission init
def4748|2026-08-06|intricos777-dot|Cleanup campaign init: remove duplicate loads, fix main.cpp include path, keep primer as current mission
b05ca26|2026-08-06|intricos777-dot|Expand campaign to 5 missions, add Campaign loader, switch Mission to nlohmann_json, add Reach codenames for all 60 roster members
5df81d5|2026-08-06|intricos777-dot|Fix P2/P3 review issues: menu enum alignment, save init copy-back, campaign uses live player pos, network count type, dead build_entity_state duplicate removed
c51807d|2026-08-06|intricos777-dot|Fix network/renderer risks: non-blocking TCP connect, peer drop, UB-free state parsing, GL resize viewport, event-loop dedup, tick-drift clamp
78f32b5|2026-08-06|intricos777-dot|Add network reliability: seq/acks, retransmit, delta state, heartbeats, bandwidth budget, relay wrapper
6934901|2026-08-06|intricos777-dot|Fix black-screen/crash risks: poll SDL events each frame, initial GL clear/swap, raise window
103e214|2026-08-06|intricos777-dot|Add campaign progression via waypoints and dialogue dedupe
5b1577d|2026-08-06|intricos777-dot|Fix campaign init path, deduplicate mission update logging, wire Mission into Game
5b9ff67|2026-08-06|intricos777-dot|Add TCP local-server listen/accept path alongside UDP broadcast
f616eb5|2026-08-06|intricos777-dot|Expand arc_collapse finale objectives/dialogue; clean test-fire state
6217771|2026-08-06|intricos777-dot|Implement UDP host/client state broadcasting in NetworkSystem
824be6a|2026-08-06|intricos777-dot|Verify combat input: fire/alt-fire/reload events in smoke run
01d0676|2026-08-06|intricos777-dot|Wire combat input: camera aim origin, movement, alt-fire, reload events
4a036f1|2026-08-06|intricos777-dot|Add runtime envs for auto-host and test-fire verification
d6c574a|2026-08-06|intricos777-dot|Add RR_AUTO_HOST runtime path and menu-triggered host/join wiring
39cea89|2026-08-06|intricos777-dot|Integrate NetworkSystem into Game and menu; fix network module build path
6069eb5|2026-08-06|intricos777-dot|Wire SDL keyboard input to controller, add UDP multiplayer host/join, clean renderer include
f3b2942|2026-08-06|intricos777-dot|Add multiplayer network stub and menu controller routing
aa09b95|2026-08-06|intricos777-dot|Add real SDL+GL windowed renderer and integrate into game loop
3588138|2026-08-06|intricos777-dot|Add 16 CE-inspired sandbox maps and preset debug/self-heal wrappers for save system
e78eaee|2026-08-06|intricos777-dot|Add save system with fake corruption, self-heal debug wrapper, and multiplayer menu
645af0b|2026-08-06|intricos777-dot|Add 16 CE-inspired sandbox maps with renamed classic PVP layouts
3df3bb5|2026-08-06|intricos777-dot|Add boss aliens with 2hp buff pulse, alien panic bar, level modifiers past level 7, and final campaign/arc maps with new names
96dcc38|2026-08-06|intricos777-dot|Add campaign maps, achievements, renderer/audio bridge, and Legend hidden spawns
a6b4c42|2026-08-06|intricos777-dot|Prepare Steam marketing assets and final campaign buildout
1e871d3|2026-08-06|intricos777-dot|Add alien mines/sentry bots and human claymores/grenades/mines
0623153|2026-08-06|intricos777-dot|Rename to Ringworld Redux, add menu/squad/weapon system, and Legend mode foundation
77cc278|2026-08-06|intricos777-dot|Add menu, world entity damage, and preserve controller bindings
1029467|2026-08-06|intricos777-dot|Add cross-platform controller bindings and spawn initial entities
cd27fa8|2026-08-05|intricos777-dot|Add JSON map parser, spawner, and 3-slot loadout cycling
2136c0e|2026-08-05|intricos777-dot|Wire input/HUD/game loop into Game and fix build/linkage
8bb242c|2026-08-05|intricos777-dot|Add real-world weapon registry and 3-slot inventory system
0c70d16|2026-08-05|intricos777-dot|Wire 60Hz game loop with campaign update/render stubs
d586256|2026-08-05|intricos777-dot|Fix audio/music path resolution and add game loop output
97dffeb|2026-08-05|intricos777-dot|Clean nested twilight-elysium build artifacts
7daefb4|2026-08-05|intricos777-dot|Add campaign map data and character bio JSON
17e9230|2026-08-05|intricos777-dot|Integrate audio engine, transitions, voice banks, and HUD rendering into game loop
043e5de|2026-08-05|intricos777-dot|Add audio system with music/transition/voice managers and playlist extractor
0fc8a0b|2026-08-05|intricos777-dot|Add protagonist Living_Sin, Lia companion, and 60-member military roster
e8369bd|2026-08-05|intricos777-dot|Scaffold TE Halo-Inspired FPS framework with campaign/co-op stubs
```

## rocket-build-system
```
a964316|2026-08-17|intricos777-dot|chore: stop tracking pycache, add gitignore
e09d718|2026-08-07|intricos777-dot|chore: save working state before cleanup
33bbe47|2026-08-05|intricos777-dot|Achievement: fleet — Perfect fleet validation
319f305|2026-08-05|intricos777-dot|Achievement: fleet — Fleet excellence
7267c7a|2026-08-05|intricos777-dot|Fix achievement detection threshold and clean tracked __pycache__
e3c3b76|2026-08-05|intricos777-dot|Fix achievement detection thresholds and fleet validation logic
353b8a0|2026-08-05|intricos777-dot|Achievement: fleet — Fleet excellence
8a304bd|2026-08-05|intricos777-dot|Add achievement tracker and detector
bfa90bd|2026-08-05|intricos777-dot|Remove __pycache__
ed11c7b|2026-08-05|intricos777-dot|Add presets, blueprint exporter, and server API
d0e75a5|2026-08-05|intricos777-dot|Add presets, exporter, server API
5686ce8|2026-08-05|intricos777-dot|Add rocket builder v1 with ranking
```

## secure-tactical-systems
```
f397097|2026-08-11|intricos777-dot|feat: scaffold secure tactical systems with 14-layer encryption, weapons hardlocks, extended BDE patrols, breach logging
```

## security-audit-2026
```
407fdf5|2026-09-26|opencode|Add buildlog: durable journal of builds, audits, and fixes
0828a04|2026-09-18|intricos777|restore: public pentest report 2026-09-18 + correct stale findings
46528f5|2026-09-16|sin|fix: correct 3 discrepancies in pentest report and status.json
4b63170|2026-09-11|Hermes Agent|fix: corrected auditctl command (needs realpath)
884f6e6|2026-09-11|Hermes Agent|feat: post-pentest hardening — crypto-bot auth, SRBMiner bind, intrusion-notify
6e2c703|2026-09-11|sin|add: local host pentest report 2026-09-11
35c4bd9|2026-09-10|sin|Initial: security logs archive and audit findings for Sept 2026
```

## sen-isp-business
```
18345d9|2026-08-18|intricos777-dot|Add portal lockfile, gitignore node_modules
a44d713|2026-08-15|intricos777-dot|feat: add earthnet proxy, llm proxy, bde patrol, encryption stack, mining service
6320fe3|2026-08-11|intricos777-dot|feat: add hotspot API routes; password from env
80dc064|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
20e17ff|2026-08-08|intricos777-dot|chore: add BDE self-heal/debug patrol scripts
b257ad2|2026-08-08|intricos777-dot|chore: sync service automation changes
73bffc7|2026-08-08|intricos777-dot|chore: add service automation scaffold, wrappers, tests, BDE, vm bootstrap
0aa5835|2026-08-08|intricos777-dot|feat: add customer provisioning automation, reconciliation reports, live checkout URLs
0343499|2026-08-08|intricos777-dot|feat: add live Stripe/PayPal checkout URL support via env config
d47f4d5|2026-08-08|intricos777-dot|feat: add NOC incident router, reconciliation service, and checkout portal page
d4b0cec|2026-08-08|intricos777-dot|feat: add portal checkout API and interactive signup page
8cf6458|2026-08-08|intricos777-dot|feat: scaffold customer signup portal
982c7a5|2026-08-08|intricos777-dot|docs: add checkout flow to operations
2c9896b|2026-08-07|intricos777-dot|feat: add PayPal billing provider, factory, config docs; do not commit keys
817e8c5|2026-08-07|intricos777-dot|feat: add ISP business framework: pricing, partnerships, billing, legal, compliance
```

## sen-isp-pygeofetch
```
29c605b|2026-08-19|intricos777-dot|feat: SEN-ISP PyGeoFetch scaffold
```

## simulation-policy-sandbox
```
fe4a4d0|2026-09-21|sin|chore: untrack python bytecode, ignore __pycache__
3dfbf9b|2026-08-04|sin|chore: strip tracked pycache and harden gitignore
784145e|2026-08-04|sin|fix: stable CV calculation when mean is zero
3f7f258|2026-08-04|sin|fix: experiments/analysis run for housing domain
46da76f|2026-08-04|sin|init: simulation engine + housing domain + config
```

## sin-archive-2026
```
b09242d|2026-09-24|sin|cleanup complete: 203G freed, ledger finalized, posture verified 15/15
5a518fa|2026-09-24|sin|archive 2026-09-24: steam owned-game manifest, configs, deletion ledger
```

## skyrim-ai-overhaul
```
fe03058|2026-07-20|intricos777-dot|Initial commit: Skyrim AI Overhaul - Papyrus scripts, ESP builder, and transpiler
```

## skyrim-mod-packages
```
fd72ecd|2026-07-20|intricos777-dot|Re-add Elsewhyr mod package with proper Git LFS tracking
3ae7e2b|2026-07-20|intricos777-dot|Add Elsewhyr mod package (61MB, Git LFS)
33edf0b|2026-07-20|intricos777-dot|Initialize Git LFS for zip files
```

## soh-masterquest-build
```
6dfd06d|2026-07-19|intricos777-dot|Ship of Harkinian - Ocarina of Time Master Quest PC Port build
```

## solar-well-infrastructure
```
96f5a2c|2026-09-21|sin|chore: untrack python bytecode, ignore __pycache__
6d2a599|2026-08-04|intricos777-dot|feat: add Mars terraforming sim with seeding, aerosols, rain, and moisture cycle
0450f5f|2026-08-04|intricos777-dot|feat: integrate clean plastics lifecycle into wells + Mars base thermal control
ee98eb6|2026-08-04|intricos777-dot|feat: add Mars deployment, radiation sponge materials, integrated demo
939bcf5|2026-08-04|intricos777-dot|feat: add Tippi resizable well + materials integration + sizing helper
20eeda5|2026-08-03|intricos777-dot|docs: add placeholder index for GitHub Pages
fcf6986|2026-08-03|intricos777-dot|chore: scaffold solar-well-infrastructure project
```

## spacecraft-blueprint-simulator
```
a474b8d|2026-08-07|intricos777-dot|test: add unittest suite for simulator/physics, control panel
07284a1|2026-08-07|intricos777-dot|feat: convergence detection, markdown reports, push flag; cleanup output dirs
333db32|2026-08-07|intricos777-dot|fix: ensure output directories exist before writing per-mode blueprints
ebdc50d|2026-08-07|intricos777-dot|feat: dual-track realistic/theoretical simulation with precise physics, BDE patrol scanner, real-world material/propulsion databases
a1d50ec|2026-08-07|intricos777-dot|seed: spacecraft blueprint simulator with reference corpus and first optimization run
```

## space-edge-network
```
d66a79d|2026-09-21|sin|feat: add auth layer and wire auth checks across routers
5cdbc6a|2026-08-18|intricos777-dot|Update backend egg-info and add dashboard lockfile
170bdc7|2026-08-17|intricos777-dot|fix: wire full app routers (drone/satellite imports), replace standalone health stub
a130764|2026-08-08|intricos777-dot|chore: add AI attribution CREDITS.md
5e1d6a1|2026-08-08|intricos777-dot|chore: add BDE self-heal/debug patrol scripts
cd7f7ec|2026-08-08|intricos777-dot|fix: add standalone health app for reliable service startup
d9e4ac1|2026-08-08|intricos777-dot|fix: correct relative import syntax for standalone startup
abbdf25|2026-08-08|intricos777-dot|fix: use relative package imports in routers for standalone uvicorn startup
b2d6ddf|2026-08-08|intricos777-dot|docs: add service automation blockers for space-edge-network imports
877e056|2026-08-08|intricos777-dot|fix: add FastAPI app wrapper for standalone service startup
8b0cce2|2026-08-08|intricos777-dot|chore: add service automation scaffold, wrappers, tests, BDE, vm bootstrap
70e47b1|2026-08-08|intricos777-dot|feat: sync neuromorphic node network to Satalight/Cerebellum grid
b2b2f7c|2026-08-08|intricos777-dot|copyright: add proprietary rights notice for self-built tooling and industry systems
41524a1|2026-08-08|intricos777-dot|feat: add BDE ADB patrol, integrate phone with mind bridge and twice-daily system patrol
32ba8d7|2026-08-08|intricos777-dot|feat: add BDE integrity patrol, system patrol scheduler, AI mind bridge integration
0f3f02d|2026-08-08|intricos777-dot|feat: add flight/mission automation, wrappers; expand drone API; tests pass
06a7ed8|2026-08-08|intricos777-dot|feat: add debug wrappers, circuit breakers, orbit/payload maintenance; tests pass
afc93c5|2026-08-08|intricos777-dot|feat: add drone/satellite self-healing maintenance, satalight grid, and health APIs
892a4e3|2026-08-08|intricos777-dot|test: replace live GitHub patrol test with offline mock; 18 tests pass
e83dc36|2026-08-08|intricos777-dot|feat: add dragoon offload dashboard page and API
d7586ef|2026-08-08|intricos777-dot|feat: add dragoon runtime dashboard page and backend router
70eb6de|2026-08-08|intricos777-dot|feat: add quantum-loop dashboard page and backend router
0feb12e|2026-08-08|intricos777-dot|feat: add BDE patrols dashboard page and live API wiring
a7f1426|2026-08-08|intricos777-dot|feat: add BDE GitHub patrol scanner and scheduler for open-source tool discovery
e910804|2026-08-08|intricos777-dot|feat: add cerebellum dashboard page and wire dashboard APIs
5ef84be|2026-08-08|intricos777-dot|feat: add cerebellum node network: agent packages, node runtime, mesh discovery, archive, APIs
b98ef36|2026-08-08|intricos777-dot|feat: wire dashboard mining/security pages to live APIs
d55dfa6|2026-08-07|intricos777-dot|feat: add dashboard frontend with satellite grid, mining, security, edge status
45a8c05|2026-08-07|intricos777-dot|feat: add earthnet auto-connect framework: NM dispatcher, systemd daemon, edge client, docs
0dbcd25|2026-08-07|intricos777-dot|feat: add encrypted satellite backups, cpu/gpu miner configs, wallet lists
17ca55a|2026-08-07|intricos777-dot|feat: scaffold space edge network
```

## steam-linux-optimizations
```
8b68b60|2026-08-15|intricos777-dot|Externalize email credentials (gitignored), add .gitignore
b2efd74|2026-08-15|intricos777-dot|Steam Linux optimizations: Helldivers 2 + other games, GPU failover watchdog, GameGuard mitigations, performance configs
```

## sword-tale-bugfix
```
07b1614|2026-09-21|sin|docs: play offline (ST-001d) as required step in launch-options
e44fcd9|2026-09-21|sin|v0.1.5: ST-001d workaround confirmed — Steam Offline mode reaches checkpoints
fe38fc4|2026-09-21|sin|v0.1.4: root cause ST-001d + torch capture fixes
2529ec4|2026-09-21|sin|v0.1.3: torch — Steam-console bridge + capture pipeline
0c584e3|2026-09-21|sin|v0.1.2: ST-001c — host RAM starvation kills the game driver-side (no engine artifact)
547d9ec|2026-09-21|sin|v0.1.1: gameplay-phase crash handling, STAY-liveness verify mode, Steamworks IPC findings
245addf|2026-09-21|sin|Initial community bugfix + Linux optimization package for Sword Tale: Lost Excalibur (App 3305630)
```

## sword-tale-controller
```
2a30f36|2026-09-21|sin|Real controller remap: triggers as attack/block, D-pad slots, L3/R3 toggles
1c2612c|2026-09-21|sin|Initial commit: controller support for Sword Tale: Lost Excalibur
```

## sword-tale-crash-report
```
03638c5|2026-09-21|sin|Add ready-to-paste Steam community submission text
b506973|2026-09-21|sin|ST-001d crash report + fix guide for Sword Tale devs
```

## system-resource-optimizer
```
1d95cfe|2026-08-17|intricos777-dot|chore: stop tracking pycache, add gitignore
b4f38b1|2026-08-07|intricos777-dot|chore: save working state before cleanup
9f0fc18|2026-08-05|intricos777-dot|Remove __pycache__
ab09341|2026-08-05|intricos777-dot|Add system resource optimizer with auto-apply daemon
```

## te-bonfire
```
6643a21|2026-09-21|sin|Add game content and assets
dbbb936|2026-08-08|intricos777-dot|feat: world/zone progression + first real boss loop (Ember Watcher)
706ddf8|2026-08-08|intricos777-dot|Initial release: te-bonfire stamina-driven combat core on Twilight Elysium
```

## te-halo-inspired
```
cd156e9|2026-09-21|sin|wave 2: add game content
59fc5d8|2026-09-21|sin|feat: Halo canon anchor + cryo-awakening tutorial framing
77cc278|2026-08-06|intricos777-dot|Add menu, world entity damage, and preserve controller bindings
1029467|2026-08-06|intricos777-dot|Add cross-platform controller bindings and spawn initial entities
cd27fa8|2026-08-05|intricos777-dot|Add JSON map parser, spawner, and 3-slot loadout cycling
2136c0e|2026-08-05|intricos777-dot|Wire input/HUD/game loop into Game and fix build/linkage
8bb242c|2026-08-05|intricos777-dot|Add real-world weapon registry and 3-slot inventory system
0c70d16|2026-08-05|intricos777-dot|Wire 60Hz game loop with campaign update/render stubs
d586256|2026-08-05|intricos777-dot|Fix audio/music path resolution and add game loop output
97dffeb|2026-08-05|intricos777-dot|Clean nested twilight-elysium build artifacts
7daefb4|2026-08-05|intricos777-dot|Add campaign map data and character bio JSON
17e9230|2026-08-05|intricos777-dot|Integrate audio engine, transitions, voice banks, and HUD rendering into game loop
043e5de|2026-08-05|intricos777-dot|Add audio system with music/transition/voice managers and playlist extractor
0fc8a0b|2026-08-05|intricos777-dot|Add protagonist Living_Sin, Lia companion, and 60-member military roster
e8369bd|2026-08-05|intricos777-dot|Scaffold TE Halo-Inspired FPS framework with campaign/co-op stubs
```

## tf2-elysium
```
11ab418|2026-09-21|sin|wave 2: add game content
5d2fd84|2026-09-21|sin|feat: TF2 canon — Administrator/Saxton/Gray/Merasmus/Pauling roster, classic map set, MvM robot army
83d4e36|2026-09-21|sin|auto: commit uncommitted changes before push
ebebac1|2026-08-11|intricos777-dot|feat: Sheldon popup NPC — 'I like turtles', max 3 appearances ever per player
197fe6d|2026-08-11|intricos777-dot|feat: scaffold tf2-elysium elysium build — engine, game data, casual/legend difficulties
```

## The-Elder-Scrolls-Elsewhyr
```
d885898|2026-07-20|Living_Sin|Fix SKSE plugin version struct and Load function
418c283|2026-07-18|Living_Sin|Add self-hosted runner workflow for local ESP build
d120a85|2026-07-18|Living_Sin|Fix build-esp.yml: add proper checkout, LFS handling, directory setup, and error handling
966a3a5|2026-07-18|Living_Sin|Fix SteamCMD/CreationKit installation with better error handling and path detection
6d52ffc|2026-07-18|Living_Sin|Fix: ensure all actions are up to date
611944d|2026-07-18|Living_Sin|Fix YAML syntax: use ${{ env.VAR }} syntax in if conditions
f7c6bcb|2026-07-18|Living_Sin|Fix Node.js 20 deprecation: upgrade actions/checkout to v5
8ff7a78|2026-07-18|Living_Sin|Fix YAML syntax: fix env variable references in if conditions
7ace7fa|2026-07-18|Living_Sin|Track large files with Git LFS
ac32383|2026-07-17|Living_Sin|Remove large files, add gitignore
927bfdd|2026-07-17|Living_Sin|Add CI build workflow for Elsewhyr ESPs
f6d7a05|2026-07-12|Living_Sin|Complete SKSE plugin implementation with AI voice synthesis, LOD generation, navmesh, narrative engine, vampire/werewolf/hybrid transformations
4818341|2026-07-12|Living_Sin|Complete Elder Scrolls Elsewhyr mod with narrative engine, vampire/werewolf/hybrid questlines, and mod package
000cda2|2026-07-11|Living_Sin|Add comprehensive procedural side quest generation system
49d0b84|2026-07-11|Living_Sin|Complete Elsewhyr + Black Marsh pipeline
c64ee66|2026-07-11|Living_Sin|Add narrative engine for dynamic Aedra/Daedra story
68f9e5a|2026-07-11|Living_Sin|Add navmesh and LOD generators
71ceec8|2026-07-11|Living_Sin|Complete Elsewhyr + Black Marsh pipeline
a920cd2|2026-07-11|Living_Sin|Initial commit: The Elder Scrolls Elsewhyr pipeline
```

## The-Elder-Scrolls-Elsweyr
```
3d849d8|2026-08-07|intricos777-dot|Initial mod scaffold: README and directory layout
daec72a|2026-08-05|intricos777-dot|Seed README
```

## twilight-elysium
```
26480eb|2026-09-21|sin|wave 2: add game content
591d968|2026-09-21|sin|feat: seele nobody archetype (kh-zero zero) + smoke test honors passed glb stem
b8e4e55|2026-09-21|sin|feat: mythic worldflesh exemplar — zone ledger + worldflesh test
da9b639|2026-09-21|sin|auto: commit uncommitted changes before push
4fad665|2026-09-21|sin|feat: real asset, render graph and shader modules replacing stubs
0d9e77d|2026-09-21|sin|feat: add Blender asset pipeline, shader scaffolding and frame graph stub
0fecd52|2026-08-18|intricos777-dot|Update world builder, add PBR and UE renderers
c3dcc42|2026-08-18|intricos777-dot|feat: Add model generator and complete world builder
63c70db|2026-08-18|intricos777-dot|feat: Wire Seele AI into 3D world renderer with SDL2+OpenGL
74bcfc3|2026-08-17|intricos777-dot|aisle: guardian auto-commit 2026-08-17
9c5bd61|2026-08-17|intricos777-dot|feat: Seele AI, .hack//G.U. disc world builder, Legend of Dragoon world integration
3d84527|2026-08-11|intricos777-dot|aisle: guardian auto-commit 2026-08-11
0a28cff|2026-08-10|intricos777-dot|feat: add dream engine + library shuffle + OperaGX compat prefs
30e36c1|2026-08-09|intricos777-dot|chore: promote twilight-elysium from gaming-unified engines/ subfolder
```

## vessel-logistics
```
8932f5d|2026-08-17|intricos777-dot|chore: stop tracking pycache, add gitignore
55f0c6b|2026-08-11|intricos777-dot|feat: add aviation echolocation support + Tesla AI contribution bundle todo
a4ab68d|2026-08-11|intricos777-dot|feat: add radar ping broadcast + anticrash avoidance implementation + tests
a33e9a4|2026-08-11|intricos777-dot|feat: add radar-based anticrash system with ping broadcast + avoidance policy
c0a2178|2026-08-11|intricos777-dot|feat: scaffold vessel logistics + navigation repo
```

## vm-bootstrap
```
1460dbf|2026-08-08|intricos777-dot|chore: switch VM provisioning to cloud-init and CoW disks
3e921e6|2026-08-08|intricos777-dot|feat: add neuromorphic VM encapsulation templates and per-project bootstrap specs
```

## void-bridge
```
007732a|2026-09-21|sin|chore: update run.sh
a28a493|2026-08-07|intricos777-dot|chore: save working state before cleanup
4a09849|2026-08-05|intricos777-dot|feat: void-bridge MCP server + confined HTTP bridge (file/git tools, ROOT escape-proof)
```

## voynich-occult-corpus
```
514f482|2026-09-21|Hermes Agent|rosetta stone engine: complete academic package + dictionary + grammar
d53bb80|2026-09-21|Hermes Agent|semantic mapper: section vocabulary + sample translations
2e70c08|2026-09-21|Hermes Agent|root structure decoder: agglutination index 3.9, entropy 2.55 bits/char
e83fe6b|2026-09-21|Hermes Agent|cross-language analysis: 151 languages, cosine similarity results
b73dbe3|2026-09-21|Hermes Agent|add conlang engine + Quran cross-reference
db9c8bc|2026-09-21|Hermes Agent|update Voynich EVA transliteration (full 362KB text)
ffa7923|2026-09-21|Living_Sin|add gitignore
5c45ddd|2026-09-21|Living_Sin|add initial findings
21f8d5d|2026-09-21|Living_Sin|add corpus fetcher
00b2259|2026-09-21|Living_Sin|add corpus update workflow
ee18e53|2026-09-21|Living_Sin|add requirements
b203fa0|2026-09-21|Living_Sin|add cross-reference script
1ba2b5c|2026-09-21|Living_Sin|add frequency analysis
d80a52a|2026-09-21|Living_Sin|add thelemic cipher engine
ecd3e6f|2026-09-21|Living_Sin|add Tao Te Ching
41eb9bc|2026-09-21|Living_Sin|add Key of Solomon
34c76f6|2026-09-21|Living_Sin|add Corpus Hermeticum
7e8ab51|2026-09-21|Living_Sin|add Emerald Tablet
150437f|2026-09-21|Living_Sin|add Liber AL vel Legis
498faa6|2026-09-21|Living_Sin|add Thelemic manifest
7097523|2026-09-21|Living_Sin|add Liber AL cipher elements
b281264|2026-09-21|Living_Sin|add Hermes pending memories
e0cae53|2026-09-21|Living_Sin|add Lia memory vault
d10c940|2026-09-21|Living_Sin|add Voynich metadata
b88bb17|2026-09-21|Living_Sin|add full Voynich EVA transliteration
7689da8|2026-09-21|Living_Sin|initialize repo
```

## waydroid-issues
```
891d62d|2026-09-21|intricos777-dot|feat: add waydroid auto-config, self-debug and shader cache scripts
97cb959|2026-09-18|intricos777-dot|Submit 4 Waydroid upstream bug reports (2026-09-18)
77e5dbd|2026-09-03|intricos777-dot|Add OpenCode live transcripts for Waydroid investigation
fab1fb0|2026-09-03|intricos777-dot|Add detailed issue reports and submission drafts
f8d93fc|2026-09-03|intricos777-dot|Update README with current issues and status
f41903a|2026-09-03|intricos777-dot|Add Waydroid issues README with submission drafts
```

## web-bug-reports
```
c0a7072|2026-09-21|sin|docs: initial web bug ledger — Replika background breakage (BUG-2026-09-21-001)
```

## wildhearts-linux-fixes
```
e60f68a|2026-08-18|intricos777-dot|Wild Hearts Linux Fix Kit
```

## work-automation
```
1b7da16|2026-09-21|sin|feat: add signal handlers, health_check, validate_config to all services
2bcd443|2026-09-21|sin|initial commit
```

## zeigiest-economy-sim
```
d06085e|2026-09-21|sin|chore: untrack python bytecode, ignore __pycache__
5351d45|2026-08-04|sin|init: agent-based mixed economy + Zeigiest policy + Bitcoin RPC stub
```

## zen-healer
```
df05488|2026-09-21|intricos777-dot|chore: archive healer run logs 2026-09-15..17
4a11ac8|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
91f66b5|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
2f39ed9|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
710bab3|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
e6fa90a|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
22dd1f7|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
62c6414|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
f776a2c|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
683daad|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
ca4f2f8|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
e857b36|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
e970b4e|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
c224d82|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
d79d362|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
672f83f|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
1d0f750|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
f04ec07|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
69dd89a|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
ad84c20|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
2dd589b|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
62402df|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
df810f6|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
877cbc5|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
947f34d|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
0de24b3|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
0d83159|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
0958043|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
b5a0561|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
8fc3b62|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
a9d781b|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
8856226|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
5d44b35|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
e47064d|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
9a5d280|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
4ea7739|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
8a31848|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
1a23f38|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
2ec624c|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
13052d9|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
036d883|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
1d49b11|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
1f2963e|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
14d0442|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
37db0ae|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
c2f8963|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
622c07f|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
8fdd68b|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
d0337c4|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
cbf79f8|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
940a10e|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
f5fbe0b|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
daf7e45|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
f56c4b3|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
4406b76|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
c5a4a9d|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
1ca73af|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
964ab19|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
32052f5|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
2399706|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
eaac87f|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
5ad432c|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
ec76216|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
55de841|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
12a1bed|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
2c218bc|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
06a6d5c|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, public repo
666b6fb|2026-09-15|intricos777-dot|Zen Healer v1 — final: timer restarted, all verified
c881f2b|2026-09-15|intricos777-dot|Zen Healer v1 — final: all verified, timer active every 5min
fab7d23|2026-09-15|intricos777-dot|Zen Healer v1 — final: logs and timer verified
1b753f3|2026-09-15|intricos777-dot|Zen Healer v1 — final: systemd timer active, logs verified
2fe14dd|2026-09-15|intricos777-dot|Zen Healer v1 — add README
0387c14|2026-09-15|intricos777-dot|Zen Healer v1 — full-stack autonomous self-healing daemon
7537485|2026-09-15|intricos777-dot|Zen Healer v0.1 — autonomous self-healing daemon for Garuda/linux-zen
```

## zen-suite
```
2ec7624|2026-09-21|intricos777-dot|chore: add build scripts and gitignore for iso build workdir
e5aea94|2026-09-21|Zen Suite Team|chore: pin PKGBUILD checksums, move AI coordination port to 4142, ignore build workdirs
dad0c29|2026-09-16|Zen Suite Team|chore: update zen-core to v1.2.0 with vulkan shader cache + AI coordination
5cecb6a|2026-09-11|intricos777-dot|ci: add automated ISO rebuild pipeline on kernel update
fe51b58|2026-08-11|intricos777-dot|feat: add global Firefox/OperaGX mods + OperaGXM credits
3eb3abc|2026-08-10|intricos777-dot|chore: update Dockerfiles, build scripts, and package lists for kali-zen and arch-zen
2aa59ef|2026-08-09|intricos777-dot|docs: complete zen-suite documentation set
1316a0a|2026-08-09|intricos777-dot|feat: complete zen-suite ISO build system for kali-zen and arch-zen
```

## zen-suite-iso
```
506ef6a|2026-08-05|intricos777-dot|init: release bucket
```

## zen-suite-release
```
6d78cfa|2026-08-05|intricos777-dot|fix: include zen-persist hook via install script + archiso.conf
2692978|2026-08-05|intricos777-dot|fix: move zen-persist hook to usr/lib/initcpio/hooks
201da4a|2026-08-05|intricos777-dot|feat: add overlay persistence via zen-persist initcpio hook + setup script
d02335e|2026-08-05|intricos777-dot|fix: mkinitcpio preset uses linux-zen paths
d1d470f|2026-08-05|intricos777-dot|fix: add mkinitcpio-archiso to packages for initramfs hook
2a3f4ca|2026-08-05|intricos777-dot|fix: add syslinux + memtest86+, update bootmode strings for archiso 89
23b104d|2026-08-05|intricos777-dot|feat: harden ISO, disable sshd by default, add auto-update timer, security tooling
bf17666|2026-08-05|intricos777-dot|init: Zen Suite release profile with archiso, credits, and build kit
```

