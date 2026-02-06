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
        self.reference_documents = []  # User-uploaded reference docs (playbooks, rules, etc.)
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
        if self.reference_documents:
            system += "\n\n" + "=" * 60 + "\n"
            system += "REFERENCE DOCUMENTS\n"
            system += "(Player-provided materials for this campaign - rules, playbooks, maps, etc.)\n"
            system += "=" * 60 + "\n\n"
            for doc in self.reference_documents:
                system += f"--- {doc['name']} ---\n\n{doc['content']}\n\n"
        return system
    
    def _default_framework(self):
        """Return the Nexus RPG framework."""
        return """GENRE-FLEXIBLE IMMERSIVE RPG FRAMEWORK
Streamlined Edition, Retuned for Dynamic Side Arcs and Player-Led Storytelling

[... (The default framework text, unchanged from previous) ...]"""
    
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
        
        ref_docs_btn = ctk.CTkButton(
            sidebar, text="  📚  Reference Docs", command=self._manage_reference_docs, **btn_style
        )
        ref_docs_btn.pack(fill="x", padx=12, pady=2)
        
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
                "claude-opus-4-6",
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
                "claude-opus-4-6",
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
            "character_sheet": self.character_sheet,  # Include for portability
            "reference_documents": self.reference_documents  # Include reference docs
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
            
            # Load reference documents if present
            self.reference_documents = story_data.get("reference_documents", [])
            
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
        
        summary_prompt = f"""You are a continuity assistant for an ongoing RPG campaign. Your job is to capture the SOUL and FACTS of the session.

CRITICAL RULES:
1. DO NOT simply summarize actions. Capture the TONE, ATMOSPHERE, and SUBTEXT.
2. Physical descriptions must be PRECISE (height, colors, scars).
3. Names must be EXACT.
4. **PRESERVE ESTABLISHED FACTS** from the existing data.
5. Distinguish between what is KNOWN and what is merely SUSPECTED.

EXISTING DATA (PRESERVE THIS):
{self.character_sheet if self.character_sheet else 'No existing character sheet - this is the first session'}

Your task: Update the sheet with NEW information from the conversation above while PRESERVING all existing facts that haven't changed.

REQUIRED SECTIONS:

## 0. NARRATIVE STYLE & PROSE ANCHOR
- Current Genre/Tone: [e.g. Gritty Noir, High Fantasy, Cyberpunk Horror]
- Prose Settings: [e.g. "Short sentences," "Purple prose," "Focus on sensory details"]
- Active World State: [From the World State Engine: e.g. Dystopian/Rupture]

## 1. THE SENSORY SNAPSHOT (The "Now")
- Immediate Surroundings: [What does the PC see/smell/hear RIGHT NOW?]
- Atmospheric Tension: [Is it quiet? Chaotic? Tense? Joyful?]
- The Last Moment: [Exactly where the camera froze - preserving the cliffhanger]

## 2. PC IMMUTABLE FACTS
- Full Name:
- Species/Race:
- Physical Description: [EXACT height, build, distinguishing features, scars, etc.]
- Age/Appearance Age:
- Background Origin:

## 3. PC CURRENT STATUS
- Current Location:
- Physical Condition: [injuries, scars gained THIS session, current health]
- Mental/Emotional State: [Internal monologue, fears, current motivation]
- Resources: [money, items, equipment - be specific with quantities]
- Reputation Changes: [Who now views PC differently and why]

## 4. GOLDEN QUOTES & MEMORIES
- [Extract 1-2 verbatim quotes of dialogue that defined this session]
- [Extract 1 verbatim sentence of description that captured the vibe]

## 5. RELATIONSHIPS & SUBTEXT
For each NPC mentioned in THIS session OR in existing sheet:
- Name: [EXACT spelling]
- Role/Occupation:
- Physical Description: [if mentioned]
- Relationship to PC: [ally/enemy/neutral, trust level]
- **Subtext/Vibes**: [Do they trust the PC? Are they hiding something? Is there sexual tension? Fear?]
- Last Known Location:
- Promises/Agreements: [EXACT quote if NPC asked PC to do something or vice versa]
- Current Status: [alive/dead/missing/unknown]

## 6. MYSTERIES & OPEN LOOPS
- Active Quests: [Objective and Status]
- **Unresolved Suspicions**: [What does the PC suspect but not know? DO NOT RESOLVE THESE.]
- **Secrets Kept**: [What is the PC hiding from the world?]

## 7. WORLD STATE & LOCATIONS
- New Locations Discovered: [name, description, how to get there]
- Faction Changes: [which groups now view PC differently]
- Major Events: [things that happened that affect the world]
- Active Threats: [enemies hunting PC, time-sensitive dangers]

## 8. TIMELINE OF THIS SESSION
1. [Chronological event 1]
2. [Chronological event 2]
...

IMPORTANT: If the existing character sheet says "As'mara is 6'3"" and this session doesn't show a height change, you MUST preserve "6'3"" exactly. Same for all immutable facts. Only update facts if the conversation explicitly changes them.

DO NOT EDITORIALIZE. Extract facts only.

SESSION CONTENT:
{chr(10).join([f"{m['role'].upper()}: {m['content']}" for m in messages_to_trim])}"""

        try:
            response = self.client.messages.create(
                model="claude-haiku-4-5-20251001",  # Use Haiku for speed/cost
                max_tokens=2000,
                temperature=0.3,  # Low temp for factual summary
                messages=[{"role": "user", "content": summary_prompt}]
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
    
    def _manage_reference_docs(self):
        """Open reference documents manager window."""
        manager = ReferenceDocsManager(self, self.reference_documents)
        manager.grab_set()
        self.wait_window(manager)
        
        if manager.updated_docs is not None:
            self.reference_documents = manager.updated_docs
            self._set_status(f"Reference documents: {len(self.reference_documents)} loaded", COLORS["success"])


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
# REFERENCE DOCUMENTS MANAGER WINDOW
# ============================================================

class ReferenceDocsManager(ctk.CTkToplevel):
    def __init__(self, parent, reference_docs):
        super().__init__(parent)
        
        self.title("Reference Documents")
        self.geometry("700x600")
        self.configure(fg_color=COLORS["bg_dark"])
        
        self.updated_docs = None
        self.docs = list(reference_docs)  # Make a copy
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="📚 Reference Documents",
            font=ctk.CTkFont(family="Georgia", size=20, weight="bold"),
            text_color=COLORS["accent"]
        )
        header.pack(pady=(20, 5))
        
        hint = ctk.CTkLabel(
            self,
            text="Upload playbooks, rules, maps, or other reference materials.\nSupports: .txt, .md, .pdf files",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_dim"]
        )
        hint.pack(pady=(0, 15))
        
        # Document list
        list_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_mid"])
        list_frame.pack(fill="both", expand=True, padx=25, pady=(0, 15))
        
        self.doc_list = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS["bg_mid"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word",
            corner_radius=8
        )
        self.doc_list.pack(fill="both", expand=True, padx=10, pady=10)
        
        self._update_doc_list()
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        
        upload_btn = ctk.CTkButton(
            btn_frame,
            text="+ Upload Document",
            command=self._upload_doc,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color=COLORS["bg_dark"],
            font=ctk.CTkFont(size=13, weight="bold"),
            width=160,
            height=36
        )
        upload_btn.pack(side="left", padx=10)
        
        remove_btn = ctk.CTkButton(
            btn_frame,
            text="Remove Selected",
            command=self._remove_doc,
            fg_color=COLORS["error"],
            hover_color="#c48080",
            text_color=COLORS["bg_dark"],
            font=ctk.CTkFont(size=13),
            width=140,
            height=36
        )
        remove_btn.pack(side="left", padx=10)
        
        done_btn = ctk.CTkButton(
            btn_frame,
            text="Done",
            command=self._done,
            fg_color=COLORS["bg_light"],
            hover_color=COLORS["border"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=13),
            width=100,
            height=36
        )
        done_btn.pack(side="left", padx=10)
    
    def _update_doc_list(self):
        """Update the document list display."""
        self.doc_list.configure(state="normal")
        self.doc_list.delete("1.0", "end")
        
        if not self.docs:
            self.doc_list.insert("1.0", "No documents uploaded yet.\n\nClick '+ Upload Document' to add reference materials.")
        else:
            for i, doc in enumerate(self.docs):
                size_kb = len(doc['content']) / 1024
                self.doc_list.insert("end", f"{i+1}. {doc['name']} ({size_kb:.1f} KB)\n")
                self.doc_list.insert("end", f"   Uploaded: {doc.get('uploadedAt', 'Unknown')}\n\n")
        
        self.doc_list.configure(state="disabled")
    
    def _upload_doc(self):
        """Upload a new document."""
        filepath = filedialog.askopenfilename(
            title="Select Reference Document",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )
        
        if not filepath:
            return
        
        try:
            filename = Path(filepath).name
            
            if filepath.endswith('.pdf'):
                # For PDFs, try to extract text using PyPDF2 if available
                try:
                    import PyPDF2
                    with open(filepath, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        content = ""
                        for page_num, page in enumerate(pdf_reader.pages, 1):
                            text = page.extract_text()
                            content += f"\n--- Page {page_num} ---\n{text}\n"
                    
                    if not content.strip():
                        raise Exception("No text could be extracted from this PDF")
                        
                except ImportError:
                    messagebox.showerror(
                        "PDF Support",
                        "PDF support requires PyPDF2.\n\nInstall with: pip install PyPDF2\n\nOr convert your PDF to .txt first."
                    )
                    return
            else:
                # Read as text
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # Check size
            if len(content) > 500000:
                if not messagebox.askyesno(
                    "Large File",
                    f"This file is {len(content)/1024:.1f} KB.\nLarge files may slow down responses.\n\nContinue?"
                ):
                    return
            
            # Add document
            self.docs.append({
                'name': filename,
                'content': content,
                'uploadedAt': datetime.now().isoformat()
            })
            
            self._update_doc_list()
            messagebox.showinfo("Success", f"Added: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def _remove_doc(self):
        """Remove a selected document."""
        if not self.docs:
            return
        
        # Simple selection dialog
        names = [f"{i+1}. {doc['name']}" for i, doc in enumerate(self.docs)]
        selection = ctk.CTkInputDialog(
            text="\n".join(names) + "\n\nEnter number to remove:",
            title="Remove Document"
        ).get_input()
        
        if selection:
            try:
                index = int(selection) - 1
                if 0 <= index < len(self.docs):
                    removed = self.docs.pop(index)
                    self._update_doc_list()
                    messagebox.showinfo("Removed", f"Removed: {removed['name']}")
                else:
                    messagebox.showerror("Error", "Invalid selection")
            except ValueError:
                messagebox.showerror("Error", "Please enter a number")
    
    def _done(self):
        """Save and close."""
        self.updated_docs = self.docs
        self.destroy()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    app = StorytellerApp()
    app.mainloop()