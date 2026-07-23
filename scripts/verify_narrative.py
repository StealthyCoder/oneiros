from oneiros.imagery import generate_image, load_pipeline
from oneiros.narrative import load_client, narrate_imagery
from oneiros.noise import generate_latents


def main() -> None:
    print("🌙 brainstem firing - generating raw noise...")
    latents, seed = generate_latents(image_height=512, image_width=512)
    print(f"latents: shape={tuple(latents.shape)} dtype={latents.dtype} seed={seed}")

    print("waking the visual cortex (loading Stable Diffusion onto the GPU)...")
    pipe = load_pipeline()

    print("constructing an image from noise...")
    image = generate_image(pipe, latents)

    print("logic centre going offline - narrating the dream...")
    client = load_client()
    narration = narrate_imagery(client, image)

    print(f"\n--- dream narrative (cost: ${narration.cost_usd:.4f}) ---")
    print(narration.text)


if __name__ == "__main__":
    main()
