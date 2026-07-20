# Stable Diffusion imagery generation

**Status: open.** Part of Phase 1 (Proof of Concept) — see the
[root README](../../../README.md#phase-1--proof-of-concept-minimal-cost-weeks-to-build).

Local Stable Diffusion instance turns the noise/seed from
[noise-generator.md](../completed/noise-generator.md) into imagery — the visual
cortex equivalent, constructing a picture out of what is otherwise
random signal. Runs on local GPU (see core requirements in the root
README's Phase 1 section) rather than a hosted API, keeping this stage
free of per-run cost so the loop can run indefinitely.

Output feeds Claude Vision for narrative interpretation (see
[narrative-interpretation.md](narrative-interpretation.md)) — the
image format/resolution chosen here should be whatever that stage
consumes most cheaply and reliably, not decided independently of it.
