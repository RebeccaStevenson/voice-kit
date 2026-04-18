---
name: talon-create-custom-repo
description: >
  Create a personal repository for custom Talon voice commands, separate
  from the community repo. Use when the user asks to "create a custom
  commands folder", "set up my own Talon repo", "make a personal command
  repository", "organize my custom commands", or wants to start writing
  their own Talon commands for the first time.
---

# Create a Personal Talon Command Repository

Guide the user through creating their own command repository that sits alongside the community repo inside `~/.talon/user/`. This is the recommended approach (Option B) for managing custom commands — it keeps upstream repos untouched so updates pull cleanly.

> Based on the [Talon Community Wiki](https://talon.wiki/). See
> [Basic Customization](https://talon.wiki/Customization/basic_customization)
> for how Talon auto-loads files from `user/`.

**Prerequisite:** Requires Claude Code (not Cowork) for filesystem and git
access. Use absolute paths (`$HOME/.talon/user/...`) for all file operations
and commands. Claude Code can be launched from any directory — do not ask the
user to relaunch.

<!-- SYNC: This "Discover Repo & Load Profile" block is shared with
     talon-create-basic-command, talon-create-python-command, and talon-setup-rango.
     Keep all four copies in sync when editing. -->

## Discover Repo & Load Profile (FIRST STEP — do both before anything else)

Before creating a new repo, check whether the user already has one and whether a profile exists.

1. **Check for an existing custom repo.** List `~/.talon/user/` and look for a folder that is NOT `community`, `rango-talon`, `cursorless-talon`, `parrot`, or any other well-known shared repo.

   ```bash
   ls ~/.talon/user/
   ```

   If a personal repo already exists, let the user know — they may not need this skill at all. If they want to start fresh or rename it, continue below.

2. **Load the profile** (if it exists):

   ```bash
   cat ~/.talon/talon-assistant/profile.md
   ```

   If the file exists, adapt your explanations for the rest of this session:
   - **Beginner (Talon):** Explain what each folder and file is for. Walk through terminal commands step by step.
   - **Intermediate (Talon):** Brief explanations; focus on the structure.
   - **Advanced (Talon):** Be concise — just show the commands.
   - **None / Basic (Coding):** Avoid jargon; explain Git and terminal concepts used.
   - **None (Git):** Explain every Git command before running it. Offer to run them for the user.

   If no profile exists, offer to run setup quickly: "I don't see a profile
   yet — would you like me to set one up real quick? It's just a few
   questions and helps me tailor my explanations. Or we can skip it and keep
   going." If the user says yes, invoke **talon-start** — and when it
   finishes, resume this skill automatically (don't make the user re-invoke
   the slash command). If they decline, default to beginner-level
   explanations to be safe.

## Why a Separate Repo?

Explain to the user in plain language:
- The `community/` folder receives updates from the Talon community. Editing files inside it creates merge conflicts when updating.
- A personal folder lets you add, change, and experiment freely without breaking anything.
- Talon automatically loads `.talon` and `.py` files from any subfolder inside `~/.talon/user/` — no configuration needed.

## Step 1: Choose a Name

Ask the user what they'd like to name their custom commands folder using AskUserQuestion. Suggest a pattern like `talon_<firstname>` or `my_talon`. The name should be:
- Lowercase with hyphens (e.g., `talon-alex`)
- Different from existing folders (`community`, `rango-talon`, `cursorless-talon`)

## Step 2: Create the Directory Structure

Once the user picks a name, provide the terminal commands. Use `REPO_NAME` as a placeholder for their chosen name:

```bash
# Create the repo and basic structure (using absolute paths)
mkdir -p "$HOME/.talon/user/REPO_NAME"/{apps,core,tags,productivity,settings,tests,docs}

# Initialize a git repository
cd "$HOME/.talon/user/REPO_NAME" && git init
```

Explain what each folder is for:
- **`apps/`**: Commands that only apply to specific applications (e.g., Chrome, VS Code, Finder)
- **`core/`**: Core behavior overrides, text/editing utilities, window management
- **`tags/`**: Tag-based commands (e.g., browser-related, editor-related commands)
- **`productivity/`**: Workflow tools and productivity commands (e.g., daily notes, project helpers)
- **`settings/`**: CSV files for custom word lists, websites, search engines
- **`tests/`**: Pytest tests for Python helpers
- **`docs/`**: Notes and documentation for personal reference

## Step 3: Create Essential Files

### .gitignore

```
__pycache__/
*.pyc
.DS_Store
system_paths-*.talon-list
```

The `system_paths-*.talon-list` pattern is important — these files contain local machine paths and should not be committed to a shared repo.

### A starter .talon file

Create a simple `hello.talon` as a first command to confirm everything works:

```talon
# My first custom command
hello talon:
    app.notify("It works!", "Your custom commands are loaded.")
```

Tell the user to save the file, then say **"hello talon"**. A notification should appear confirming the command loaded.

### pyproject.toml (for testing)

```toml
[tool.pytest.ini_options]
pythonpath = ["tests/stubs"]
testpaths = ["tests"]
```

## Step 4: Create Initial Commit

```bash
cd "$HOME/.talon/user/REPO_NAME" && git add . && git commit -m "initial setup: directory structure and starter command"
```

## Step 5: Optional — Back Up to GitHub

This step is **entirely optional** — Git works locally without a GitHub account.
Only offer this if the user wants cloud backup or to share their commands.

If the user wants to back up their commands remotely:

```bash
# Create a repo on GitHub first (can be private), then:
git remote add origin git@github.com:USERNAME/REPO_NAME.git
git push -u origin main
```

## Best Practices

Share these with the user:

1. **One command per file is fine to start** — don't worry about organization until you have many commands.
2. **Use object-verb phrasing** like `file save` instead of `save file` to match community conventions and avoid naming conflicts.
3. **Check the log after saving** — right-click Talon icon > Scripting > View Log, or say `talon open log`. A `[+]` line means the file loaded; `ERROR` means something needs fixing.
4. **Keep upstream repos read-only** — never edit files in `community/`, `rango-talon/`, or other upstream folders for personal customizations.
5. **Back up before big changes** — a quick `git commit` before experimenting saves headaches.

## Adding Commands Later

After initial setup, point the user to the **talon-create-basic-command** or **talon-create-python-command** skills for guidance on writing new commands. The talon-test-and-debug skill covers how to verify commands work correctly.
