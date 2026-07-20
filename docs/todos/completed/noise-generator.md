# Random seed/noise generator (brainstem equivalent)

**Status: done (built 2026-07-20).** First piece of Phase 1 (Proof of
Concept) — see the [root README](../../../README.md#phase-1--proof-of-concept-minimal-cost-weeks-to-build).

`oneiros/noise.py`'s `generate_latents()` produces the raw noise the
rest of the pipeline builds on. Settled the shape/format question this
item was waiting on: a Stable Diffusion UNet latent tensor (4 channels,
8x spatial downsample from the target image size — `(batch, 4, 64,
64)` for a 512x512 image), not a generic noise blob or a bare seed
integer. A bare seed wouldn't support the feedback loop's later
requirement of blending a narrative-derived seed with fresh noise each
cycle (see [feedback-loop.md](../active/feedback-loop.md)) — an actual
latent tensor does, since it can be blended/perturbed directly.

Seeded via a local `torch.Generator` rather than torch's global RNG,
with the seed returned alongside the tensor — keeps runs reproducible
and loggable with no global-state side effects.

Verified against a real pipeline, not just shape-checked in isolation:
`scripts/verify_noise.py` loads `stable-diffusion-v1-5/stable-diffusion-v1-5`
(fp16, attention slicing — fits the dev laptop's 4GB VRAM) and feeds
the generated latents straight into its `latents=` argument for a
2-step smoke run. Produced a 512x512 image with no shape/dtype errors,
confirming the format decision end-to-end. (The safety checker flags
the output as NSFW and returns a black image — expected at 2 inference
steps with an empty prompt on near-random latents, not a real finding.)

Real bug hit along the way: running the verify script directly
(`.venv/bin/python scripts/verify_noise.py`) failed with
`ModuleNotFoundError: No module named 'oneiros'` — the script's own
directory lands on `sys.path`, not the repo root, so the sibling
`oneiros` package wasn't importable. Fixed by adding `pyproject.toml`
and installing the project itself in editable mode (`uv pip install
-e .`) rather than patching `sys.path` by hand — this is also what
makes the package resolve correctly for the editor/type-checker.

Environment: `uv venv` + `uv pip install -e .`; torch/diffusers/
transformers/accelerate/safetensors/pillow declared in
`pyproject.toml`. `.venv/` is gitignored; the Hugging Face model-weight
cache lives outside the repo and isn't (and shouldn't be) committed.
