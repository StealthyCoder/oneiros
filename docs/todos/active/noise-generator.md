# Random seed/noise generator (brainstem equivalent)

**Status: open.** Part of Phase 1 (Proof of Concept) — see the
[root README](../../../README.md#phase-1--proof-of-concept-minimal-cost-weeks-to-build).

Generates the random signal that stands in for brainstem activity
during dreaming — the raw noise everything downstream (imagery,
narrative) gets constructed from. This is the first stage of the
feedback loop and has no upstream input of its own within a fresh
cycle; later cycles blend this with the previous narrative's partial
seed (see [feedback-loop.md](feedback-loop.md)).

Needs to produce whatever seed/noise format the image generation stage
(Stable Diffusion) expects as input — shape and format to be pinned
down alongside [image-generation.md](image-generation.md) rather than
decided in isolation.
