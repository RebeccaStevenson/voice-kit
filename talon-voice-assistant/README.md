# Talon-voice-assistant

A collection of skills that guides new users through installing, configuring, and creating custom voice commands with [Talon](https://talonvoice.com/), hopefully making the process mostly hands off i.e. the agent does pretty much everything for you. Beginner friendly, no coding experience required.


| Skill | What it helps with |
|---|---|
| **Start** | Initialize the assistant — creates your profile so all other skills adapt to your experience level (run this first) |
| **Setup Talon** | Install Talon, the community command set, and optionally Rango for browser voice control |
| **Setup Rango** | Install and configure Rango for hands-free browser control — clicking, scrolling, tabs, and forms |
| **Create Custom Repo** | Set up a personal commands folder alongside the community repo (the recommended approach) |
| **Create Basic Command** | Write `.talon` files that map spoken phrases to keyboard shortcuts, text input, and app actions |
| **Create Python Command** | Build advanced commands with Python logic — file operations, conditional behavior, reusable actions |
| **Test and Debug** | Verify commands work using the Talon log, REPL introspection, pytest, and live voice testing |

## How to Use

**Installation**

- **Cowork** — This is usually the easiest path if you are not comfortable working in the terminal or running install commands yourself. You can skim the official [Discover and install plugins](https://docs.anthropic.com/en/discover-plugins) guide (and [Create plugins](https://docs.anthropic.com/en/docs/claude-code/plugins) if you want more context), then ask cowork to install this repository as a plugin for you.
- **Claude Code, Codex, Cursor, and similar** — You can copy each subfolder under `skills/` into that product’s skills directory so these guides appear like any other skill.
- **Plugins** — Claude Code and Codex can also load this project as a plugin, but their plugin documentation is changing quickly; until that stabilizes, copying the skill folders is the most straightforward option.

After installing, just ask your agent for help with any Talon-related task. For example:

- "Help me install Talon on my Mac"
- "Set up Rango so I can control the browser with my voice"
- "Set up a folder for my custom commands"
- "Create a voice command that opens my notes folder"
- "Write a Python action that counts words in my selection"
- "My command isn't working — help me debug it"

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

Packaging, versioning, and distribution are covered in [Create plugins](https://docs.anthropic.com/en/docs/claude-code/plugins) and the [Plugins reference](https://docs.anthropic.com/en/plugins-reference).

## Key Resources

- [Talon Voice](https://talonvoice.com/) — Official site and downloads
- [Talon Wiki](https://talon.wiki/) — Community documentation
- [Community Commands](https://github.com/talonhub/community) — The standard command set
- [Rango](https://github.com/david-tejada/rango) — Browser voice control extension
- [Rango Documentation](https://rango.click) — Rango usage guide and configuration
- [Talon Practice](https://chaosparrot.github.io/talon_practice/) — Interactive browser-based drills
- [Talon Slack](https://talonvoice.com/chat) — Community support (`#help` channel)


## Training Page

The plugin includes an interactive HTML training page at `resources/talon-training.html`. Double click it or ask the agent to open it for you. For more practice in the browser, try [Talon Practice](https://chaosparrot.github.io/talon_practice/) as well.