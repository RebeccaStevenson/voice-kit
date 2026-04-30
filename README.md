# Voice-Kit

## What this is

Skills and resources for setting up and customizing voice control (Talon Voice) and dictation (SuperWhisper) tools

## Who this is for

- People with repetitive strain injury (RSI) or other mobility constraints
- People that want to set up voice-powered automations for everything from simple keyboard shortcuts to multi-step workflows
- Parents who want to work while holding babies
- Non-coders and software engineers and everyone in between

## What you can do with these skills

| Workflow | Example request |
|---|---|
| Install Talon and the community command set | "Help me install Talon on my Mac." |
| Add browser voice control with Rango | "Set up Rango so I can control Chrome with my voice." |
| Create simple Talon commands | "Make a voice command that opens my notes folder." |
| Create Python-backed Talon actions | "Make a voice command that starts a new terminal window and launches VS Code in a specified folder." |
| Test and debug Talon commands | "My Talon command is not working. Help me debug it." |
| Create or edit SuperWhisper modes | "Make a SuperWhisper mode for email with the following specifications..." |

## Install

For agents that support project-local skills, clone this repo and copy the skill folders into `.agents/skills`:

```bash
mkdir -p .agents/skills && \
tmpdir="$(mktemp -d)" && \
git clone --single-branch --depth 1 https://github.com/RebeccaStevenson/voice-kit.git "$tmpdir/voice-kit" && \
cp -R "$tmpdir/voice-kit"/talon-* "$tmpdir/voice-kit"/superwhisper-assistant .agents/skills/ && \
rm -rf "$tmpdir"
```

This copies the actual skill directories into `.agents/skills` so the agent sees each skill as a direct child directory with its own `SKILL.md`.

Then add a short note to your `AGENTS.md` telling the agent to use these skills for Talon Voice and SuperWhisper tasks. For example:

```md
## Voice-Kit skills

Use the skills in `.agents/skills/` for Talon Voice and SuperWhisper tasks:
- `talon-start`
- `talon-setup-talon`
- `talon-setup-rango`
- `talon-create-custom-repo`
- `talon-create-basic-command`
- `talon-create-python-command`
- `talon-test-and-debug`
- `talon-setup-cursorless`
- `superwhisper-assistant`
```

After installing, restart your agent so it reloads the skill list.

## Voice control skills

| Skill | What it does | Example request |
|---|---|---|
| [talon-start/](talon-start/) | Creates a user profile so later Talon help can match the user’s experience level. | "Set up the Talon assistant for me." |
| [talon-setup-talon/](talon-setup-talon/) | Walks a beginner through installing Talon, enabling speech recognition, and cloning the community repo. | "Help me get Talon running from scratch." |
| [talon-setup-rango/](talon-setup-rango/) | Adds Rango so the browser can be controlled by voice. | "Set up browser voice control with Rango." |
| [talon-create-custom-repo/](talon-create-custom-repo/) | Creates a personal Talon repo so custom commands stay separate from upstream repos. | "Set up my own Talon commands folder." |
| [talon-create-basic-command/](talon-create-basic-command/) | Creates `.talon` commands for shortcuts, text insertion, and app-specific actions. | "Make a command that pastes my email signature." |
| [talon-create-python-command/](talon-create-python-command/) | Builds more advanced Talon commands with Python logic and reusable actions. | "Create a Talon action that cleans up selected text." |
| [talon-test-and-debug/](talon-test-and-debug/) | Checks logs, REPL output, and tests so broken commands can be diagnosed quickly. | "This command loads but never triggers. Debug it." |
| [talon-setup-cursorless/](talon-setup-cursorless/) | Installs Cursorless for hat-and-target-style voice editing in VSCode (and Cursor / VSCodium). | "Set up Cursorless so I can edit code by voice." |
| `talon-settings` | Planned skill for editing Talon settings such as phrase timeout timing, pause lengths between commands, subtitle display, and other configuration values. | "Adjust Talon's end-of-phrase timing and subtitle settings." |

## SuperWhisper skills

| Skill | What it does | Example request |
|---|---|---|
| [superwhisper-assistant/](superwhisper-assistant/) | Installs SuperWhisper, configures models, and creates or edits custom mode JSON files. | "Create a SuperWhisper mode for editing emails." |
| `voice-memo-transcriber` | Planned skill for turning voice memos into transcripts, summaries, and action items. | "Transcribe my latest voice memos and pull out tasks." |

## Resource links

See [resource-links.md](resource-links.md) for a more complete list of tools and resources that I use
