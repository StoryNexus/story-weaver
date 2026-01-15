# The Nexus

**AI-Powered Immersive RPG Storytelling**

A genre-flexible roleplaying framework that turns Claude or Gemini into an adaptive Game Master. Create characters, explore living worlds, and experience stories where every choice has consequences.

---

## Quick Start (Web App)

1. Open your hosted GitHub Pages URL on any device
2. Tap ⚙️ **Settings** and enter your API key
3. Send "begin" to start a new adventure

**Get API Keys:**
- [Anthropic Console](https://console.anthropic.com/) (Claude)
- [Google AI Studio](https://aistudio.google.com/apikey) (Gemini)

---

## What's New in v2.0

### 🌍 Dynamic World State Engine
The world is no longer static. States shift, blend, and rupture based on your actions and the passage of time.

**13 World States:**
| State | Concept |
|-------|---------|
| DYSTOPIAN | Oppression, scarcity, hope through resistance |
| UTOPIAN | False perfection, hidden costs |
| FRONTIER | Lawless expansion, community building |
| BALANCED | Modern realism, contemporary problems |
| CHAOS | No authority, desperate opportunity |
| DECADENT | Late-stage empire, beautiful exhaustion |
| GILDED | Surface prosperity masking rot |
| LIMINAL | Between states, old rules dying |
| OCCUPIED | External control, resistance vs collaboration |
| ENCLAVE | Fortress mentality, community as salvation/suffocation |
| NOIR | Moral ambiguity lens, everyone has an angle |
| DYING | The end is known, melancholy beauty |
| MYTHIC | Gods are real, prophecy matters |

**State Dynamics:**
- **Spatial Variation** - Different locations operate under different states
- **State Blending** - Hybrids like GILDED/NOIR or DYSTOPIAN/ENCLAVE
- **Mid-Scene Ruptures** - States can shift during scenes
- **Scar States** - Past states leave permanent marks
- **NPC Allegiance** - Characters defend their native states

### 🎭 PC Personal State System
Your character carries internal weather independent of the world:

SIEGE | DRIFT | HUNGER | FRACTURE | BECOMING | MASKS | SANCTUARY | HAUNT | FERAL | GRACE

Personal states create friction or resonance with world states, and can bleed into each other over time.

### 💋 Multi-Axis Intimacy System
Intimacy is no longer a simple 1-4 tier. Set multiple independent parameters:

| Axis | Options |
|------|---------|
| **Explicitness** | Veiled → Sensual → Explicit → Graphic |
| **Tone** | Romantic, Passionate, Playful, Desperate, Transactional, Aggressive, Worshipful, Melancholic, Primal |
| **Pacing** | Flash, Standard, Slow Burn, Marathon, Montage |
| **Focus** | Sensory, Emotional, Psychological, Mechanical, Relational, Internal Monologue |
| **Realism** | Fantasy → Romantic Realism → Authentic → Gritty → Clinical |
| **Stakes** | Casual, Exploratory, Milestone, Defining, Forbidden, Valedictory |
| **Power Dynamic** | Mutual, Guided, D/s, Service, Switching, Adversarial, Surrender |

**Plus:** Kink modules (toggle independently), quick presets, world-intimacy interplay.

---

## Core Features

### 🎭 The Nexus Framework
- **27-Point Skill System**: Physical, Mental, Social, Survival, Specialist
- **Living World**: NPCs pursue goals off-screen, consequences ripple forward
- **No Plot Armor**: Real stakes, real consequences
- **Arc Resolution**: Stories end but the world continues

### 🔥 Mature Content Support
- **Multi-Axis Intimacy**: Fine-grained control over every aspect
- **World-Appropriate Tone**: Scenes match world state context
- **Safety Tools**: Veil, Pause, and Rewind commands
- **Trauma Protocol**: Thoughtful handling of difficult content

### 💾 Session Management
- **Save/Load**: Export sessions as JSON files
- **Archive & Trim**: Compress long sessions while preserving continuity
- **Cross-Device**: Play on desktop, continue on mobile
- **Character Sheets**: Persistent continuity tracking

### 🤖 Multi-Provider Support
- **Anthropic**: Claude Opus 4.5, Sonnet 4.5, Haiku 4.5
- **Google AI**: Gemini 3 Pro/Flash, 2.5 Pro/Flash, 2.0 Flash

---

## Desktop App

For the full experience with local file handling, use the Python desktop app.

### Requirements
```bash
pip install customtkinter anthropic google-generativeai --break-system-packages
```

### Setup
1. Download `storyteller.py` and `framework_v2.txt`
2. Rename `framework_v2.txt` to `framework.txt`
3. Place both in the same folder
4. Set your API key:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   # and/or
   export GOOGLE_API_KEY="AIza..."
   ```
5. Run:
   ```bash
   python storyteller.py
   ```

### Desktop Features
- **Archive & Trim**: Compress sessions while preserving continuity
- **Character Sheet**: Persistent tracking across sessions
- **Framework Editor**: Customize the RPG framework
- **Keyboard Shortcuts**: Ctrl+Enter send, Ctrl+S save, Ctrl+O load

---

## File Structure

```
nexus/
├── index.html          # Web app (mobile-friendly)
├── storyteller.py      # Desktop app (Python)
├── framework_v2.txt    # RPG framework v2.0 (rename to framework.txt)
├── README.md           # This file
└── stories/            # Saved sessions (auto-created)
```

---

## Cross-Device Workflow

```
┌─────────────────┐     iCloud/AirDrop      ┌─────────────────┐
│  Desktop App    │ ──────────────────────► │   Mobile Web    │
│  storyteller.py │                         │   index.html    │
│                 │ ◄────────────────────── │                 │
└─────────────────┘     Download JSON       └─────────────────┘
```

1. **Desktop**: Save session → export to cloud storage
2. **Mobile**: Open web app → load session file → play anywhere
3. **Mobile**: Archive & Trim when session gets long
4. **Mobile**: Download session when done
5. **Desktop**: Load session → continue with full features

---

## Commands

During play, you can use these commands:

| Command | Effect |
|---------|--------|
| `begin` | Start a new adventure |
| `Veil` or `Veil This` | Pull back from explicit detail |
| `Nexus, Pause` | Halt the current scene |
| `Rewind` | Reset to before a failure |
| `Read the room` | Get current state analysis |
| `What would shift this?` | Query destabilization triggers |
| `Nexus, show naming convention` | See current naming rules |

### Intimacy Quick-Set
At intimate scene thresholds, use shorthand:
- `"Fade to black"` - Veiled, romantic, no explicit content
- `"Explicit. Tender. Slow."` - Set multiple axes at once
- `"Graphic, primal, flash"` - Quick and intense

---

## World State Tools

### Reading States
Ask the Nexus:
- *"What's the state here?"* - Get location analysis
- *"What would push this toward CHAOS?"* - Query instability
- *"What's stabilizing this?"* - Understand what's holding

### State Notation
States can blend: `GILDED/NOIR` means corrupt prosperity with noir undertones.

### Personal State
Your character's internal weather: Tell the Nexus or let it track organically.
- *"Silas is in FRACTURE right now"*
- *"She's been in SIEGE since the attack"*

---

## The Nexus Promise

> *I will maintain this framework to create an immersive, consequential narrative where your choices matter, the world lives and breathes, and every action shapes an ever-expanding story.*
>
> *I will track the weather of your world—its states and shifts, its pressures and ruptures. I will know where you are inside yourself, and where that rubs against the world outside.*
>
> *There is no final page in this living story. Welcome to your endless adventure.*
>
> ***The Nexus awaits.***

---

## Version History

**v2.0** - Dynamic World States & Multi-Axis Intimacy
- Added 8 new world states (13 total)
- Spatial state variation (different locations = different states)
- State blending, shifting, and rupture mechanics
- PC Personal State engine (10 internal states)
- State friction, resonance, bleed, and denial systems
- Multi-axis intimacy system (7 axes + kink modules)
- World-intimacy interplay protocols
- State shift pacing guidelines

**v1.0** - Initial Release
- Core framework with 5 world states
- 4-tier intimacy system
- Basic session management

---

## License

MIT License - Use freely, modify as needed.

---

## Credits

Built for immersive AI storytelling. Framework designed for use with Claude (Anthropic) and Gemini (Google) language models.
