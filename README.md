# The Nexus

**Version 2.1** - An immersive RPG engine powered by Claude — your AI Game Master for genre-flexible, consequence-driven adventures.

## Features

### Core System
- **Nexus Framework v2.1**: Complete RPG system with anti-railroading safeguards and prose calibration
- **13 World States**: Dystopian, Utopian, Frontier, Balanced, Chaos, Decadent, Occupied, Gilded, Liminal, Enclave, Noir, Dying, Mythic
- **Dynamic State Shifts**: World states can blend, shift, and rupture based on your actions
- **Player Agency Protection**: Multiple redundant safeguards prevent AI from narrating your character's actions

### New in 2.1
- **📚 Reference Documents**: Upload playbooks, rules, maps (supports .txt, .md, .pdf)
- **Prose Calibration Engine**: Fine-tune writing style with author references and density controls
- **Character Sheet Continuity**: Persistent tracking across sessions with Archive & Trim feature
- **Enhanced Anti-Railroading**: Explicit protections with concrete examples of violations

### Technical Features
- **Save/Load Sessions**: Pick up any campaign where you left off
- **Model Selection**: Claude Opus 4.6, Opus 4.5, Sonnet 4.5, Haiku 4.5
- **Multi-Provider Support**: Anthropic Claude and Google Gemini
- **Temperature Control**: Dial creativity up for wild sessions, down for consistency
- **Mobile Server**: Play on your phone while running locally on desktop
- **Dark UI**: Easy on the eyes for marathon sessions

## Quick Start

### 1. Install dependencies

```bash
pip install customtkinter anthropic PyPDF2 --break-system-packages

# Optional: for Google AI support
pip install google-generativeai --break-system-packages
```

### 2. Set your API key

```bash
# Linux/Mac: add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

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
4. Character creation with skill point distribution
5. Your adventure begins

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Send message |
| `Ctrl+S` | Save session |
| `Ctrl+O` | Load session |
| `Ctrl+N` | New session |

## Reference Documents

Upload reference materials that The Nexus can access during gameplay:

1. Click **📚 Reference Docs** button
2. Upload your files (.txt, .md, .pdf)
3. Documents are automatically included in every AI response
4. Perfect for:
   - Sports playbooks (flag football, etc.)
   - RPG rules and house rules
   - World lore and setting documents
   - Character backgrounds
   - Maps and location details

**PDF Support**: Automatically extracts text from PDFs using PyPDF2. For scanned PDFs, convert to text first.

## Character Sheet & Archive

The **Character Sheet** feature maintains continuity across long campaigns:

- **Character Sheet Editor**: Track character details, relationships, and story developments
- **Archive & Trim**: Compress long sessions while preserving key information
  1. Saves full archive to file
  2. Generates AI summary of important events
  3. Trims chat to last 10 messages
  4. Updates character sheet with summary

Perfect for maintaining context in 100+ message campaigns without hitting token limits.

## In-Game Commands

The Nexus framework includes built-in safety and control commands:

- **"Veil this"** — Pull back from explicit content
- **"Nexus, Pause"** — Halt the scene entirely
- **"Rewind"** — Reset to before a failed choice
- **"Nexus, show naming convention"** — See current cultural naming rules
- **"Nexus, adjust prose: [style]"** — Change writing style mid-session
- **"Read the room"** — Get current state analysis
- **"What would shift this?"** — Query world state destabilization triggers

## Session Format

Sessions are saved as JSON with full conversation history and metadata:

```json
{
  "version": "1.0",
  "created": "2025-01-15T14:30:00",
  "provider": "Anthropic",
  "model": "claude-sonnet-4-5-20250929",
  "temperature": 1.0,
  "messages": [...],
  "character_sheet": "...",
  "reference_documents": [...]
}
```

## Model Recommendations

| Model | Best For | Cost* |
|-------|----------|------|
| **Opus 4.6** | Most advanced, complex narratives, nuanced NPCs | ~$0.075/exchange |
| **Opus 4.5** | High quality, complex reasoning | ~$0.075/exchange |
| **Sonnet 4.5** | Daily play, excellent balance of quality and cost | ~$0.015/exchange |
| **Haiku 4.5** | Quick sessions, testing, budget-conscious | ~$0.002/exchange |

*Approximate costs based on typical exchange length (~500 tokens in, 800 tokens out)

## Temperature Guide

- **0.7-0.8**: More predictable, consistent characterization
- **1.0** (default): Balanced creativity
- **1.1-1.3**: Wilder, more surprising narrative choices
- **1.4-1.5**: Maximum chaos (use sparingly)

## Prose Calibration

New in v2.1: Fine-tune the writing style during character creation or mid-session:

**Style Anchoring**:
- "Write in the style of Cormac McCarthy"
- "Noir detective style"
- "Conversational, like Firefly"

**Density Control** (automatic based on scene type):
- **Lean**: Action/combat (short, punchy)
- **Medium**: Investigation/dialogue
- **Dense**: Emotional/intimate scenes
- **Minimal**: Transitions

**World State Defaults**:
Each world state has a default prose style. For example:
- DYSTOPIAN → McCarthy's sparse brutality
- NOIR → Chandler's hard-boiled cynicism
- MYTHIC → Homeric formality

## Anti-Railroading Safeguards

The Nexus respects player agency with multiple protections:

- ✅ Stops after describing situations (never assumes PC actions)
- ✅ Never narrates "you feel/think/decide" without player input
- ✅ Explicit checkpoints in combat and social scenes
- ✅ Concrete examples of violations in framework
- ✅ Quick Reference reminders in every response

If the AI ever railroads, you can say: **"Stop. You're narrating my character's actions. Let me decide."**

## Mobile Server

Play on your phone while running the desktop app:

1. Click **📱 Mobile Server** in the app
2. Note the URL (e.g., `http://192.168.1.100:8000`)
3. Open that URL on your phone (same WiFi network)
4. Full-featured mobile interface
5. Click **Stop Server** when done

## Tips

### For Long Campaigns
- Use **Archive & Trim** every 30-50 messages to maintain performance
- Character sheet automatically preserves continuity
- Reference documents persist across Archive & Trim

### For Sports/Tactical Stories
- Upload playbooks or rule PDFs via Reference Docs
- The Nexus will reference specific plays/formations
- Perfect for flag football, basketball plays, military tactics

### For Intimate Content
- Use Intimacy Check-in system (Tiers 1-4)
- Set boundaries before scenes escalate
- "Veil this" command available anytime

### Framework Customization
- Click **◈ Edit Framework** to modify rules
- Add house rules, custom mechanics
- Adjust anti-railroading sensitivity

## Web Version

The Nexus is also available as a web app (GitHub Pages):
- Same features as desktop
- Works on mobile browsers
- No installation required
- Saves to JSON for cross-device sync

See `index.html` in the repository.

## File Structure

```
nexus/
├── storyteller.py       # Desktop application
├── framework.txt        # Nexus Framework v2.1
├── character_sheet.txt  # Persistent character data
├── index.html           # Web version
├── stories/             # Saved session files
└── README.md
```

## Troubleshooting

**"Model error: claude-opus-4..."**
- The correct model string is: `claude-opus-4-6` (not 4-20250514 or other variants)

**PDF upload fails**
- Install PyPDF2: `pip install PyPDF2 --break-system-packages`
- For scanned PDFs, convert to text first

**Download hangs in web version**
- Hard refresh browser (Ctrl+Shift+R)
- Check browser console (F12) for errors

**Archive & Trim fails**
- Check API key is valid
- Verify you're not hitting rate limits
- Error message will show specific API error

## Version History

**v2.1** (Current)
- Added Reference Documents with PDF support
- Prose Calibration Engine
- Enhanced anti-railroading safeguards
- Claude Opus 4.6 support
- Improved download/save error handling

**v2.0**
- Dynamic World States (13 states)
- Personal State Engine
- Multi-Axis Intimacy System
- Archive & Trim feature

**v1.0**
- Initial release
- Basic framework
- Save/load functionality

## License

MIT License - Use freely, modify as needed.

## Credits

Built for immersive AI storytelling. Framework designed for use with Claude (Anthropic) and Gemini (Google) language models.
