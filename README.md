# The Nexus

**Version 3.1** — Master Engine Edition. An immersive RPG engine powered by AI — your Game Master for genre-flexible, consequence-driven adventures across Claude, ChatGPT, and Gemini.

## What's New in 3.1

### Dialogue Overhaul
- **Advance the Ball Directive**: NPCs must escalate, pivot, concede, or misdirect — never re-litigate
- **The Silent Turn**: NPCs with nothing new to add use physical beats instead of filler dialogue
- **Scene Disruption Protocol**: Mundane intrusions break conversational loops organically

### Combat & Action Rework
- **Threat Vector Pause**: Incoming attacks described and STOPPED — player decides response
- **Combat Environment Mandate**: 1-2 tactical environmental elements per fight, battlefield degrades with missed strikes
- **Anatomical Consequence**: Injuries degrade specific capabilities (no abstract HP)
- **Complication Engine**: Narrow success/failure margins always produce tactical trade-offs

### NPC Autonomy Expansion
- **Agenda Clocks**: Significant NPCs pursue tracked off-screen goals that advance during time skips
- **Missed Connection**: PC encounters aftermath of NPC actions (resources already taken, safehouses already compromised)
- **Unprompted Intercept**: NPCs interrupt when their clock completes or tension axis tips

### Conditioned Response Upgrades
- **Threshold Carryover**: Physical friction of previous scene persists into new environments
- **Ghost Sensations**: 1-3 scene micro-flashbacks from mundane stimuli post-priming

### Arc & Pacing Improvements
- **The Season Premiere**: New arcs get hard cut cold opens, not smooth transitions
- **Arc Escalation Directive**: Dramatic questions must shift axes between arcs (physical → social → moral)
- **Resolution Rupture**: Arc endings set Pressure Gauge to Rupture/Collapsed — next arc begins in friction

### Intimacy & Trauma Refinements
- **The Invisible Ledger**: Bond/Trauma updates noted via system log, not immersion-breaking announcements
- **Cool-Down Mandate**: 1-3 scene buffer after Tier 3/4 intimacy or trauma events
- **Sensory Triggers (Scar Tissue)**: Registered sensory inputs per trauma, fed through Conditioned Response Engine
- **Intimacy Bleed**: Bond history surfaces as subtext during conflict with bonded NPCs

### Nomenclature Hardening
- **"Cheap Alien" Prohibition**: No gratuitous apostrophes, edgy starting consonants, or double vowels
- **Linguistic Blend Mandate**: Names blend two cultural anchors, not one
- **Occupational Drift**: Name length/formality reflects world state (Frontier shortens, Gilded expands)

### Prose Calibration Updates
- **Stylistic Primer**: Internal alignment step before every response prevents style drift
- **Lexical Bounty**: World State vocabulary profile actively incorporated (Anglo-Saxon for Dystopian, brand-adjacent for Gilded, etc.)

### World State Engine Expansion
- Every world state now defines **Information** (how truth works), **Currency** (what holds value), **Justice** (how disruption is punished), and **Mobility** (barriers to movement)

### New Commands
- **"Nexus, Export State"**: Outputs dense technical summary (PC, NPCs, world state, threads, cold open seed) for pasting into a fresh session

### OpenAI Integration
- Full ChatGPT API support across all three interfaces (desktop, web, mobile)
- GPT-5.2, GPT-5.2 Instant, GPT-5 Mini, GPT-4o, GPT-4o Mini

## What Was New in 3.0

### Origin Arc System
- **4 Character Tiers**: Origin, Journeyman, Veteran, Legend — each with distinct skill budgets, entry styles, and gameplay feel
- **Origin Arc**: A guided 3-8 scene prologue for new characters that builds who they are before the main story
- **Cold Open** preserved for experienced characters (Tier 3-4 mandatory, Tier 2 optional)
- **Tier-adjusted difficulty**: DCs, skill caps, and advancement rates scale to character experience
- **Legacy Complications**: Tier 4 (Legend) characters carry narrative weight — debts, enemies, promises

### Narrative Architecture Engine
- **Story Spine Tracking**: Every scene connects through status quo → disruption → choice → new status quo
- **Dramatic Question Engine**: Each arc has a core question shaping choices, NPC behavior, and resolution
- **Thematic Thread Registration**: Emergent themes woven into environment, dialogue, and choice framing
- **Scene Tension Curve**: Every scene must move — entry tension ≠ exit tension
- **Breath Protocol**: Mandated quiet beats after 2-3 high-tension scenes
- **Contrast Pulse**: Strategic prose style breaks every 5-7 responses for human-feeling narration

### NPC Arc Engine
- **Tension Axis**: NPCs have internal conflicts that shift based on PC actions
- **Progressive Revelation**: Secrets discovered through play, not exposition
- **Dialogue Fingerprinting**: NPCs identifiable by voice alone

### Enhanced Continuity (Archive & Trim v2)
- **Rolling Summary**: Character sheets consolidated into one coherent document (not stacked appendages)
- **Causal Chain**: Tracks *why* things are the way they are, not just what
- **Campaign Chronicle**: Append-only timeline persisting across all archives
- **Smart Trim**: Finds natural scene breaks near your requested trim point
- **Bridge Context**: Auto-generated "Previously..." message connecting archive to remaining conversation
- **Summary Quality Choice**: Quick (Haiku) or Deep (Sonnet) summary generation
- **Reference Doc Awareness**: Summary generation knows which game rules/playbooks are in play

## Features

### Core System
- **Nexus Framework v3.1**: Complete RPG system with tiered character creation, narrative architecture, combat anatomy, NPC agenda clocks, and prose calibration
- **13 World States**: Dystopian, Utopian, Frontier, Balanced, Chaos, Decadent, Occupied, Gilded, Liminal, Enclave, Noir, Dying, Mythic — each with Information, Currency, Justice, and Mobility profiles
- **Dynamic State Shifts**: World states blend, shift, and rupture based on your actions
- **Player Agency Protection**: Multiple redundant safeguards prevent AI from narrating your character's actions
- **Conditioned Response Engine**: NPCs react based on accumulated emotional/physical context, not just immediate stimulus

### Technical Features
- **📚 Reference Documents**: Upload playbooks, rules, maps (supports .txt, .md, .pdf)
- **Prose Calibration Engine**: Fine-tune writing style with author references and density controls
- **Character Sheet Continuity**: Persistent tracking with rolling summary consolidation
- **Save/Load Sessions**: Pick up any campaign where you left off
- **Model Selection**: Claude Opus 4.6, Opus 4.5, Sonnet 4.6, Sonnet 4.5, Haiku 4.5
- **Multi-Provider Support**: Anthropic Claude, Google Gemini (up to 3.1 Pro), and OpenAI (GPT-5.2, GPT-5 Mini, GPT-4o)
- **Temperature Control**: Dial creativity up for wild sessions, down for consistency
- **Mobile Server**: Play on your phone while running locally on desktop
- **Dark UI**: Easy on the eyes for marathon sessions

## Quick Start

### 1. Install dependencies

```bash
pip install customtkinter anthropic PyPDF2 --break-system-packages

# Optional: for Google AI support
pip install google-generativeai --break-system-packages

# Optional: for OpenAI support
pip install openai --break-system-packages
```

### 2. Set your API key

```bash
# Linux/Mac: add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Optional: for Google AI
export GOOGLE_API_KEY="your-google-key-here"

# Optional: for OpenAI
export OPENAI_API_KEY="sk-your-key-here"

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

Or just run the app — it'll prompt you for the key on first message.

### 3. Run

```bash
python storyteller.py
```

### 4. Begin

Type `Begin` to start a new session. The Nexus will guide you through:
1. World State selection (13 options with blending support)
2. Genre selection (Cyberpunk, Fantasy, Sci-Fi, etc.)
3. Optional prose style calibration
4. **Character Tier selection** (Origin, Journeyman, Veteran, Legend)
5. Character creation with tier-appropriate skill point distribution
6. **Origin Arc** (Tier 1-2) or **Cold Open** (Tier 2-4) — your story begins

## Character Tiers

| Tier | Name | Skill Budget | Skill Range | Entry Style | Example |
|------|------|-------------|-------------|-------------|---------|
| 1 | **Origin** | 15 points | -2 to +5 | Origin Arc (default) | Farm boy, raw recruit, untrained Force-sensitive |
| 2 | **Journeyman** | 27 points | -2 to +7 | Origin Arc or Cold Open | Padawan, seasoned merc, junior detective |
| 3 | **Veteran** | 36 points | -2 to +9 | Cold Open (mandatory) | Jedi Knight, master thief, spec-ops |
| 4 | **Legend** | 45 points | -2 to +9 | Cold Open + Legacy Complication | Jedi Master, Sith Lord, galactic crime boss |

### Tier-Adjusted Gameplay
- **Difficulty**: DCs scale with tier (Tier 1: forgiving 10-15, Tier 4: legendary 18-25)
- **Advancement**: Origin Arc characters level faster; Legends grow in depth, not numbers
- **Skill Caps**: Tier 1 caps at +5 during Origin, rising to +7 after. Tier 3-4 cap at +9.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Send message |
| `Ctrl+S` | Save session |
| `Ctrl+O` | Load session |
| `Ctrl+N` | New session |

## Archive & Trim (v2)

The enhanced Archive & Trim system maintains continuity across long campaigns:

### Rolling Summary
Instead of stacking session summaries, the system generates a **single consolidated character sheet** that merges new content with existing data. Outdated information is updated, not preserved.

### Smart Trim
Instead of cutting at an arbitrary message count, the system finds a **natural scene break** near your requested trim point — scene transitions, choice prompts, or time skips.

### Bridge Context
After trimming, a **"Previously..."** message is generated to connect the archived content to the remaining conversation.

### Summary Quality
Choose between:
- **Quick** (Haiku): Fast, cheaper — good for routine trims
- **Deep** (Sonnet): Better continuity preservation — recommended for complex campaigns

### Character Sheet Format
The consolidated sheet includes:
1. **Narrative Lens** — Voice, tension, pacing, thematic threads, dramatic questions
2. **Technical Continuity** — Hard facts, tier, skills, NPCs, inventory
3. **Sensory Snapshot** — Where the scene was cut, physical details
4. **Active Micro-Dynamics** — NPC internal states, tension axes, secrets, dialogue fingerprints
5. **Golden Moments** — Prose style anchors from the session
6. **Causal Chain** — How decisions led to current state
7. **Open Loops** — Immediate, short-term, and long-game threads
8. **Campaign Chronicle** — Append-only timeline of major events

## In-Game Commands

- **"Veil this"** — Pull back from explicit content
- **"Nexus, Pause"** — Halt the scene entirely
- **"Rewind"** — Reset to before a failed choice
- **"Nexus, Export State"** — Output dense technical summary for pasting into a new session
- **"Nexus, show naming convention"** — See current cultural naming rules
- **"Nexus, adjust prose: [style]"** — Change writing style mid-session
- **"Read the room"** — Get current state analysis
- **"What would shift this?"** — Query world state destabilization triggers

## Model Recommendations

### Anthropic (Claude)

| Model | Best For | Cost* |
|-------|----------|------|
| **Opus 4.6** | Most advanced, complex narratives, nuanced NPCs | ~$0.075/exchange |
| **Opus 4.5** | High quality, complex reasoning | ~$0.075/exchange |
| **Sonnet 4.6** | **Recommended default.** Near-Opus quality at Sonnet pricing | ~$0.015/exchange |
| **Sonnet 4.5** | Still solid, slightly cheaper on cached prompts | ~$0.015/exchange |
| **Haiku 4.5** | Quick sessions, testing, budget-conscious | ~$0.002/exchange |

### OpenAI (ChatGPT)

| Model | Best For | Cost* |
|-------|----------|------|
| **GPT-5.2** | Thinking/reasoning model, deep narrative, complex problem-solving | ~$0.013/exchange |
| **GPT-5.2 Instant** | **Recommended default.** Fast, capable everyday model | ~$0.013/exchange |
| **GPT-5 Mini** | Budget-friendly, quick sessions | ~$0.002/exchange |
| **GPT-4o** | Legacy multimodal, still solid | ~$0.009/exchange |
| **GPT-4o Mini** | Cheapest option for testing | ~$0.001/exchange |

### Google AI (Gemini)

| Model | Best For | Cost* |
|-------|----------|------|
| **Gemini 3.1 Pro** | Top-tier reasoning, long context | ~$0.010/exchange |
| **Gemini 3 Pro** | Strong all-around performance | ~$0.010/exchange |
| **Gemini 3 Flash** | Fast and cheap | ~$0.001/exchange |

*Approximate costs based on typical exchange length (~500 tokens in, 800 tokens out)

## Temperature Guide

- **0.3-0.5**: Tight, consistent, predictable — good for mechanical/rules-heavy sessions
- **0.7-0.8**: Reliable characterization with room to breathe
- **0.9** : Slightly more creative, occasional surprises
- **1.0** (default, max): Full creative range — best for narrative-heavy play

## Anti-Railroading Safeguards

The Nexus respects player agency with multiple protections:

- ✅ Stops after describing situations (never assumes PC actions)
- ✅ Never narrates "you feel/think/decide" without player input
- ✅ Explicit checkpoints in combat and social scenes
- ✅ Concrete examples of violations in framework

If the AI ever railroads: **"Stop. You're narrating my character's actions. Let me decide."**

## Mobile Server

1. Click **📱 Mobile Server** in the app
2. Note the URL (e.g., `http://192.168.1.100:8080`)
3. Open on your phone (same WiFi network)
4. Click **Stop Server** when done

## File Structure

```
nexus/
├── storyteller.py       # Desktop application
├── framework.txt        # Nexus Framework v3.1
├── character_sheet.txt  # Persistent character data (rolling summary)
├── index.html           # Web version
├── nexus.html           # Mobile-optimized web version
├── stories/             # Saved session files
└── README.md
```

## Version History

**v3.1** (Current) — Master Engine Edition
- OpenAI ChatGPT API integration (GPT-5.2, GPT-5 Mini, GPT-4o across all interfaces)
- Advance the Ball Directive + Silent Turn (dialogue anti-looping)
- Scene Disruption Protocol (organic loop-breaking)
- Threat Vector Pause (combat attacks require player response before resolution)
- Combat Environment Mandate (tactical terrain + degrading battlefields)
- Anatomical Consequence system (injuries degrade specific capabilities, no abstract HP)
- Complication Engine (narrow margins produce tactical trade-offs)
- NPC Agenda Clocks + Missed Connection + Unprompted Intercept
- Conditioned Response upgrades: Threshold Carryover + Ghost Sensations
- Season Premiere (hard cut arc transitions), Arc Escalation Directive, Resolution Rupture
- Invisible Ledger, Cool-Down Mandate, Sensory Triggers, Intimacy Bleed
- "Cheap Alien" Prohibition, Linguistic Blend Mandate, Occupational Drift
- Stylistic Primer + Lexical Bounty (prose calibration hardening)
- World State expansion: Information, Currency, Justice, Mobility profiles for all 13 states
- "Nexus, Export State" command for session migration

**v3.0** — Origin Arc Edition
- Added Claude Sonnet 4.6 support (new default model)
- Character Tier system (Origin, Journeyman, Veteran, Legend)
- Origin Arc guided prologue
- Narrative Architecture Engine (story spine, dramatic questions, thematic threads)
- NPC Arc Engine (tension axes, progressive revelation, dialogue fingerprinting)
- Scene Tension Curve, Breath Protocol, Contrast Pulse
- Rolling Summary continuity (consolidated character sheets)
- Causal Chain and Campaign Chronicle tracking
- Smart Trim with natural scene break detection
- Bridge Context generation
- Summary quality selection (Quick/Deep)
- Increased max tokens (12288)
- Character sheet preservation across new sessions
- Character Integrity Directive (anti-redemption-railroading)
- Dynamic Nomenclature with LLM ban lists
- Echo Chamber of Awe prohibition
- Conditioned Response Engine
- UI redesign (Wope-inspired gradient aesthetic)

**v2.1**
- Reference Documents with PDF support
- Prose Calibration Engine
- Enhanced anti-railroading safeguards
- Claude Opus 4.6 support

**v2.0**
- Dynamic World States (13 states)
- Personal State Engine
- Multi-Axis Intimacy System
- Archive & Trim feature

**v1.0**
- Initial release

## License

MIT License — Use freely, modify as needed.

## Credits

Built for immersive AI storytelling. Framework designed for use with Claude (Anthropic), ChatGPT (OpenAI), and Gemini (Google) language models.
