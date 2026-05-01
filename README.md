# Voice-Kit

## What this is

Skills and resources for setting up and customizing voice control (Talon Voice) and dictation (SuperWhisper) tools.

The Talon skills distill the [Talon Community Wiki](https://talon.wiki/) into on-demand, agent-driven workflows. Instead of reading the wiki and configuring Talon yourself, you describe what you want and your agent runs the skill — pointing back at the wiki when there's more to read.

## Who this is for

- People with repetitive strain injury (RSI) or other mobility constraints looking for hands-free ways to use a computer
- Anyone who wants voice-powered automations, from simple keyboard shortcuts to multi-step workflows

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

Tested with [Claude Code](https://claude.com/claude-code) and the [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview). Should work with any agent that loads project-local skills — if your agent reads from a different folder (e.g. `.agents/skills/`), swap the destination path below to match.

Clone this repo and copy the skill folders into `.claude/skills`:

```bash
mkdir -p .claude/skills && \
tmpdir="$(mktemp -d)" && \
git clone --single-branch --depth 1 https://github.com/RebeccaStevenson/voice-kit.git "$tmpdir/voice-kit" && \
cp -R "$tmpdir/voice-kit"/talon-* "$tmpdir/voice-kit"/superwhisper-assistant .claude/skills/ && \
rm -rf "$tmpdir"
```

This copies the actual skill directories into `.claude/skills` so the agent sees each skill as a direct child directory with its own `SKILL.md`.

Then add a short note to your `CLAUDE.md` telling the agent to use these skills for Talon Voice and SuperWhisper tasks. For example:

```md
## Voice-Kit skills

Use the skills in `.claude/skills/` for Talon Voice and SuperWhisper tasks:
- `talon-start`
- `talon-setup-talon`
- `talon-setup-rango`
- `talon-setup-cursorless`
- `talon-create-custom-repo`
- `talon-create-command`
- `talon-customize-settings`
- `talon-test-and-debug`
- `superwhisper-assistant`
```

After installing, restart your agent so it reloads the skill list.

## Quickstart

These skills give your coding agent (Claude Code, etc.) the know-how to set up and customize Talon and SuperWhisper on your machine. After installing the skills, ask the agent for help in plain language — for example:

> "Help me install Talon on my Mac."

The agent picks up the `talon-setup-talon` skill and walks you through downloading Talon, configuring your mic, and adding a starter set of voice commands. Every request in the table above triggers a skill the same way — describe the goal and the right skill activates.

## Voice control skills

The wiki is the source of truth — when a skill points you at further reading, it links to the wiki rather than paraphrasing.

| Skill | What it does | Example request |
|---|---|---|
| [talon-start/](talon-start/) | Creates a user profile so later Talon help can match the user’s experience level. | "Set up the Talon assistant for me." |
| [talon-setup-talon/](talon-setup-talon/) | Walks a beginner through installing Talon, enabling speech recognition, and cloning the community repo. | "Help me get Talon running from scratch." |
| [talon-setup-rango/](talon-setup-rango/) | Adds Rango so the browser can be controlled by voice. | "Set up browser voice control with Rango." |
| [talon-create-custom-repo/](talon-create-custom-repo/) | Creates a personal Talon repo so custom commands stay separate from upstream repos. | "Set up my own Talon commands folder." |
| [talon-create-command/](talon-create-command/) | Creates `.talon` commands and Python-backed actions — from simple keyboard shortcuts to actions with logic. | "Make a command that pastes my email signature." |
| [talon-customize-settings/](talon-customize-settings/) | Edits vocabulary, words to replace, websites, search engines, subtitles, system paths, speech timeout, and alphabet/modifier alternates. | "Add 'PubMed' to my vocabulary and bump the speech timeout." |
| [talon-test-and-debug/](talon-test-and-debug/) | Checks logs, REPL output, and tests so broken commands can be diagnosed quickly. | "This command loads but never triggers. Debug it." |
| [talon-setup-cursorless/](talon-setup-cursorless/) | Installs Cursorless for hat-and-target-style voice editing in VSCode (and Cursor / VSCodium). | "Set up Cursorless so I can edit code by voice." |

## SuperWhisper skills

| Skill | What it does | Example request |
|---|---|---|
| [superwhisper-assistant/](superwhisper-assistant/) | Installs SuperWhisper, configures models, and creates or edits custom mode JSON files. | "Create a SuperWhisper mode for editing emails." |

## Resource links

See [resource-links.md](resource-links.md) for a more complete list of tools and resources that I use
