---
name: talon-start
description: >
  Initialize the Talon voice assistant and create a user profile. This should
  be the FIRST skill new users run — before talon-setup-talon or any other skill.
  Use when the user says "set up the assistant", "start", "initialize",
  "create my profile", "get started", or is using the Talon voice assistant
  plugin for the first time.
---

# Start — Talon Voice Assistant Setup

Initialize the assistant by discovering the user's environment and interviewing
them about their experience level. This creates a persistent profile that all
other skills read to adapt their explanations and tone.

**Prerequisite:** Requires Claude Code (not Cowork). Step 0 ensures
`~/.talon/` exists and resolves its absolute path — Claude Code can be
launched from any directory.

## Important: Designed for Claude Code

This skill (and all voice-kit skills) is designed for **Claude Code** — the
CLI / desktop app that runs directly on the user's machine. It will NOT work
correctly in Claude Cowork or any sandboxed environment, because the skills
need direct filesystem access to `~/.talon/` and the Talon REPL at
`~/.talon/bin/repl`.

## Instructions

### 0. Ensure ~/.talon/ Exists (do this before anything else)

All Talon files live under `~/.talon/`. Before proceeding, make sure it
exists and resolve its absolute path for use in all later commands:

```bash
TALON_HOME="$HOME/.talon"
mkdir -p "$TALON_HOME"
echo "$TALON_HOME"
```

Store this absolute path (e.g., `/Users/alex/.talon`) and use it as a prefix
for **every file operation and command** in this skill. Do not rely on the
current working directory — Claude Code may have been launched from anywhere.

**Use absolute paths everywhere.** For example:
- `$TALON_HOME/user/` instead of `user/` or `~/.talon/user/`
- `$TALON_HOME/bin/repl` for the REPL
- `$TALON_HOME/talon.log` for the log

If Claude Code was launched outside `~/.talon/`, briefly note:
> "You started Claude outside `~/.talon/`, so I'll use absolute paths to
> access your Talon setup — everything will work fine."

Then continue — do **not** ask the user to restart or relaunch.

### 1. Check What Exists

Look for an existing profile and memory directory. The profile lives inside
the user's personal Talon repo:

```bash
ls ~/.talon/user/
```

Identify the user's custom repo (the folder that is NOT `community`,
`rango-talon`, `cursorless-talon`, `parrot`, or any other well-known shared
repo). Then check for:

```bash
ls ~/.talon/talon-assistant/
```

If `talon-assistant/profile.md` already exists, read it, greet the user by
name, and show a brief status summary instead of re-running the interview.
Then stop — setup is already done.

### 2. Create the Directory

```bash
mkdir -p ~/.talon/talon-assistant
```

### 3. Run the Proficiency Interview

Gather the user's background in **one message, not four**. Present all
questions together so the user answers once. If you already know some answers
(e.g., their name from git config, or info mentioned in conversation),
pre-fill those and only ask what's missing.

Use **AskUserQuestion** with a single prompt like this:

> I need a few quick details to set up your profile. You can answer all at
> once or one at a time:
>
> 1. **Your name** (what should I call you?)
> 2. **Talon experience:** Beginner / Intermediate / Advanced
> 3. **Coding experience:** None / Basic / Comfortable / Experienced
> 4. **Git experience:** None / Basic / Comfortable
> 5. **Learning depth** — How much do you want to learn about how Talon
>    actually works (its file structure, syntax, and the engine behind the
>    scenes)?
>    - **Just make it work** — Give me working commands; I don't need to know how the sausage is made
>    - **Brief context** — A sentence or two about what's happening under the hood is nice, but keep it short
>    - **Teach me as we go** — Explain the syntax and structure as it comes up naturally while we build things
>    - **Deep dive** — I want to really understand how Talon works — show me the internals, the file anatomy, the API

Provide brief descriptions only if the user asks for clarification:
- Talon Beginner = just installed or learning basics; Intermediate = use daily, customized some things; Advanced = write own commands, know the API
- Coding None = don't code; Basic = can read/edit simple scripts; Comfortable = write code regularly; Experienced = coding is core to my work
- Git None = don't know what it is; Basic = know clone/pull/commit; Comfortable = branches, PRs, conflicts

**Pre-fill what you can:** Check `git config user.name` and
`git config user.email` for the user's name. If you find it, say "I see your
name is \<name\> from your computer's settings — should I use that?" rather
than making them type it.

**Note on Git:** This plugin always uses Git for cloning repos and tracking
changes locally. A **GitHub account is not required** — Git works entirely on
the user's machine. If the user's Git experience is "None", the assistant
will explain every Git command before running it and offer to run commands on
the user's behalf. If Git is not installed, help the user install it (on
macOS: typing `git` in Terminal prompts Xcode Command Line Tools).

### 4. Write the Profile (DO NOT SKIP)

Once the interview answers are in, immediately write the profile file — don't
defer this or say "I'll create it later." Use the Write tool right now to
create `~/.talon/talon-assistant/profile.md`:

```markdown
# Talon Assistant Profile

## User
- **Name:** <name>
- **Custom repo:** <user_repo>
- **Created:** <today's date>

## Proficiency
| Area | Level |
|------|-------|
| Talon | beginner / intermediate / advanced |
| Coding | none / basic / comfortable / experienced |
| Git | none / basic / comfortable |
| Learning depth | just-make-it-work / brief-context / teach-me / deep-dive |

## Preferences
<!-- Add user preferences as they come up in conversation -->

## Setup Progress
| Step | Status | Date |
|------|--------|------|
| Install Talon | — | |
| Community commands | — | |
| Personal repo | — | |
| Personalize: vocabulary | — | |
| Personalize: words to replace | — | |
| Personalize: websites | — | |
| Personalize: search engines | — | |
| Personalize: subtitles | — | |
| Personalize: system paths | — | |
| Rango | — | |
| Learn the basics | — | |
```

### 5. Create the Memory File (DO NOT SKIP)

Immediately after the profile, also write the memory file. Use the Write tool
to create `~/.talon/talon-assistant/memory.md`:

```markdown
# Talon Assistant Memory

Persistent context that the assistant learns over time.

## Terms
| Term | Meaning |
|------|---------|
<!-- Filled in as the user mentions custom terms, project names, etc. -->

## Custom Commands Created
| Voice phrase | File | Date |
|-------------|------|------|
<!-- Updated each time a command is created -->

## Notes
<!-- Anything else worth remembering across sessions -->
```

### 6. Create the CLAUDE.md (DO NOT SKIP)

Immediately after the memory file, write a `CLAUDE.md` to the assistant
directory so that **every future agent session** has the context it needs
without re-reading every skill file. Use the Write tool to create
`~/.talon/talon-assistant/CLAUDE.md`:

````markdown
# Talon Voice Assistant — Agent Context

> Auto-generated by the **talon-start** skill on <today's date>.
> Edit freely — this file is the agent's primary briefing for this plugin.

## User Profile

- **Name:** <name>
- **Custom repo:** <user_repo>
- **Proficiency:** Talon <level> · Coding <level> · Git <level> · Learning depth <level>
- **Profile file:** `~/.talon/talon-assistant/profile.md`
- **Memory file:** `~/.talon/talon-assistant/memory.md`

## Environment

- **OS:** macOS (do not generate cross-platform variants unless asked)
- **Talon user directory:** `~/.talon/user/`
- **Custom scripts go in:** `~/.talon/user/<user_repo>/` — never in upstream repos
- **Upstream repos (read-only):** community, rango-talon, cursorless-talon, parrot, talon-ai-tools
- **Talon log:** `~/.talon/talon.log`
- **Talon REPL:** `~/.talon/bin/repl`
- **Talon auto-reloads** `.talon` and `.py` files on save — no restart needed
- **Speech engine:** Conformer (enabled via Talon menu bar → Speech Recognition)

## Command Naming Convention

Use **object-verb** phrasing: `file save`, `browser refresh`, `tab close`.
This matches the community convention and avoids collisions with upstream
commands.

## Available Skills

### talon-start
**Purpose:** Create the user profile and initialize the assistant.
**When to use:** First-time setup, or when the user says "update my profile."
**Creates:** `talon-assistant/profile.md`, `talon-assistant/memory.md`,
`talon-assistant/CLAUDE.md` (this file).

### talon-setup-talon
**Purpose:** Step-by-step Talon installation, community command setup, and
personalization walkthrough.
**When to use:** User needs to install Talon, enable the speech engine,
clone the community repo, or personalize settings. Also handles resume —
reads the `## Setup Progress` table in `profile.md` and picks up where
the user left off.
**Prerequisite:** Profile must exist (run **talon-start** first).
**Reference doc:** `references/troubleshooting.md` — startup issues, mic
problems, permissions, common log errors.

### talon-customize-settings
**Purpose:** Add or update Talon settings — vocabulary, words to replace,
websites, search engines, subtitles, and system paths.
**When to use:** User wants to modify settings after initial setup. For
example: "add a word to vocabulary", "Talon keeps misspelling a name",
"add a website", "change subtitle size." Not for creating voice commands.
**Prerequisite:** Personal repo must exist.

### talon-create-custom-repo
**Purpose:** Create a personal commands folder alongside the community repo.
**When to use:** User wants to start writing custom commands but doesn't have
a personal repo yet.
**Prerequisite:** Talon and community must be installed.
**Creates:** Directory structure (`apps/`, `core/`, `tags/`, `productivity/`,
`settings/`, `tests/`, `tests/stubs/`, `docs/`), `.gitignore`,
`pyproject.toml`, starter `.talon` file; initializes git.
**Reference doc:** `references/directory-layout.md`

### talon-create-basic-command
**Purpose:** Write `.talon` files for voice commands — keyboard shortcuts,
text insertion, app-specific actions.
**When to use:** User wants a new voice command that doesn't require
programming logic.
**Mandatory rules:**
1. **Search before creating** — always search both the community and user
   repos for existing commands first. Report: `Searched: community ✓ /
   <user_repo> ✓`
2. **Prefer named actions** over raw key presses (`edit.copy()` not
   `key(cmd-c)`)
3. **Verify with sim()** after writing the command
**File placement:** Mirror community structure — `apps/`, `core/`, `tags/`,
`productivity/`.
**Reference doc:** `references/syntax-guide.md` — context matchers, captures,
lists, key names, settings, tags.

### talon-create-python-command
**Purpose:** Combine `.talon` + `.py` files for commands that need real
programming logic (if/else, loops, file I/O, clipboard, APIs).
**When to use:** The command needs conditional logic, data processing,
reusable helper functions, or system interaction.
**Mandatory rules:**
1. **Search before creating** — same as talon-create-basic-command
2. **Type annotations and docstrings** required on every action
3. **Always invoke talon-test-and-debug** after writing Python commands
**Key Talon Python APIs:** `Module`, `Context`, `actions`, `clip`,
`app.notify()`, `cron`, `ui`, `scope`.
**Reference doc:** `references/python-api-reference.md` — full API reference,
common patterns, type annotations cheat sheet.

### talon-test-and-debug
**Purpose:** Structured 5-step testing checklist to verify commands and
diagnose failures.
**When to use:** After creating any command (mandatory for Python), or when a
command doesn't work.
**The 5 steps:**
1. Check `~/.talon/talon.log` for load errors
2. Verify action registration with `actions.find()`
3. Test voice routing with `sim()`
4. Run `pytest` for non-trivial Python logic
5. Live voice test in the target app
**Test infrastructure:** Tests go in `<user_repo>/tests/`; Talon API stubs
live in `<user_repo>/tests/stubs/talon/`.
**Reference doc:** `references/common-errors.md` — .talon errors, .py errors,
context issues, log interpretation.

### talon-setup-rango
**Purpose:** Install the Rango browser extension for hands-free web browsing.
**When to use:** User wants to click links, fill forms, scroll, or manage
tabs by voice in the browser.
**Prerequisite:** Talon and community must be installed.
**Key concepts:** Hint labels (say `air` to click element A), direct vs
explicit clicking mode, tab markers, saved references.
**Supported browsers:** Chrome, Brave, Edge, Vivaldi, Opera, Firefox, Safari.
**Reference doc:** `references/rango-commands.md` — complete command reference
grouped by category.

## Cross-Cutting Rules (All Skills Must Follow)

1. **Read the profile first** — adapt tone and detail level to the user's
   Talon / Coding / Git proficiency.
2. **Search before creating** — both command-creation skills must search
   existing repos to avoid duplicating commands that already exist.
3. **Test after creating** — Python commands always go through the full
   5-step talon-test-and-debug checklist.
4. **Never edit upstream repos** — all custom work belongs in `<user_repo>/`.
5. **Update memory.md** — after creating commands, log them in
   `talon-assistant/memory.md` (voice phrase, file path, date).
6. **Same quality for all levels** — proficiency only changes explanation
   depth and tone, never the quality of commands or file structure.

## Proficiency Adaptation Quick Reference

| Level | Behavior |
|-------|----------|
| Talon beginner | Explain syntax, walk through step-by-step, spell out what each command does |
| Talon intermediate | Skip basics, explain non-obvious patterns (contexts, tags, modules) |
| Talon advanced | Show code with brief notes on design choices |
| Coding none/basic | Avoid jargon, explain Python concepts in plain language |
| Coding comfortable+ | Use standard programming terminology freely |
| Git none | Explain every git command, offer to run them for the user |
| Git basic+ | Include git commands normally |
| Learning: just-make-it-work | Don't explain file structure, syntax rules, or how Talon processes commands — just produce working files |
| Learning: brief-context | Add a sentence or two about *what* a file or syntax element does, but no deep explanation |
| Learning: teach-me | When introducing new syntax or file types, explain the structure and why it works that way, woven into the workflow |
| Learning: deep-dive | Proactively teach Talon internals — file anatomy, context matching, action resolution, module/tag system — even when the user hasn't asked |

## Skill Dependency Order

```
talon-start → talon-setup-talon → talon-create-custom-repo → talon-create-basic-command
                                          → talon-create-python-command → talon-test-and-debug
                                          → talon-setup-rango (optional)
                                          → talon-customize-settings (ongoing)
```

Each skill builds on the previous. Users can skip ahead, but this order
avoids missing prerequisites.

## Training Resource

An interactive browser-based training page is bundled with this plugin
(alphabet, spelling, numbers, symbols, formatters). The user can ask to
"open the training page" anytime.

## Git and GitHub

Git is always used for cloning repos and local version control. A **GitHub
account is never required**. Pushing to GitHub is presented as optional.
When the user's Git level is "None", explain every command and offer to run
it for them.
````

**Adapt the template:** Fill in all `<placeholder>` values from the interview
answers and environment discovery. If you found additional repos when listing
`~/.talon/user/`, include them in the upstream repos list. If the user
mentioned any custom terms or tools during the interview, seed the Terms
table in `memory.md` with those.

---

### 7. Confirm Setup (DO NOT SKIP)

After all three files are written, show the user a confirmation summary. This
is the last thing the user sees — make it clear and complete:

```
All set, <name>! Here's your profile:

- **Talon:** <level>  —  **Coding:** <level>  —  **Git:** <level>  —  **Learning depth:** <level>
- **Custom repo:** <user_repo>
- **Profile saved to:** ~/.talon/talon-assistant/

Three files were created:
  • profile.md — your proficiency levels and preferences
  • memory.md — tracks terms and commands across sessions
  • CLAUDE.md — gives the assistant context about this plugin's skills

Other skills will now adapt their explanations to your experience level.
You can update your profile any time by saying "update my profile" or by
editing any of these files directly.
```

This plugin also includes an interactive training page for practicing the
alphabet, spelling, numbers, symbols, and formatters in the browser. Let the
user know they can ask to "open the training page" anytime to try it.

### Recommended Learning Path

After the profile is set up, suggest this order for the other skills:

1. **talon-setup-talon** — Install Talon and the community command set
2. **talon-create-custom-repo** — Set up your personal commands folder
3. **talon-create-basic-command** — Write your first voice commands
4. **talon-create-python-command** — Build commands with programming logic
5. **talon-test-and-debug** — Verify commands work and troubleshoot issues
6. **talon-setup-rango** (optional) — Add hands-free browser control
7. **talon-customize-settings** (ongoing) — Update vocabulary, websites, and other settings anytime

You don't have to do them all at once — feel free to jump ahead if you want
to try something specific. But this order works well because each skill
builds on what the previous one taught you.

### Resume Interrupted Flow

If the user was in the middle of another skill (e.g., `create-basic-command`)
and pivoted to `/start` to create their profile, **don't just suggest the
learning path** — acknowledge what they were doing and offer to resume it
automatically. For example: "You were creating a voice command before we
set up your profile — would you like to continue with that?" If yes,
invoke the appropriate skill directly rather than making the user re-type
the slash command.

If this is a fresh session with no prior context, then suggest the standard
learning path and ask: "Would you like to continue with installing Talon and
the community commands?" If yes, invoke the **talon-setup-talon** skill —
it will read the profile you just created and adapt accordingly.

---

## How Other Skills Use the Profile

Every skill in this plugin should, as an early step:

1. Read `~/.talon/talon-assistant/profile.md`
2. Adapt **tone and detail level** based on what it finds:

| Proficiency | How to adapt |
|------------|--------------|
| **Beginner (Talon)** | Explain what `.talon` files are, what context headers do, walk through syntax step by step. Spell out what each voice command will do. |
| **Intermediate (Talon)** | Skip basic syntax explanations. Still explain non-obvious patterns (contexts, tags, modules). |
| **Advanced (Talon)** | Be concise. Just show the code with brief notes on design choices. |
| **None / Basic (Coding)** | Avoid jargon like "decorator", "class", "import". Explain any Python concepts used. |
| **Comfortable+ (Coding)** | Use standard programming terminology freely. |
| **None (Git)** | Never include Git commands in your instructions without explaining them. Offer to run them for the user. |
| **Basic+ (Git)** | Include Git commands normally. |
| **Just make it work (Learning)** | Produce working files without explaining Talon's structure or syntax rules. |
| **Brief context (Learning)** | Add a line or two about what a syntax element or file does — enough for orientation, not a lesson. |
| **Teach me (Learning)** | Explain syntax, file structure, and how Talon processes commands as they come up naturally in the workflow. |
| **Deep dive (Learning)** | Proactively teach Talon internals — context matching, action resolution, the module/tag system, file anatomy — even when the user didn't explicitly ask. |

### Git and GitHub

This plugin always uses Git (for cloning repos and local version control).
A **GitHub account is never required**. Pushing to GitHub is always presented
as optional — useful for backups, but not necessary.

When the user's Git level is "None":
- Explain every Git command before running it
- Offer to run Git commands for the user
- Never assume they know what clone, commit, or push mean

**Important:** All adaptations only affect explanation depth and tone.
Every proficiency level gets the same quality commands and the same file
structure. Never skip testing or search steps because of a user's level.

---

## Updating the Profile

If the user says "update my profile", "change my level", or similar:

1. Read the existing profile
2. Ask which field(s) to change (or let them specify directly)
3. Update the file
4. Confirm the change
