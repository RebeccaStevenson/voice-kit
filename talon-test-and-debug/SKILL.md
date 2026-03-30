---
name: talon-test-and-debug
description: >
  Test and debug Talon voice commands using logs, the REPL, and pytest.
  Use when the user asks to "test my command", "debug a Talon command",
  "my command isn't working", "check if my action registered", "run
  Talon tests", "use the REPL", "check the Talon log", or encounters
  errors after creating or editing .talon or .py files.
---

# Testing and Debugging Talon Commands

Walk the user through a structured testing checklist. Follow these steps in order — each step catches a different class of problem, from syntax errors to runtime failures.

**Note:** This skill is often invoked automatically after creating commands via the **talon-create-basic-command** or **talon-create-python-command** skills. When invoked that way, you already know which files were just created/edited — jump straight into the relevant checklist steps rather than asking the user what to test.

Local workspace note: in Becky's environment, AI agents usually start in `~/.talon/`, but Talon-managed repos and profiles still live under `~/.talon/user/`.

## Read the User Profile

Before starting, discover the user's custom repo name (see the **talon-create-basic-command** skill for the full discovery step). Then check for a profile at `~/.talon/user/<user_repo>/.talon-assistant/profile.md`. If it exists, read it and adapt:

- **Beginner (Talon):** Explain what each testing step does and why. Walk through log output and REPL commands in detail.
- **Intermediate (Talon):** Brief explanations; focus on results.
- **Advanced (Talon):** Just show commands and results — skip the "why."
- **None / Basic (Coding):** Explain pytest concepts, what assertions mean, and how to read test output.
- **None (Git):** If debugging involves checking git status or diffs, explain the commands.

If no profile exists, default to intermediate-level explanations.

## The Testing Checklist

Present this as a clear numbered sequence. Work through each step with the user.

### Step 1: Confirm Files Loaded Without Errors

Talon auto-reloads whenever a `.talon` or `.py` file is saved. Check the log to see if the reload succeeded.

Tell the user to open the log:
- **By voice**: say `talon open log`
- **By menu**: right-click the Talon menu bar icon > Scripting > View Log

Then check the recent lines:

```bash
tail -n 100 ~/.talon/talon.log | grep -E "ERROR|WARNING|your_filename"
```

**What to look for:**
- `[+] /path/to/file.py` — file loaded successfully
- `[-] /path/to/file.py` — file was unloaded (normal before a reload)
- `ERROR` or `CompileError` — syntax error in a `.talon` file. The log shows the file path, line number, and what was expected.
- `ImportError` — a `.py` file has a missing import or typo
- `ActionProtoError` — an action's parameters don't match its declaration (missing type annotations or docstrings)

If there's an error, fix it before moving to Step 2. The error message always includes the file path and usually the line number.

### Step 2: Verify Action Registration (Python Commands)

Skip this step for pure `.talon` files with no Python. For commands backed by Python actions, confirm Talon registered the action:

```bash
# List all actions matching a prefix
echo 'actions.list("user.my_prefix")' | ~/.talon/bin/repl

# Search actions by keyword — shows full source code
echo 'actions.find("my_action")' | ~/.talon/bin/repl
```

`actions.find()` is especially useful — it prints every matching action with its full implementation, confirming Talon parsed the code correctly.

**If the action doesn't appear:**
- Check that the `.py` file uses `@mod.action_class` decorator
- Verify every action has a docstring and type annotations
- Look at the log again for import errors

### Step 3: Verify Voice Command Routing with sim()

`sim()` shows which `.talon` rule would handle a spoken phrase in the **current context**:

```bash
echo 'sim("your command phrase")' | ~/.talon/bin/repl
```

**Important context notes:**
- If the command has a context header (e.g., `app.bundle: com.google.Chrome`), `sim()` will only match it when that app is focused.
- To test context-gated commands, use a delay and switch to the target app:
  ```bash
  echo 'import time; time.sleep(5); sim("your command phrase")' | ~/.talon/bin/repl
  ```
  Then quickly switch to the target app within 5 seconds.

**If sim() doesn't match your command:**
- Double-check the spoken phrase is exact
- Verify the context header matches the current app
- Check for conflicting commands with the same phrase in other files

### Step 4: Test Python Logic with Pytest

For commands with non-trivial Python logic (file operations, string manipulation, calculations), write automated tests. This is more reliable than manual testing because:
- The REPL only supports simple single-line statements
- You can't easily import Talon user modules in the REPL
- Tests are repeatable and catch regressions

#### Setting Up Tests

Create a test file in your personal repo's `tests/` folder:

```python
# tests/test_my_feature.py

# Import your helper functions directly
from my_feature import _helper_function

def test_basic_behavior():
    result = _helper_function("input")
    assert result == "expected output"

def test_edge_case():
    result = _helper_function("")
    assert result is None
```

#### Talon Stubs for Testing

Since tests run outside Talon, you need stubs to mock Talon's APIs. If the user's repo has a `tests/stubs/` directory, explain that it already provides mocks for `actions`, `Module`, `Context`, `clip`, `app`, and `ui`.

If no stubs exist yet, help create a minimal stub:

```python
# tests/stubs/talon/__init__.py
class Module:
    def action_class(self, cls):
        return cls
    def tag(self, name, desc=""):
        pass
    def list(self, name, desc=""):
        pass
    def setting(self, name, **kwargs):
        pass

class Context:
    matches = ""
    lists = {}
    def action_class(self, path):
        def decorator(cls):
            return cls
        return decorator

class actions:
    @staticmethod
    def insert(text): pass
    @staticmethod
    def key(keys): pass
    @staticmethod
    def sleep(duration): pass
    class edit:
        @staticmethod
        def selected_text(): return ""
        @staticmethod
        def copy(): pass
        @staticmethod
        def paste(): pass
    class app:
        @staticmethod
        def notify(title, body=""): pass

class app:
    platform = "mac"
    notifications = []
    @staticmethod
    def notify(title, body=""):
        app.notifications.append((title, body))

class clip:
    _text = ""
    @staticmethod
    def text(): return clip._text
    @staticmethod
    def set_text(t): clip._text = t
```

#### Running Tests

```bash
cd ~/.talon && cd user/YOUR_REPO && python -m pytest tests/ -v
```

Quick filter by keyword:
```bash
python -m pytest tests/ -k "test_my_feature" -v
```

### Step 5: Live Voice Test

The final check — actually speak the command:

1. Focus the target application (if the command is app-specific)
2. Say the command phrase clearly
3. Verify the expected behavior occurred

**If the command doesn't trigger:**
- Say `help search <phrase>` to check if Talon recognizes the phrase
- Check the log for runtime errors: `tail -n 50 ~/.talon/talon.log`
- Use `sim()` with a sleep-and-switch to verify context matching

**If the command triggers but does the wrong thing:**
- Add `app.notify()` calls at key points in your Python code to trace execution
- Check the log for Python exceptions
- Test the Python logic in isolation with pytest

## REPL Quick Reference

| Command | What it does |
|---|---|
| `sim("phrase")` | Show which rule handles a phrase |
| `mimic("phrase")` | Actually execute a command (use carefully!) |
| `actions.find("keyword")` | Search actions by name, shows source code |
| `actions.list("user.prefix")` | List all actions with a prefix |
| `events.tail()` | Live stream of all Talon events |
| `registry.commands` | All commands active in current context |
| `registry.lists` | All active lists and their contents |
| `settings.list()` | All available settings |

### REPL Tips

- **Pipe single-liners**: `echo 'command' | ~/.talon/bin/repl` works reliably
- **Multi-line code**: Open the REPL interactively via `~/.talon/bin/repl` or Scripting > Console
- **Piped multi-line blocks** (`printf` with `\n`) may silently produce no output — use interactive mode instead

## Output Format

When testing is complete, ALWAYS format your results using this exact template. Copy the structure — don't paraphrase it into prose.

### Test results

```
- **Log check** — ✅ No errors on reload (or ❌ ERROR: <details>)
- **actions.find()** — ✅ `user.my_action` registered (or ❌ not found)
- **sim() check** — ✅ "voice phrase" → `file.talon` line N (or ❌ no match)
- **pytest** — ✅ 3/3 passing (or ❌ 2/3, failure in test_xyz)
```

Use ✅ for passed and ❌ for failed. If a step was skipped (e.g., pytest for a simple command), write "⏭️ skipped (simple command)".

If any step fails, state what went wrong and what needs to be fixed IMMEDIATELY — don't continue to the next step until it's resolved.

### Commands verified

Repeat the commands summary so the user knows what's ready to use:

- **"voice phrase"** — Description of what it does

### Files involved

- `path/to/file.talon`
- `path/to/file.py`

## Common Error Patterns

See `references/common-errors.md` for a table of frequent errors and their fixes.
