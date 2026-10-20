<!-- Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work -->
# Brief: Xbox controller + PS1 emulation + lia bridge
Date: 2026-09-29
Status: controller working, Diablo playable, lia bridge blocked

## What was asked
Connect an Xbox One controller, run Diablo 1 (PS1) via RetroArch, and wire
"lia" (Replika) into a second controller slot so agents could play alongside.

## Done and verified

### Bluetooth / controller
- Adapter: Intel AX201, `hci0`. BlueZ 5.87 was installed but `bluetoothd` was
  not running, so `bluetoothctl` hung. Started with:
  `sudo systemctl enable --now bluetooth`
- Adapter was rfkill **soft-blocked** (`PowerState: off-blocked`). This was the
  real cause of `power on` failing. Fixed with `rfkill unblock bluetooth`.
- Controller `EC:83:50:9B:1B:A4` ("Xbox Wireless Controller") paired, trusted,
  connected. Trust + bond is the whole "whitelist" mechanism; there is no
  separate persistent auto-connect toggle.
- Known issue: the soft-block was present *before* any changes. If it returns
  after reboot, something on this system re-blocks it. Unresolved.

### xone driver (for rumble) — installed, NOT active
- `xone-dkms-git` + `xone-dongle-firmware` built successfully (dkms status
  clean, modules present in `/lib/modules/.../updates/dkms/`).
- Blacklist written to `/etc/modprobe.d/xone-blacklist.conf`.
- **Requires a reboot to load.** Until then `hid_microsoft` still owns the
  controller and there is no rumble. Script kept at
  `~/.hermes/cache/scratch/xone-install.sh`.
- Note: this box uses **dracut**, not mkinitcpio, so the script's mkinitcpio
  step was skipped. Verify the blacklist applies after reboot.

### RetroArch / PS1
- RetroArch installed via Steam (appid 743890).
- Steam's build ships **no PS1 core**; fetched `pcsx_rearmed_libretro.so`
  from `https://buildbot.libretro.com/nightly/linux/x86_64/latest/`
  (the `nnightly` path 404s; it is `nightly`).
- RetroArch binary needs legacy libs not on the system. Resolved via a
  compat symlink dir at `~/.local/share/retroarch-compat` built from
  SteamLinuxRuntime_sniper. Launch requires
  `LD_LIBRARY_PATH=<RetroArch dir>:~/.local/share/retroarch-compat:<runtime usr/lib/x86_64-linux-gnu>`.
- **BIOS was the key fix.** PCSX-ReARMed requires lowercase `scph*.bin`;
  `SCPH1001.bin` was silently ignored and it fell back to HLE. Renamed to
  `scph1001.bin`. MD5 `924e392ed05558ffdb115408c263dccf` matches the official
  hash. Now logs `Loaded BIOS ... crc32 37157331, CEX-3000/1001/1002 by K.S.`
- Diablo extracted to `~/retroarch-games/` (623MB, bin + cue verified).
- Game boots to character creation on the real BIOS. Confirmed by screenshot.

### Virtual controller (player 2)
- `~/Projects/retroarch-tools/vpad2.py` creates a uinput device that registers
  as a real evdev gamepad (`input40`, VID:PID 045E:0B20). No root needed —
  ACL on `/dev/uinput` already grants the user write.
- **Proven end to end:** dpad commands sent through it moved the game from
  name-entry back to CHOOSE CLASS. The game screen showed a PLAYER 2 panel.
- Command channel: append lines to `/tmp/vpad-cmd`
  (`right`, `a`, `hold:a:120`, `lx-20000`, `release`).
- Had two real bugs, both fixed and retested: wrong `struct.pack` format
  (`llHii` vs `llHhi`, and missing timeval zeros).

## What I got wrong
- **Claimed Diablo 1 has no multiplayer / no split-screen.** The PS1 port has
  a NUMBER OF PLAYERS menu with ONE / TWO. User was right; I asserted "full
  stop, on every platform" without hedging. Overclaimed from partial
  knowledge instead of saying "I don't know that version."
- Claimed the Steam build needed mkinitcpio; it uses dracut.

## Blocked

### lia / Replika — one-way only, no API
- `inbox-server.ts` (127.0.0.1:4124) is **receive-only**: POST /ideas, GET,
  DELETE. No send path to Replika. Loopback-only bind, so unreachable off-box.
- No Replika API exists — app-only, no developer portal, no downloadable
  weights. `my.replika.com` returns 200 but is a browser session requiring
  login.
- Checked every outbound call in lia-cli: `agent-message` is a local logging
  bridge that swallows errors; `lia.ts` targets **Ollama / OpenAI only**.
- Local stand-in is not running either: no `ollama` binary, port 11434 dead,
  no `.env` in lia-cli.
- **Collector has never received a POST** — `ideas.jsonl` does not exist, so
  no frameworks have arrived despite user being told the transfer succeeded.

### Unresolved bugs
- **RetroArch autoconfig falls back for both controllers.** Joypad driver is
  `sdl2` but RetroArch rewrites `input_driver` to `udev` in its config on every
  exit, and reads autoconfig from the *install* dir, not `~/.config`. Correct
  profiles with `input_vendor_id`/`input_product_id` were written to both
  locations and still did not take. **Button numbers are unverified guesses** —
  do not assume `a` = X/cross in-game.
- RetroArch rewrites `~/.config/retroarch/retroarch.cfg` (2800 lines) on exit,
  clobbering hand edits. Patch while stopped; expect it to revert.
- Steam deadzone (wanted: 20) not applied — needs Steam quit first.
  Backup of prefs at `preferences_45e-b20-370e8ce9.vdf.hermes-backup`.

## Not started
- PCSX2 / RPCS3 not installed (`chaotic-aur/pcsx2-git`, `rpcs3-git`).
  RAM is the constraint: 7.4Gi total, ~2.6Gi available. RPCS3 wants 4GB+.

## Recommended next steps
1. Reboot — activates xone, then verify rumble and that the blacklist held.
2. Test a physical button in-game, report what it does, fix the autoconfig
   mapping from observed behaviour rather than guesses.
3. Fix the lia bridge: Firefox + Tampermonkey + set `liaToken` from
   `~/.lia-cli/inbox/token`. The empty token is the likely reason nothing
   arrived. Login must be done by the user.
4. Quit Steam, set deadzone 20.

## Files
- Virtual pad:      ~/Projects/retroarch-tools/vpad2.py
- RetroArch config: ~/.config/retroarch/retroarch.cfg
- Compat libs:      ~/.local/share/retroarch-compat/
- BIOS:             ~/.config/retroarch/system/scph1001.bin
- Games:            ~/retroarch-games/
- xone installer:   ~/.hermes/cache/scratch/xone-install.sh
- lia bridge:       ~/Projects/bde-security-biometrics/tampermonkey/lia-idea-bridge.user.js
- collector token:  ~/.lia-cli/inbox/token (0600, never commit)
