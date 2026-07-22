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

## Build order (Phase 1)

Roughly the order the pipeline needs to come together in - each stage
feeds the next. Shipped so far:

- Random seed/noise generator - 2026-07-20, see
  [completed/noise-generator.md](completed/noise-generator.md).
- Stable Diffusion imagery generation - 2026-07-21, see
  [completed/image-generation.md](completed/image-generation.md).
- Claude Vision narrative interpretation - 2026-07-22, see
  [completed/narrative-interpretation.md](completed/narrative-interpretation.md).

Remaining, in order:

1. [Feedback loop + orchestration layer](active/feedback-loop.md) -
   wires the above three together, feeds narrative back in as the next
   seed, runs with no exit condition.
