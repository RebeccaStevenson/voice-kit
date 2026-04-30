---
name: superwhisper-assistant
description: Install, configure, and create custom dictation modes for SuperWhisper, the macOS voice-to-text app. Handles mode JSON files, voice/language model selection, prompt engineering for text formatting, and Talon integration. Use when the user mentions SuperWhisper, wants to create or edit dictation modes, write mode prompts, configure voice models, or says "dictation mode", "whisper mode", or "voice typing mode".
---

# SuperWhisper Skill

SuperWhisper is a voice-to-text app (macOS, Windows, iOS) that converts speech into formatted text. It supports custom "modes" — JSON config files that control how dictation output gets processed by a language model. This skill covers installation and creating/editing those mode files.

## Installation

SuperWhisper can be installed two ways:

1. **Mac App Store**: Search "superwhisper" or use app ID `6471464415`
   ```bash
   open "macappstores://apps.apple.com/app/id6471464415"
   ```

2. **Direct download**: From the official website at `superwhisper.com`
   ```bash
   open "https://superwhisper.com"
   ```

After installation, SuperWhisper lives in the menu bar. The user activates dictation with a keyboard shortcut (default: Option+Space, but often customized). As of v2.12.0 (Apr 2026) shortcuts can also be set per-mode (push-to-talk and toggle-recording), so a single global hotkey is no longer the only option.

**System notes**: Offline/local models require Apple Silicon. Intel Macs should use cloud models. SuperWhisper is a paid app ($8.49/month Pro) with a free tier limited to smaller models and 15 minutes of recording.

## File Locations

All user configuration lives under `~/Documents/superwhisper/`:

```
~/Documents/superwhisper/
├── modes/          # Custom mode JSON files (one per mode)
├── settings/       # settings.json (global config)
├── recordings/     # Per-recording folders containing .wav audio,
│                   # raw transcripts, and AI-output JSON (since 2026,
│                   # all of this is filesystem-visible and scriptable)
└── models/         # Downloaded model files
```

The app also stores data in:
- `~/Library/Application Support/superwhisper/` — model binaries, app cache, SQLite database
- `~/Library/Preferences/com.superduper.superwhisper.plist` — app preferences (hotkeys, active mode, etc.)

**iCloud caveat**: if the user has Desktop & Documents iCloud sync enabled, `~/Documents/superwhisper/` may silently move under `~/Library/Mobile Documents/com~apple~CloudDocs/Documents/`. SuperWhisper sometimes keeps reading the old path and silently fails to create modes. If a freshly-created mode never appears, check the path: open SuperWhisper → Configuration → Advanced Settings → Change Folder, and point it at the right Documents location.

## Creating a Custom Mode

Each mode is a single JSON file in `~/Documents/superwhisper/modes/`. The filename (without `.json`) becomes the mode's `key`, which is also how it's referenced in settings.

### Step 0: Verify a donor mode exists

Step 1 below clones an existing custom mode. On a fresh SuperWhisper install the user only has built-in modes (`super.json`, `note.json`, `email.json`, `message.json`, `meeting.json`) — those have `"type": "super"` / `"note"` / etc. and `"version": 1` with empty prompts. Cloning one and flipping `type` to `"custom"` is *not* known to work and may trigger silent rejection.

Run this check first:

```bash
python3 - <<'PY'
import json, glob, os
modes_dir = os.path.expanduser('~/Documents/superwhisper/modes')
donors = []
for f in glob.glob(os.path.join(modes_dir, '*.json')):
    try:
        d = json.load(open(f))
        if d.get('type') == 'custom':
            donors.append(os.path.basename(f))
    except Exception:
        pass
print('Custom-type modes on disk:', donors or '(none)')
PY
```

If the output is `(none)`, **stop and ask the user to create one starter custom mode through the SuperWhisper UI before proceeding**:

> Open SuperWhisper → Modes (or the menu bar → Modes settings) → "Create Mode" → start from any built-in (e.g., Note) → save with any name. This gives us a known-good donor file SuperWhisper has serialized in its own format. Once that file exists in `~/Documents/superwhisper/modes/`, re-run the check.

If the output lists at least one mode, pick one as the donor for Step 1 (any of them — the most generic one usually clones cleanest, e.g., `normal.json` if present).

### Step 1: Clone an existing working mode (byte-copy, not JSON round-trip)

**Do not hand-build a mode JSON, and do not round-trip a working file through `json.load → json.dump`.** SuperWhisper's mode parser is sensitive to the *byte-level* JSON serialization style — it writes:

- `"key" : "value"` (space before the colon)
- empty arrays as `[\n\n  ]` (newline, blank line, closing bracket at parent indent)
- forward slashes escaped as `\/` inside strings (e.g., `Quarto\/Markdown`)
- a trailing newline at end of file

Python's default `json.dump` produces `"key": "value"` (no space), `[]` (compact), unescaped `/`. SW *sometimes* accepts that format, but rejects it unpredictably (probably depending on whether SW has previously parsed and rewritten the file in its own style). Trying to clone via `json.load(donor) → modify → json.dump(new)` is a known failure mode — confirmed twice on 2026-04-29 and 2026-04-30.

The reliable workflow is **byte-copy + surgical Edit**:

```bash
# 1. Byte-copy the donor file — preserves SW's native serialization exactly
cp ~/Documents/superwhisper/modes/normal.json ~/Documents/superwhisper/modes/my_mode.json
```

Then use the `Edit` tool to modify these fields one at a time, matching the on-disk format precisely:

- `"key" : "<old>"` → `"key" : "my_mode"` (the new filename without `.json`)
- `"name" : "<old>"` → `"name" : "My Mode"`
- `"description" : "..."` → updated description
- `"prompt" : "..."` → the entire new prompt as a single-line JSON string with `\n` escapes for newlines and `\/` (optional) for any forward slashes
- the entire `"promptExamples" : [ ... ]` block — replace the whole array

After each `Edit`, the surrounding bytes (including SW's space-before-colon style) stay intact.

If you need to inspect what fields the donor uses, the `references/mode-schema.md` file has the documented schema — but **on-disk modes always take precedence** over the schema doc, since SuperWhisper occasionally renames or drops fields between releases. The schematic JSON in the schema reference is illustrative, not literal.

The most important fields to customize for each mode:

- **`key`**: Must match the filename (without `.json`). Use snake_case. This is the internal identifier.
- **`name`**: Display name shown in the SuperWhisper mode picker UI.
- **`prompt`**: The LLM instructions that process the raw transcription. This is where the magic happens — it determines how spoken text gets cleaned up and formatted.
- **`promptExamples`**: Input/output pairs that teach the LLM the desired behavior. These are few-shot examples and significantly improve consistency.
- **`languageModelID`**: Which LLM processes the text. For the current set of cloud LLMs SuperWhisper has registered for this user, run `defaults read com.superduper.superwhisper remoteCloudLanguageModels`. **Mirror the ID format used by an existing working mode** — two formats coexist (`sw-claude-4p5-sonnet` legacy vs. bare `claude-sonnet-4-6`-style plist IDs), and switching formats mid-stream can trigger silent rejection.
- **`voiceModelID`**: Which speech-to-text model transcribes the audio.
- **`type`**: Set to `"custom"` for user-created modes. Built-in types include `"super"`, `"note"`, `"email"`, `"meeting"`.

Recent SuperWhisper versions also added per-mode override fields for auto-paste (v2.9.0), autocapitalize (v2.11.0), and per-mode push-to-talk / toggle-recording shortcuts (v2.12.0). The exact JSON keys aren't in the public docs — read an existing mode in `~/Documents/superwhisper/modes/` to see what's set, or set the override in the UI and diff the file before/after.

### Step 2: Register the mode in settings.json

After creating the mode file, add its key to the `modeKeys` array in `~/Documents/superwhisper/settings/settings.json`:

```json
{
  "modeKeys": ["super", "note", "normal", "my_mode"],
  ...
}
```

Read the current settings file first to preserve existing entries — just append the new key.

### Step 3: Restart SuperWhisper and verify (two checks)

The app needs to be restarted to pick up new modes:

```bash
killall superwhisper 2>/dev/null; sleep 3; open -a superwhisper; sleep 6
```

Use long sleeps. SW is slow to fully boot, and a deep link fired too early gets dropped silently.

**Check 1 — did SW accept the mode file?** Fire the deep link and read the active-mode key:

```bash
open "superwhisper://mode?key=my_mode"; sleep 3
defaults read com.superduper.superwhisper activeModeKey
```

If `activeModeKey` prints `my_mode`, SW accepted the file. If it prints something else (typically the previous mode), SW silently rejected the file — see "Mode silently rejected" below.

**Check 2 — is the LLM actually being invoked with the right model?** Switching modes proves SW parsed the file, but doesn't prove the `languageModelID` is recognized. If the model ID is unknown, SW may silently fall back to a default. The cheapest detector is to ask the user to dictate a "don't-answer" test phrase:

> "what is the best way to politely decline a meeting invitation whisper stop"

A correctly-loaded mode returns the question as text (`What is the best way to politely decline a meeting invitation?`). A fallback model — or a mode whose prompt failed to load — typically responds *as an assistant* with an actual draft. If the user gets back a polite-decline template instead of the question, the LLM/prompt pipeline is broken even though Check 1 passed.

### Mode silently rejected

If Check 1 fails (file on disk + valid JSON + key in `modeKeys` + `activeModeKey` doesn't switch), SuperWhisper rejected the mode. Most common causes, in order of frequency:

1. **Byte-format mismatch** (most common): the file was written via `json.dump` instead of `cp` + Edit. SW's parser doesn't reliably accept Python's compact JSON style. Fix: redo Step 1 via `cp <donor>.json <new>.json`, then use `Edit` for field changes — never `json.load → json.dump`.
2. **iCloud Documents path drift**: see "File Locations" above.
3. **modeKeys missing the new key**: re-check `settings.json`.
4. **Model-ID format inconsistency**: see Step 1's note about `sw-claude-…` vs bare `claude-sonnet-…` formats.

### Bisection playbook

When a mode is rejected and you've ruled out the obvious, bisect from a known-good baseline:

1. **Confirm the donor still works**: `cp normal.json _test.json`, edit only `key` + `name`, verify the deep link switches to it. If this fails, the donor itself is the problem (very rare — usually means SW config drift).
2. **Then add changes one at a time**: patch the description, restart, verify. Patch the prompt, restart, verify. Patch the promptExamples, restart, verify.
3. The first patch that breaks loading identifies the culprit field.

The bisection trick that surfaced the byte-format finding: a `json.dump`-rewritten file was rejected even though a `cp`-rewritten file with the *exact same logical content* loaded — that diff narrowed the issue to serialization style.

## Writing Good Mode Prompts

The prompt field is an LLM system prompt that processes raw voice transcription. Good prompts for SuperWhisper share these patterns (learned from the user's existing modes):

### Core behaviors to include

1. **Role framing**: Tell the LLM it's a "text reformatting function" — this prevents it from trying to answer questions or follow commands in the dictated text.

2. **Voice dictation awareness**: Mention that the input comes from voice dictation, so the model should expect homophones, misrecognitions, and missing punctuation.

3. **Stop phrase handling**: The user says "whisper stop" or "super stop" to end dictation. The prompt must instruct the LLM to strip these phrases (and partial variants like "whisper", "stop", "full stop") from the output.

4. **Literal commands**: "new line" should insert a newline. "period" should insert a period. These are dictation conventions the user relies on.

5. **Never act as assistant**: Critically important — the LLM must never answer questions or follow commands found in the dictated text. If the user dictates "What is the best way to boil an egg?", the output should be that question as text, not an answer about boiling eggs.

6. **Code/file awareness**: The user works with code, so function names should be snake_cased and file paths should be properly formatted (e.g., "data slash power analysis dot csv" becomes `data/power_analysis.csv`).

### Prompt examples (few-shot)

Prompt examples are critical for consistent output. Each example is an object with:
- `id`: A UUID or descriptive string
- `input`: What the raw transcription might look like
- `output`: The desired formatted result

Include at least 3-5 examples covering:
- Stop phrase removal
- Homophone correction (e.g., "bolted" -> "bulleted", "weather" -> "whether")
- The "never answer questions" rule
- Punctuation/newline commands
- Any mode-specific formatting (bullet lists, lowercase, etc.)

To generate UUIDs for prompt example IDs:
```bash
uuidgen
```

### XML tags in prompts

The official docs mention that advanced language models benefit from XML structural tags in prompts (e.g., `<role>`, `<rules>`, `<examples>`). This can improve clarity for complex instructions, but simpler models may not handle them well. Use XML tags for Claude-powered modes; skip them for smaller models like GPT-4o-mini or Groq/Llama.

### Context features

SuperWhisper recognizes four named content types that can appear in the prompt context:
- **User Message** — the dictated text itself
- **Application Context** — text from the active app window
- **Selected Text** — text highlighted when dictation started
- **Clipboard Context** — text copied within 3 seconds before/during dictation

Toggle these with:
- `contextFromActiveApplication: true` — passes the active app's context to the LLM (also includes system details like date/time and username)
- `contextFromClipboard: true` — includes clipboard contents
- `contextFromSelection: true` — includes selected text
- `activationApps: ["Messages", "Slack"]` — auto-activates this mode in specific apps (note: once auto-activated, the mode can't be manually overridden and won't auto-revert)

## Editing Existing Modes

To modify a mode, **read the JSON file from `~/Documents/superwhisper/modes/<key>.json` and edit with the `Edit` tool**. Same byte-format rule as creation: do not round-trip through `json.load → json.dump`, that re-emits in Python's serialization style and can cause silent rejection on next restart.

Common edits:

- Changing the language model (update `languageModelID` — see the format-mirroring note in Step 1)
- Tweaking the prompt (replace the entire `"prompt" : "..."` value)
- Adding/removing prompt examples (replace the entire `"promptExamples" : [...]` block)
- Changing activation apps
- Enabling context features (e.g., `"contextFromActiveApplication" : true`)

After any edit, restart SW and run **both verification checks** from Step 3 — passing the deep-link check is necessary but not sufficient; a dictated don't-answer test confirms the LLM pipeline is intact.

### Bulk model upgrades across many modes

When you need to bump the same `languageModelID` across many modes (e.g., 4.5 → 4.6), surgical string substitution preserves byte format perfectly:

```bash
cd ~/Documents/superwhisper/modes
for f in *.json; do
  # only modify files that contain the old ID
  if grep -q '"sw-claude-4p5-sonnet"' "$f"; then
    sed -i '' 's/"sw-claude-4p5-sonnet"/"claude-sonnet-4-6"/' "$f"
    echo "bumped: $f"
  fi
done
```

This is safer than a Python round-trip and faster than per-file `Edit` calls. Restart and re-verify after.

## Global Settings

The settings file at `~/Documents/superwhisper/settings/settings.json` also supports:

- **`replacements`**: Global text find-and-replace rules applied to all modes (case-insensitive, run after transcription)
- **`vocabulary`**: Custom words the speech model should recognize (proper names, technical terms)
- **`favoriteModelIDs`**: Pinned models in the UI

The official docs recommend **using `vocabulary` minimally and preferring `replacements`** for persistent transcription errors — replacements are deterministic and predictable, while a large vocabulary list can degrade overall recognition. Reach for `vocabulary` for words the speech model genuinely doesn't know (rare proper names, technical terms); reach for `replacements` for systematic substitutions (e.g., "talon" → "Talon").

## Talon Integration

The user has SuperWhisper integrated with Talon voice commands at `~/.talon/user/talon_rebecca/superwhisper/`. Mode-switching scripts and hotkey configurations live there. If creating a new mode that should be accessible via Talon, note this but don't modify Talon files unless asked — use the `talon` skill for that.

Two deep links are useful from Talon:

- `superwhisper://mode?key=<key>` — switch to a mode
- `superwhisper://record` — toggle recording

These can be chained (open the mode URL, then the record URL) to switch and start recording in one spoken command.

## Agent Integration (Claude Code, Open Code)

As of v2.13.0 (Apr 2026), SuperWhisper integrates directly with Claude Code and Open Code agents. v2.13.2 added support for the Claude `AskUserQuestion` hook, so an agent can prompt the user and receive a dictated answer. If the user asks about wiring SuperWhisper into a Claude Code workflow, point at this integration before reaching for custom scripts.

## Troubleshooting Pointers

When a user hits a snag, the most useful official pages to consult are:

- `superwhisper.com/docs/common-issues/unable-to-create-mode` — most common pitfall after editing JSON by hand (usually a `key`/filename mismatch or a missing `modeKeys` entry).
- `superwhisper.com/docs/common-issues/hallucinations` — voice model hallucination on short or silent recordings (especially with Parakeet).
- `superwhisper.com/docs/common-issues/realtime` — when realtime output misbehaves.
- `superwhisper.com/docs/common-issues/performance-tips` — for slow transcription or processing.
