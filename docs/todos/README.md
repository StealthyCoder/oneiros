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
- Feedback loop + orchestration layer - 2026-07-23, see
  [completed/feedback-loop.md](completed/feedback-loop.md).

Phase 1 (Proof of Concept) is fully built - all four items above are
shipped and verified against real infrastructure. Phase 2 isn't broken
into `docs/todos/` items yet; see the root README's roadmap for what
that phase covers.

## Open follow-on questions

Not build-order items - these are ideas and open questions on top of the
shipped Phase 1 loop, tracked so they aren't lost before there's time to
work through them:

- [active/narrative-latent-influence.md](active/narrative-latent-influence.md) -
  whether narrative content actually has any causal influence on
  subsequent imagery (currently: no). Open design question, blocks the
  item below.
- [active/blend-weight-gradient.md](active/blend-weight-gradient.md) -
  drifting `blend_weight` across a run on a sleep-cycle-shaped schedule
  instead of holding it fixed. Blocked on the item above.

See also [../findings/](../findings/README.md) for observations from
actually running the loop, which inform both items above but aren't
build-tracking work themselves.
