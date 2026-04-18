---
name: talon-create-command
description: >
  Create new Talon voice commands. Use when the user asks to "create a
  voice command", "add a new command", "make a Talon command", "write a
  talon file", "add a keyboard shortcut", "map a voice command", "create
  a Python command", "add Python to a Talon command", "write a Talon
  action", "make a command with logic", or wants to define spoken phrases
  that trigger actions on their computer. Handles both simple .talon-only
  commands and Python-scripted commands with logic.
---

# Creating Talon Voice Commands

Guide the user through creating voice commands — from simple keyboard
shortcuts to Python-scripted actions with logic. Assume the user has
Talon and the community repo installed, and has a personal commands folder
(if not, point them to **talon-setup-talon** and **talon-create-custom-repo**
first).

> Based on the [Talon Community Wiki](https://talon.wiki/). Key
> references: [Talon Files](https://talon.wiki/Customization/talon-files),
> [Basic Customization](https://talon.wiki/Customization/basic_customization),
> [Actions](https://talon.wiki/Customization/Talon%20Framework/actions),
> [Modules & Contexts](https://talon.wiki/Customization/Talon%20Framework/modules_and_contexts),
> [Talon Lists](https://talon.wiki/Customization/talon_lists).

**Prerequisite:** Requires Claude Code (not Cowork) for filesystem and REPL
access. Use absolute paths (`$HOME/.talon/user/...`, `$HOME/.talon/bin/repl`)
for all file operations and commands. Claude Code can be launched from any
directory — do not ask the user to relaunch.

## Discover Repo & Load Profile (FIRST STEP)

1. **Find the user's custom repo.** List `~/.talon/user/` and identify the
   folder that is NOT `community`, `rango-talon`, `cursorless-talon`,
   `parrot`, or any other well-known shared repo.

   ```bash
   ls ~/.talon/user/
   ```

   Store this name as `<user_repo>`. If unclear, ask the user.

2. **Load the profile:**

   ```bash
   cat ~/.talon/talon-assistant/profile.md
   ```

   Adapt explanations to the user's proficiency:
   - **Beginner (Talon):** Explain syntax step by step.
   - **Intermediate:** Skip basics, explain non-obvious patterns.
   - **Advanced:** Show code with brief design notes.
   - **None / Basic (Coding):** Avoid jargon; explain Python concepts.
   - **Comfortable+ (Coding):** Use standard terminology.

   If no profile exists, offer to run **talon-start** quickly, then resume
   this skill automatically.

## Search Before Creating (MANDATORY)

Before writing ANY new command, search existing repos thoroughly.

1. **Search community** (`~/.talon/user/community/`) — existing commands,
   actions, tags, contexts, and patterns for similar features.
2. **Search user repo** (`~/.talon/user/<user_repo>/`) — avoid duplicating
   existing custom commands.
3. **Search broadly** — multiple keywords, synonyms, action names.

**Always report findings:**

> **Searched:** community ✓ / <user_repo> ✓
> **Existing commands found:** (list any, or "none")
> **Reusable actions found:** (list any, or "none")
> **Recommendation:** reuse / extend / create new

**If an existing command already does what the user wants, stop there.**
Show them the voice phrase. Don't create a duplicate.

## Gathering Requirements

If the user already described what they want, **don't re-ask** — proceed
to searching and writing. Only ask when the request is ambiguous, and ask
in **one message**:

> I need a few details:
> 1. **What should it do?** (e.g., press a shortcut, type text, open an app)
> 2. **Where should it work?** Everywhere, or only in a specific app?
> 3. **What phrase triggers it?** (I'll suggest one if you're not sure)

Suggest object-verb phrasing (e.g., `file save` not `save file`).

## Does This Need Python?

Most commands only need a `.talon` file. Use Python only when the command
genuinely needs:
- **Logic**: if/else decisions, loops, calculations
- **Data**: reading files, clipboard manipulation, string formatting
- **System interaction**: running shell commands, OS-level operations
- **Reusable behavior**: shared helper functions used by multiple commands

If none of these apply, stay in `.talon` — especially for beginners, a
single file avoids the overhead of paired `.py` + `.talon` files.

If Python is needed, **don't ask the user** — just tell them "This one
needs a bit of Python" and proceed to the Python path below.

## File Placement

### Prefer Existing Files

Before creating a new file, search `<user_repo>/` for an existing file
whose topic or command group matches. Add to it when the new commands
clearly belong and the file stays coherent. Create a new file when no
existing file fits or when the new commands form a distinct feature area.

### Directory Structure (for new files)

| Command type | Where to put it | Example |
|---|---|---|
| App-specific | `<user_repo>/apps/<app>/` | `apps/vscode/vscode_custom.talon` |
| Core overrides | `<user_repo>/core/` | `core/edit_custom.talon` |
| Tag-based | `<user_repo>/tags/` | `tags/browser_custom.talon` |
| Productivity / workflow | `<user_repo>/productivity/` | `productivity/daily_notes.talon` |

**Never place files at the `<user_repo>/` root.** Mirror the community
structure when overriding or extending community commands. Keep `.talon`
and `.py` files for the same feature side by side.

## Path A: .talon-Only Commands

### Global Commands (Work Everywhere)

```talon
my command phrase:
    key(cmd-a)
```

### App-Specific Commands

Add a context header above the `---` separator:

```talon
app.bundle: com.google.Chrome
-

bookmark page:
    key(cmd-d)
```

Common macOS bundle IDs: Chrome (`com.google.Chrome`), Safari
(`com.apple.Safari`), VS Code (`com.microsoft.VSCode`), Finder
(`com.apple.finder`), Terminal (`com.apple.Terminal`), iTerm2
(`com.googlecode.iterm2`). Find any app's bundle ID with:
`osascript -e 'id of app "App Name"'`

### Title-Based Context

```talon
title: /Gmail/
-

archive message:
    key(e)
```

### Syntax Rules

1. Spoken phrase followed by colon, actions indented below (4 spaces)
2. Separate commands with blank lines
3. Comments start with `#` on their own line

### Prefer Named Actions Over Raw Key Presses

Call actions instead of raw `key()` when possible — actions respect
context overrides across apps.

| Action | Instead of | What it does |
|---|---|---|
| `edit.copy()` | `key(cmd-c)` | Copy selection |
| `edit.paste()` | `key(cmd-v)` | Paste clipboard |
| `edit.save()` | `key(cmd-s)` | Save file |
| `edit.undo()` | `key(cmd-z)` | Undo |
| `app.tab_open()` | `key(cmd-t)` | Open new tab |
| `app.tab_close()` | `key(cmd-w)` | Close current tab |

Use `key()` only when no named action exists.

### Other Common Actions

| Action | What it does |
|---|---|
| `key(cmd-s)` | Press a keyboard shortcut |
| `insert("text")` | Type out text |
| `sleep(100ms)` | Pause briefly |
| `app.notify("title")` | Show a notification |

Key modifiers: `cmd`, `ctrl`, `alt`, `shift`. Combine with hyphens:
`key(cmd-shift-alt-p)`

### Captures and Lists

For variable input:

```talon
go to line <number>:
    edit.jump_line(number)

search for <user.text>:
    key(cmd-f)
    sleep(100ms)
    insert(user.text)

open {user.website}:
    user.open_url(user.website)
```

See `references/syntax-guide.md` for the full list of captures and lists.

### Overriding Existing Commands

Create a `.talon` file with a more specific context header — more context
rules take precedence:

```talon
os: mac
-
touch:
    mouse_click(0)
    user.mouse_drag_end()
```

## Path B: Python-Scripted Commands

### The Pattern: .talon + .py Side by Side

```
<user_repo>/
├── my_feature.talon    # Voice commands (what you say)
└── my_feature.py       # Actions (what happens)
```

Talon connects them through **actions** — the `.py` file declares them,
the `.talon` file calls them.

### Complete Example

**my_feature.py:**
```python
from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
    def count_words() -> int:
        """Count words in the selected text and show the result."""
        text = actions.edit.selected_text()
        count = len(text.split())
        actions.app.notify("Word Count", f"{count} words selected")
        return count
```

**my_feature.talon:**
```talon
count words:
    user.count_words()
```

Explain each part for beginners:
- `Module()` registers actions with Talon
- `@mod.action_class` marks these as voice-callable
- Type annotations (`-> int`) and docstrings (`"""..."""`) are required
- `user.` prefix connects `.talon` to `.py`

### Python File Rules

1. **Every action needs a docstring** — Talon errors without one
2. **Every parameter needs a type annotation** — `def process(text: str)`
3. **Return types must be annotated** — use `-> None` if nothing returned
4. **One `@mod.action_class` per file** is simplest

### Common Talon Python APIs

| API | What it does |
|---|---|
| `actions.insert(text)` | Type text at cursor |
| `actions.key(keys)` | Press key combo |
| `actions.edit.selected_text()` | Get selected text |
| `clip.text()` / `clip.set_text(s)` | Get/set clipboard |
| `actions.app.notify(title, body)` | Show notification |
| `actions.sleep(duration)` | Pause execution |

For the full API reference including Context overrides, cron timers, and
file/OS operations, see `references/python-api-reference.md`.

## Verify List Dependencies Before Writing

If your command uses a `{user.*}` list, **check that the list file
exists** before writing the command:

```bash
find ~/.talon/user/ -name "system_paths*" -type f
```

If missing, create a starter list file so the command works immediately.

## After Writing the Command (MANDATORY)

### For .talon-only commands

Run these checks yourself — don't ask the user:

**Step 1: Check the log**
```bash
tail -n 50 ~/.talon/talon.log | grep -E "ERROR|WARNING"
```

**Step 2: Verify voice routing**
```bash
echo 'sim("your command phrase")' | ~/.talon/bin/repl
```

If `sim()` returns the expected rule, the command is working. These two
checks are sufficient for simple `.talon` commands.

### For Python-scripted commands

**Automatically invoke talon-test-and-debug** — do not ask, do not skip.
Python commands get the full testing checklist because they have more
failure modes (import errors, type mismatches, action registration). The
test-and-debug skill will check the log, verify action registration via
`actions.find()`, verify voice routing via `sim()`, and run pytest for
non-trivial logic.

Invoke it immediately after writing the files — before presenting the
output summary. Fix any issues before reporting success.

## Output Format

When done, ALWAYS format your response as:

### Commands summary

- **"voice phrase here"** — Description of what it does

### Files

- `path/to/file.talon` (created / edited)
- `path/to/file.py` (created / edited)
