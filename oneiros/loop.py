import hashlib
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import torch
from anthropic import Anthropic
from diffusers import StableDiffusionPipeline
from PIL.Image import Image

from oneiros.imagery import generate_image
from oneiros.narrative import narrate_imagery
from oneiros.noise import generate_latents

SEED_FRAGMENT_WORDS = 12
DEFAULT_BLEND_WEIGHT = 0.5


@dataclass
class Cycle:
    """One pass through the loop: the imagery and narrative it produced,
    what it cost, and the latents primed for the next pass.
    """

    image: Image
    narrative: str
    narrative_seed: int
    next_latents: torch.Tensor
    cost_usd: float


def _seed_from_narrative(narrative: str, word_count: int = SEED_FRAGMENT_WORDS) -> int:
    """Turns the tail of a narrative into a reproducible seed - what the
    dream was doing right as it faded, not the whole thing. `random.seed()`
    isn't reproducible across processes for str input the way this needs to
    be, so this hashes explicitly via hashlib instead.
    """
    fragment = " ".join(narrative.split()[-word_count:])
    digest = hashlib.sha256(fragment.encode("utf-8")).hexdigest()
    return int(digest, 16) % (2**32)


def _blend_latents(
    narrative_latents: torch.Tensor, fresh_latents: torch.Tensor, weight: float
) -> torch.Tensor:
    """Variance-preserving mix of narrative-derived and fresh noise: for two
    independent unit-normal tensors, w*a + sqrt(1-w^2)*b stays unit-normal,
    unlike a plain average, which would quietly shrink variance cycle over
    cycle and drift the diffusion pipeline toward flatter, less noisy input.
    """
    return weight * narrative_latents + math.sqrt(1 - weight**2) * fresh_latents


def run_cycle(
    pipe: StableDiffusionPipeline,
    client: Anthropic,
    latents: torch.Tensor,
    blend_weight: float = DEFAULT_BLEND_WEIGHT,
) -> Cycle:
    """One noise -> imagery -> narrative pass, ending with the latents for
    the next cycle: the narrative's tail blended with fresh noise.
    """
    image = generate_image(pipe, latents)
    narration = narrate_imagery(client, image)

    batch_size, channels, latent_h, latent_w = latents.shape
    narrative_seed = _seed_from_narrative(narration.text)
    narrative_latents, _ = generate_latents(
        seed=narrative_seed,
        batch_size=batch_size,
        image_height=latent_h * 8,
        image_width=latent_w * 8,
        channels=channels,
    )
    fresh_latents, _ = generate_latents(
        batch_size=batch_size,
        image_height=latent_h * 8,
        image_width=latent_w * 8,
        channels=channels,
    )
    next_latents = _blend_latents(narrative_latents, fresh_latents, blend_weight)

    return Cycle(
        image=image,
        narrative=narration.text,
        narrative_seed=narrative_seed,
        next_latents=next_latents,
        cost_usd=narration.cost_usd,
    )


def _save_cycle(run_dir: Path, cycle_number: int, cycle: Cycle) -> None:
    stem = f"{cycle_number:04d}"
    cycle.image.save(run_dir / f"{stem}.png")
    (run_dir / f"{stem}.txt").write_text(cycle.narrative)


def run_loop(
    pipe: StableDiffusionPipeline,
    client: Anthropic,
    max_cycles: int | None = None,
    max_spend_usd: float | None = None,
    blend_weight: float = DEFAULT_BLEND_WEIGHT,
    output_dir: Path = Path("output/dreams"),
) -> None:
    """Runs the dream cycle. The loop itself never decides to stop on its
    own account - no convergence check, no "this looks done." max_cycles
    and max_spend_usd are external operating caps a caller opts into, same
    category as Ctrl+C: they bound how long someone chooses to run this,
    not something the loop concludes about its own output. Leave both unset
    to run until interrupted, which stays the default.
    """
    run_dir = output_dir / datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    latents, seed = generate_latents()
    cycle_number = 0
    total_cost_usd = 0.0
    stop_reason = "interrupted (Ctrl+C)"

    try:
        while True:
            cycle_number += 1
            source = "fresh noise" if cycle_number == 1 else "last cycle's narrative"
            print(f"cycle {cycle_number} - dreaming from {source} (seed={seed})...")

            cycle = run_cycle(pipe, client, latents, blend_weight=blend_weight)
            total_cost_usd += cycle.cost_usd
            _save_cycle(run_dir, cycle_number, cycle)
            print(
                f"  narrated {len(cycle.narrative.split())} words - "
                f"cost=${cycle.cost_usd:.4f} total=${total_cost_usd:.4f}"
            )

            if max_cycles is not None and cycle_number >= max_cycles:
                stop_reason = f"reached max_cycles={max_cycles}"
                break
            if max_spend_usd is not None and total_cost_usd >= max_spend_usd:
                stop_reason = f"reached max_spend_usd=${max_spend_usd:.2f}"
                break

            latents, seed = cycle.next_latents, cycle.narrative_seed
    except KeyboardInterrupt:
        pass

    print(
        f"\n🌙 the loop stopped after {cycle_number} cycles "
        f"(${total_cost_usd:.4f} spent) - {stop_reason}. Artifacts in {run_dir}"
    )
