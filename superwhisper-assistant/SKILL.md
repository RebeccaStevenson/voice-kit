name: superwhisper-assistant
description: Set up, configure, and create custom dictation modes for SuperWhisper, the macOS voice-to-text app. Use this skill when the user mentions SuperWhisper, wants to install it, create or edit dictation modes, configure voice models, write mode prompts, or anything related to speech-to-text mode configuration on their Mac. Also trigger when the user talks about "dictation modes", "voice typing modes", "whisper modes", or wants to customize how their voice dictation formats text.
---

# Superwhisper-assistant skill

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

After installation, SuperWhisper lives in the menu bar. The user activates dictation with a keyboard shortcut (default: Option+Space, but often customized).

**System notes**: Offline/local models require Apple Silicon. Intel Macs should use cloud models. SuperWhisper is a paid app ($8.49/month Pro) with a free tier limited to smaller models and 15 minutes of recording.

## File locations

All user configuration lives under `~/Documents/superwhisper/`:

```
~/Documents/superwhisper/
├── modes/          # Custom mode JSON files (one per mode)
├── settings/       # settings.json (global config)
├── recordings/     # Saved audio recordings
└── models/         # Downloaded model files
```

The app also stores data in:
- `~/Library/Application Support/superwhisper/` — model binaries, app cache, SQLite database
- `~/Library/Preferences/com.superduper.superwhisper.plist` — app preferences (hotkeys, active mode, etc.)

## Creating a custom mode

Each mode is a single JSON file in `~/Documents/superwhisper/modes/`. The filename (without `.json`) becomes the mode's `key`, which is also how it's referenced in settings.

### Step 1: Write the mode JSON file

Create a new `.json` file in the modes directory. Read `references/mode-schema.md` for the full field reference and available model IDs. Here's the minimal pattern:

```json
{
  "activationApps": [],
  "activationSites": [],
  "adjustOutputVolume": false,
  "contextFromActiveApplication": false,
  "contextFromClipboard": false,
  "contextFromSelection": false,
  "contextTemplate": "Use the copied text as context to complete this task.\n\nCopied text: ",
  "description": "",
  "diarize": false,
  "iconName": "",
  "key": "my_mode",
  "language": "en",
  "languageModelEnabled": true,
  "languageModelID": "sw-claude-4p5-sonnet",
  "literalPunctuation": false,
  "name": "My Mode",
  "pauseMediaPlayback": false,
  "prompt": "Your instructions to the language model here...",
  "promptExamples": [],
  "realtimeOutput": false,
  "script": "",
  "scriptEnabled": false,
  "translateToEnglish": false,
  "type": "custom",
  "useSystemAudio": false,
  "version": 2,
  "voiceModelID": "sw-ultra-cloud-v1-east"
}
```

The most important fields to customize for each mode:

- **`key`**: Must match the filename (without `.json`). Use snake_case. This is the internal identifier.
- **`name`**: Display name shown in the SuperWhisper mode picker UI.
- **`prompt`**: The LLM instructions that process the raw transcription. This is where the magic happens — it determines how spoken text gets cleaned up and formatted.
- **`promptExamples`**: Input/output pairs that teach the LLM the desired behavior. These are few-shot examples and significantly improve consistency.
- **`languageModelID`**: Which LLM processes the text. See the schema reference for available models.
- **`voiceModelID`**: Which speech-to-text model transcribes the audio.
- **`type`**: Set to `"custom"` for user-created modes. Built-in types include `"super"`, `"note"`, `"email"`, `"meeting"`.

### Step 2: Register the mode in settings.json

After creating the mode file, add its key to the `modeKeys` array in `~/Documents/superwhisper/settings/settings.json`:

```json
{
  "modeKeys": ["super", "note", "normal", "my_mode"],
  ...
}
```

Read the current settings file first to preserve existing entries — just append the new key.

### Step 3: Restart SuperWhisper

The app needs to be restarted to pick up new modes:

```bash
killall superwhisper 2>/dev/null; sleep 1; open -a superwhisper
```

## Writing good mode prompts

The prompt field is an LLM system prompt that processes raw voice transcription. Good prompts for SuperWhisper share these patterns (learned from the user's existing modes):

### Core behaviors to include

1. **Role framing**: Tell the LLM it's a "text reformatting function" — this prevents it from trying to answer questions or follow commands in the dictated text.

2. **Voice dictation awareness**: Mention that the input comes from voice dictation, so the model should expect homophones, misrecognitions, and missing punctuation.

3. **Literal commands**: "new line" should insert a newline. "period" should insert a period. These are dictation conventions the user relies on.

4. **Never act as assistant**: Critically important — the LLM must never answer questions or follow commands found in the dictated text. If the user dictates "What is the best way to boil an egg?", the output should be that question as text, not an answer about boiling eggs.

5. **Code/file awareness**: The user works with code, so function names should be snake_cased and file paths should be properly formatted (e.g., "data slash power analysis dot csv" becomes `data/power_analysis.csv`).

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

## Editing existing modes

To modify a mode, read the JSON file from `~/Documents/superwhisper/modes/<key>.json`, make changes with the Edit tool, and restart SuperWhisper. Common edits:

- Changing the language model (update `languageModelID`)
- Tweaking the prompt
- Adding/removing prompt examples
- Changing activation apps
- Enabling context features

## Global settings

The settings file at `~/Documents/superwhisper/settings/settings.json` also supports:

- **`replacements`**: Global text find-and-replace rules applied to all modes
- **`vocabulary`**: Custom words the speech model should recognize (proper names, technical terms)
- **`favoriteModelIDs`**: Pinned models in the UI
