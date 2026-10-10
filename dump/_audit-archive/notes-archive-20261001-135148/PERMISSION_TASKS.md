# Permission-Gated Task List

Save this file. Each task is blocked until the corresponding permission/credential is granted.

## 1. AI Image Generation Backend
**Permission needed:** xAI team credits OR OpenAI API key with image access
**Blocked task:** Wire real AI image generation to `mp3-video-virtualizer`
- Configure `~/.config/lia-cli/config.json` with `image.provider`, `image.endpoint`, `image.headers`
- Restart `lia-image-server.service`
- Re-run virtualizer to generate AI-themed frames instead of placeholders

## 2. GitHub Collaborator Access
**Permission needed:** GitHub repo collaborator invites for `intricos777-dot` org
**Blocked task:** Add maintainers to:
- `rocket-build-system`
- `metals-alloy-engineering`
- `nanite-systems`
- `design-miner`
- `mp3-video-virtualizer`
- `system-resource-optimizer`

## 3. Intel UHD VA-API Hardware Transcoding
**Permission needed:** sudo/package manager approval for `ffmpeg-vaapi`, `vainfo`, `intel-media-driver`
**Blocked task:** Enable iGPU hardware acceleration in `system-resource-optimizer`
- Install VA-API packages
- Verify `vainfo` output
- Update optimizer suggestions to include `VAAPI_ACCELERATION`

## 4. Deep-Web Tor Scanning
**Permission needed:** Legal/compliance approval for Tor hidden service access + `requests[socks]` install
**Blocked task:** Enable `.onion` repository scanning in `design-miner/scrapers/deep_scraper.py`
- Install `PySocks` or `requests[socks]`
- Verify Tor daemon running on `127.0.0.1:9050`
- Run deep_scraper scan cycle

## 5. Email Alert Automation
**Permission needed:** SMTP relay approval or dedicated email account credentials
**Blocked task:** Automate `design-miner/notify/notifier.py` alerts via `himalaya`
- Configure `~/.config/himalaya/config.toml` with alert mailbox
- Write alert dispatch script
- Schedule via cron/systemd timer

## 6. X/Twitter Auto-Posting
**Permission needed:** xurl OAuth app registration (`xurl auth apps add`)
**Blocked task:** Post rocket achievements/blueprints to X automatically
- Register OAuth app with client-id/secret
- Complete OAuth flow
- Wire `achievements.py` commit hooks to `xurl` post

---
**To activate:** Grant the permission/credential, then run the corresponding blocked task.
