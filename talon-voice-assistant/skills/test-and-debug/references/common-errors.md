# Common Talon Errors and Fixes

## .talon File Errors

| Error | Cause | Fix |
|---|---|---|
| `CompileError: unexpected token` | Syntax error — missing parenthesis, bad indentation, etc. | Check the line number in the error. Common issues: missing `)` in `key()`, tabs instead of spaces, or a colon missing after the command phrase. |
| `CompileError: Expected: )` | Unclosed parenthesis in an action call | Add the missing `)` — e.g., `key(cmd-a` should be `key(cmd-a)` |
| `No matching action` | Calling an action that doesn't exist | Check spelling. Use `actions.find("name")` in the REPL to verify. For user actions, ensure the `.py` file loaded without errors. |
| Command doesn't trigger | Context header doesn't match | Verify with `sim("phrase")`. Check that `app.bundle`, `title`, or `mode` matches the current state. |
| Wrong command triggers | Another file has the same phrase with a broader context | Use `sim("phrase")` to see which file is matching. Make your context header more specific. |

## .py File Errors

| Error | Cause | Fix |
|---|---|---|
| `ActionProtoError` | Missing type annotations or docstring on an action | Add type hints to all parameters and return value. Add a docstring. |
| `ImportError: No module named 'talon'` | Running the file outside Talon (e.g., directly with `python`) | `.py` files in the user directory are loaded by Talon, not run directly. Use pytest with stubs for testing. |
| `AttributeError: module 'actions' has no attribute 'user'` | Trying to call a user action before its module loaded | This usually means the `.py` file defining the action has an error. Check the log. |
| `TypeError: missing required argument` | Action called with wrong number of arguments | Check the action definition. The `.talon` file must pass the same number of arguments the Python function expects. |
| `NameError: name 'actions' is not defined` | Forgot to import from talon | Add `from talon import actions` at the top of the file. |

## Context and Override Issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Custom command is ignored | Another file has a more specific context for the same phrase | Add more context matchers to your file (e.g., `os: mac`, `mode: command`) to increase specificity. |
| Command works in one app but not another | Context header restricts it to one app | Remove the context header to make it global, or add the new app to the context. |
| Settings changes don't apply | Another settings block with a more specific context overrides yours | Use a more specific context header for your settings block. |
| List items not recognized | CSV file has formatting issues | Check header line matches exactly, use LF newlines, ensure trailing newline at EOF. |

## Testing Errors

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'talon'` in pytest | Stubs not on the Python path | Add `pythonpath = ["tests/stubs"]` to `pyproject.toml` under `[tool.pytest.ini_options]`. |
| Tests pass but command fails live | Test doesn't match real Talon environment | Tests verify logic in isolation. Always follow up with a live voice test (Step 5 of the checklist). |
| `sim()` returns nothing | Command not active in current context | Switch to the target app first, or use the sleep-and-switch technique. |

## Log Interpretation

### Success indicators
```
[+] /path/to/file.py          # File loaded
[+] /path/to/file.talon       # File loaded
```

### Warning indicators
```
WARNING ... Malformed headers   # CSV file has wrong header format
WARNING ... duplicate           # Two files define the same thing
```

### Error indicators
```
ERROR ... CompileError          # .talon syntax error
ERROR ... ImportError           # .py import problem
ERROR ... ActionProtoError      # Action signature mismatch
ERROR ... Exception             # Runtime error in Python code
```

Always read from the **bottom** of the error output — that's where the most useful information is (file path, line number, and what went wrong).
