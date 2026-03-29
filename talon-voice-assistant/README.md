# Talon Voice Assistant Plugin

An agent plugin (i.e. collection of skills) that guides new users through installing, configuring, and creating custom voice commands with [Talon](https://talonvoice.com/) — no prior experience required.

## What This Plugin Does

This plugin provides seven skills that walk you through the complete Talon journey, from first install to writing and testing your own voice commands:

| Skill | What it helps with |
|---|---|
| **Start** | Initialize the assistant — creates your profile so all other skills adapt to your experience level (run this first) |
| **Setup Talon** | Install Talon, the community command set, and optionally Rango for browser voice control |
| **Setup Rango** | Install and configure Rango for hands-free browser control — clicking, scrolling, tabs, and forms |
| **Create Custom Repo** | Set up a personal commands folder alongside the community repo (the recommended approach) |
| **Create Basic Command** | Write `.talon` files that map spoken phrases to keyboard shortcuts, text input, and app actions |
| **Create Python Command** | Build advanced commands with Python logic — file operations, conditional behavior, reusable actions |
| **Test and Debug** | Verify commands work using the Talon log, REPL introspection, pytest, and live voice testing |

## Training Page

The plugin includes an interactive HTML training page (`resources/talon-training.html`) for practicing Talon voice commands in the browser. Open it locally and use your voice to complete drills. (this is still quite incomplete)

**Modes:**

- **Alphabet** — Say the phonetic word for each letter (e.g., "gust" for G). Retry on wrong answers before moving on.
- **Spell Words** — Chain alphabet commands to spell whole words. Letter boxes fill in as you go, with per-character retry and hints.
- **Numbers** — Say the number shown.
- **Symbols** — Say the name for each punctuation mark or special character.
- **Formatters** — Apply formatters like `snake`, `camel`, and `kebab` to sample text.

Features: score tracking, streak counter, sound cues, adjustable question counts, alphabet reference panel.

## How to Use

After installing the plugin or just adding the set of skills to your setup, just ask your agent for help with any Talon-related task. For example:

- "Help me install Talon on my Mac"
- "Set up Rango so I can control the browser with my voice"
- "Set up a folder for my custom commands"
- "Create a voice command that opens my notes folder"
- "Write a Python action that counts words in my selection"
- "My command isn't working — help me debug it"

Claude will walk you through each step with clear, jargon-free instructions.

## Prerequisites

- **macOS High Sierra (10.13) or later** (Apple Silicon natively supported)
- **Terminal access** (for running git commands during setup)
- No prior experience with Talon, voice control, or programming is needed

## Project Structure

```
talon-voice-assistant/
├── .claude-plugin/
│   └── plugin.json                         # Plugin metadata
├── skills/
│   ├── start/
│   │   └── SKILL.md                        # Profile setup and onboarding
│   ├── setup-talon/
│   │   ├── SKILL.md                        # Installation walkthrough
│   │   └── references/troubleshooting.md   # Common setup issues
│   ├── setup-rango/
│   │   ├── SKILL.md                        # Rango installation and first-15-minutes guide
│   │   └── references/rango-commands.md    # Complete Rango voice command reference
│   ├── create-custom-repo/
│   │   ├── SKILL.md                        # Personal repo setup guide
│   │   └── references/directory-layout.md  # Talon user directory structure
│   ├── create-basic-command/
│   │   ├── SKILL.md                        # .talon file authoring guide
│   │   └── references/syntax-guide.md      # Complete .talon syntax reference
│   ├── create-python-command/
│   │   ├── SKILL.md                        # Python-scripted commands guide
│   │   └── references/python-api-reference.md  # Talon Python API cheat sheet
│   └── test-and-debug/
│       ├── SKILL.md                        # 5-step testing checklist
│       └── references/common-errors.md     # Error patterns and fixes
├── resources/
│   └── talon-training.html                 # Interactive voice training page
└── README.md
```

## Building the Plugin

To package the source into a `.plugin` file:

```bash
cd talon-voice-assistant
zip -r ../talon-voice-assistant.plugin . -x '*.git*' -x '*.DS_Store'
```

## Key Resources

- [Talon Voice](https://talonvoice.com/) — Official site and downloads
- [Talon Wiki](https://talon.wiki/) — Community documentation
- [Community Commands](https://github.com/talonhub/community) — The standard command set
- [Rango](https://github.com/david-tejada/rango) — Browser voice control extension
- [Rango Documentation](https://rango.click) — Rango usage guide and configuration
- [Talon Practice](https://chaosparrot.github.io/talon_practice/) — Interactive browser-based drills
- [Talon Slack](https://talonvoice.com/chat) — Community support (`#help` channel)

