# Feedback loop + orchestration layer

**Status: open.** Part of Phase 1 (Proof of Concept) — see the
[root README](../../../README.md#phase-1--proof-of-concept-minimal-cost-weeks-to-build).
Depends on the other three Phase 1 items existing first:
[noise-generator.md](../completed/noise-generator.md),
[image-generation.md](../completed/image-generation.md),
[narrative-interpretation.md](../completed/narrative-interpretation.md).

Python orchestration layer that wires the three stages together into
an actual cycle: noise → imagery → narrative, then takes part of that
narrative as a seed, blends in fresh noise, and starts the next cycle.
This is the piece that turns three independent stages into "the loop
runs" — the core deliverable of Phase 1 per the root README.

Deliberately **no exit condition** — the loop is meant to run
indefinitely rather than terminate after N cycles or on some
convergence check. Whatever stopping happens (for observation,
debugging, cost) should be an external interrupt, not something the
loop itself decides.

Out of scope for Phase 1 (see Phase 2/3 in the root README): audio,
video, emotional state tracking, and splitting this into separate
brain-region agents. This item is just the single-loop PoC.
