# Stable Diffusion imagery generation

**Status: done (built 2026-07-21).** Part of Phase 1 (Proof of
Concept) — see the [root README](../../../README.md#phase-1--proof-of-concept-minimal-cost-weeks-to-build).

`oneiros/imagery.py` turns the latents from
[noise-generator.md](noise-generator.md) into a picture — the visual
cortex equivalent. Two functions, split deliberately:

- `load_pipeline()` — loads the Stable Diffusion pipeline onto the
  GPU. Meant to be called once per process, not once per cycle: the
  upcoming [feedback-loop.md](../active/feedback-loop.md) stage runs
  with no exit condition, and reloading several GB of weights every
  cycle would make that impossible to run at any usable pace.
- `generate_image()` — takes an already-loaded pipeline plus a latent
  tensor and returns a `PIL.Image.Image`. No text prompt: imagery here
  is meant to come from the noise alone. `guidance_scale=1.0` skips
  classifier-free guidance's unconditional branch, which would
  otherwise double per-step cost for no benefit against an empty
  prompt.

Settled the two questions this item was waiting on:

- **Resolution** — stayed at 512x512, inherited from `noise.py`'s
  existing default rather than decided independently.
- **Output format** — a `PIL.Image.Image`, not pre-encoded bytes. It
  converts trivially to whatever
  [narrative-interpretation.md](../active/narrative-interpretation.md)
  turns out to need (base64 PNG/JPEG for the Claude Vision API), and
  that stage is better placed to decide the encoding trade-offs since
  they depend on API specifics this item shouldn't need to guess at.

Verified against the real pipeline, not just shape-checked:
`scripts/verify_imagery.py` generates latents, loads the pipeline,
runs `generate_image()` at 25 inference steps, and saves the result to
`output/verify_imagery.png` (gitignored) for a look. Produced a
coherent 512x512 image on the first real run — no NSFW black-frame
fallback this time, unlike the noise generator's 2-step verification
run, since 25 steps gives the model enough room to converge on
something real.

Real (environmental, not code) issue hit along the way: the dev
laptop's NVIDIA driver had updated but the machine hadn't rebooted,
so `nvidia-smi` and `pipe.to("cuda")` both failed with a driver/library
version mismatch (`cudaGetDeviceCount()` error 804 — "forward
compatibility was attempted on non supported HW"). Not something to
work around in code; fixed by rebooting, then re-running the verify
script to confirm the real GPU path.

25 inference steps was chosen as a middle ground rather than measured
against a real quality bar: SD1.5's usual default is closer to 50, but
this stage needs to run indefinitely inside a feedback loop with no
exit condition, so per-cycle wall-clock time matters more here than it
would for a one-off generation. Worth revisiting once the feedback
loop is running and it's clear whether 25 steps produces imagery
varied/coherent enough for the narrative-interpretation stage to work
with.
