import torch
from diffusers import StableDiffusionPipeline
from PIL.Image import Image

MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"


def load_pipeline(
    model_id: str = MODEL_ID, device: str = "cuda"
) -> StableDiffusionPipeline:
    """Loads the Stable Diffusion pipeline once - callers running a loop
    should hold onto the result and reuse it, not call this per cycle.
    """
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.to(device)
    pipe.enable_attention_slicing()  # keeps this under a 4GB-VRAM card
    return pipe


def generate_image(
    pipe: StableDiffusionPipeline,
    latents: torch.Tensor,
    num_inference_steps: int = 25,
    guidance_scale: float = 1.0,
) -> Image:
    """Visual cortex equivalent: constructs an image from brainstem noise.

    No text prompt - imagery here is meant to come from the noise alone,
    not text guidance. guidance_scale=1.0 skips classifier-free
    guidance's unconditional branch, which would otherwise double the
    per-step cost for no benefit against an empty prompt.
    """
    result = pipe(
        prompt="",
        latents=latents.to(device=pipe.device, dtype=pipe.unet.dtype),
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
    )
    return result.images[0]
