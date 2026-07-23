import argparse
from pathlib import Path

from oneiros.imagery import load_pipeline
from oneiros.loop import DEFAULT_BLEND_WEIGHT, run_loop
from oneiros.narrative import load_client

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output" / "dreams"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Runs the Oneiros feedback loop: noise -> imagery -> narrative, fed "
            "back as the next cycle's seed. No exit condition by default - stop "
            "with Ctrl+C, or opt into --max-cycles / --max-spend."
        )
    )
    parser.add_argument(
        "--max-cycles",
        type=int,
        default=None,
        help="Stop after this many cycles (default: unbounded).",
    )
    parser.add_argument(
        "--max-spend",
        type=float,
        default=None,
        metavar="USD",
        help="Stop once cumulative Claude API spend reaches this many dollars "
        "(default: unbounded).",
    )
    parser.add_argument(
        "--blend-weight",
        type=float,
        default=DEFAULT_BLEND_WEIGHT,
        help="Share of each cycle's next latents drawn from the narrative-derived "
        f"seed vs. fresh noise, 0-1 (default: {DEFAULT_BLEND_WEIGHT}).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("waking the visual cortex (loading Stable Diffusion onto the GPU)...")
    pipe = load_pipeline()
    client = load_client()

    print("🌙 the loop begins.")
    run_loop(
        pipe,
        client,
        max_cycles=args.max_cycles,
        max_spend_usd=args.max_spend,
        blend_weight=args.blend_weight,
        output_dir=OUTPUT_DIR,
    )


if __name__ == "__main__":
    main()
