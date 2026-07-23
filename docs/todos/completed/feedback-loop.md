# Feedback loop + orchestration layer

**Status: done (built 2026-07-23).** Part of Phase 1 (Proof of Concept) — see
the [root README](../../../README.md#phase-1--proof-of-concept-minimal-cost-weeks-to-build).
Last of the four Phase 1 items — wires
[noise-generator.md](noise-generator.md),
[image-generation.md](image-generation.md), and
[narrative-interpretation.md](narrative-interpretation.md) into an actual
cycle. This is "the loop runs" — the core deliverable of Phase 1.

`oneiros/loop.py` splits the same way the prior three stages do:

- `run_cycle()` — one noise → imagery → narrative pass, ending with the
  latents primed for the next pass. Pure with respect to disk/process state
  (no I/O beyond the GPU/API calls the prior stages already make), so it's
  testable without a real pipeline or API key.
- `run_loop()` — the actual `while True`, plus artifact saving and the stop
  conditions below. `scripts/dream.py` is its driver — the real PoC entry
  point, not a one-off verify smoke test like the other three.

## Narrative → next seed

The root README specifies the narrative becomes a *partial* seed, and
[noise-generator.md](noise-generator.md) already flagged that this needs
real tensor blending rather than a bare seed swap — that's why
`generate_latents()` returns a tensor, not just an int. Settled shape:

- **Partial**: the seed is derived from only the last 12 words of the
  narrative (`_seed_from_narrative()`), not the whole text — whatever the
  dream was doing right as it faded, not an anchor to everything it said.
  Hashed via `hashlib.sha256` (not Python's per-process-randomized `hash()`)
  for determinism.
- **Blending**: that hash seeds a `generate_latents()` call to produce a
  narrative-derived latent tensor, which is then mixed with an independent
  `generate_latents(seed=None)` fresh-noise tensor via
  `w·narrative + √(1-w²)·fresh` (`_blend_latents()`, default `w=0.5`,
  exposed as `--blend-weight`). That's a variance-preserving mix for two
  independent unit-normal tensors — a plain average would quietly shrink
  variance cycle over cycle and drift the diffusion pipeline toward flatter,
  less-noisy input over a long run, which a loop with no exit condition
  would run into eventually.

## Stopping the loop

The loop still never decides to stop on its own — no convergence check, no
"this looks done." What changed from the original design is that a caller
can now opt into external caps, the same category as an interrupt signal
rather than something the loop concludes about its own output:

- **Ctrl+C** — free; `run_loop()` catches `KeyboardInterrupt` around the
  cycle body so a manual stop ends with a clean summary line instead of a
  raw traceback, then exits.
- **`--max-cycles N`** — stops after N cycles.
- **`--max-spend USD`** — stops once cumulative Claude API spend (the only
  metered cost in the pipeline — Stable Diffusion is local) reaches the
  cap. Needed `narrate_imagery()` in `oneiros/narrative.py` to start
  returning cost alongside text, so it now returns a `Narration(text,
  cost_usd)` dataclass instead of a bare string; `cost_usd` is computed from
  `response.usage.{input,output}_tokens` against `claude-sonnet-4-5`'s
  published per-token rate (`INPUT_PRICE_PER_MTOK` / `OUTPUT_PRICE_PER_MTOK`
  in `narrative.py`, confirmed against Anthropic's live pricing docs
  2026-07-23 — not exposed via the Models API, so there's nowhere to fetch
  it at runtime; worth re-checking if the model tier ever changes).
  `scripts/verify_narrative.py` updated for the new return shape.

Both caps default to unset, so the default behavior is still unbounded —
opting into a bound is a deliberate per-run choice (`python scripts/dream.py
--max-cycles 20 --max-spend 5.00`), not a change to what the loop does when
you don't ask it to stop.

## Artifacts

Each cycle's image and narrative are saved to
`output/dreams/<run-timestamp>/NNNN.{png,txt}` (gitignored, same convention
`verify_imagery.py` uses) rather than only printed — a long unattended run
needs something to look at afterward, and this is the record Phase 4's
later "recurring themes" monitoring would eventually work from.

## Verification

Ran for real, not just mocked: `python scripts/dream.py --max-cycles 2`
against the cached Stable Diffusion pipeline and the real Claude API.
Produced two coherent, distinct dream-register narratives (fleshy pink
ground-cover breathing under silver cracks; a bird nested in antler-or-coral
branches) with no rationalizing language and no "image" framing carried
over from the narrative stage — confirming the loop stays in character
across a real cycle, not just the first call. Seed derivation, blending,
per-cycle cost, and the `--max-cycles` stop all behaved as designed:
correct running total ($0.0061 + $0.0055 = $0.0116), clean stop message,
artifacts written. `run_cycle()`, `_seed_from_narrative()`, and
`_blend_latents()` also covered directly with mocked pipeline/client calls
before the real run, to pin the wiring and the blend's variance behavior
independent of GPU/API cost.

No real bugs hit this time — the three prior stages' interfaces
(`generate_latents()`'s `(tensor, seed)` return, `generate_image()`'s plain
`Image`, `narrate_imagery()`'s now-`Narration` return) composed without
needing changes beyond the `Narration` extension above.

Phase 1 (Proof of Concept) is now fully built — noise, imagery, narrative,
and the loop tying them together all exist and have been verified against
real infrastructure. Phase 2 (Sensory Expansion) isn't started, and per
[docs/todos/README.md](../README.md) won't be broken into its own
`docs/todos/` items until it's worth doing so.
