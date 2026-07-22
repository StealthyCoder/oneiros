# Claude Vision narrative interpretation

**Status: done (built 2026-07-22).** Part of Phase 1 (Proof of Concept) -
see the [root README](../../../README.md#phase-1--proof-of-concept-minimal-cost-weeks-to-build).

`oneiros/narrative.py`'s `narrate_imagery()` takes the imagery from
[image-generation.md](image-generation.md) and narrates it - the
hippocampus/amygdala equivalent that builds a coherent-feeling story out of
chaotic input while the logic centre stays offline. Two functions, split the
same way `imagery.py` splits `load_pipeline()`/`generate_image()`:

- `load_client()` - constructs the Anthropic client once, reading
  `ANTHROPIC_API_KEY` from a local `.env` via `load_dotenv()`. Cheap compared
  to loading Stable Diffusion's weights, but reused across cycles for the
  same reason: the upcoming [feedback-loop.md](../active/feedback-loop.md)
  stage runs with no exit condition.
- `narrate_imagery()` - sends the image plus the two deliberate settings to
  Claude and returns the narrative text.

Settled the questions this item was waiting on:

- **Model - and the temperature conflict.** The root README calls for "high
  temperature" as one of the two non-default settings this stage exists to
  apply. That parameter has been removed entirely from every current-generation
  Claude model (Opus 4.6 and later, Sonnet 5, Fable 5 all reject it outright)
  - only the older Sonnet 4.5 / Opus 4.5 tier still accepts it. Rather than
  drop the literal sampling knob in favour of a prompt instruction standing
  in for it, this stage deliberately stays on `claude-sonnet-4-5` at
  `temperature=1.0` so "high temperature" means what it says. Worth
  revisiting if that tier is ever retired.
- **Logic suppression** - a system prompt (`LOGIC_OFFLINE_PROMPT`) instructing
  against rationalising, hedging, or imposing coherence the image doesn't
  have, and against describing the input as "an image" rather than the dream
  itself.
- **Image encoding** - base64-encoded PNG, matching
  [image-generation.md](image-generation.md)'s decision to leave that
  encoding choice to this stage.

**Credentials.** The Claude API is billed separately from a claude.ai/Claude
Code subscription - a claude.ai Pro/Max plan covers claude.ai and Claude Code
usage, not standalone API calls from other code, and Claude Code's own
session credentials aren't meant to be extracted and reused outside it.
`load_client()` reads `ANTHROPIC_API_KEY` from a gitignored `.env`
(`.env.example` committed as the template) via `python-dotenv`, so a real key
never ends up hardcoded or committed.

Verified against the real API, not just shape-checked:
`scripts/verify_narrative.py` runs noise -> imagery -> narrative end to end
and prints the resulting text. First real run produced a coherent
dream-register narrative (a rusted cross, gold leaves, wood grain "like water
that forgot to move") with no rationalising or hedging language and no
"image"/"picture" framing - the system prompt held on the first try, no
retuning needed yet. No bugs hit along the way this time - the noise ->
imagery plumbing from the prior two stages fed straight in without changes.

Output narrative becomes the input to
[feedback-loop.md](../active/feedback-loop.md), which turns part of it into
the seed for the next cycle.
