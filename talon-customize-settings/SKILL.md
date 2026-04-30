---
name: talon-customize-settings
description: >
  Add or update Talon settings like vocabulary, words to replace, websites,
  search engines, subtitles, system paths, and speech recognition tuning
  (timeout, alphabet/modifier alternates, remapping problem commands). Use
  when the user wants to customize Talon settings after initial setup —
  e.g., "add a word to vocabulary", "add a website", "change subtitle
  size", "Talon keeps misspelling a name", "Talon cuts me off
  mid-command", "I can't say 'sit'", "remap the touch command", or any
  request to modify Talon's word lists, display preferences, path aliases,
  or recognition behavior. Do NOT use for creating voice commands — that's
  talon-create-command.
---

# Customize Talon Settings

Help the user add or update entries in their Talon settings files. This
skill handles the ongoing maintenance of settings that were initially
set up during onboarding — vocabulary, words to replace, websites, search
engines, subtitles, and system paths.

Keep the tone conversational and concise. The user already has Talon
working — they just want to tweak something.

> Based on the [Talon Community Wiki](https://talon.wiki/). See
> [Basic Customization](https://talon.wiki/Customization/basic_customization)
> and [Improving Recognition Accuracy](https://talon.wiki/Resource%20Hub/Speech%20Recognition/improving_recognition_accuracy).

## Before Starting

### Read the Profile

```bash
cat ~/.talon/talon-assistant/profile.md
```

Adapt tone to the user's proficiency level. Advanced users get concise
responses; beginners get a bit more context.

### Find the Personal Repo

```bash
TALON_HOME="$HOME/.talon"
ls "$TALON_HOME/user/" | grep -v community | grep -v rango-talon | grep -v cursorless-talon | grep -v parrot | grep -v talon-ai-tools
```

If no personal repo exists, tell the user they need one first and invoke
**talon-create-custom-repo**.

## Figuring Out What They Want

The user might ask in different ways. Map their request to the right
setting:

| User says something like... | Setting |
|---|---|
| "add a word", "Talon doesn't know this word", "vocabulary" | Vocabulary |
| "Talon keeps misspelling", "wrong spelling", "name is spelled wrong" | Words to replace |
| "add a website", "open [site] by voice" | Websites |
| "add a search engine", "search [site] by voice" | Search engines |
| "turn off subtitles", "change subtitle size", "move subtitles" | Subtitles / display |
| "add a folder", "system paths", "path alias" | System paths |
| "Talon cuts me off mid-command", "phrase timeout", "end of phrase too fast" | Speech timeout |
| "I can't say 'sit'", "alphabet alternative", "trouble saying 'control'" | Alphabet / modifier alternates |
| "remap a community command", "stop the X command from firing", "rebind touch" | Replace a problem command |

If it's not clear which setting they need, ask:

> "What would you like to change? I can help with vocabulary, word
> corrections, websites, search engines, subtitles, or system paths."

## Handling Each Setting

For each setting, the pattern is: check what exists → ask what to
add/change → write the file → confirm → suggest the voice command for
next time.

**Important:** The agent writes the files directly. Do not ask the user to
open a text editor.

### Vocabulary

**When to use:** Talon doesn't recognize a word, or the user wants to add
software names, project names, technical terms, or unusual names.

**File:** `<user_repo>/settings/vocabulary.talon-list`

**Steps:**
1. Read the existing file to see what's already there
2. Ask: "What words would you want to add?" (if the user hasn't already
   told you)
3. For words with specific capitalization (brand names, acronyms), use
   `spoken: Written` format — e.g., `superwhisper: SuperWhisper`. For
   plain terms, use the word alone.
4. Append entries to the file (or create it with header
   `list: user.vocabulary` and `-` separator if it doesn't exist)
5. Confirm: "Added [words]. Try saying one to verify."

**Voice command for next time:** `customize vocabulary` opens the file in
a text editor. `copy to vocab` adds selected text directly.

### Words to Replace

**When to use:** Talon hears a word correctly but writes the wrong
spelling — common with names, technical terms, or homophones.

**File:** `<user_repo>/settings/words_to_replace.csv`

**Steps:**
1. Read the existing file to check for duplicates
2. Ask: "What words does Talon keep getting wrong?" (if not already clear)
3. Append each pair as `correct,incorrect` — the word you *want* comes
   first. For example, `Ryon,Ryan` means "replace Ryan with Ryon."
4. Confirm: "Added [pairs]. Next time Talon writes [incorrect], it'll
   output [correct] instead."

**Voice command for next time:** `customize words to replace` opens the
file. `copy to replacements as <word>` adds from selected text.

### Websites

**When to use:** The user wants to open a site by saying `open [name]`.

**File:** `<user_repo>/settings/website.talon-list` (or personal repo
equivalent)

**Steps:**
1. Check both community defaults and existing personal entries for
   duplicates. Community defaults are at:
   `$TALON_HOME/user/community/core/websites_and_search_engines/website.talon-list`
   (includes gmail, github, youtube, google, wikipedia, etc.)
2. Ask: "What sites would you want to open by voice?" (if not already
   clear). The user will often just give a name — look up or construct
   the URL yourself.
3. Append entries as `spoken name: https://...` (or create the file with
   header `list: user.website` and `-` separator)
4. Confirm: "Added [sites]. Try saying `open [name]` to test it."

**Voice command for next time:** `customize websites`

### Search Engines

**When to use:** The user wants to run a named search by voice — e.g.,
`pubmed hunt reversal learning`.

**File:** `<user_repo>/settings/search_engine.talon-list` (or personal
repo equivalent)

**Steps:**
1. Check community defaults (google, amazon, scholar, wiki, map) and
   existing personal entries for duplicates
2. Ask: "What search engines would you want to add?" (if not already
   clear). The user will usually just say a name — construct the search
   URL yourself with `%s` as the query placeholder. For example,
   "PubMed" → `https://pubmed.ncbi.nlm.nih.gov/?term=%s`
3. Append entries as `spoken name: https://...%s` (or create the file
   with header `list: user.search_engine` and `-` separator)
4. Confirm: "Added [engines]. Try saying `[name] hunt [your query]` to
   test it."

**Voice command for next time:** `customize search engines`

### Subtitles / Display

**When to use:** The user wants to turn subtitles on/off, or adjust their
appearance.

There are two subtitle systems:
1. **Talon's built-in subtitles** — toggled from the Talon menu bar under
   Speech Recognition → Show Subtitles. No file controls this.
2. **Community plugin subtitles** — controlled by settings in a `.talon`
   file. More customizable: font size (`user.subtitles_size`) and
   position on screen (`user.subtitles_y`).

**File:** A `.talon` file in `<user_repo>/settings/` (e.g.,
`display.talon`) with a `settings():` block.

**Steps:**
- If **off entirely:** Set `user.subtitles_show = false` in the settings
  file. Mention the menu bar toggle for built-in subtitles. Also mention
  that the community plugin can be adjusted (font size, position) rather
  than just disabled.
- If **adjust size:** Set `user.subtitles_size` (default is 100, in
  pixels).
- If **adjust position:** Set `user.subtitles_y` (0.0 = top, 1.0 =
  bottom, default is 0.93).
- Confirm what was changed.

### System Paths

**When to use:** The user wants Talon to understand spoken names for
folders on their computer.

**File:** `<user_repo>/settings/system_paths-<hostname>.talon-list`

**Steps:**
1. Read the existing file to see what's already there
2. Ask: "What folders would you want to refer to by voice? Give me a
   short name and the full path." (if not already clear)
3. Append entries as `spoken name: /full/path` (or create the file with
   header `list: user.system_paths` and `-` separator)
4. Confirm: "Added [paths]."

### Speech Timeout

**When to use:** Talon cuts the user off before they finish a phrase, or
splits one command into two. This is the single most impactful recognition
setting and the first thing to try if commands are firing partially.

**File:** A `.talon` file in `<user_repo>/settings/` (e.g., `settings.talon`)
with a `settings():` block. No context header — the setting applies
globally.

**Steps:**
1. Read the existing file (if any) to see the current value
2. Default Talon timeout is fairly tight; a good starting point is `0.4`
   seconds. Raise in 0.1s steps if commands are still being clipped.
3. Write or update the block:

   ```talon
   settings():
       speech.timeout = 0.4
   ```

4. Confirm: "Set `speech.timeout` to 0.4s. Talon picks this up
   immediately. If commands still cut off, bump it to 0.5 or 0.6 — but
   higher values make Talon feel laggier, so go in small increments."

### Alphabet / Modifier Alternates

**When to use:** Talon mishears a specific letter or modifier consistently
— e.g., "sit" for the letter S, or "control" sounding like "patrol." The
community ships alternative phonics for both.

**File:** Edit the existing alphabet/modifier definitions in the community
repo via override. The cleanest pattern is to redefine the offending entry
in the user's personal repo so it takes precedence, rather than modifying
community files.

**Steps:**
1. Confirm which letter or modifier is misrecognizing. Ask the user to say
   it a few times and check `command history` or the log.
2. Pick a replacement word that's phonetically distinct. The wiki suggests
   `ivy` for S (instead of `sit`) and `troll` for ctrl (instead of
   `control`), but any clear, unambiguous word works.
3. In the user's repo, override the relevant list. For example, to swap
   the spoken form of the letter S to `ivy`, find the community alphabet
   list, copy the relevant entry into a `.talon-list` in the user repo
   with the override, and confirm via `help alphabet`.
4. Confirm: "Replaced spoken form for [letter/modifier]. Try saying [new
   word] to test."

If the user is uncertain which letters cause them trouble, suggest they
run through the training page (`resources/talon-training.html`) — it
surfaces problem letters quickly.

### Replace a Problem Command

**When to use:** A community command keeps misfiring or has a phrase that
collides with the user's accent or vocabulary. The wiki's recommended fix
is to find every occurrence in `.talon` files and replace the phrase with
something less ambiguous.

**Steps:**
1. Identify the command. Use `command history` to see what was actually
   recognized, or `help search <phrase>` to find which file defines it.
2. Search community for occurrences:

   ```bash
   grep -rn "the offending phrase" "$TALON_HOME/user/community/"
   ```

3. **Don't edit community.** Instead, in the user's repo, redefine the
   command with the same context header but a new spoken phrase. The
   more-specific or later-loaded definition wins; if both files have
   identical context, add a hostname matcher to the user override.
4. Confirm: "Rebound `[old phrase]` → `[new phrase]` in `<user_repo>/...`.
   The community version is unchanged so updates pull cleanly."

If the user just wants to *disable* a community command rather than rename
it, redefine it in the user repo with an empty body or a `#` no-op, with
the same caveat about context specificity.

## After Making Changes

After completing a change, briefly remind the user of the voice command
they can use next time to make similar changes themselves:

| Setting | Voice command |
|---|---|
| Vocabulary | `customize vocabulary` or `copy to vocab` |
| Words to replace | `customize words to replace` or `copy to replacements as <word>` |
| Websites | `customize websites` |
| Search engines | `customize search engines` |
| Subtitles | Edit the settings file or `customize settings` |
| System paths | Edit the settings file directly |
| Speech timeout | `customize settings` |
| Alphabet / modifier alternates | Edit the override `.talon-list` directly |
| Replace a problem command | Edit the override `.talon` file directly |

Also mention `help customize` to see all customizable files.
