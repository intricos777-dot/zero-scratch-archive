<!-- Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work -->
GitHub account is intricos777-dot (120 repos, mostly private). As of 2026-09-26: no `gh` CLI, no token on disk (~/.config/gh is empty), and the ~/.ssh/id_ed25519 key is offered to github.com but REJECTED — so neither push nor repo creation works until the user registers a key or supplies a token. lifsea-security-suite has an SSH remote but cannot currently be pushed.
§
Root installs need a sudo password (passwordless sudo unavailable) — hand PAM/udev/systemd/firewalld changes to the user as an exact `sudo <script>` command rather than trying to run them or asking for the password.
§
~/Projects/_inventory/ holds scratch full-history clones of all 120 GitHub repos (1.1G) for audit work; ~/Projects/_inventory/{_verify.json,_secrets.json,_clone_results.json} hold audit output. Keep audit clones separate from real working checkouts.
§
lifsea/lia-cli: the Replika Tampermonkey bridge (bde-security-biometrics/tampermonkey/lia-idea-bridge.user.js) posts {lines:[...]} to 127.0.0.1:4124 and only advances its ack on HTTP 200. Collector is ~/Projects/lia-cli/src/inbox-server.ts, run as user service lia-inbox-collector.service; bearer token generated 0600 at ~/.lia-cli/inbox/token. Tests must use ports 47314/47324, never 4124.
§
Toolchain quirks on this box: uv is the installer (no system pip; PEP 668), python3 is 3.14. `pkill -f <script>` matches systemd user units' ExecStart and kills live services — kill by PID. Piping a background job inline truncates the terminal tool's output capture; write to a file and read it. Heredocs inside execute_code f-strings break on \n — use write_file or the patch tool.
§
Standing convention: any security- or business-related work is pushed to GitHub as a PRIVATE repo by default, always. Never create these as public without asking first.
§
Account: uid=1000 `livings`, home /home/livings, GECOS name `Living_Sin` (that is the 'Sin' in old repo paths). Old host used /home/sin — 72 of 120 inventory repos still hardcode it.
§
faillock unlock_time=30 is a deliberate operator choice, not drift — do not "fix" to 1800. Current audit artifact: ~/Projects/REBUILD-TODO-20260928.md (supersedes REBUILD-TODO.md).