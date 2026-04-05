---
name: talon-create-python-command
description: >
  Create Talon voice commands with Python scripting for advanced logic.
  Use when the user asks to "create a Python command", "add Python to
  a Talon command", "write a Talon action in Python", "make a command
  with logic", "register a custom action", or needs commands that go
  beyond simple key presses — such as file operations, string
  manipulation, API calls, or conditional behavior.
---

# Creating Python-Scripted Talon Commands

Guide the user through combining `.talon` and `.py` files to build commands with real programming logic. Assume the user has basic Talon setup complete and a personal commands folder. No prior Python experience is assumed — explain each concept.

**Prerequisite:** Requires Claude Code (not Cowork) for filesystem and REPL
access. Use absolute paths (`$HOME/.talon/user/...`, `$HOME/.talon/bin/repl`)
for all file operations and commands. Claude Code can be launched from any
directory — do not ask the user to relaunch.

<!-- SYNC: This "Discover Repo & Load Profile" block is shared with
     talon-create-basic-command, talon-create-custom-repo, and talon-setup-rango.
     Keep all four copies in sync when editing. -->

## Discover Repo & Load Profile (FIRST STEP — do both before anything else)

1. **Find the user's custom repo.** List `~/.talon/user/` and identify the folder that is NOT `community`, `rango-talon`, `cursorless-talon`, `parrot`, or any other well-known shared repo. The remaining folder is the user's personal repo (e.g., `talon-rebecca`, `talon-john`, `my-commands`, etc.).

   ```bash
   ls ~/.talon/user/
   ```

   Store this name and use it everywhere this skill says `<user_repo>`. If you can't determine the repo name, ask the user: "What's the name of your personal Talon commands folder?"

2. **Load the profile.** Immediately after discovering the repo, read the profile:

   ```bash
   cat ~/.talon/talon-assistant/profile.md
   ```

   If the file exists, adapt your explanations for the rest of this session:
   - **Beginner (Talon):** Explain what `.talon` and `.py` files are, how they connect, what decorators and actions mean — step by step.
   - **Intermediate (Talon):** Skip basics; explain module/context patterns and less-common API features.
   - **Advanced (Talon):** Be concise — show the code with brief design notes.
   - **None / Basic (Coding):** Avoid terms like "decorator", "class", "import" without explaining them. Walk through each line of Python.
   - **Comfortable+ (Coding):** Use standard programming terminology freely.
   - **None (Git):** Don't include Git commands without explaining them.

   If no profile exists, offer to run setup quickly: "I don't see a profile
   yet — would you like me to set one up real quick? It's just a few
   questions and helps me tailor my explanations. Or we can skip it and keep
   going." If the user says yes, invoke **talon-start** — and when it
   finishes, resume this skill automatically (don't make the user re-invoke
   the slash command). If they decline, default to beginner-level
   explanations to be safe.

<!-- SYNC: This "Search Before Creating" block is shared with
     talon-create-basic-command. Keep both copies in sync when editing. -->

## Search Before Creating (MANDATORY)

Before writing ANY new command or action, you MUST thoroughly search the existing repositories for commands, actions, and patterns that already accomplish the goal or that should be reused.

### How to Search

1. **Search the community repo** (`~/.talon/user/community/`) — use `Grep` and `Glob` to look for:
   - Existing voice commands with similar phrases (search `.talon` files)
   - Existing Python actions that do what the user wants (search `.py` files for `def ` + action names, `@mod.action_class`, `@ctx.action_class`)
   - Existing helper functions, modules, tags, or lists that you can reuse or extend
   - Patterns for how the community structures similar features (module naming, context matching, etc.)
2. **Search the user's custom repo** (`~/.talon/user/<user_repo>/`) — same approach, to avoid duplicating actions already created.
3. **Search broadly** — try multiple keywords and synonyms. Look for both the action name and what it does. For example, if creating a "paste matching style" action, search for `paste`, `style`, `match`, `plain`, `edit.paste`, etc.

### How to Report Findings

ALWAYS present your search results using this exact format before proceeding:

> **Searched:** community ✓ / <user_repo> ✓ (and any other repos the user mentioned, e.g., cursorless-talon ✓)
> **Existing commands found:** (list any, or "none")
> **Reusable actions found:** (list any, or "none")
> **Recommendation:** call existing / extend / create new

Explicitly name every repo you checked so the user can see at a glance that you searched everywhere. Then briefly describe what you found — any existing actions that fully or partially accomplish the goal, and any reusable patterns, helper functions, or modules that should be leveraged.

Prefer calling community actions (e.g., `actions.user.*`, `actions.edit.*`) over reimplementing with raw key presses — actions respect context overrides across apps.

**If an existing command or action already does what the user wants, stop there.** Tell the user it exists, show them the voice phrase, and do NOT create a duplicate. Only offer to create something new if they want to customize or extend the existing behavior.

## File Placement

### Prefer Existing Files

Before creating new `.talon` or `.py` files, search `<user_repo>/` for existing files whose topic or feature area matches the new commands/actions. Here, "related" means conceptual fit — the file covers the same app, feature area, or command family — not Talon's technical context header.

**For `.talon` files — add to an existing file when:**
- The new spoken rules clearly belong to the same topic or command group (e.g., adding a new Chrome shortcut to an existing `chrome_custom.talon` that already holds Chrome shortcuts).
- The existing file would remain coherent and easy to scan after the addition.

**For `.py` files — add to an existing file when:**
- The new actions or logic are part of the same feature or command family as the existing code (e.g., adding a new text-manipulation action to an existing `text_utils.py`).
- The existing module would remain clear and navigable after the addition.

**Create new files when:**
- No existing file covers the topic, or the closest file covers a different enough area that adding to it would make it less coherent.
- The new commands/actions form a distinct feature area (e.g., a new "daily notes" workflow that doesn't belong in any current file).
- The new Python logic is substantial enough that folding it into an existing module would make that module harder to navigate.
- The existing file is already large and adding more would hurt readability.

When adding to an existing file, place new rules/actions in a logical position (grouped with related items, not just appended to the end) and add a brief comment if the grouping isn't obvious.

### Directory Structure (for new files)

When you do need to create new files, place them in `<user_repo>/` using a structure that mirrors the community repo:

| File type | Where to put it | Example path |
|---|---|---|
| App-specific commands + actions | `<user_repo>/apps/<app_name>/` | `apps/vscode/vscode_snippets.py` |
| Core behavior overrides | `<user_repo>/core/` | `core/edit_extensions.py` |
| Text/editing utilities | `<user_repo>/core/` | `core/text_utils.py` |
| Tag-based commands | `<user_repo>/tags/` | `tags/browser_helpers.py` |
| Productivity / workflow tools | `<user_repo>/productivity/` | `productivity/daily_notes.py` |
| Navigation / window management | `<user_repo>/core/` | `core/window_helpers.py` |

**Never place files directly at the `<user_repo>/` root.** Always use a subfolder — pick the closest category from the table above. Keep the `.talon` and `.py` files for a feature side by side in the same directory. When overriding a community action with a context-specific implementation, check where the original lives in `community/` and mirror that path in `<user_repo>/`.

## When to Use Python

Explain to the user that basic commands (keyboard shortcuts, typing text) need only `.talon` files. Python is for when you need:
- **Logic**: if/else decisions, loops, calculations
- **Data**: reading files, clipboard manipulation, string formatting
- **System interaction**: running shell commands, OS-level operations
- **Reusable behavior**: shared helper functions used by multiple commands

## The Pattern: .talon + .py Side by Side

The standard pattern is two files in the same folder:

```
talon-yourname/
├── my_feature.talon    # Defines the voice commands (what you say)
└── my_feature.py       # Implements the actions (what happens)
```

Talon connects them through **actions** — the `.py` file declares actions, and the `.talon` file calls them.

## Step-by-Step: A Complete Example

### 1. The Python File (my_feature.py)

```python
from talon import Module, actions

# Create a module to register your actions
mod = Module()

@mod.action_class
class Actions:
    def greet_user(name: str) -> str:
        """Greet a user by name and insert the greeting."""
        greeting = f"Hello, {name}! Welcome."
        actions.insert(greeting)
        return greeting

    def count_words() -> int:
        """Count words in the selected text and show the result."""
        # Get the currently selected text
        text = actions.edit.selected_text()
        count = len(text.split())
        actions.app.notify("Word Count", f"{count} words selected")
        return count
```

Explain each part:
- **`from talon import Module, actions`** — imports Talon's API
- **`mod = Module()`** — creates a module that registers your actions with Talon
- **`@mod.action_class`** — decorator that tells Talon "these are voice-callable actions"
- **Type annotations** (`name: str`, `-> str`) — required by Talon for all action parameters and return values
- **Docstrings** (`"""..."""`) — required by Talon; describes what the action does

### 2. The Talon File (my_feature.talon)

```talon
# Pair this with my_feature.py

greet <user.text>:
    user.greet_user(user.text)

count words:
    user.count_words()
```

The `user.` prefix is how Talon knows to look for actions registered by user modules.

## Python File Structure Rules

Present these clearly:

1. **Every action needs a docstring** — Talon will error without one:
   ```python
   def my_action(arg: str):
       """This docstring is required."""
       # ...
   ```

2. **Every parameter needs a type annotation**:
   ```python
   # Good
   def process(text: str, count: int) -> None:

   # Bad — will cause an error
   def process(text, count):
   ```

3. **Return types must be annotated** (use `-> None` if nothing is returned):
   ```python
   def show_message(msg: str) -> None:
       """Display a notification."""
       actions.app.notify("Info", msg)
   ```

4. **One `@mod.action_class` per file** is the simplest pattern. You can have multiple, but start with one.

## Common Talon Python APIs

| API | What it does | Example |
|---|---|---|
| `actions.insert(text)` | Type text at cursor | `actions.insert("hello")` |
| `actions.key(keys)` | Press key combo | `actions.key("cmd-s")` |
| `actions.edit.selected_text()` | Get selected text | `text = actions.edit.selected_text()` |
| `clip.text()` | Get clipboard text | `from talon import clip; content = clip.text()` |
| `clip.set_text(s)` | Set clipboard text | `clip.set_text("copied")` |
| `actions.app.notify(title, body)` | Show notification | `actions.app.notify("Done", "Saved")` |
| `actions.sleep(duration)` | Pause execution | `actions.sleep("100ms")` |

## Using Context for App-Specific Overrides

To make an action behave differently depending on the active app, use a Context:

```python
from talon import Module, Context, actions

mod = Module()
ctx = Context()

# Default implementation
@mod.action_class
class Actions:
    def save_project():
        """Save the current project."""
        actions.key("cmd-s")

# VS Code override
ctx_vscode = Context()
ctx_vscode.matches = r"""
app.bundle: com.microsoft.VSCode
"""

@ctx_vscode.action_class("user")
class VSCodeActions:
    def save_project():
        """Save all files in VS Code."""
        actions.key("cmd-alt-s")  # Save All in VS Code
```

## Working with Files and the OS

For commands that interact with the filesystem:

```python
import os
from pathlib import Path
from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
    def open_notes_folder():
        """Open the user's notes folder in Finder."""
        notes_path = Path.home() / "Documents" / "Notes"
        notes_path.mkdir(exist_ok=True)
        os.system(f'open "{notes_path}"')

    def create_daily_note():
        """Create a timestamped daily note file."""
        from datetime import date
        notes_path = Path.home() / "Documents" / "Notes"
        notes_path.mkdir(exist_ok=True)
        today = date.today().isoformat()
        note_file = notes_path / f"{today}.md"
        note_file.write_text(f"# Notes for {today}\n\n")
        actions.app.notify("Note Created", str(note_file))
```

## Using Talon's Cron for Timers

```python
from talon import cron, Module

mod = Module()
timer_job = None

@mod.action_class
class Actions:
    def start_break_timer():
        """Start a 25-minute focus timer."""
        global timer_job
        timer_job = cron.after("25m", _notify_break)

    def cancel_timer():
        """Cancel the running timer."""
        global timer_job
        if timer_job:
            cron.cancel(timer_job)
            timer_job = None

def _notify_break():
    from talon import app
    app.notify("Break Time", "Take a 5-minute break!")
```

## Verify List and Data Dependencies Before Writing

If your command or `.talon` file uses a `{user.*}` list (e.g.,
`{user.system_paths}`, `{user.website}`), **check that the backing list file
exists** before writing the command. Don't tell the user to wait for it to
be auto-generated — create a starter file so the command works immediately.

```bash
# Check if the list file exists anywhere in the Talon user directory
find ~/.talon/user/ -name "system_paths*" -type f
```

If missing, create one in the user's custom repo. Example for system_paths:

```
# ~/.talon/user/<user_repo>/settings/system_paths-<hostname>.talon-list
list: user.system_paths
-
desktop: ~/Desktop
documents: ~/Documents
downloads: ~/Downloads
```

Get the hostname via `hostname`. Tell the user how to add their own entries.
The `system_paths-*` pattern is gitignored by convention.

## After Writing the Command — AUTO-INVOKE test-and-debug (MANDATORY)

After creating or editing any Python-backed command, you MUST **automatically
invoke the talon-test-and-debug skill** — do not ask the user whether to
test, do not skip this step, do not just run sim() yourself. Python commands
always get the full testing checklist because they have more failure modes
than pure `.talon` files (import errors, type mismatches, runtime exceptions,
action registration issues).

The test-and-debug skill will:

1. **Check the log** for import errors or `ActionProtoError`
2. **Verify action registration** via `actions.find()`
3. **Verify voice routing** via `sim()`
4. **Run pytest** for any non-trivial logic

Invoke it immediately after writing the files — before presenting the
output summary to the user. If tests reveal issues, fix them before
reporting success.

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
- `path/to/test_file.py` (created / edited)

This format helps the user quickly see what they can say and where the files live.

## Best Practices

- Keep Python functions focused — one action, one job.
- Use `actions.user.*` (not direct key presses) when calling other community actions so context overrides work.
- Reuse existing community actions and helpers wherever possible instead of reimplementing from scratch.
- Format code with `black` for consistency.
- Write pytest tests for any non-trivial logic (see the **talon-test-and-debug** skill).
