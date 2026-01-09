# The Nexus

**AI-Powered Immersive RPG Storytelling**

A genre-flexible roleplaying framework that turns Claude or Gemini into an adaptive Game Master. Create characters, explore living worlds, and experience stories where every choice has consequences.

---

## Quick Start (Web App)

1. Open [**your-username.github.io/nexus**](https://your-username.github.io/nexus) on any device
2. Tap ⚙️ **Settings** and enter your API key
3. Send "begin" to start a new adventure

**Get API Keys:**
- [Anthropic Console](https://console.anthropic.com/) (Claude)
- [Google AI Studio](https://aistudio.google.com/apikey) (Gemini)

---

## Features

### 🎭 The Nexus Framework
- **5 World States**: Dystopian, Utopian, Frontier, Balanced, Chaos
- **Any Genre**: Cyberpunk, Fantasy, Sci-Fi, Modern, Post-Apocalyptic, or custom
- **27-Point Skill System**: Physical, Mental, Social, Survival, Specialist
- **Living World**: NPCs pursue goals off-screen, consequences ripple forward
- **No Plot Armor**: Real stakes, real consequences

### 🔥 Mature Content Support
- **Intimacy Spectrum**: 4 tiers from emotional to explicit (player-controlled)
- **World-Appropriate Tone**: Intimate scenes match the world state
- **Safety Tools**: Veil, Pause, and Rewind commands
- **Trauma Protocol**: Thoughtful handling of difficult content

### 💾 Session Management
- **Save/Load**: Export sessions as JSON files
- **Cross-Device**: Play on desktop, continue on mobile
- **Character Sheets**: Persistent continuity tracking
- **Browser Storage**: Quick-save to localStorage

### 🤖 Multi-Provider Support
- **Anthropic**: Claude Opus 4.5, Sonnet 4.5, Haiku 4.5
- **Google AI**: Gemini 3 Pro/Flash, 2.5 Pro/Flash, 2.0 Flash

---

## Desktop App

For the full experience with Archive & Trim, character sheet management, and local file handling, use the Python desktop app:

### Requirements
```bash
pip install customtkinter anthropic google-generativeai --break-system-packages
```

### Setup
1. Download `storyteller.py` and `framework.txt`
2. Place them in the same folder
3. Set your API key:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   # and/or
   export GOOGLE_API_KEY="AIza..."
   ```
4. Run:
   ```bash
   python storyteller.py
   ```

### Desktop Features
- **Archive & Trim**: Compress long sessions while preserving continuity
- **Character Sheet**: Persistent tracking across sessions
- **Framework Editor**: Customize the RPG framework
- **Keyboard Shortcuts**: Ctrl+Enter to send, Ctrl+S to save, Ctrl+O to load

---

## File Structure

```
nexus/
├── index.html          # Web app (mobile-friendly)
├── storyteller.py      # Desktop app (Python)
├── framework.txt       # RPG framework (customizable)
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
3. **Mobile**: Download session when done
4. **Desktop**: Load session → continue with full features

---

## Commands

During play, you can use these commands:

| Command | Effect |
|---------|--------|
| `begin` | Start a new adventure |
| `Veil` | Pull back from explicit detail |
| `Nexus, Pause` | Halt the current scene |
| `Rewind` | Reset to before a failure |
| `Nexus, show naming convention` | See current naming rules |

---

## The Nexus Promise

> *I will maintain this framework to create an immersive, consequential narrative where your choices matter, the world lives and breathes, and every action shapes an ever-expanding story.*
>
> *There is no final page in this living story. Welcome to your endless adventure.*
>
> ***The Nexus awaits.***

---

## License

MIT License - Use freely, modify as needed.

---

## Credits

Built for immersive AI storytelling. Framework designed for use with Claude (Anthropic) and Gemini (Google) language models.
