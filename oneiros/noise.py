import random

import torch


def generate_latents(
    seed: int | None = None,
    batch_size: int = 1,
    image_height: int = 512,
    image_width: int = 512,
    channels: int = 4,
) -> tuple[torch.Tensor, int]:
    """Brainstem equivalent: raw noise for the image-generation stage to build on.

    Shape follows Stable Diffusion's UNet latent convention (4 channels,
    8x spatial downsample from the target image size), not a generic
    noise tensor - this is meant to be fed straight into a diffusion
    pipeline's `latents=` argument.
    """
    if seed is None:
        seed = random.randint(0, 2**32 - 1)

    generator = torch.Generator().manual_seed(seed)
    latents = torch.randn(
        (batch_size, channels, image_height // 8, image_width // 8),
        generator=generator,
    )
    return latents, seed
