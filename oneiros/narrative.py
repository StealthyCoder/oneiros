import base64
from io import BytesIO

import anthropic
from dotenv import load_dotenv
from PIL.Image import Image

# Kept on this legacy tier deliberately: temperature was removed entirely
# from every current-generation Claude model (Opus 4.6+, Sonnet 5, Fable 5),
# and this stage needs the literal sampling knob, not just a prompted
# approximation of it.
MODEL_ID = "claude-sonnet-4-5"
TEMPERATURE = 1.0

LOGIC_OFFLINE_PROMPT = (
    "You are the part of a dreaming brain that turns raw visual noise into "
    "a narrative, with the logical, self-critical part of the brain offline. "
    "Describe what you see as a dream unfolding, not a photograph being "
    "analyzed. Favor free association, sensory impressions, and emotional "
    "coloring over explanation. Do not rationalize, caveat, or impose "
    "narrative coherence the image doesn't actually have. Do not describe "
    "this as an image, a picture, or a generated artifact - describe it as "
    "the dream itself. Contradictions and impossible details are fine; do "
    "not resolve them."
)


def load_client() -> anthropic.Anthropic:
    """Loads the Anthropic client once - callers running a loop should hold
    onto the result and reuse it, not construct one per cycle.

    Reads ANTHROPIC_API_KEY from a local .env file (gitignored - see
    .env.example) via load_dotenv(), falling back to whatever's already in
    the environment. Never hardcode a key here.
    """
    load_dotenv()
    return anthropic.Anthropic()


def _image_to_base64_png(image: Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")


def narrate_imagery(
    client: anthropic.Anthropic,
    image: Image,
    model: str = MODEL_ID,
    temperature: float = TEMPERATURE,
    max_tokens: int = 1024,
) -> str:
    """Hippocampus/amygdala equivalent: narrates imagery into a dream fragment.

    High temperature and the logic-suppression system prompt are the two
    deliberate, non-default settings this stage exists to apply - see
    docs/todos/completed/narrative-interpretation.md.
    """
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=LOGIC_OFFLINE_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": _image_to_base64_png(image),
                        },
                    },
                    {"type": "text", "text": "What is happening in this dream?"},
                ],
            }
        ],
    )
    return next(block.text for block in response.content if block.type == "text")
