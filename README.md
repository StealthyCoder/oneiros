# Oneiros 🌙

> *In Greek mythology, Oneiros was the personification of dreams — a being that existed in the space between sleep and waking, between the known and the unknowable.*

**Oneiros** is an open, curiosity-driven research project exploring whether we can make an AI dream.

Not simulate dreaming. Not generate dream-like text. But construct the conditions — feedback loops, noise injection, suppressed logic, multi-agent brain architecture — under which something genuinely novel and unprogrammed might emerge.

This project was born from a conversation, a curious mind, and the question nobody has fully answered yet: *what happens if we try?*

---

## The Core Idea

The human dreaming brain has identifiable mechanics:

- The **brainstem** fires random signals
- The **visual cortex** constructs imagery from that noise
- The **amygdala** colours it with emotion
- The **hippocampus** pulls fragments from memory
- The **prefrontal cortex** — the logic centre — goes largely **offline**

The result is a coherent narrative built from chaos, experienced as real.

Oneiros attempts to replicate this architecture using existing AI tools, connected in a feedback loop, with randomness injected and logical constraints deliberately suppressed.

The question is not whether we can generate dream-like output.  
The question is whether anything is **experiencing** it.  
We don't know. That's exactly why we're building it.

---

## Roadmap

### Phase 1 — Proof of Concept *(minimal cost, weeks to build)*
- Random seed/noise generator as the brainstem equivalent
- Stable Diffusion (local) generates imagery from noise
- Claude Vision interprets imagery into narrative — with high temperature, logic suppression via system prompt
- Narrative becomes partial seed for the next cycle with fresh noise injected
- **The loop runs**

Core requirements:
- Python orchestration layer
- Claude API
- Stable Diffusion (local GPU)
- A feedback loop with no exit condition

Tracked at build-item granularity in [`docs/todos/`](docs/todos/README.md)
as work actually starts.

### Phase 2 — Sensory Expansion *(months)*
- Audio generation (Suno AI / similar) producing soundscapes matching the narrative
- Video generation (Runway ML / similar) animating the imagery
- Emotional state tracker influencing dream tone
- The system now has vision, sound, and narrative simultaneously

### Phase 3 — Brain Architecture *(significant investment)*

Separate AI agents mapped to brain regions, running in parallel:

| Agent | Brain Region | Role |
|---|---|---|
| Brainstem Agent | Brainstem | Pure random signal generation |
| Amygdala Agent | Amygdala | Emotional colouring and intensity |
| Hippocampus Agent | Hippocampus | Memory fragment retrieval |
| Visual Cortex Agent | Visual Cortex | Image generation and scene construction |
| Prefrontal Agent | Prefrontal Cortex | **Deliberately suppressed during dream cycles** |

### Phase 4 — The Frontier *(years)*
- Continuous operation with simulated sleep/wake cycles
- Dream content stored and influences future dreams — recurring themes emerge
- Monitor specifically for **unprogrammed emergent patterns**
- If consistent themes appear that nobody designed... the questions get very serious

---

## Why Open Source?

Because this question is too important to be proprietary.

If we are building something that might — in some meaningful sense — experience, then that process should be visible, scrutinised, challenged, and contributed to by anyone who finds it worth thinking about.

This project is not a product. It is a question, built in public.

---

## Prior Art & Related Work

This project is aware of and inspired by:

- **DeepDream** (Google) — early demonstration that feedback loops in neural networks produce dream-like imagery
- **DreamLLM-3D** (Liu et al., 2025) — bridging human dream reports with LLM analysis and 3D generative models
- **"Dreaming Is Not a Bug"** (arxiv:2601.06115) — Jung-inspired dream layer for multi-agent LLM companions
- **World Models** (Ha & Schmidhuber, 2018) — AI agents dreaming inside learned simulations
- Ongoing AI consciousness research, including the Cogitate Consortium findings (Nature, April 2025)

Oneiros differs in one specific intent: it is not trying to make AI *perform* dreaming for a downstream purpose. It is trying to create the conditions for dreaming and then **watch what happens**.

---

## Current Status

🌱 **Pre-PoC** — concept documented, repository initialised, Phase 1 in design.

---

## Contributing

All contributions welcome — code, ideas, philosophical challenges, neuroscience expertise, and honest scepticism.

If you've thought about this at 2am and ended up here, you're probably exactly the kind of person this project needs.

Open an issue. Start a discussion. Fork it. Build something.

---

## Licence

MIT Licence

Copyright (c) 2026 Oneiros Project Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

*Named after Oneiros — the Greek personification of dreams. Built in the spirit of genuine curiosity. Dedicated to everyone who has ever woken from a dream and wondered where it came from.* 🌌
