---
name: start
description: >
  Initialize the Talon voice assistant and create a user profile. This should
  be the FIRST skill new users run — before setup-talon or any other skill.
  Use when the user says "set up the assistant", "start", "initialize",
  "create my profile", "get started", or is using the Talon voice assistant
  plugin for the first time.
---

# Start — Talon Voice Assistant Setup

Initialize the assistant by discovering the user's environment and interviewing
them about their experience level. This creates a persistent profile that all
other skills read to adapt their explanations and tone.

Local workspace note: in Becky's environment, AI agents usually start in `~/.talon/`, but Talon-managed repos and profiles still live under `~/.talon/user/`.

## Instructions

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
ls ~/.talon/user/<user_repo>/.talon-assistant/
```

If `.talon-assistant/profile.md` already exists, read it, greet the user by
name, and show a brief status summary instead of re-running the interview.
Then stop — setup is already done.

### 2. Create the Directory

```bash
mkdir -p ~/.talon/user/<user_repo>/.talon-assistant
```

### 3. Run the Proficiency Interview

Use **AskUserQuestion** to gather the user's background. Ask all questions in
a single call so the user only has to answer once.

**Question 1 — Talon experience:**

> How much experience do you have with Talon voice control?

- **Beginner** — Just installed or still learning the basics (alphabet, basic navigation)
- **Intermediate** — Comfortable with everyday commands; have customized some things
- **Advanced** — Write my own commands regularly; familiar with the Talon API, contexts, and modules

**Question 2 — Coding experience:**

> How comfortable are you with programming / writing code?

- **None** — I don't code
- **Basic** — I can read simple scripts and make small edits
- **Comfortable** — I write code regularly in at least one language
- **Experienced** — Coding is a major part of my work

**Question 3 — Git experience:**

> How familiar are you with Git (version control)?

- **None** — I don't know what Git is
- **Basic** — I know clone, pull, and commit
- **Comfortable** — I use branches, PRs, and resolve conflicts

Also ask for their **name** (so the assistant can greet them in future
sessions) using a simple text question, or infer it from the conversation if
already known.

**Note on Git:** This plugin always uses Git for cloning repos and tracking
changes locally. A **GitHub account is not required** — Git works entirely on
the user's machine. If the user's Git experience is "None", the assistant
will explain every Git command before running it and offer to run commands on
the user's behalf. If Git is not installed, help the user install it (on
macOS: typing `git` in Terminal prompts Xcode Command Line Tools).

### 4. Write the Profile (DO NOT SKIP)

Once the interview answers are in, immediately write the profile file — don't
defer this or say "I'll create it later." Use the Write tool right now to
create `~/.talon/user/<user_repo>/.talon-assistant/profile.md`:

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

## Preferences
<!-- Add user preferences as they come up in conversation -->
```

### 5. Create the Memory File (DO NOT SKIP)

Immediately after the profile, also write the memory file. Use the Write tool
to create `~/.talon/user/<user_repo>/.talon-assistant/memory.md`:

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

### 6. Confirm Setup (DO NOT SKIP)

After both files are written, show the user a confirmation summary. This is
the last thing the user sees — make it clear and complete:

```
All set, <name>! Here's your profile:

- **Talon:** <level>  —  **Coding:** <level>  —  **Git:** <level>
- **Custom repo:** <user_repo>
- **Profile saved to:** ~/.talon/user/<user_repo>/.talon-assistant/profile.md

Other skills will now adapt their explanations to your experience level.
You can update your profile any time by saying "update my profile" or by
editing the file directly.
```

This plugin also includes an interactive training page for practicing the
alphabet, spelling, numbers, symbols, and formatters in the browser. Let the
user know they can ask to "open the training page" anytime to try it.

### Recommended Learning Path

After the profile is set up, suggest this order for the other skills:

1. **setup-talon** — Install Talon and the community command set
2. **create-custom-repo** — Set up your personal commands folder
3. **create-basic-command** — Write your first voice commands
4. **create-python-command** — Build commands with programming logic
5. **test-and-debug** — Verify commands work and troubleshoot issues
6. **setup-rango** (optional) — Add hands-free browser control

You don't have to do them all at once — feel free to jump ahead if you want
to try something specific. But this order works well because each skill
builds on what the previous one taught you.

Then ask: "Would you like to continue with installing Talon and the community
commands?" If yes, invoke the **setup-talon** skill — it will read the
profile you just created and adapt accordingly.

---

## How Other Skills Use the Profile

Every skill in this plugin should, as an early step:

1. Read `~/.talon/user/<user_repo>/.talon-assistant/profile.md`
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
