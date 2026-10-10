# Provenance records

Local, not committed to any repository. These exist to answer "who wrote this
and under what terms" if a third party ever asserts a claim.

## Authorship position

- Operator: `intricos777-dot` (Living Sin)
- Public repos: MIT, `Copyright (c) 2026 intricos777-dot`
- Third-party code: relocated to private repos, see each repo's
  `THIRD_PARTY_NOTICE.md`

**Agent-assisted authoring.** A significant share of this fleet was written
with AI agent assistance (Hermes, opencode, and related tooling). The US
Copyright Office position is that copyright requires human authorship, and that
purely AI-generated material is not protectable. Where a file is wholly
agent-generated, an MIT grant may be of doubtful validity, which leaves it
effectively **unlicensed** rather than protected.

This is recorded here rather than in public repo files. Publishing
AI-authorship disclosures was deliberately left to the operator: it is a
reputational and commercial decision, not a technical one, and several public
repos (portfolio sites, product repos with pricing) would be affected.

**Action recommended before relying on MIT over the whole fleet:** have a
copyright attorney review the agent-generated files and decide whether to
assert a licence over them, dual-license, or leave them undisclosed-but-
unlicensed. Not actioned unilaterally.

## Tamper-evidence

GPG signing key created 2026-09-29 to provide tamper-evidence, which copyright
does not: copyright does not prevent a fork or an edit. Signatures do allow
detection of a rewritten tag or commit.

- Fingerprint: `633AE761D5E54C3C59286FF06537201C5AA459C7`
- Public key + revocation cert: `~/.local/state/quarantine/gpg-backup-20260929/`
  (see `REVOCATION-NOTES.md` there)
- **6 tags across 5 repos are signed and pushed:** `gaming-unified v1.0.0`,
  `bde-security-biometrics v1.0.0`, `linux-zen-suite v1.0.0` and `v1.2.0`,
  `linux-zen-build v1.0.0-stable`, `zen-suite-iso v2026.08.05`.

**The private key was shredded on 2026-09-29, on purpose.** Deleted from the
keyring and the exported copy shredded 4 passes. The public key was kept,
because verification only needs the public half and the signatures above must
stay checkable. `user.signingkey` / `tag.gpgsign` / `commit.gpgsign` were
removed from git config so no future commit fails against a dead key.

**Consequence:** nothing can be signed with this identity again. The pacman
repo build in `bde-security-biometrics/scripts/sign-repo.sh` now exits with "no
GPG secret key found" and will refuse to publish an unsigned repo. Generating
a new key is required to resume signing or to publish that repository.

## What the pre-push gate does and does not catch

`~/.git-hooks/pre-push` blocks vendored dependency trees, declared copyleft
licences, and foreign copyright headers. It passed `gaming-unified` while that
repo was publishing 973 files of GPL-3.0 and GPL-2.0 code under an MIT licence,
and it passed `bde-security-biometrics` while 3,971 third-party objects sat in
history. **The gate is not a provenance audit.** It raises cost; it is not proof
of authorship, and it does not inspect history.
