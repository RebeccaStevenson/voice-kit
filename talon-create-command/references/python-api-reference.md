# Talon Python API Reference

## Core Imports

```python
from talon import Module, Context, actions, app, ui, clip, cron, scope, settings
```

## Module — Registering Actions

```python
mod = Module()

# Declare an action class
@mod.action_class
class Actions:
    def my_action(param: str) -> str:
        """Docstring is required."""
        return param.upper()
```

### Declaring Tags

```python
mod = Module()
mod.tag("my_feature", desc="Enable my feature commands")
```

### Declaring Lists

```python
mod = Module()
mod.list("my_items", desc="A list of items")
```

### Declaring Settings

```python
mod = Module()
mod.setting("my_setting", type=str, default="value", desc="Description")
```

## Context — Conditional Behavior

```python
ctx = Context()

# Match specific apps
ctx.matches = r"""
app.bundle: com.microsoft.VSCode
"""

# Override actions for this context
@ctx.action_class("user")
class ContextActions:
    def my_action(param: str) -> str:
        """VS Code specific version."""
        return f"[VSCode] {param}"

# Populate lists dynamically
ctx.lists["user.my_items"] = {"spoken form": "value", "another": "value2"}
```

### Extending an action without replacing it

Use `actions.next()` to run the next-most-specific implementation from
inside an override. This is the right pattern when you want to add
behavior around a community action rather than replace it:

```python
ctx = Context()
ctx.matches = "app: Emacs"

@ctx.action_class("edit")
class EditActions:
    def save():
        actions.user.maybe_format_buffer()
        actions.next()  # falls through to the default edit.save()
```

`actions.next()` is also useful for conditional overrides — return early
without calling it to fully replace, or call it at the end to chain.

### Picking the namespace for `@ctx.action_class`

| Namespace | Use for |
|---|---|
| `"user"` | Overriding actions you (or community) declared with `@mod.action_class` |
| `"edit"` | Overriding built-in `edit.*` actions (copy, paste, save, jump_line, ...) |
| `"app"` | Overriding `app.*` actions (tab_open, notify, ...) |
| `"code"` | Overriding language-feature actions used by community voice-coding tags |

## Actions — Calling Existing Actions

```python
from talon import actions

# Built-in actions
actions.insert("text")                    # Type text
actions.key("cmd-s")                      # Press keys
actions.sleep("100ms")                    # Pause

# Edit actions
actions.edit.selected_text()              # Get selection
actions.edit.copy()                       # Copy
actions.edit.paste()                      # Paste
actions.edit.cut()                        # Cut
actions.edit.undo()                       # Undo
actions.edit.redo()                       # Redo
actions.edit.select_all()                 # Select all
actions.edit.find()                       # Open find dialog
actions.edit.jump_line(number)            # Go to line

# App actions
actions.app.notify("title", "body")       # Show notification
actions.app.tab_open()                    # New tab
actions.app.tab_close()                   # Close tab
actions.app.tab_next()                    # Next tab
actions.app.tab_previous()                # Previous tab
```

## Clipboard — clip

```python
from talon import clip

text = clip.text()                        # Get clipboard text
clip.set_text("new content")              # Set clipboard text

# Clipboard context manager (preserves previous clipboard)
with clip.revert():
    actions.edit.copy()
    text = clip.text()
    # Original clipboard restored when block exits
```

## UI — Window Information

```python
from talon import ui

win = ui.active_window()
print(win.title)                          # Window title
print(win.app.name)                       # App name
print(win.app.bundle)                     # Bundle ID (macOS)

# List all running apps
for app_instance in ui.apps():
    print(app_instance.name, app_instance.bundle)
```

## App — Notifications and Platform

```python
from talon import app

# Full signature: app.notify(title, subtitle, body, sound)
# Only title is required; the rest are optional
app.notify("Title")                       # Title only
app.notify("Title", "Subtitle")           # Title + subtitle
app.notify("Title", "", "Body text")      # Title + body (empty subtitle)
print(app.platform)                       # "mac", "windows", or "linux"
```

## Cron — Timers

```python
from talon import cron

# One-shot timer
job = cron.after("5m", my_callback)

# Repeating timer
job = cron.interval("30s", my_callback)

# Cancel
cron.cancel(job)
```

## Settings — Reading Values

```python
from talon import settings

value = settings.get("user.my_setting")
```

## Scope — Checking State

```python
from talon import scope

mode = scope.get("mode", "")
language = scope.get("language", "")
```

## Type Annotations Cheat Sheet

| Python type | Use for |
|---|---|
| `str` | Text, file paths |
| `int` | Whole numbers |
| `float` | Decimal numbers |
| `bool` | True/False |
| `list` | Sequences |
| `dict` | Key-value mappings |
| `None` (in `-> None`) | Actions that don't return a value |
| `Optional[str]` | String or None |

## Common Patterns

### Clipboard-based text manipulation

```python
@mod.action_class
class Actions:
    def uppercase_selection():
        """Convert selected text to uppercase."""
        with clip.revert():
            actions.edit.copy()
            actions.sleep("50ms")
            text = clip.text()
            if text:
                clip.set_text(text.upper())
                actions.edit.paste()
```

### Running shell commands

```python
import subprocess

@mod.action_class
class Actions:
    def git_status():
        """Show git status notification."""
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True, text=True, cwd=str(Path.home())
        )
        actions.app.notify("Git Status", result.stdout or "Clean")
```

### Platform-aware behavior

```python
from talon import app

@mod.action_class
class Actions:
    def open_terminal():
        """Open the system terminal."""
        if app.platform == "mac":
            os.system("open -a Terminal")
        elif app.platform == "linux":
            os.system("gnome-terminal &")
```
