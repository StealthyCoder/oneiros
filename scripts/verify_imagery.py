from pathlib import Path

from oneiros.imagery import generate_image, load_pipeline
from oneiros.noise import generate_latents

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "output" / "verify_imagery.png"


def main() -> None:
    print("🌙 brainstem firing - generating raw noise...")
    latents, seed = generate_latents(image_height=512, image_width=512)
    print(f"latents: shape={tuple(latents.shape)} dtype={latents.dtype} seed={seed}")

    print("waking the visual cortex (loading Stable Diffusion onto the GPU)...")
    pipe = load_pipeline()

    print("constructing an image from noise...")
    image = generate_image(pipe, latents)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    image.save(OUTPUT_PATH)
    print(f"✨ noise became imagery - saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
