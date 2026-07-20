# Todos

Breaks Phase 1 (Proof of Concept) out of the root README's prose
roadmap into one file per unit of work, following the same
active/completed split used elsewhere:

- `active/` - not built yet. One file per item.
- `completed/` - built and shipped. Kept (not deleted) as the detailed
  record of what was built, real bugs caught along the way, and
  deliberate scope decisions.

The root [README.md](../../README.md) stays the narrative/context doc
- what this project is and why, plus the full Phase 1-4 roadmap at a
glance. This directory is where Phase 1 gets tracked at build-item
granularity as it actually happens. Phases 2-4 aren't broken out yet -
do that once Phase 1 is far enough along to make it worthwhile.

## Build order (Phase 1, all open)

Roughly the order the pipeline needs to come together in - each stage
feeds the next:

1. [Random seed/noise generator](active/noise-generator.md) - brainstem
   equivalent, the raw signal everything else is built from.
2. [Stable Diffusion imagery generation](active/image-generation.md) -
   turns the noise into an image, local GPU.
3. [Claude Vision narrative interpretation](active/narrative-interpretation.md) -
   narrates the imagery, high temperature + logic suppression.
4. [Feedback loop + orchestration layer](active/feedback-loop.md) -
   wires the above three together, feeds narrative back in as the next
   seed, runs with no exit condition.

Nothing completed yet - `completed/` will fill in as Phase 1 items
ship.
