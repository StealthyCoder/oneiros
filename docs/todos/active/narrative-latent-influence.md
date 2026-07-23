# Does narrative content actually influence subsequent imagery?

**Status: open — design question, not yet decided.** Surfaced while
looking at whether [oneiros/loop.py](../../../oneiros/loop.py)'s
`blend_weight` is worth scheduling over a run (see
[blend-weight-gradient.md](blend-weight-gradient.md), which is blocked on
this).

[feedback-loop.md](../completed/feedback-loop.md) documents `blend_weight`
as controlling the mix between narrative-derived and fresh noise. That's
true at the mechanism level, but not at the level a reader would probably
assume: for two independent unit-Gaussian tensors `A` and `B`,
`w·A + √(1-w²)·B` is *itself* unit-Gaussian, for every `w` between 0 and
1 — that's what "variance-preserving" means. Since both
`narrative_latents` and `fresh_latents` are independent unit-Gaussian
draws (separate `torch.Generator` seeds, no shared state), the blended
tensor Stable Diffusion receives is statistically indistinguishable from
plain fresh noise regardless of `blend_weight`. The parameter changes
reproducibility — identical narrative text would reproduce identical
latents — but not the character of what gets generated, at any setting.

That means "narrative becomes partial seed for the next cycle" (root
README) is satisfied literally — the seed genuinely depends on the
narrative's last 12 words — but not in the sense of narrative *content*
shaping subsequent *imagery*. `hashlib.sha256` is exactly as opaque to
meaning as it needs to be for determinism, which also means two
narratives about the same theme in different words land on unrelated,
uncorrelated seeds. There's currently no path from what a narrative
*says* to what the next image *looks like*.

Options, none chosen yet:

- **Leave it as a determinism property, not a content-steering one.**
  Phase 1's loop was scoped as noise → imagery → narrative → next seed;
  real content-level feedback (memory, emotional coloring, thematic
  continuity) may squarely be a Phase 3 concern — that's what the
  Hippocampus and Amygdala agents in the root README's roadmap are for —
  and Phase 1's job was to prove the mechanical loop runs, which it does.
- **Feed narrative text to Stable Diffusion as an actual prompt**, with
  `guidance_scale` doing real work instead of sitting at `1.0` against an
  empty string. This is the standard, well-supported way text shapes
  diffusion output. It directly reverses
  [image-generation.md](../completed/image-generation.md)'s deliberate
  "no text prompt — imagery comes from noise alone" decision, which
  exists to keep the visual cortex pre-linguistic and logic/language
  confined to the narrative stage. Crossing that line needs to be a
  deliberate call on its own, not a side effect of making a gradient
  feature do something.
- **Some other structural feedback that isn't full prompt-conditioning**
  — e.g. deriving a noise perturbation from a semantic text embedding
  rather than a hash, so similarly-themed narratives land near each other
  in latent space instead of at uncorrelated points. Unexplored; brings
  in a model dependency and a different (embedding-based, not
  hash-based) notion of "partial seed" than what's built now.

Not resolving this inline — it changes what "the loop" is even trying to
demonstrate, and deserves its own decision rather than getting folded
into scheduling work on top of it.
