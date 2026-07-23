# Sleep-cycle-shaped blend-weight gradient

**Status: open, blocked on
[narrative-latent-influence.md](narrative-latent-influence.md).** Don't
build this until that's resolved — scheduling `blend_weight` to change
over a run only matters once `blend_weight` actually changes something
about the output, which right now it doesn't (see that file).

Once it does, the idea: instead of holding `blend_weight` fixed for the
whole run, drift it. Real REM sleep isn't linear across a night — cycles
come in waves that are short and shallow early, longer and deeper later.
A fixed 50/50 split held for an entire multi-hour run is a much cruder
model of that than a shaped drift would be.

**Shape.** An S-curve (slow start, faster shift through the middle,
levelling off) rather than a straight linear ramp — closer to how the
actual sleep-stage transition looks.

**Progress, without assuming an end.** The loop runs with no exit
condition by default
([feedback-loop.md](../completed/feedback-loop.md)), so "how far through
the run are we" isn't always answerable as a clean fraction. Two shapes
that both work, for different modes:

- **Bounded runs** (`--max-cycles` or `--max-spend` set): progress is
  cheap to compute — `cycle_number / max_cycles`, or
  `total_cost_usd / max_spend_usd` — drive the S-curve off whichever cap
  is active, and hold at the narrative-heavy end once the curve completes
  rather than resetting.
- **Unbounded runs** (the default): a fraction-of-total doesn't exist to
  compute. Two options - an elapsed-wall-clock arc (full S-curve over
  some fixed span, e.g. 8 hours, then hold), or **periodic mini-cycles**:
  reset the ratio back toward noise-heavy every ~90 minutes and climb
  again. Mini-cycles mirror real REM-cycle timing closely and, unlike the
  wall-clock arc, need no notion of an end at all - they're the more
  natural default for the loop's primary no-exit-condition mode, and
  would likely show the dream's character shift at each reset rather
  than drifting once and settling.

**Noise floor.** Keep some minimum fresh-noise share even at peak
narrative weight (e.g. 15-20%), as a general defensive habit against a
schedule ever pushing a parameter to an extreme it wasn't tested at -
though per
[narrative-latent-influence.md](narrative-latent-influence.md), this
isn't currently defending against a real risk: `blend_weight=1.0`
doesn't collapse the loop toward a repeated fixed point, since the
narrative seeding the latents is different (and Claude-generated, so
already unpredictable) every cycle. Worth keeping as a habit regardless -
just documenting that it isn't load-bearing yet.

**Log the ratio per cycle.** Whatever the schedule, write the resolved
`blend_weight` alongside each cycle's other output (`_save_cycle()`
currently writes only the image and narrative text) so cycles can be
correlated against where they fell on the gradient during later review.
