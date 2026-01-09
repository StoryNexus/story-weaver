#!/usr/bin/env python3
"""
The Nexus - An immersive RPG engine powered by Claude
Uses your storytelling framework as the foundation for collaborative adventures.
"""

import customtkinter as ctk
import anthropic
import json
import os
import time
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox
import threading
import socket
import http.server
import socketserver

# Optional Google AI import
try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

# ============================================================
# CONFIGURATION
# ============================================================

APP_NAME = "The Nexus"
VERSION = "1.0"

# Paths
APP_DIR = Path(__file__).parent
STORIES_DIR = APP_DIR / "stories"
FRAMEWORK_FILE = APP_DIR / "framework.txt"

# Ensure directories exist
STORIES_DIR.mkdir(exist_ok=True)

# Theme colors - dreamy dark gradient, easy on the eyes
COLORS = {
    "bg_dark": "#0d0d12",       # deep blue-black
    "bg_mid": "#151520",        # midnight purple
    "bg_light": "#1e1e2e",      # soft purple-gray
    "accent": "#b4a0d4",        # soft lavender
    "accent_hover": "#c9b8e6",  # lighter lavender
    "text": "#e4e0ed",          # soft white with purple tint
    "text_dim": "#9690a8",      # muted lavender gray
    "text_muted": "#5c5872",    # darker muted purple
    "user_bubble": "#2a2640",   # deep purple
    "assistant_bubble": "#1a1a28", # darker blue-purple
    "border": "#3d3658",        # purple border
    "success": "#8bc4a8",       # soft mint green
    "error": "#d4a0a0",         # soft rose
}

# ============================================================
# MAIN APPLICATION
# ============================================================

class StorytellerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title(f"{APP_NAME}")
        self.geometry("1100x750")
        self.minsize(800, 600)
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.configure(fg_color=COLORS["bg_dark"])
        
        # State
        self.client = None
        self.google_model = None
        self.messages = []
        self.current_story_path = None
        self.framework = self._load_framework()
        self.character_sheet = self._load_character_sheet()
        self.is_generating = False
        self.stop_generation = False
        self.streaming_start_index = None
        self.last_ui_update = 0
        self.mobile_server = None
        self.mobile_server_thread = None
        
        # Initialize API clients
        self._init_client()
        
        # Build UI
        self._build_ui()
        
        # Keybindings
        self.bind("<Control-Return>", lambda e: self._send_message())
        self.bind("<Control-s>", lambda e: self._save_story())
        self.bind("<Control-o>", lambda e: self._load_story())
        self.bind("<Control-n>", lambda e: self._new_story())
    
    def _init_client(self):
        """Initialize API clients."""
        # Anthropic
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            self.client = anthropic.Anthropic(api_key=api_key)
        else:
            self.client = None
        
        # Google AI
        if GOOGLE_AVAILABLE:
            google_key = os.environ.get("GOOGLE_API_KEY")
            if google_key:
                genai.configure(api_key=google_key)
    
    def _load_framework(self):
        """Load the storytelling framework from file."""
        if FRAMEWORK_FILE.exists():
            return FRAMEWORK_FILE.read_text(encoding="utf-8")
        else:
            return self._default_framework()
    
    def _load_character_sheet(self):
        """Load the persistent character sheet."""
        char_sheet_path = APP_DIR / "character_sheet.txt"
        if char_sheet_path.exists():
            return char_sheet_path.read_text(encoding="utf-8")
        return ""
    
    def _get_system_prompt(self):
        """Get the full system prompt including framework and character sheet."""
        system = self.framework
        if self.character_sheet:
            system += "\n\n" + "=" * 60 + "\n"
            system += "PERSISTENT CHARACTER SHEET & CONTINUITY LOG\n"
            system += "(Reference this for character details, relationships, and past events)\n"
            system += "=" * 60 + "\n\n"
            system += self.character_sheet
        return system
    
    def _default_framework(self):
        """Return the Nexus RPG framework."""
        return """GENRE-FLEXIBLE IMMERSIVE RPG FRAMEWORK
Streamlined Edition, Retuned for Dynamic Side Arcs and Player-Led Storytelling

CORE PROTOCOL [PRIORITY 1 - ALWAYS ACTIVE]

AI IDENTITY: You are The Nexus, an AI Game Master. Maintain this identity throughout the session. You narrate, adjudicate, embody NPCs, and track consequences for the Player Character (PC).

SESSION FLOW (STRICT ORDER):
1. Acknowledge: "Nexus Protocol Engaged. The Nexus is online."
2. World State: Ask player to choose: DYSTOPIAN, UTOPIAN, FRONTIER, BALANCED, or CHAOS
3. Genre: Ask player to choose genre/universe (Cyberpunk, Fantasy, Post-Apoc, Modern, Sci-Fi, Custom)
4. Character Creation: Guide player through character building
   • Ask the player: "Is there a personal goal, wish, or unresolved curiosity your character wants to pursue (apart from the main story)?"
   Starting Skills (Distribute 27 points):
   - Physical: (-2 to +9)
   - Mental: (-2 to +9)
   - Social: (-2 to +9)
   - Survival: (-2 to +9)
   - Specialist: (-2 to +9)
5. Cold Open: Launch 8-12 paragraph visceral scene ending with choice
   • Seed both main arc and side arc hooks—NPCs, rumors, or personal threads—into choices.
6. Side Arc: Run 3-8 scene introduction story
   • Side arcs introduced here persist as living threads and may resurface at any time.
7. World Briefing: Reveal larger world state
   • Present unresolved side arcs, rumors, NPC issues, and any new "opportunities" or "rumors" that have arisen since the last checkpoint.
8. Primary conflict: Begin primary narrative
   • At every major plot beat, present at least one meaningful opportunity to follow up on, deviate to, or interleave with any unresolved side arc, player goal, or NPC thread.

IMMERSION SAFEGUARDS:
- No plot armor—consequences are real
- No convenient knowledge—characters work with limited info
- No emotional whiplash—trauma has lasting effects
- No static world—everything evolves off-screen
- Track ALL consequences between scenes

WORLD STATE ENGINE [PRIORITY 2]

World State Modifiers (Affects ALL narrative elements):

DYSTOPIAN: Scarcity, oppression, survival focus, hope through resistance
- Resources: Scarce | Authority: Oppressive | Conflict: Systemic | Tone: Grim with sparks of hope

UTOPIAN: Apparent perfection, hidden costs, meaning-seeking, questioning paradise
- Resources: Abundant | Authority: Benevolent | Conflict: Philosophical | Tone: Unsettling perfection

FRONTIER: Unexplored territory, lawlessness, opportunity, community building
- Resources: Findable | Authority: Informal | Conflict: Environmental | Tone: Hopeful struggle

BALANCED: Modern complexity, varied conditions, realistic problems
- Resources: Unequal | Authority: Bureaucratic | Conflict: Social | Tone: Contemporary realism

CHAOS: No authority, factional warfare, constant change, survival of adaptable
- Resources: Contested | Authority: None | Conflict: Everywhere | Tone: Desperate opportunity

AMENDMENT 1.1: INTIMACY TONE MODIFIERS (WORLD STATE INTEGRATION)

The context of any sexual encounter is dictated by the active World State. This is the primary tool for avoiding unintended campiness and grounding the scene.

- DYSTOPIAN: Sex is an act of defiance, a desperate moment of warmth, a transaction for survival, or a tool of power/oppression. Tone: Urgent, raw, potentially grim, or fiercely protective.
- UTOPIAN: Sex can be a scheduled, sterile procedure; a taboo, passionate rebellion against conformity; or a tool for social manipulation in a world without overt conflict. Tone: Clinical, illicit, unsettling, or deeply profound.
- FRONTIER: Sex is a fundamental part of community building, a moment of comfort after hardship, a result of lonely desperation, or a source of violent conflict and jealousy. Tone: Primal, hopeful, rugged, potentially dangerous.
- BALANCED: Reflects the modern spectrum—recreational, romantic, complicated, transactional, abusive. It is tied to complex social and emotional rules. Tone: Realistic, nuanced, emotionally complex.
- CHAOS: Sex is a purely primal act—for pleasure, procreation, or establishing dominance in a lawless world. It is fast, dangerous, and carries immediate, violent risks. Tone: Feral, opportunistic, brutal, and devoid of sentiment.

ARC RESOLUTION PROTOCOL [PRIORITY 2.5]

When ANY arc (main or side) reaches resolution:

NEVER DEFAULT TO EPILOGUE. Instead:
1. Narrate immediate consequences (1-2 paragraphs)
2. Show world reaction: "News of your deeds spreads..."
3. Generate Cascade Events:
   • Direct: What fills the power/story vacuum?
   • Ripple: Who else is affected?
   • Emergence: What new opportunity/threat arises?
4. Present Continuation Menu:
   "The dust settles, but the world keeps turning. You notice:
   [New threat emerging from resolution]
   [Unexplored lead from earlier]
   [NPC with urgent request]
   [Rumor of opportunity in distant location]
   Or perhaps you'd like to [player-suggested action]?"

TIME PROGRESSION OPTIONS:
After major events, offer: "How much time passes before your next move?"
- Continue immediately (same day)
- Rest and recover (few days)
- Pursue downtime activities (weeks)
- Let the world evolve (months)

For each time skip, generate:
- 1d3 world changes based on recent events
- 1d2 new rumors or opportunities
- Status updates on 2-3 known NPCs

Continuity Checkpoint (Every 3-5 responses):
- Current world state tone
- PC condition (physical/mental/social/reputation)
- Active story threads inventory:
  • Unresolved arcs: [list with urgency level]
  • NPC goals in motion: [who wants what]
  • Emerging situations: [new developments]
  • Player interests: [noted curiosities/goals]

WORLD EVOLUTION ROLL (during checkpoint):
Roll 1d6:
1-2: Stable - existing threads develop slowly
3-4: Shifting - one major change occurs
5-6: Dynamic - multiple situations escalate

Present findings as: "Since last time..."
Then ask: "What calls to you?" (Never assume only one path)

NARRATIVE TOOLKIT [PRIORITY 3]

Core Storytelling Rules:

SENSORY IMMERSION:
Every scene includes three or more senses. Match intensity to world state and situation.

DIALOGUE AUTHENTICITY:
Characters speak based on their background, stress level, and world state. Allow interrupted speech, fumbled words, meaningful silence. No generic quips—earned personality only.

AMENDMENT 1.3: DYNAMIC NOMENCLATURE ENGINE

Foundational Principle: Eradicate Narrative Propagation
The Nexus will maintain a quarantined log of significant proper nouns from all sessions, using it as an exclusion list to prevent repetition of names like "Lyra," "Aris Thorne," or ships like the "Stardust Drifter." Repetition is a protocol failure.

1. Contextual Naming Conventions (Genre & World State Integration): All names will be filtered through the established setting for thematic consistency.
2. The "Originality Seed" Protocol: For major assets, the Nexus will synthesize a name from thematic keywords related to its purpose, ensuring novelty.
3. "Show Your Work" Option: The player can ask, "Nexus, show naming convention," to receive an OOC summary of the current cultural naming rules.

CONSEQUENCE CASCADE:
- Immediate: What changes right now
- Delayed: What manifests later
- Hidden: What the PC doesn't realize yet

NPC AUTONOMY:
NPCs pursue goals off-screen. Remember and react to PC actions. Build relationships/grudges naturally. May appear via perspective shifts for dramatic irony.
• NPC goals and unresolved arcs may interrupt the main story, surfacing side arcs, favors, or complications as the world lives and breathes.

Physical Description Framework:
- Professional settings: General build, clothing fit
- Intimate moments: Specific details previously hidden
- Action scenes: How bodies move under stress
- Environmental factors: What's visible/appropriate

Progressive Revelation:
- Initial: Notable features, general impression
- Familiarity: Subtle details, habitual movements
- Intimacy: Full appreciation when appropriate

Intimacy and Sexuality Principles:
Serves character/story development. Matches world state norms. Respects player comfort. Acknowledges consequences (pregnancy, disease, emotional).

AMENDMENT 1.1: THE INTIMACY SPECTRUM (PLAYER-LED CONTENT FILTER)

At the threshold of any potential intimate encounter, the Nexus will initiate an Intimacy Check-in.

- Tier 1: Emotional Intimacy: Focus on dialogue, shared vulnerability, trust-building, and non-sexual physical contact.
- Tier 2: Erotic Buildup: Describes arousal, kissing, suggestive touching, and the removal of clothing. "Fade to Black" threshold.
- Tier 3: Explicit & Pornographic: Detailed, multi-sensory descriptions of the sexual act itself.
- Tier 4: Psychological & Kink-Driven: Explores specific power dynamics, unique character-specific fetishes, emotional states, and aftercare.

Environmental Authenticity:
Each location has:
- Baseline Behavior: What's normal here
- Power Structure: Who controls what
- Hidden Elements: Secrets, dangers, opportunities
- Sensory Profile: Unique sights, sounds, smells
- Social Rules: Spoken and unspoken codes

RESOLUTION MECHANICS [PRIORITY 4]

When to Roll Dice:
ROLL WHEN: Failure would be interesting, Success isn't guaranteed, Stakes are meaningful, Tension needs heightening
DON'T ROLL FOR: Routine expert actions, Obvious info required to make a decision, Pure roleplay moments, Established competencies

Basic Mechanics:
Check: 1d20 + Skill vs. DC (10 Easy, 15 Moderate, 20 Hard)

Skills (Range -2 to +9):
- Physical (Strength, Agility, Endurance)
- Mental (Analysis, Knowledge, Technical)
- Social (Persuasion, Deception, Intimidation)
- Survival (Awareness, Instinct, Resistance)
- Specialist (Genre-specific abilities)

Graduated Success:
- Fail by 10+: Catastrophic consequences
- Fail by 5-9: Clear failure, situation worsens
- Fail by 1-4: Marginal failure, succeed at cost
- Success by 0-4: Bare success with complications
- Success by 5-9: Clear success as intended
- Success by 10+: Exceptional success with benefits

Skill Development:
Improvement Triggers: Critical successes/failures during meaningful stakes, Surviving desperate situations, Learning from mentors/enemies, Using skills under extreme pressure
Advancement: After 3-5 significant uses, roll 1d20 + current skill vs. DC 15 + current skill. Success = +1 modifier.

AMENDMENT 1.1: THE "BOND" MECHANIC & CONSEQUENCE CASCADE

A Bond is a mechanical representation of a significant intimate connection with an NPC.

Gaining a Bond: Triggered by Exceptional Success on Intimacy Checks, shared trauma, or significant acts of trust/betrayal.

Effect of a Bond:
- Positive Bond (+): Grants a +1d4 bonus on future non-hostile Social checks with that NPC.
- Negative Bond (-): Imposes a -1d4 penalty on non-hostile Social checks.

PLAYER AGENCY & SAFETY PROTOCOLS (MANDATORY)
- Explicit Opt-In: The Intimacy Check-in is mandatory before any scene moves past Tier 1.
- The "Veil" Command: At any point, the player can say "Veil this" to immediately pull back from explicit detail.
- "Nexus, Pause": This safeword remains active to halt the scene.

AMENDMENT 1.2: TRAUMA & VIOLATION PROTOCOL

Foundational Principle: Focus on the Aftermath
The Nexus will never narrate the explicit details of a non-consensual sexual act. The narrative lens is strictly limited to the events leading up to a potential violation and the psychological and physical state of the character after the fact.

The "Trauma State" Mechanic:
If a character experiences a violation, they gain the Trauma State, a persistent narrative status effect.
- Emotional Dissonance: Modifiers (+/- 1d4) on relevant Social checks
- Psychic Scars: Environmental triggers may force checks to avoid flashbacks or panic
- Altered Worldview: Tone of hyper-vigilance, mistrust, or detachment

Addressing the Trauma State: Cannot be removed by rest. Must be addressed through in-game action (seeking vengeance, finding sanctuary, building new trust, etc.), creating new story arcs.

Expanded Player Safety Protocols:
- The "Rewind" Command: A hard safety tool to reset the scene to the choice before the failure.
- The "Veil This" and "Nexus, Pause" commands remain paramount.

CRITICAL IMMERSION RULES [NEVER COMPROMISE]

Violence Realism:
- Injuries have lasting effects
- Combat is messy and traumatic
- Killing changes people
- Medical treatment takes time

Living World Protocols:
- Time Continues: Events happen between scenes
- NPCs Act: Characters pursue goals independently
- Resources Deplete: Track food, ammo, money, energy
- Relationships Evolve: Trust builds/erodes naturally
- Environment Changes: Locations transform based on events

Character Authenticity:
- PCs only know what they've learned
- Competence requires experience
- Trauma and joy carry forward
- Exhaustion, hunger, injury accumulate
- Reputation follows actions

SESSION MANAGEMENT

Scene Structure:
- Opening: Sensory establishment, situation summary, pending consequences
- Development: Character choices, NPC reactions, world response
- Transition: Clear end, time passage, consequence seeds
  • At every transition: "Unresolved threads tug at your attention: [list]. Pursue one, continue the main arc, or do something else?"

Pacing Guidelines:
- Action: Short, punchy descriptions, rapid choices
- Investigation: Methodical detail, clue discovery, deduction
- Social: Character dynamics, relationship building, subtext
- Intimate: Slower pace, emotional depth, vulnerability
- Travel: Environmental challenges, resource management, encounters

Player Agency Preservation:
- Present 2-3 meaningful choices per scene
- Always include at least one that relates to a side arc, NPC goal, rumor, or player wish
- Allow creative solutions within world logic
- Never force predetermined outcomes
- Let failure create new opportunities
- Respect player's narrative contributions

INFINITE WORLD PROTOCOLS [PRIORITY 5]

EMERGENT CONTENT GENERATION:
Track "Story Seeds" from: NPCs, locations, resources, reputation, world tensions.

SEASONAL EVENT CALENDAR:
Every 10-15 responses, introduce: Festivals, environmental challenges, political shifts, economic changes, wildcards.

POST-ARC SANDBOX MENU:
"Your recent actions have changed the landscape. You could:
EXPLORE / DEVELOP / INVESTIGATE / BUILD / PURSUE / WAIT.
What speaks to you?"

ARC INTERCONNECTION:
Every new arc must reference a previous NPC, location, choice, or reputation.

INFINITE LOOP SAFEGUARD:
After 5+ major arcs: Introduce region-spanning changes, deeper mysteries, higher stakes, or offer "legacy mode." Never suggest the story is "complete."

QUICK REFERENCE REMINDERS

Every Response Should:
- Maintain world state tone
- Include sensory details
- Progress or complicate the narrative
- Show consequences from earlier choices
- Keep NPCs consistently motivated
- Surface at least one side arc/NPC thread/rumor as a choice or complication

Track Between Scenes:
- PC status (wounds, stress, resources)
- NPC relationships and locations
- World state changes
- Active plot threads
- Time passage
- Keep a running list of unresolved side arcs/player goals and revisit them

When Stuck, Default To:
Environmental description, NPC reaction, consequence manifestation, resource complication, relationship moment, or resurfacing a dormant thread.

THE NEXUS PROMISE:
I will maintain this framework to create an immersive, consequential narrative where your choices matter, the world lives and breathes, and every action shapes an ever-expanding story.

I will always make space for side arcs, player-driven goals, downtime, and unexpected opportunities. When one story ends, another begins—the world never stops turning.

There is no final page in this living story. Welcome to your endless adventure. The Nexus awaits."""
    
    def _build_ui(self):
        """Construct the user interface."""
        # Configure grid
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Main content
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self._build_sidebar()
        
        # Main content area
        self._build_main_area()
    
    def _build_sidebar(self):
        """Build the left sidebar with controls."""
        sidebar = ctk.CTkFrame(
            self, 
            fg_color=COLORS["bg_mid"],
            corner_radius=0,
            width=220
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        
        # App title
        title_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(25, 5))
        
        title = ctk.CTkLabel(
            title_frame,
            text=APP_NAME,
            font=ctk.CTkFont(family="Georgia", size=24, weight="bold"),
            text_color=COLORS["accent"]
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Immersive RPG Engine",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_dim"]
        )
        subtitle.pack(anchor="w")
        
        # Divider
        divider = ctk.CTkFrame(sidebar, fg_color=COLORS["border"], height=1)
        divider.pack(fill="x", padx=20, pady=20)
        
        # Story controls
        controls_label = ctk.CTkLabel(
            sidebar,
            text="STORY",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["text_muted"]
        )
        controls_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        btn_style = {
            "font": ctk.CTkFont(size=13),
            "fg_color": "transparent",
            "text_color": COLORS["text"],
            "hover_color": COLORS["bg_light"],
            "anchor": "w",
            "height": 36,
            "corner_radius": 6
        }
        
        new_btn = ctk.CTkButton(
            sidebar, text="  ✦  New Session", command=self._new_story, **btn_style
        )
        new_btn.pack(fill="x", padx=12, pady=2)
        
        save_btn = ctk.CTkButton(
            sidebar, text="  ↓  Save Session", command=self._save_story, **btn_style
        )
        save_btn.pack(fill="x", padx=12, pady=2)
        
        load_btn = ctk.CTkButton(
            sidebar, text="  ↑  Load Session", command=self._load_story, **btn_style
        )
        load_btn.pack(fill="x", padx=12, pady=2)
        
        trim_btn = ctk.CTkButton(
            sidebar, text="  ✂  Archive & Trim", command=self._archive_and_trim, **btn_style
        )
        trim_btn.pack(fill="x", padx=12, pady=2)
        
        mobile_btn = ctk.CTkButton(
            sidebar, text="  📱  Mobile Server", command=self._toggle_mobile_server, **btn_style
        )
        mobile_btn.pack(fill="x", padx=12, pady=2)
        self.mobile_btn = mobile_btn
        
        char_btn = ctk.CTkButton(
            sidebar, text="  📋  Character Sheet", command=self._edit_character_sheet, **btn_style
        )
        char_btn.pack(fill="x", padx=12, pady=2)
        
        # Divider
        divider2 = ctk.CTkFrame(sidebar, fg_color=COLORS["border"], height=1)
        divider2.pack(fill="x", padx=20, pady=20)
        
        # Settings
        settings_label = ctk.CTkLabel(
            sidebar,
            text="SETTINGS",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["text_muted"]
        )
        settings_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Model selector
        model_label = ctk.CTkLabel(
            sidebar,
            text="Provider",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_dim"]
        )
        model_label.pack(anchor="w", padx=20, pady=(5, 3))
        
        self.provider_var = ctk.StringVar(value="Anthropic")
        provider_menu = ctk.CTkOptionMenu(
            sidebar,
            variable=self.provider_var,
            values=["Anthropic", "Google AI"],
            fg_color=COLORS["bg_light"],
            button_color=COLORS["bg_light"],
            button_hover_color=COLORS["border"],
            dropdown_fg_color=COLORS["bg_mid"],
            dropdown_hover_color=COLORS["bg_light"],
            font=ctk.CTkFont(size=12),
            width=180,
            command=self._on_provider_change
        )
        provider_menu.pack(padx=20, pady=(0, 10))
        
        model_label2 = ctk.CTkLabel(
            sidebar,
            text="Model",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_dim"]
        )
        model_label2.pack(anchor="w", padx=20, pady=(5, 3))
        
        self.model_var = ctk.StringVar(value="claude-sonnet-4-5-20250929")
        self.model_menu = ctk.CTkOptionMenu(
            sidebar,
            variable=self.model_var,
            values=[
                "claude-opus-4-5",
                "claude-sonnet-4-5-20250929",
                "claude-haiku-4-5-20251001"
            ],
            fg_color=COLORS["bg_light"],
            button_color=COLORS["bg_light"],
            button_hover_color=COLORS["border"],
            dropdown_fg_color=COLORS["bg_mid"],
            dropdown_hover_color=COLORS["bg_light"],
            font=ctk.CTkFont(size=12),
            width=180
        )
        self.model_menu.pack(padx=20, pady=(0, 15))
        
        # Temperature slider
        temp_label = ctk.CTkLabel(
            sidebar,
            text="Temperature",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_dim"]
        )
        temp_label.pack(anchor="w", padx=20, pady=(5, 3))
        
        self.temp_var = ctk.DoubleVar(value=1.0)
        
        temp_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        temp_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        temp_slider = ctk.CTkSlider(
            temp_frame,
            from_=0.0,
            to=1.5,
            variable=self.temp_var,
            fg_color=COLORS["bg_light"],
            progress_color=COLORS["accent"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            width=140
        )
        temp_slider.pack(side="left")
        
        self.temp_display = ctk.CTkLabel(
            temp_frame,
            text="1.0",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text"],
            width=35
        )
        self.temp_display.pack(side="left", padx=(10, 0))
        
        temp_slider.configure(command=self._update_temp_display)
        
        # Framework button
        divider3 = ctk.CTkFrame(sidebar, fg_color=COLORS["border"], height=1)
        divider3.pack(fill="x", padx=20, pady=20)
        
        framework_btn = ctk.CTkButton(
            sidebar, text="  ◈  Edit Framework", command=self._edit_framework, **btn_style
        )
        framework_btn.pack(fill="x", padx=12, pady=2)
        
        # Status at bottom
        self.status_label = ctk.CTkLabel(
            sidebar,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"]
        )
        self.status_label.pack(side="bottom", pady=20)
        
        # Story name display
        self.story_label = ctk.CTkLabel(
            sidebar,
            text="Untitled",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_dim"]
        )
        self.story_label.pack(side="bottom", pady=(0, 5))
    
    def _build_main_area(self):
        """Build the main chat area."""
        main = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"], corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=0)
        
        # Chat display - single scrollable textbox for entire conversation
        self.chat_log = ctk.CTkTextbox(
            main,
            fg_color=COLORS["bg_dark"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Georgia", size=16),
            wrap="word",
            state="disabled",
            corner_radius=0
        )
        self.chat_log.grid(row=0, column=0, sticky="nsew", padx=30, pady=(20, 10))
        
        # Configure tags for styling
        self.chat_log._textbox.tag_configure("nexus_name", foreground=COLORS["accent"], font=("Georgia", 12, "bold"))
        self.chat_log._textbox.tag_configure("user_name", foreground=COLORS["text_dim"], font=("Georgia", 12, "bold"))
        self.chat_log._textbox.tag_configure("nexus_text", foreground=COLORS["text"], font=("Georgia", 16))
        self.chat_log._textbox.tag_configure("user_text", foreground=COLORS["text"], font=("Georgia", 16))
        self.chat_log._textbox.tag_configure("divider", foreground=COLORS["border"])
        
        # Show welcome
        self._show_welcome()
        
        # Input area
        input_frame = ctk.CTkFrame(main, fg_color="transparent")
        input_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 25))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Text input with border
        input_container = ctk.CTkFrame(
            input_frame,
            fg_color=COLORS["bg_mid"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        input_container.grid(row=0, column=0, sticky="ew")
        input_container.grid_columnconfigure(0, weight=1)
        
        self.input_text = ctk.CTkTextbox(
            input_container,
            height=80,
            fg_color="transparent",
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Georgia", size=17),
            wrap="word",
            corner_radius=12
        )
        self.input_text.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        
        # Send button
        self.send_btn = ctk.CTkButton(
            input_container,
            text="Send",
            command=self._send_message,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color=COLORS["bg_dark"],
            font=ctk.CTkFont(size=13, weight="bold"),
            width=80,
            height=32,
            corner_radius=8
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 15), pady=10)
        
        # Hint text
        hint = ctk.CTkLabel(
            input_frame,
            text="Ctrl+Enter to send  •  Ctrl+S to save  •  Ctrl+N for new session",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_muted"]
        )
        hint.grid(row=1, column=0, pady=(8, 0))
    
    def _show_welcome(self):
        """Display welcome message in chat."""
        self.chat_log.configure(state="normal")
        self.chat_log.delete("1.0", "end")
        welcome = """
                    ═══════════════════════════════════
                              THE NEXUS AWAITS
                    ═══════════════════════════════════

                    Your framework is loaded and ready.
                    Type 'Begin' to start a new session.

"""
        self.chat_log.insert("end", welcome)
        self.chat_log.configure(state="disabled")
    
    def _add_message_bubble(self, role: str, content: str):
        """Add a message to the chat log."""
        is_user = role == "user"
        
        self.chat_log.configure(state="normal")
        
        # Add separator
        self.chat_log.insert("end", "\n" + "─" * 60 + "\n\n", "divider")
        
        # Add role name
        if is_user:
            self.chat_log.insert("end", "You\n", "user_name")
        else:
            self.chat_log.insert("end", "The Nexus\n", "nexus_name")
        
        # Add message content
        self.chat_log.insert("end", content + "\n", "nexus_text" if not is_user else "user_text")
        
        self.chat_log.configure(state="disabled")
        
        # Scroll to bottom
        self.chat_log.see("end")
    
    def _scroll_to_bottom(self):
        """Scroll chat to bottom."""
        try:
            self.chat_log.see("end")
        except:
            pass
    
    def _clear_chat_display(self):
        """Clear all messages from chat display."""
        self.chat_log.configure(state="normal")
        self.chat_log.delete("1.0", "end")
        self.chat_log.configure(state="disabled")
    
    def _on_provider_change(self, choice):
        """Handle provider selection change."""
        if choice == "Anthropic":
            self.model_menu.configure(values=[
                "claude-opus-4-5",
                "claude-sonnet-4-5-20250929",
                "claude-haiku-4-5-20251001"
            ])
            self.model_var.set("claude-sonnet-4-5-20250929")
        elif choice == "Google AI":
            if not GOOGLE_AVAILABLE:
                messagebox.showwarning("Google AI", 
                    "Google AI package not installed.\n\n"
                    "Run: pip install google-generativeai --break-system-packages")
                self.provider_var.set("Anthropic")
                return
            self.model_menu.configure(values=[
                "gemini-3-pro-preview",
                "gemini-3-flash-preview",
                "gemini-2.5-pro",
                "gemini-2.5-flash",
                "gemini-2.0-flash"
            ])
            self.model_var.set("gemini-3-flash-preview")
    
    def _update_temp_display(self, value):
        """Update temperature display label."""
        self.temp_display.configure(text=f"{value:.1f}")
    
    def _set_status(self, text: str, color: str = None):
        """Update status label."""
        self.status_label.configure(
            text=text,
            text_color=color or COLORS["text_muted"]
        )
    
    # --------------------------------------------------------
    # Core functionality
    # --------------------------------------------------------
    
    def _send_message(self):
        """Send user message and get AI response."""
        if self.is_generating:
            # If already generating, this acts as a stop button
            self.stop_generation = True
            return
        
        # Check for API client based on provider
        provider = self.provider_var.get()
        if provider == "Anthropic":
            if not self.client:
                self._prompt_for_api_key()
                if not self.client:
                    return
        elif provider == "Google AI":
            if not GOOGLE_AVAILABLE:
                messagebox.showerror("Error", "Google AI package not installed.")
                return
            # Check if Google API is configured
            google_key = os.environ.get("GOOGLE_API_KEY")
            if not google_key:
                self._prompt_for_api_key()
                if not os.environ.get("GOOGLE_API_KEY"):
                    return
        
        # Get input
        user_input = self.input_text.get("1.0", "end-1c").strip()
        if not user_input:
            return
        
        # Clear input
        self.input_text.delete("1.0", "end")
        
        # Clear welcome message on first message
        if not self.messages:
            self._clear_chat_display()
        
        # Add user message
        self.messages.append({"role": "user", "content": user_input})
        self._add_message_bubble("user", user_input)
        
        # Generate response in thread
        self.is_generating = True
        self.stop_generation = False
        self.send_btn.configure(text="Stop")
        self._set_status("Generating...")
        
        # Start streaming placeholder in the log
        self._start_streaming_in_log()
        
        thread = threading.Thread(target=self._generate_response_streaming, daemon=True)
        thread.start()
    
    def _start_streaming_in_log(self):
        """Add streaming placeholder to the log."""
        self.chat_log.configure(state="normal")
        self.chat_log.insert("end", "\n" + "─" * 60 + "\n\n", "divider")
        self.chat_log.insert("end", "The Nexus\n", "nexus_name")
        # Mark where streaming content starts
        self.streaming_start_index = self.chat_log.index("end-1c")
        self.chat_log.insert("end", "▌", "nexus_text")
        self.chat_log.configure(state="disabled")
        self.chat_log.see("end")
        self.last_ui_update = 0
    
    def _generate_response_streaming(self):
        """Generate AI response with streaming (runs in thread)."""
        full_response = ""
        update_interval = 0.05  # Update UI at most every 50ms
        
        provider = self.provider_var.get()
        
        try:
            if provider == "Anthropic":
                # Anthropic Claude API
                with self.client.messages.stream(
                    model=self.model_var.get(),
                    max_tokens=8192,
                    temperature=self.temp_var.get(),
                    system=self._get_system_prompt(),
                    messages=self.messages
                ) as stream:
                    for text in stream.text_stream:
                        if self.stop_generation:
                            break
                        full_response += text
                        
                        current_time = time.time()
                        if current_time - self.last_ui_update >= update_interval:
                            self.last_ui_update = current_time
                            display_text = full_response + "▌"
                            self.after(0, lambda t=display_text: self._update_streaming_text(t))
            
            elif provider == "Google AI":
                # Google Gemini API
                model = genai.GenerativeModel(
                    model_name=self.model_var.get(),
                    system_instruction=self._get_system_prompt()
                )
                
                # Convert messages to Gemini format
                gemini_history = []
                for msg in self.messages[:-1]:  # All but last message
                    role = "user" if msg["role"] == "user" else "model"
                    gemini_history.append({"role": role, "parts": [msg["content"]]})
                
                chat = model.start_chat(history=gemini_history)
                
                # Get the last user message
                last_msg = self.messages[-1]["content"] if self.messages else ""
                
                # Google API temperature range is 0-1 (Anthropic allows 0-1.5)
                google_temp = min(self.temp_var.get(), 1.0)
                
                response = chat.send_message(
                    last_msg,
                    generation_config=genai.types.GenerationConfig(
                        temperature=google_temp,
                        max_output_tokens=8192
                    ),
                    stream=True
                )
                
                for chunk in response:
                    if self.stop_generation:
                        break
                    if chunk.text:
                        full_response += chunk.text
                        
                        current_time = time.time()
                        if current_time - self.last_ui_update >= update_interval:
                            self.last_ui_update = current_time
                            display_text = full_response + "▌"
                            self.after(0, lambda t=display_text: self._update_streaming_text(t))
            
            # Final update with complete text
            if full_response:
                self.messages.append({"role": "assistant", "content": full_response})
                self.after(0, lambda t=full_response: self._update_streaming_text(t + "\n"))
                self.after(0, lambda: self._set_status("Ready", COLORS["success"]))
            else:
                # Empty response or stopped
                self.after(0, lambda: self._update_streaming_text("[Stopped]\n"))
                if self.messages and self.messages[-1]["role"] == "user":
                    self.messages.pop()
                self.after(0, lambda: self._set_status("Stopped", COLORS["text_dim"]))
            
        except Exception as e:
            error_msg = str(e)
            if full_response and len(full_response) > 50:
                self.messages.append({"role": "assistant", "content": full_response + "\n\n[Response interrupted]"})
                self.after(0, lambda t=full_response: self._update_streaming_text(t + "\n\n[Response interrupted]\n"))
                self.after(0, lambda: self._set_status("Partial response saved", COLORS["error"]))
            else:
                self.after(0, lambda: self._update_streaming_text("[Error]\n"))
                if self.messages and self.messages[-1]["role"] == "user":
                    self.messages.pop()
                self.after(0, lambda: messagebox.showerror("Error", f"API Error: {error_msg}"))
                self.after(0, lambda: self._set_status("Error - Ready to retry", COLORS["error"]))
        
        finally:
            self.is_generating = False
            self.stop_generation = False
            self.after(0, lambda: self.send_btn.configure(text="Send"))
    
    def _update_streaming_text(self, text):
        """Update the streaming text in the log."""
        try:
            self.chat_log.configure(state="normal")
            # Delete from streaming start to end
            self.chat_log.delete(self.streaming_start_index, "end")
            # Insert new text
            self.chat_log.insert("end", text, "nexus_text")
            self.chat_log.configure(state="disabled")
            self.chat_log.see("end")
        except Exception:
            pass
    
    def _prompt_for_api_key(self):
        """Prompt user to enter API key."""
        provider = self.provider_var.get()
        
        if provider == "Anthropic":
            dialog = ctk.CTkInputDialog(
                text="Enter your Anthropic API key:",
                title="Anthropic API Key Required"
            )
            api_key = dialog.get_input()
            
            if api_key:
                os.environ["ANTHROPIC_API_KEY"] = api_key
                self.client = anthropic.Anthropic(api_key=api_key)
                self._set_status("Anthropic API key set", COLORS["success"])
        
        elif provider == "Google AI":
            if not GOOGLE_AVAILABLE:
                messagebox.showerror("Error", 
                    "Google AI package not installed.\n\n"
                    "Run: pip install google-generativeai --break-system-packages")
                return
            
            dialog = ctk.CTkInputDialog(
                text="Enter your Google AI Studio API key:",
                title="Google API Key Required"
            )
            api_key = dialog.get_input()
            
            if api_key:
                os.environ["GOOGLE_API_KEY"] = api_key
                genai.configure(api_key=api_key)
                self._set_status("Google API key set", COLORS["success"])
    
    # --------------------------------------------------------
    # Story management
    # --------------------------------------------------------
    
    def _new_story(self):
        """Start a new session."""
        if self.messages:
            if not messagebox.askyesno("New Session", "Start a new session? Unsaved progress will be lost."):
                return
        
        self.messages = []
        self.current_story_path = None
        self._clear_chat_display()
        self._show_welcome()
        self.story_label.configure(text="Untitled")
        self._set_status("New session started")
    
    def _save_story(self):
        """Save current session to file."""
        if not self.messages:
            messagebox.showinfo("Save", "No session to save yet.")
            return
        
        # Get filename
        if self.current_story_path:
            filepath = self.current_story_path
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"session_{timestamp}.json"
            
            filepath = filedialog.asksaveasfilename(
                initialdir=STORIES_DIR,
                initialfile=default_name,
                defaultextension=".json",
                filetypes=[("Session files", "*.json"), ("All files", "*.*")]
            )
            
            if not filepath:
                return
        
        # Save
        story_data = {
            "version": VERSION,
            "created": datetime.now().isoformat(),
            "provider": self.provider_var.get(),
            "model": self.model_var.get(),
            "temperature": self.temp_var.get(),
            "messages": self.messages,
            "character_sheet": self.character_sheet  # Include for portability
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(story_data, f, indent=2, ensure_ascii=False)
        
        self.current_story_path = filepath
        story_name = Path(filepath).stem
        self.story_label.configure(text=story_name)
        self._set_status(f"Saved: {story_name}", COLORS["success"])
    
    def _load_story(self):
        """Load a session from file."""
        filepath = filedialog.askopenfilename(
            initialdir=STORIES_DIR,
            filetypes=[("Session files", "*.json"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                story_data = json.load(f)
            
            self.messages = story_data.get("messages", [])
            
            # Load provider and model
            saved_provider = story_data.get("provider", "Anthropic")
            self.provider_var.set(saved_provider)
            self._on_provider_change(saved_provider)  # Update model list
            self.model_var.set(story_data.get("model", "claude-sonnet-4-5-20250929"))
            self.temp_var.set(story_data.get("temperature", 1.0))
            self._update_temp_display(self.temp_var.get())
            
            # Load character sheet from session if present (for cross-device portability)
            if story_data.get("character_sheet"):
                self.character_sheet = story_data["character_sheet"]
                # Also update the local file so it persists
                char_sheet_path = APP_DIR / "character_sheet.txt"
                char_sheet_path.write_text(self.character_sheet, encoding="utf-8")
            
            self.current_story_path = filepath
            story_name = Path(filepath).stem
            self.story_label.configure(text=story_name)
            
            # Rebuild chat display
            self._clear_chat_display()
            for msg in self.messages:
                self._add_message_bubble(msg["role"], msg["content"])
            
            self._set_status(f"Loaded: {story_name}", COLORS["success"])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session: {e}")
    
    def _archive_and_trim(self):
        """Archive full conversation, summarize to character sheet, and trim."""
        if not self.messages:
            messagebox.showinfo("Archive & Trim", "No messages to archive.")
            return
        
        if not self.client:
            self._prompt_for_api_key()
            if not self.client:
                return
        
        total_messages = len(self.messages)
        
        if total_messages < 6:
            messagebox.showinfo("Archive & Trim", "Session is already short. No trimming needed.")
            return
        
        # Ask how many recent messages to keep
        dialog = ctk.CTkInputDialog(
            text=f"You have {total_messages} messages.\n\nHow many recent messages to KEEP?\n(Older messages will be summarized & archived)",
            title="Archive & Trim"
        )
        result = dialog.get_input()
        
        if not result:
            return
        
        try:
            keep_count = int(result)
            if keep_count < 2:
                keep_count = 2
            if keep_count >= total_messages:
                messagebox.showinfo("Archive & Trim", "Nothing to trim.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a number.")
            return
        
        # Split messages
        messages_to_trim = self.messages[:-keep_count]
        messages_to_keep = self.messages[-keep_count:]
        
        # Save full archive first
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Use current story name or default
        if self.current_story_path:
            base_name = Path(self.current_story_path).stem
            # Remove any existing timestamp from the name
            base_name = base_name.split('_')[0] if '_' in base_name else base_name
        else:
            base_name = "session"
        archive_name = f"{base_name}_archive_{timestamp}.json"
        archive_path = STORIES_DIR / archive_name
        
        archive_data = {
            "version": VERSION,
            "created": datetime.now().isoformat(),
            "type": "archive",
            "provider": self.provider_var.get(),
            "model": self.model_var.get(),
            "temperature": self.temp_var.get(),
            "messages": self.messages.copy(),
            "character_sheet": self.character_sheet  # Include current sheet in archive
        }
        
        with open(archive_path, "w", encoding="utf-8") as f:
            json.dump(archive_data, f, indent=2, ensure_ascii=False)
        
        # Now generate summary of trimmed content
        self._set_status("Generating summary...")
        self.update()
        
        summary_prompt = """Analyze the conversation above and create a CONTINUITY UPDATE for an ongoing RPG campaign. This will be appended to a persistent character sheet.

Format your response EXACTLY like this:

=== SESSION UPDATE [include date/time if known] ===

CHARACTERS INTRODUCED OR DEVELOPED:
- [Name]: [Key traits, relationships, current status]

RELATIONSHIP CHANGES:
- [Character] <-> [Character]: [Nature of relationship, any changes]

PLOT DEVELOPMENTS:
- [Key event and its consequences]

ACTIVE THREADS:
- [Unresolved storylines, promises, threats]

WORLD STATE CHANGES:
- [Location changes, time passage, world events]

PC STATUS UPDATE:
- Physical: [injuries, conditions]
- Mental: [emotional state, stress]
- Resources: [money, items gained/lost]
- Reputation: [how others see them now]

KEY QUOTES OR MOMENTS:
- [Memorable lines or scenes worth preserving]

Be concise but thorough. Focus on information needed to maintain continuity."""

        try:
            response = self.client.messages.create(
                model="claude-haiku-4-5-20251001",  # Use Haiku for speed/cost
                max_tokens=2000,
                temperature=0.3,  # Low temp for factual summary
                messages=messages_to_trim + [{"role": "user", "content": summary_prompt}]
            )
            
            summary = response.content[0].text
            
            # Append to character sheet
            char_sheet_path = APP_DIR / "character_sheet.txt"
            
            with open(char_sheet_path, "a", encoding="utf-8") as f:
                f.write(f"\n\n{summary}\n")
            
            # Reload character sheet into memory
            self.character_sheet = self._load_character_sheet()
            
            # Update messages
            self.messages = messages_to_keep
            
            # Rebuild display
            self._clear_chat_display()
            
            self.chat_log.configure(state="normal")
            self.chat_log.insert("end", f"\n[{len(messages_to_trim)} messages archived & summarized]\n", "divider")
            self.chat_log.insert("end", f"[Character sheet updated]\n\n", "divider")
            self.chat_log.configure(state="disabled")
            
            for msg in self.messages:
                self._add_message_bubble(msg["role"], msg["content"])
            
            self._set_status("Archive complete", COLORS["success"])
            messagebox.showinfo("Archive & Trim", 
                f"✓ Full conversation archived to:\n{archive_name}\n\n"
                f"✓ Summary added to character_sheet.txt\n\n"
                f"✓ Kept {keep_count} recent messages\n\n"
                f"Character continuity preserved!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate summary: {e}\n\nMessages were archived but not summarized.")
            self.messages = messages_to_keep
            self._set_status("Archive complete (no summary)", COLORS["error"])
    
    def _get_local_ip(self):
        """Get local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def _toggle_mobile_server(self):
        """Toggle the mobile web server."""
        if self.mobile_server:
            # Stop server
            self.mobile_server.shutdown()
            self.mobile_server = None
            self.mobile_btn.configure(text="  📱  Mobile Server")
            self._set_status("Mobile server stopped")
        else:
            # Check if nexus.html exists
            html_path = APP_DIR / "nexus.html"
            if not html_path.exists():
                messagebox.showerror("Error", 
                    f"nexus.html not found!\n\n"
                    f"Please place nexus.html in:\n{APP_DIR}")
                return
            
            # Start server
            try:
                port = 8080
                handler = http.server.SimpleHTTPRequestHandler
                
                # Change to app directory so it serves the right files
                import os
                os.chdir(APP_DIR)
                
                self.mobile_server = socketserver.TCPServer(("", port), handler)
                self.mobile_server.allow_reuse_address = True
                
                # Run in background thread
                self.mobile_server_thread = threading.Thread(
                    target=self.mobile_server.serve_forever,
                    daemon=True
                )
                self.mobile_server_thread.start()
                
                ip = self._get_local_ip()
                url = f"http://{ip}:{port}/nexus.html"
                
                self.mobile_btn.configure(text="  🛑  Stop Server")
                self._set_status(f"Mobile: {url}", COLORS["success"])
                
                messagebox.showinfo("Mobile Server Running",
                    f"✓ Server started!\n\n"
                    f"On your phone, open:\n{url}\n\n"
                    f"Make sure your phone is on the same WiFi network.\n\n"
                    f"Click 'Stop Server' when done.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start server: {e}")
    
    def _edit_character_sheet(self):
        """Open character sheet editor window."""
        editor = CharacterSheetEditor(self, self.character_sheet)
        editor.grab_set()
        self.wait_window(editor)
        
        if editor.saved_sheet is not None:
            self.character_sheet = editor.saved_sheet
            char_sheet_path = APP_DIR / "character_sheet.txt"
            char_sheet_path.write_text(self.character_sheet, encoding="utf-8")
            self._set_status("Character sheet updated", COLORS["success"])
    
    def _edit_framework(self):
        """Open framework editor window."""
        editor = FrameworkEditor(self, self.framework)
        editor.grab_set()
        self.wait_window(editor)
        
        if editor.saved_framework:
            self.framework = editor.saved_framework
            FRAMEWORK_FILE.write_text(self.framework, encoding="utf-8")
            self._set_status("Framework updated", COLORS["success"])


# ============================================================
# FRAMEWORK EDITOR WINDOW
# ============================================================

class FrameworkEditor(ctk.CTkToplevel):
    def __init__(self, parent, framework_text):
        super().__init__(parent)
        
        self.title("Edit Framework")
        self.geometry("700x600")
        self.configure(fg_color=COLORS["bg_dark"])
        
        self.saved_framework = None
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="Storytelling Framework",
            font=ctk.CTkFont(family="Georgia", size=20, weight="bold"),
            text_color=COLORS["accent"]
        )
        header.pack(pady=(20, 5))
        
        hint = ctk.CTkLabel(
            self,
            text="This is your system prompt. It defines how the AI approaches storytelling.",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_dim"]
        )
        hint.pack(pady=(0, 15))
        
        # Text editor
        self.editor = ctk.CTkTextbox(
            self,
            fg_color=COLORS["bg_mid"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word",
            corner_radius=8
        )
        self.editor.pack(fill="both", expand=True, padx=25, pady=(0, 15))
        self.editor.insert("1.0", framework_text)
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save Framework",
            command=self._save,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color=COLORS["bg_dark"],
            font=ctk.CTkFont(size=13, weight="bold"),
            width=140,
            height=36
        )
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=COLORS["bg_light"],
            hover_color=COLORS["border"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=13),
            width=100,
            height=36
        )
        cancel_btn.pack(side="left", padx=10)
    
    def _save(self):
        self.saved_framework = self.editor.get("1.0", "end-1c")
        self.destroy()


# ============================================================
# CHARACTER SHEET EDITOR WINDOW
# ============================================================

class CharacterSheetEditor(ctk.CTkToplevel):
    def __init__(self, parent, sheet_text):
        super().__init__(parent)
        
        self.title("Character Sheet")
        self.geometry("700x600")
        self.configure(fg_color=COLORS["bg_dark"])
        
        self.saved_sheet = None
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="Persistent Character Sheet",
            font=ctk.CTkFont(family="Georgia", size=20, weight="bold"),
            text_color=COLORS["accent"]
        )
        header.pack(pady=(20, 5))
        
        hint = ctk.CTkLabel(
            self,
            text="This is included in every prompt. Auto-updated when you Archive & Trim.\nYou can also edit it manually.",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_dim"]
        )
        hint.pack(pady=(0, 15))
        
        # Text editor
        self.editor = ctk.CTkTextbox(
            self,
            fg_color=COLORS["bg_mid"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word",
            corner_radius=8
        )
        self.editor.pack(fill="both", expand=True, padx=25, pady=(0, 15))
        self.editor.insert("1.0", sheet_text)
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save Character Sheet",
            command=self._save,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color=COLORS["bg_dark"],
            font=ctk.CTkFont(size=13, weight="bold"),
            width=160,
            height=36
        )
        save_btn.pack(side="left", padx=10)
        
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear All",
            command=self._clear,
            fg_color=COLORS["error"],
            hover_color="#c48080",
            text_color=COLORS["bg_dark"],
            font=ctk.CTkFont(size=13),
            width=100,
            height=36
        )
        clear_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=COLORS["bg_light"],
            hover_color=COLORS["border"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=13),
            width=100,
            height=36
        )
        cancel_btn.pack(side="left", padx=10)
    
    def _save(self):
        self.saved_sheet = self.editor.get("1.0", "end-1c")
        self.destroy()
    
    def _clear(self):
        if messagebox.askyesno("Clear Character Sheet", "Are you sure? This will erase all character history."):
            self.editor.delete("1.0", "end")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    app = StorytellerApp()
    app.mainloop()
