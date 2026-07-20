import torch
from diffusers import StableDiffusionPipeline

from oneiros.noise import generate_latents

MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"


def main() -> None:
    latents, seed = generate_latents(image_height=512, image_width=512)
    print(f"generated latents: shape={tuple(latents.shape)} dtype={latents.dtype} seed={seed}")

    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
    pipe.to("cuda")
    pipe.enable_attention_slicing()  # keeps this under the 3050 Ti's 4GB VRAM

    result = pipe(
        prompt="",
        latents=latents.to(device="cuda", dtype=torch.float16),
        num_inference_steps=2,
        guidance_scale=1.0,  # skips the unconditional branch, halves memory for this smoke test
    )
    print(f"pipeline accepted the generated latents, produced image size={result.images[0].size}")


if __name__ == "__main__":
    main()
