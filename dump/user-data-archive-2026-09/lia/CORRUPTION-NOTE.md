# Lia.CLI — older corrupted versions: findings

## What was found (2026-09-26, hermes session 20260926_121135_408774)

Hermes verdict while auditing the 120-repo inventory clone:

    `lia-cli` is corrupted source — truncated imports and docstring text used as code. This never worked.

Evidence captured at the time (verify_all.py syntax failures):

    === lia-cli: broken at line 8? ===
    from owlready2 import
    onto = get_ontology("http://example.com/myOnto.owl")
    ...

## Where the corrupted/older files live

- `lia/older-corrupted/kg_schema.py` — the truncated owlready2 file (320 bytes, never valid Python).
- `lia/older-corrupted/main.py` / `__init__.py` — one-line click stubs from the original standalone commit (39f544b).
- `lia/older-corrupted/ssh-keygen-transcript-old-host.txt` — `.env`-adjacent artifact `keygen key.txt` from upstream:
  transcript of an ssh-keygen run on the OLD machine `/home/sin`, host `sin-asustufdashf15fx517zcfx517zc`
  (fingerprint only — no private key material).
- `lia/older-corrupted/data/` — memory vault + legal reports as of the upstream clone (commit 609f4bc).
- `lia/lia-cli-full-history.bundle` — full git history of lia-cli (restore with `git clone lia-cli-full-history.bundle`).
  The corrupted files were DELETED in commit f0f6235 (2026-09-26) and exist only in history — bundle preserves them.

## Memories recovered from Lia.CLI

- `lia/current-checkout/data/memory/lia-memory.vault.json` — vault created 2026-07-17, 3 entries
  (2 plaintext test entries + 1 AES-encrypted hidden entry).
- `lia/scattered-memory-copies/lia-vault.json` — separate vault copy created 2026-09-03, 1 entry
  ('opened replika bridge via browser from Lia skillbridge').
- `lia/scattered-memory-copies/hermes-pending-memories.json` — 18K pending hermes memory batch (2026-09-21).
- `lia/current-checkout/data/legal_report_20260721_*.json` — two legal scans from 2026-07-21 (both empty: 0 emails/memories).
- `lia/tasks/` — active-plan + supercode task files (2026-09-26).

## Already on GitHub (not duplicated here)

- lia-cli full history: github.com/intricos777-dot/lia-cli (private) — bundle above is a belt-and-braces copy.
- lia-groq-bridge, living-sin-models/lia-sync.py, metals-alloy-engineering/lia_memory_bridge.py,
  nanite-systems/lia_nanite_bridge.py — all present in ~/Projects/_inventory clones (already pushed).
