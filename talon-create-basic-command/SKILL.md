---
name: talon-create-basic-command
description: >
  Create new Talon voice commands using .talon files. Use when the user asks
  to "create a voice command", "add a new command", "make a Talon command",
  "write a talon file", "add a keyboard shortcut", "map a voice command",
  or wants to define spoken phrases that trigger actions on their computer.
---

# Creating Basic Talon Voice Commands

Guide the user through writing `.talon` files to define voice commands. Assume the user has Talon and the community repo installed, and has a personal commands folder (if not, point them to the **talon-setup-talon** and **talon-create-custom-repo** skills first).

Local workspace note: in Becky's environment, AI agents usually start in `~/.talon/`, but Talon-managed repos and profiles still live under `~/.talon/user/`.

<!-- SYNC: This "Discover Repo & Load Profile" block is shared with
     talon-create-python-command, talon-create-custom-repo, and talon-setup-rango.
     Keep all four copies in sync when editing. -->

## Discover Repo & Load Profile (FIRST STEP — do both before anything else)

1. **Find the user's custom repo.** List `~/.talon/user/` and identify the folder that is NOT `community`, `rango-talon`, `cursorless-talon`, `parrot`, or any other well-known shared repo. The remaining folder is the user's personal repo (e.g., `talon-rebecca`, `talon-john`, `my-commands`, etc.).

   ```bash
   ls ~/.talon/user/
   ```

   Store this name and use it everywhere this skill says `<user_repo>`. If you can't determine the repo name, ask the user: "What's the name of your personal Talon commands folder?"

2. **Load the profile.** Immediately after discovering the repo, read the profile:

   ```bash
   cat ~/.talon/user/<user_repo>/.talon-assistant/profile.md
   ```

   If the file exists, adapt your explanations for the rest of this session:
   - **Beginner (Talon):** Explain what `.talon` files are, what context headers do, and walk through syntax step by step.
   - **Intermediate (Talon):** Skip basic syntax explanations; still explain non-obvious patterns.
   - **Advanced (Talon):** Be concise — show the code with brief design notes.
   - **None / Basic (Coding):** Avoid jargon; explain any concepts used.
   - **None (Git):** Don't include Git commands without explaining them.

   If no profile exists, mention: "I don't see a profile yet — you can run the **talon-start** skill to set one up, but we can keep going for now." Then default to intermediate-level explanations.

<!-- SYNC: This "Search Before Creating" block is shared with
     talon-create-python-command. Keep both copies in sync when editing. -->

## Search Before Creating (MANDATORY)

Before writing ANY new command, you MUST thoroughly search the existing repositories for commands, actions, and patterns that already accomplish the goal or that should be reused.

### How to Search

1. **Search the community repo** (`~/.talon/user/community/`) — use `Grep` and `Glob` to look for:
   - Existing voice commands with similar phrases (search `.talon` files for the key verbs/nouns)
   - Existing actions that do what the user wants (search `.py` files for action class definitions)
   - Existing tags or contexts that relate to the target app
   - Patterns for how similar commands are structured (e.g., how community handles app-specific overrides)
2. **Search the user's custom repo** (`~/.talon/user/<user_repo>/`) — same approach, to avoid duplicating commands already created.
3. **Search broadly** — try multiple keywords and synonyms. If the user wants "close tab", search for `close`, `tab`, the app name, the bundle ID, related actions like `app.tab_close()`, etc.

### How to Report Findings

ALWAYS present your search results using this exact format before proceeding:

> **Searched:** community ✓ / <user_repo> ✓
> **Existing commands found:** (list any, or "none")
> **Reusable actions found:** (list any, or "none")
> **Recommendation:** reuse / extend / create new

Explicitly name both repos so the user can see at a glance that you checked everywhere. Then briefly describe what you found — any existing commands that fully or partially accomplish the goal, and any reusable actions (e.g., `user.some_action()`, `edit.some_action()`, `app.tab_close()`) that should be called instead of raw key presses.

**If an existing command already does what the user wants, stop there.** Tell the user the command exists, show them the voice phrase, and do NOT create a duplicate. Only offer to create something new if they want to customize or extend the existing behavior.

## Gathering Requirements

Before writing any file, ask the user with AskUserQuestion:

1. **What should the voice command do?** (e.g., press a keyboard shortcut, type text, open an app)
2. **Should it work everywhere or only in a specific app?** (e.g., only in Chrome, only in VS Code)
3. **What phrase should trigger it?** Suggest object-verb phrasing (e.g., `file save` not `save file`).

## File Placement

### Prefer Existing Files

Before creating a new `.talon` file, search `<user_repo>/` for an existing file whose topic or command group matches the new commands. Here, "related" means conceptual fit — the file covers the same app, feature area, or command family — not Talon's technical context header.

**Add to an existing `.talon` file when:**
- The new spoken rules clearly belong to the same topic or command group (e.g., adding a new Chrome shortcut to an existing `chrome_custom.talon` that already holds Chrome shortcuts).
- The existing file would remain coherent and easy to scan after the addition.

**Create a new `.talon` file when:**
- No existing file covers the topic, or the closest file covers a different enough area that adding to it would make it less coherent.
- The new commands form a distinct feature area (e.g., a new "daily notes" workflow that doesn't belong in any current file).
- The existing file is already large and adding more commands would make it harder to navigate.

When adding to an existing file, place the new rules in a logical position (grouped with related commands, not just appended to the end) and add a brief comment if the grouping isn't obvious.

### Directory Structure (for new files)

When you do need to create a new file, place it in `<user_repo>/` using a structure that mirrors the community repo:

| Command type | Where to put it | Example path |
|---|---|---|
| App-specific commands | `<user_repo>/apps/<app_name>/` | `apps/vscode/vscode_custom.talon` |
| Core behavior overrides | `<user_repo>/core/` | `core/edit_custom.talon` |
| Text/editing utilities | `<user_repo>/core/` | `core/text_utils.talon` |
| Tag-based commands | `<user_repo>/tags/` | `tags/browser_custom.talon` |
| Productivity / workflow tools | `<user_repo>/productivity/` | `productivity/daily_notes.talon` |
| Navigation / window management | `<user_repo>/core/` | `core/window_custom.talon` |

**Never place files directly at the `<user_repo>/` root.** Always use a subfolder. When overriding or extending a community command, check the community repo's file structure first and mirror it. For example, if you're overriding a VS Code command that lives in `community/apps/vscode/`, put your override in `<user_repo>/apps/vscode/`. This makes it obvious what you're customizing.

If the community has no precedent for where a command should go, pick the closest category from the table above.

## Writing the .talon File

### Global Commands (Work Everywhere)

If the command should work in any application, write a `.talon` file with no context header:

```talon
# filename: my_command.talon

my command phrase:
    key(cmd-a)
```

### App-Specific Commands

If the command should only work in a specific application, add a context header above the `---` separator. Use `app.bundle` on macOS for precision:

```talon
# filename: apps/chrome_custom.talon
app.bundle: com.google.Chrome
-

bookmark page:
    key(cmd-d)
```

Common macOS bundle identifiers:
- Chrome: `com.google.Chrome`
- Safari: `com.apple.Safari`
- VS Code: `com.microsoft.VSCode`
- Finder: `com.apple.finder`
- Terminal: `com.apple.Terminal`
- iTerm2: `com.googlecode.iterm2`

To find any app's bundle ID, the user can run:
```bash
osascript -e 'id of app "App Name"'
```

### Title-Based Context

For web apps or specific pages, use a title regex:

```talon
title: /Gmail/
-

archive message:
    key(e)
```

## Command Syntax Rules

Explain these rules clearly:

1. **Spoken phrase** followed by a colon, then the action(s) indented below:
   ```talon
   spoken phrase:
       action_one()
       action_two()
   ```

2. **Single-line shorthand** for simple commands:
   ```talon
   spoken phrase: key(cmd-s)
   ```

3. **Separate commands with blank lines**:
   ```talon
   save file:
       key(cmd-s)

   close file:
       key(cmd-w)
   ```

4. **Comments** start with `#` on their own line:
   ```talon
   # This command selects all text
   select everything:
       key(cmd-a)
   ```

5. **Indent with spaces** (4 spaces recommended, but any consistent amount works).

## Prefer Named Actions Over Raw Key Presses

Whenever a built-in or community action exists for what you want to do, call the action instead of a raw `key()` press. Actions respect context overrides across apps — a raw key press doesn't.

For example, instead of `key(cmd-t)` to open a new tab, use `app.tab_open()` if it exists. Instead of `key(cmd-c)`, use `edit.copy()`. Search the community repo for available actions before falling back to `key()`.

Common built-in actions to prefer:

| Action | Instead of | What it does |
|---|---|---|
| `edit.copy()` | `key(cmd-c)` | Copy selection |
| `edit.paste()` | `key(cmd-v)` | Paste clipboard |
| `edit.save()` | `key(cmd-s)` | Save file |
| `edit.undo()` | `key(cmd-z)` | Undo |
| `edit.find()` | `key(cmd-f)` | Open find dialog |
| `app.tab_open()` | `key(cmd-t)` | Open new tab |
| `app.tab_close()` | `key(cmd-w)` | Close current tab |
| `app.tab_next()` | `key(cmd-shift-])` | Next tab |
| `app.tab_previous()` | `key(cmd-shift-[)` | Previous tab |

Use `key()` only when no named action exists for the behavior you need.

## Other Common Actions

| Action | What it does | Example |
|---|---|---|
| `key(cmd-s)` | Press a keyboard shortcut | `key(cmd-shift-p)` |
| `insert("text")` | Type out text | `insert("Hello world")` |
| `sleep(100ms)` | Pause briefly | Useful between keystrokes |
| `mouse_click(0)` | Left click | `mouse_click(1)` for right-click |
| `app.notify("title")` | Show a notification | Full form: `app.notify(title, subtitle, body, sound)` |

### Key Modifiers

| Modifier | Mac key |
|---|---|
| `cmd` | Command |
| `ctrl` | Control |
| `alt` | Option |
| `shift` | Shift |
| `super` | Command (alias) |

Combine with hyphens: `key(cmd-shift-alt-p)`

## Using Captures and Lists

For commands that accept variable input, use angle brackets for captures:

```talon
# Numbers
go to line <number>:
    edit.jump_line(number)

# Free-form text
search for <user.text>:
    key(cmd-f)
    sleep(100ms)
    insert(user.text)

# Selecting from a list
open {user.website}:
    user.open_url(user.website)
```

See `references/syntax-guide.md` for the full list of available captures and lists.

## Overriding Existing Commands

To change an existing community command without editing upstream files, create a new `.talon` file with a **more specific** context header:

```talon
os: mac
-
# Override the default "touch" command to skip closing the grid
touch:
    mouse_click(0)
    user.mouse_drag_end()
```

A context with more rules (e.g., adding `os: mac` or `mode: command`) takes precedence over one with fewer rules.

## After Writing the Command (MANDATORY)

After creating or editing any command, you MUST verify it registers correctly. At minimum, use `sim()` via the REPL to confirm Talon recognizes the voice phrase:

```bash
echo 'sim("your command phrase")' | ~/.talon/bin/repl
```

If the command is backed by Python actions, also verify the action registered:

```bash
echo 'actions.find("your_action_name")' | ~/.talon/bin/repl
```

For **complex commands** (multi-file changes, Python logic, file operations, context overrides), invoke the full **talon-test-and-debug** skill to run the complete testing checklist including pytest where applicable.

For **simple commands** (single `.talon` rule with a key press or insert), the `sim()` check plus a log check is sufficient.

## Output Format

When you are done creating or editing commands, ALWAYS format your response as follows:

### Commands summary

Use a bulleted list with the voice phrase bolded and the resulting action described:

- **"voice phrase here"** — Description of what it does
- **"another phrase"** — Description of what it does

### Files

List every file you created or edited:

- `path/to/file.talon` (created / edited)
- `path/to/file.py` (created / edited)

This format helps the user quickly see what they can say and where the files live.
