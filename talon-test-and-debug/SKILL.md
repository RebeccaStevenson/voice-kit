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

> Based on the [Talon Community Wiki](https://talon.wiki/). See
> [Troubleshooting](https://talon.wiki/Resource%20Hub/Speech%20Recognition/troubleshooting)
> and [Basic Customization](https://talon.wiki/Customization/basic_customization)
> for log interpretation and debugging tips.

**Note:** This skill is often invoked automatically after creating commands via the **talon-create-command** skill. When invoked that way, you already know which files were just created/edited — jump straight into the relevant checklist steps rather than asking the user what to test.

**Prerequisite:** Requires Claude Code (not Cowork) for REPL, log, and pytest
access. Use absolute paths for all operations:
- REPL: `$HOME/.talon/bin/repl`
- Log: `$HOME/.talon/talon.log`
- User repos: `$HOME/.talon/user/`

Claude Code can be launched from any directory — do not ask the user to
relaunch.

## Bootstrap (FIRST STEP)

Run the shared bootstrap to discover `<user_repo>` and load the proficiency
profile:

```bash
cat ~/.claude/skills/talon-create-command/references/bootstrap.md
```

If invoked automatically by **talon-create-command**, the bootstrap has
already run — skip it and jump to the relevant checklist step using the
files that were just created.

## Diagnose First, Ask Second

When the user says something "doesn't work" or "nothing happened", **do not
immediately ask them to describe the failure**. Since Claude Code has direct
access to the log and REPL, run the diagnostic steps yourself first:

1. Check the log for errors (`tail -n 100 ~/.talon/talon.log`)
2. Run `sim("the command phrase")` via the REPL
3. If the command has Python, run `actions.find("the_action_name")`

Only ask the user for more information if the automated checks come back
clean and you need context about what they observed (e.g., "the command
routes correctly in sim() — does it work when you actually say it?").

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

If no stubs exist yet, copy the minimal template into the user repo:

```bash
mkdir -p ~/.talon/user/<user_repo>/tests/stubs/talon
cp ~/.claude/skills/talon-test-and-debug/references/test-stubs-template.py \
   ~/.talon/user/<user_repo>/tests/stubs/talon/__init__.py
```

The template covers `Module`, `Context`, `actions`, `app`, and `clip`. Add
mocks for additional Talon APIs only as the tests need them.

#### Running Tests

```bash
cd ~/.talon/user/<user_repo> && python -m pytest tests/ -v
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
| `sim("phrase")` | Show which rule handles a phrase (read-only) |
| `mimic("phrase")` | Actually execute the command — see warning below |
| `actions.find("keyword")` | Search actions by name, shows source code |
| `actions.list("user.prefix")` | List all actions with a prefix |
| `events.tail()` | Live stream of all Talon events |
| `registry.commands` | All commands active in current context |
| `registry.lists` | All active lists and their contents |
| `settings.list()` | All available settings |

### `mimic()` Warning

`mimic("phrase")` runs the command **for real, in the currently focused
app** — exactly as if the user had spoken it. That means:

- It can trigger destructive actions (delete file, close window, send
  message, run shell commands) with no undo.
- The REPL is not the focused app, so the command fires wherever focus
  *actually* is — often not where you expect.
- Context-gated commands resolve against the focused app's context, not
  the one you had in mind when typing.

Default to `sim()` for routing checks. Reach for `mimic()` only when (a)
you've already verified the route with `sim()`, (b) the command is safe
to actually execute, and (c) you control which app is focused (e.g., via
a `time.sleep()` + manual switch).

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
