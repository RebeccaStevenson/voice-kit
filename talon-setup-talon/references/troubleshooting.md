# Troubleshooting Talon Setup

## Talon Won't Start

- **macOS permissions**: Talon requires Accessibility and Microphone permissions. Go to System Settings > Privacy & Security > Accessibility and ensure Talon is listed and enabled. Do the same for Microphone.
- **Relaunch after permissions**: After granting permissions, quit Talon completely (right-click menu bar icon > Quit) and reopen it.

## Voice Commands Not Recognized

- **Is Talon awake?** Say "wake up". If Talon is asleep, it ignores all commands except wake phrases.
- **Microphone check**: Right-click the Talon menu bar icon > Preferences to verify the correct microphone is selected.
- **Background noise**: Talon works best in a reasonably quiet environment. Reduce background noise or move closer to the microphone.
- **Speak naturally**: The Conformer engine handles natural speech well. Avoid over-enunciating — speak at a normal pace and volume.

## Community Commands Not Loading

- **Wrong directory**: The community folder must be at `~/.talon/user/community/`. A common mistake is cloning it one level too deep (e.g., `~/.talon/user/community/community/`).
- **Check the log**: Right-click the Talon menu bar icon > Scripting > View Log. Look for `ERROR` lines mentioning file paths.
- **Verify with terminal**:
  ```bash
  ls ~/.talon/user/community/
  ```
  You should see folders like `core/`, `plugin/`, `apps/`, and files like `README.md`.

## Rango Hints Not Showing

- **Extension enabled?** Check your browser's extension settings and make sure Rango is turned on.
- **Safari extra step**: Safari > Preferences > Extensions > Rango > check "Always Allow on Every Website".
- **Rango-talon installed?** The browser extension alone is not enough — the Talon commands must also be installed:
  ```bash
  ls ~/.talon/user/rango-talon/
  ```
- **Refresh the page**: Some pages need a refresh after installing the extension for hints to appear.

## Common Log Errors

Open the log with: right-click Talon menu bar icon > Scripting > View Log (or say `talon open log`).

| Error | Meaning | Fix |
|---|---|---|
| `[+] /path/to/file.py` | File loaded successfully | No action needed |
| `[-] /path/to/file.py` | File was unloaded (usually before a reload) | Normal behavior |
| `ERROR ... CompileError` | Syntax error in a .talon file | Check the file path and line number in the error |
| `ERROR ... ImportError` | Python import failed | A .py file has a missing dependency or typo |
| `ActionProtoError` | Action signature mismatch | Check that the action's parameters match its declaration |

## Getting Help

- **Talon Slack**: Join at https://talonvoice.com/chat — the `#help` channel is very active and welcoming
- **Talon Wiki**: Community documentation at https://talon.wiki/
- **Community GitHub**: https://github.com/talonhub/community/issues for bug reports
