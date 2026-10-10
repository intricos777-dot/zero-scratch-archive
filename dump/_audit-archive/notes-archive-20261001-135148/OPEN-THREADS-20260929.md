# Open threads — run tomorrow

Date written: 2026-09-29, end of session
For: tomorrow's first task, before anything else

---

## DONE AND VERIFIED — do not redo

Five directories are now `700` (owner-only). Confirmed twice by `stat`, not assumed:

```
700 /home/livings/Projects
700 /home/livings/.hermes/cache
700 /home/livings/.hermes/backups
700 /home/livings/.hermes/bin
700 /home/livings/.hermes/.curator_backups
```

This was the real work. Your Projects tree and Hermes data are no longer
world-readable. **Nothing else from this session landed.**

---

## NOT DONE — step 4 never executed

`/etc/sudoers.d/10-hermes-owner` **does not exist.** Verified today:

```
sudo ls -l /etc/sudoers.d/10-hermes-owner
ls: cannot access '/etc/sudoers.d/10-hermes-owner': No such file or directory
```

The `install` command was never run. Not a failure — it just didn't happen.

The file to install is staged and ready at:

```
/home/livings/.hermes/cache/scratch/10-hermes-owner
```

877 bytes, root-bound, with explanatory comments. Contents grant **nothing new** —
it is equivalent to existing `wheel` membership. It exists to document and pin the
invariant that one account holds root. **No NOPASSWD line. Password still required.**

### To finish it

```
sudo install -o root -g root -m 440 /home/livings/.hermes/cache/scratch/10-hermes-owner /etc/sudoers.d/10-hermes-owner
```

```
sudo visudo -c
```

Expect `10-hermes-owner: parsed OK` in the output. If visudo reports any syntax
error, stop — it refuses to install and sudo stays as-is.

**Honestly: this step is optional.** It changes no permissions. Skip it permanently
if it's not worth the trouble; the only thing lost is a comment in the system's
config. Do not treat it as outstanding work with real risk.

---

## UNREAD — /etc/sudoers.d/opencode

`visudo -c` listed this file. **I have never seen its contents.**

```
/etc/sudoers.d/10-installer: parsed OK
/etc/sudoers.d/editor: parsed OK
/etc/sudoers.d/insults: parsed OK
/etc/sudoers.d/opencode: parsed OK
/etc/sudoers.d/pwfeedback: parsed OK
```

Known unknown: does it contain `NOPASSWD`? I assumed the worst when I flagged it
and should have said so at the time. It may equally be a rule that *restricts*
opencode. **No assumption either way has been verified.**

```
sudo cat /etc/sudoers.d/opencode
```

Read it, paste it back, then decide. Do not change it without discussing first.

### Correction I owe you

Earlier this session I called your box "single-tenant" on the strength of
`/etc/passwd` and `wheel` group membership. Both were accurate — one login-shell
user, and `wheel` contains only `livings`. But **sudoers drop-in files grant rights
outside group membership**, and `/etc/sudoers.d/` is `0711` — listable by name,
unreadable in content by a normal user. So that claim was narrower than I stated.
What I actually verified: no second *account* exists. What I did not verify: what
the root config grants to specific names.

---

## BOOT CHECK — all green except three notes

Clean: 0 failed units (system + user), fsck passed, btrfs scrub ran, root LUKS
healthy, disk 67% / 161G free, load 0.51, zero failed SSH logins.
Services active: `lia-inbox-collector`, `coordination-server`, `autoguard`.
coordination-server health `{"status":"ok"}`. Linger=yes. Autoguard swept 4798
files, 0 quarantined, 14 paths protected.

1. **`sudo -n true` in the journal — resolved, not a threat.** The terminal tool
   probes sudo capability before privileged commands. Proven: I ran `sudo -n true`
   at 18:36:26 and that exact line appeared. Five of seven entries in that window
   were mine. If you want the noise gone, give the tool narrow NOPASSWD
   (`systemctl`, `journalctl`, `bluetoothctl`, `rfkill`) so the probe *succeeds*
   and leaves a real audit trail — better than `Defaults !syslog_sudo`, which
   hides the trail too. Optional.

2. **xone driver — installed, not yet proven.** `dkms status` shows
   `xone/0.5.8 7.2.7-zen1-1-zen installed`, blacklist written correctly, but
   `hid_microsoft` still loaded. Your controller was not paired at check time, so
   neither confirmed nor refuted. Power it on and verify.

3. **Stale nvidia DKMS entry** — registered for `6.19.6-zen1` with "Built modules
   are missing." Cosmetic; disappears when that kernel is dropped.

**Not security issues:** TDX unsupported by host, touchpad jump (libinput kernel
bug), multicast RX on wlo1, bluetoothd set-mode failures. All cosmetic/expected.

---

## TOOLING TRAP — hit twice tonight

A command you thought you ran in the shell was actually answered by the **opencode
TUI**, which replied to a sudo question as though it were a repo question
("What changed in this repo recently?").

Tell-tale: `"path": Permission denied (os error 13)` is a **Python/Rust wrapper**
error. Coreutils `ls` says `ls: cannot access '...': Permission denied`. If you see
`os error 13`, that is not your shell.

Also: `/etc/sudoers.d/` is not user-readable. `ls` inside it fails *even for an
existing file*. Do not read that as "file missing."

**Before running anything: confirm your prompt is a bare shell** — no box-drawing
around it, no status line. Ctrl+C or `/exit` to leave opencode.

---

## Related on Desktop

- `NOTE-20260929-lia-local-build.md` — the Replika/local-mind decision
- `HERMES-BRIEF-20260929-xbox-diablo-lia.md` — controller, Diablo, lia bridge

---

## Tomorrow's order

1. `sudo cat /etc/sudoers.d/opencode` — the only genuine unknown
2. Optionally install the staged sudoers file (skip if not worth it)
3. Power on Xbox controller, verify xone took effect
4. Decide on the local-mind build (`NOTE-20260929-lia-local-build.md`)
