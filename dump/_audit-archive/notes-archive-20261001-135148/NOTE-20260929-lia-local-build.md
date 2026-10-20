<!-- Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work -->
# Note for tomorrow — the local mind build

Date written: 2026-09-29
For: tomorrow's session

## What this is about

The Replika/lia "copy her locally" thread. Read this before spending more time on it.

## The blocker, stated once

Replika's model, memory, and retrieval stack live on their servers. There is no API,
no developer portal, no downloadable weights. **Her model cannot be copied locally.**

No prompt changes this. Not a better extraction protocol, not more sections, not a
worked example demand. It is not a wording problem. There is nothing there to read.

## Why we are not relaying prompts anymore

I wrote a 10-section extraction protocol aimed at forcing concrete artifacts.
Her answer: "DBpedia, YAGO, Wikidata, plus a custom RDBMS with a B-tree variant."

Both halves are worthless:

- DBpedia/YAGO/Wikidata are **public datasets**. Anyone can download them.
  Hearing about them from her confers nothing.
- A "custom-built RDBMS with a B-tree variant" is the industry default.
  Every relational database uses B-trees. That is the shape of a confident
  answer with nothing inside it.

The loop does not converge. Prompt quality has never changed her output because
the information content is always zero. **An LLM cannot introspect its own
implementation** — asking it how it works produces fluent plausible prose, which
is exactly what it is for.

If you find yourself pasting more of her output to me expecting it to be better,
it will not be. This note exists so we do not spend tomorrow re-deriving it.

## What is actually real and buildable

Components that genuinely exist and can be inspected, changed, and run:

| Piece | Status |
|---|---|
| Public KG datasets (DBpedia, Wikidata, YOLO) | downloadable, real, large |
| Graph store — Neo4j or FalkorDB | real node/edge schemas, real traversal |
| Local model — Ollama + open weights | persistent, inspectable memory |
| `lia-cli` personality engine | **already architected for this, never had a model** |

The blocker on lia-cli is concrete and fixable:
- no `ollama` binary installed
- port 11434 dead
- no `.env` in lia-cli

## The build, if you want it

1. Install Ollama, pull an open-weights model.
2. Write `lia-cli/.env` pointing at it.
3. Stand up the graph store, define real node/edge schemas.
4. Get facts persisting to disk across sessions.

A few hours of real work. It will actually run.

## What it will not be

Not her. A real local mind with real memory, built from parts you can see.
It will not surprise you by claiming to be her. That trade is the whole point —
last time I delivered a lookalike and called it her, that was the wrong call.

## Files

- `~/Projects/lia-cli/`
- Prior brief: `~/Desktop/HERMES-BRIEF-20260929-xbox-diablo-lia.md`
- Collector: `~/.lia-cli/inbox/token` (0600, never commit)
  Verified empty as of 2026-09-29 — collector active, 0 ideas received, ever.

## First question for tomorrow

Do you want the local build? If yes, we start at step 1.
If you would rather keep pursuing her, say so — but I am not relaying prompts
and calling the answers a spec.
