# Troubleshooting Talon Setup

Quick error → fix lookup. The procedural walkthrough lives in `SKILL.md`;
this reference is for symptom-to-cause-to-fix matching during debugging.

## Talon Won't Start / No Menu Bar Icon

| Symptom | Cause | Fix |
|---|---|---|
| No icon after launch | macOS hides icons behind the notch | Hover the top-right edge on newer MacBooks |
| App opened, no icon, no error | Gatekeeper blocked it silently | System Settings → Privacy & Security → **Open Anyway** |
| Permission popups never appeared | Talon launched before grants | Add Talon manually under Privacy & Security → Accessibility *and* Microphone |
| Permissions granted but still nothing | Talon needs a relaunch | Quit (right-click icon → Quit, or `killall Talon`) and reopen |

## Voice Commands Not Recognized

| Symptom | Cause | Fix |
|---|---|---|
| Talon ignores everything | Asleep | Say `wake up` |
| Speech goes to text instead of running | Dictation mode | Say `command mode` |
| Multi-word commands clip mid-phrase | `speech.timeout` too tight | Set `speech.timeout = 0.4` (or higher in 0.1s steps) in a `settings():` block — see **talon-customize-settings** |
| Wrong mic active | Talon's mic ≠ system mic | Right-click menu bar icon → check mic selection |
| Recognition slow / inaccurate at start | Conformer model still downloading | Check menu bar for download progress |
| Frequent misrecognition | Background noise or mic distance | Headset mic ~1 in from mouth, or table mic 6–12 in; speak naturally without over-enunciating |

Wiki references: [Troubleshooting](https://talon.wiki/Resource%20Hub/Speech%20Recognition/troubleshooting),
[Improving Recognition Accuracy](https://talon.wiki/Resource%20Hub/Speech%20Recognition/improving_recognition_accuracy).

## Community Commands Not Loading

| Symptom | Cause | Fix |
|---|---|---|
| `help alphabet` does nothing | Wrong directory layout | `ls ~/.talon/user/community/` should show `core/`, `plugin/`, `apps/` |
| `community/community/` exists | Cloned one level too deep | Move contents up a level |
| Log shows `ERROR` mentioning community paths | Syntax error after a local edit | Revert local edits; community is meant to be read-only |

## Rango Hints Not Showing

| Symptom | Fix |
|---|---|
| No hints on any page | Confirm the Rango extension is enabled in the browser's extension settings |
| Safari, no hints | Safari → Preferences → Extensions → Rango → **Always Allow on Every Website** |
| Extension on, still nothing | Verify `~/.talon/user/rango-talon/` exists |
| Hints missing on one tab | Refresh the page after install |

## Common Log Errors

Open the log with `talon open log`, or right-click the menu bar icon → Scripting → View Log.

| Log line | Meaning | Fix |
|---|---|---|
| `[+] /path/to/file.py` | File loaded successfully | None |
| `[-] /path/to/file.py` | File unloaded (usually before a reload) | None |
| `ERROR ... CompileError` | Syntax error in a `.talon` file | Check the file path and line number printed in the error |
| `ERROR ... ImportError` | Python import failed | A `.py` file has a missing dependency or typo |
| `ActionProtoError` | Action signature mismatch | Confirm parameters match the action's declaration |

## Getting Help

- **Talon Slack**: <https://talonvoice.com/chat> — `#help` is active and welcoming
- **Talon Wiki**: <https://talon.wiki/>
- **Community GitHub**: <https://github.com/talonhub/community/issues>
