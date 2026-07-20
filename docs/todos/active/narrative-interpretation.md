# Claude Vision narrative interpretation

**Status: open.** Part of Phase 1 (Proof of Concept) — see the
[root README](../../../README.md#phase-1--proof-of-concept-minimal-cost-weeks-to-build).

Claude Vision looks at the imagery produced in
[image-generation.md](image-generation.md) and narrates it — the
stage standing in for the parts of the dreaming brain that build a
coherent story out of chaotic input (hippocampus pulling in memory-like
association, amygdala colouring it emotionally) while the logic centre
stays offline.

Two deliberate, non-default settings, called out explicitly in the
root README because they're the whole point of this stage rather than
incidental tuning:

- **High temperature** — favour novel/unexpected narration over the
  most probable continuation.
- **Logic suppression via system prompt** — explicitly instruct against
  the model's default tendency to rationalise, explain, or impose
  coherence on the imagery. This is the closest analogue to the
  prefrontal cortex going offline during dreaming, and is the
  mechanism most likely to need iteration once real output is seen.

Output narrative becomes the input to
[feedback-loop.md](feedback-loop.md), which turns part of it into the
seed for the next cycle.
