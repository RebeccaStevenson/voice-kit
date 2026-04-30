# Talon File Syntax Reference

## File Structure

Every `.talon` file has two parts separated by a line containing only `-`:

```talon
# Context header (optional — defines WHEN this file is active)
app.bundle: com.google.Chrome
os: mac
-
# Body (defines WHAT commands and settings are available)
my command:
    key(cmd-a)
```

If there is no context header (no `-` line), the file is always active.

## Context Header Matchers

| Matcher | Description | Example |
|---|---|---|
| `os` | Operating system | `os: mac`, `os: windows`, `os: linux` |
| `app` | Registered app name | `app: vscode` |
| `app.bundle` | macOS app bundle ID | `app.bundle: com.microsoft.VSCode` |
| `app.name` | Application name | `app.name: Firefox` |
| `app.exe` | Executable name (Windows) | `app.exe: code.exe` |
| `title` | Window title (regex) | `title: /Gmail/` |
| `mode` | Talon mode | `mode: command`, `mode: dictation` |
| `tag` | Active tag | `tag: user.git` |
| `code.language` | Programming language | `code.language: python` |
| `language` | Spoken human language | `language: en` |
| `hostname` | Machine hostname | `hostname: my-laptop` |

### Combining Matchers

Multiple matchers on separate lines are AND-combined:

```talon
app.bundle: com.microsoft.VSCode
title: /\.py/
-
# Active only in VS Code when editing a Python file
```

Use `and` and `not` for complex conditions:

```talon
app.bundle: com.google.Chrome
and not title: /Gmail/
-
# Active in Chrome but NOT on Gmail pages
```

## Voice Command Syntax

### Basic command

```talon
phrase to speak:
    action_to_perform()
```

### Multiple actions

```talon
save and close:
    key(cmd-s)
    sleep(200ms)
    key(cmd-w)
```

### Single-line shorthand

```talon
save file: key(cmd-s)
```

### Commands with arguments

```talon
# <number> is a built-in capture
go line <number>:
    edit.jump_line(number)

# <user.text> captures free-form dictation
type <user.text>:
    insert(user.text)

# {user.website} pulls from a defined list
open {user.website}:
    user.open_url(user.website)
```

### Optional words

```talon
# Square brackets make words optional
[please] save file:
    key(cmd-s)
```

### Alternative words

```talon
# Pipe separates alternatives
(copy | yank) that:
    key(cmd-c)
```

### Combining optional and alternative

```talon
[please] (save | write) file:
    key(cmd-s)
```

### Repetition

```talon
# * means zero or more
noise(pop) [<number_small>]*:
    # handles "pop", "pop three", etc.

# + means one or more
say <word>+:
    insert(word_list)
```

### Anchoring

```talon
# ^ anchors to start of utterance, $ to end
^dictation mode$:
    mode.enable("dictation")
```

Anchoring blocks command chaining — an anchored command can't be said
back-to-back with another command in the same utterance. Only anchor
when the command must not be triggered as part of a longer phrase
(typical use: mode switches).

### Reusing the same capture

When a rule references the same capture twice, the body addresses them
by `_1`, `_2`:

```talon
join <user.letter> [and] <user.letter>:
    insert(letter_1 + letter_2)
```

For `+` repetition (one-or-more), the body gets `<name>_list` plus
indexed entries.

## Built-in Captures

| Capture | Matches | Example phrase |
|---|---|---|
| `<number>` | Any number | "fifty two" → 52 |
| `<number_small>` | Numbers 0-99 | "twelve" → 12 |
| `<user.letter>` | Single letter from alphabet | "air" → a |
| `<user.text>` | Free-form dictated text | "hello world" |
| `<user.number_string>` | Number spoken digit-by-digit | "one two three" → "123" |
| `<phrase>` | Raw speech text | Any spoken words |

## Built-in Action Shorthand

| Function | What it does | Example |
|---|---|---|
| `auto_insert("text")` | Types text (used implicitly by string shorthand) | `hello: auto_insert("hello world")` |
| `repeat(n)` | Repeats the previous action line `n` times | `repeat(3)` |

**String shorthand**: Writing `hello: "hello world"` is equivalent to `hello: auto_insert("hello world")`.

## Community-Provided Lists

These are commonly populated by `.talon-list` files, with a few settings still using CSV files:

| List | Populated by |
|---|---|
| `{user.website}` | `settings/websites.talon-list` |
| `{user.search_engine}` | `settings/search_engines.talon-list` |
| `{user.system_paths}` | `settings/system_paths-<hostname>.talon-list` (local-only, gitignored) |
| `{user.vocabulary}` | `core/vocabulary/vocabulary.talon-list` plus personal `settings/vocabulary.talon-list` additions |
| `{user.word_map}` | `settings/words_to_replace.csv` |
| `{user.application}` | Auto-detected running apps |

## Settings Block

Configure Talon behavior per-context:

```talon
app.exe: my_game.exe
-
settings():
    key_hold = 32
    speech.timeout = 0.5
```

## Tags

Enable additional command sets:

```talon
app.bundle: com.apple.Terminal
-
tag(): user.file_manager
tag(): user.git
tag(): user.tabs
```

## Keyboard Shortcuts (Non-Voice)

Map a physical key combo to an action:

```talon
key(ctrl-t): speech.toggle()
```

## Key Names Reference

### Modifiers
`cmd`, `ctrl`, `alt` (Option), `shift`, `super` (Command alias), `fn`

### Special Keys
`enter`, `tab`, `escape`, `space`, `backspace`, `delete`, `home`, `end`, `pageup`, `pagedown`, `up`, `down`, `left`, `right`

### Function Keys
`f1` through `f20`

### Combining
`key(cmd-shift-alt-p)` — separate modifiers with hyphens

### Repetition, hold/release, passive, key-up

| Form | What it does |
|---|---|
| `key(left:5)` | Press the same key N times |
| `key(ctrl:down)` | Hold the key down (paired with `:up` later) |
| `key(ctrl:up)` | Release a previously-held key |
| `key(f9:passive)` | Bind without blocking the key from other apps |
| `key(f9:up)` | Trigger on key release instead of press |

## Sleep Duration Formats

`sleep()` accepts:

| Form | Meaning |
|---|---|
| `sleep(500ms)` | 500 milliseconds |
| `sleep(2s)` | 2 seconds |
| `sleep(1m)` | 1 minute |
| `sleep(0.5)` | 0.5 seconds (bare float) |

`ms` is the right unit for short pauses between key presses. Sleep
blocks Talon from processing further commands for the duration, so keep
it short outside of intentional pauses.
