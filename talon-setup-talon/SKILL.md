---
name: talon-setup-talon
description: >
  Step-by-step Talon installation, setup, and personalization for complete
  beginners on macOS. Use when the user asks to "install Talon", "set up
  Talon", "get started with voice control", "install community commands",
  "personalize settings", "customize Talon", "resume setup", "continue
  setup", "set up Rango", "install rango", or wants help with initial
  Talon configuration.
---

# Setting Up Talon Voice Control

Walk the user through every step of installing and configuring Talon from scratch on macOS. Assume zero prior experience with voice control software. Keep language friendly, jargon-free, and encouraging.

> This guide draws from the [Talon Community Wiki](https://talon.wiki/),
> a community-maintained resource for learning and troubleshooting Talon.
> When linking users to further reading, prefer wiki pages over
> paraphrasing — the wiki stays current.

**Prerequisite:** Requires Claude Code (not Cowork). Before running any
commands, resolve the Talon home directory and use absolute paths throughout:

```bash
TALON_HOME="$HOME/.talon"
mkdir -p "$TALON_HOME"
```

Claude Code can be launched from any directory — do not ask the user to
relaunch. If cwd is not `~/.talon/`, briefly note "You started Claude outside
`~/.talon/`, so I'll use absolute paths" and continue.

## Before Starting

### Step 0: Create a Profile First

Before installing anything, check whether the user already has a profile:

```bash
cat ~/.talon/talon-assistant/profile.md
```

If no profile exists, **always tell the user**: "Before we install Talon, let
me set up a quick profile so I know how much detail to give you — especially
around Git commands. This only takes a minute." Then invoke the **talon-start**
skill. The profile captures Talon, coding, and Git experience levels so this
skill can adapt its explanations — for example, a user with zero Git
experience needs every `git clone` command explained, while someone
comfortable with Git just needs the URL.

If the user specifically declines the full interview, at minimum ask about
their Git experience so you know how much to explain during the clone steps
below.

### Check Setup Progress

If the profile exists and has a `## Setup Progress` section, read it. If any
steps are already marked `done`, the user is resuming a previous session.

Also verify progress against the filesystem in case the table wasn't updated
(crash, interruption). Check:
- `$TALON_HOME/user/community/` exists → Install Talon and Community
  commands are done
- A personal repo exists under `$TALON_HOME/user/` → Personal repo is done
- `$TALON_HOME/user/rango-talon/` exists → Rango is done

If the filesystem shows a step is complete but the table still says `—`,
update the table to `done` before presenting the resume prompt.

When resuming, tell the user where they left off conversationally:

> "Looks like you've already [done steps]. Want to pick up where you left
> off with [next incomplete step], or jump to something else?"

If all steps are `—` (fresh start), proceed normally with Choose Components.

### Choose Components

Use **AskUserQuestion** to ask what to install:

```
AskUserQuestion({
  questions: [
    {
      question: "What would you like to set up?",
      header: "Components",
      multiSelect: false,
      options: [
        {
          label: "Talon + Community commands",
          description: "The core voice control system with hundreds of ready-made commands"
        },
        {
          label: "Talon + Community + Rango",
          description: "Adds browser voice control — click links, fill forms, and navigate tabs by voice"
        }
      ]
    }
  ]
})
```

### Updating Progress

After completing each step, update `~/.talon/talon-assistant/profile.md` by
changing the relevant row in the `## Setup Progress` table:
- Change `—` to `done` and add today's date
- If the user explicitly skips a step, mark it `skipped` with the date
- Use the Edit tool to update the specific row — do not rewrite the whole
  file

## Step 1: Install Talon

See also: [Talon Installation Guide](https://talon.wiki/Resource%20Hub/Talon%20Installation/installation_guide)

1. Confirm the user is on **macOS High Sierra (10.13) or later** — Talon requires this as a minimum. Apple Silicon Macs are natively supported.
2. Direct the user to download Talon from https://talonvoice.com
3. Explain that Talon is a voice control framework — it listens to speech and converts it into computer actions.
4. Walk through the macOS installation:
   - Open the downloaded `.dmg` file
   - Drag the Talon app to the Applications folder
   - Launch Talon from Applications
   - Grant macOS accessibility permissions when prompted (System Settings > Privacy & Security > Accessibility)
   - Grant microphone permission when prompted

### What Talon Looks Like When Running

**This is important to explain upfront** — Talon confuses many first-time
users because it doesn't open a window. Tell the user:

> Talon is a **background app** — it doesn't open a window or show a splash
> screen. The **only visible sign** that Talon is running is a small icon
> that appears in your **menu bar** (the strip of tiny icons at the very
> top-right of your screen, next to the clock, Wi-Fi, and battery icons).
>
> The Talon icon is small and easy to miss. Look for a new icon that wasn't
> there before — it looks like a small talon/claw shape. If you see it,
> Talon is running!
>
> If you don't see a new icon, don't worry — macOS sometimes blocks new apps
> silently. See the troubleshooting steps below.

### "Nothing happened" — First Launch Troubleshooting

If the user says nothing happened, Talon didn't open, or they can't tell if
it's running, walk through these steps **in order**:

1. **Look carefully at the menu bar** — the icon is small and could be hidden
   behind the notch on newer MacBooks. Try hovering along the top-right edge.
2. **Check if macOS blocked it** — go to **System Settings → Privacy &
   Security**, scroll down, and look for "Talon was blocked from opening."
   Click **Open Anyway** if you see this.
3. **Add permissions manually** — sometimes the permission popups don't
   appear on first launch:
   - **System Settings → Privacy & Security → Accessibility** — click the
     **+** button and add Talon from Applications
   - **System Settings → Privacy & Security → Microphone** — same thing
4. **Try right-click → Open** — go to Applications, right-click the Talon
   app, and choose **Open** instead of double-clicking. This bypasses the
   macOS Gatekeeper warning for unsigned apps.
5. **Quit and relaunch** — if you granted permissions after the first launch
   attempt, you need to fully quit Talon (if it's in the menu bar,
   right-click it → Quit) and open it again for the permissions to take
   effect.

### Speech Engine

Once Talon is confirmed running (icon visible in menu bar), the user needs to
enable the speech engine:

1. **Click the Talon icon** in your menu bar (the tiny icon at the top-right
   of your screen, near the clock)
2. A menu will drop down — select **Speech Recognition → Conformer D**
3. Talon will start downloading the speech model. A progress indicator may
   appear. This can take a few minutes depending on internet speed.
4. Once the download completes, Talon is ready to listen.

**Conformer** is Talon's built-in, high-accuracy speech engine and the
recommended choice for all users. It runs entirely on your computer — no
internet connection needed after the initial download.

> **Note for guides referencing wav2letter:** Conformer D is the current
> recommended engine and significantly more accurate than wav2letter. Dragon
> NaturallySpeaking is also supported as an alternative but is not required.

After confirming the speech engine is working, update the progress table:
mark **Install Talon** as `done`.

## Step 2: Clone the Community Command Set

The community repo provides hundreds of ready-made voice commands. It goes inside Talon's user directory.

> **No GitHub account needed.** Git is a tool that runs on your computer —
> cloning a public repository doesn't require an account.

Since Claude Code runs directly on the user's machine, **you can run these
commands for the user** — no need to ask them to open Terminal separately.
If the user's Git experience is "None" (check the profile), explain what
each command does before running it, but go ahead and execute it.

```bash
# Clone the community commands into the Talon user directory
git clone https://github.com/talonhub/community "$HOME/.talon/user/community"
```

If the user doesn't have `git` installed, help them install it:
- Typing `git` in Terminal on macOS will prompt Xcode Command Line Tools installation
- Alternatively: `xcode-select --install`

After cloning, Talon will automatically detect and load the new commands within a few seconds — no restart required.

### Verify It Worked

Tell the user to try saying:
- **"help alphabet"** — should display the spelling alphabet
- **"help active"** — should show available commands for the current app
- **"help close"** — closes the help window

If nothing happens, check:
1. Talon is running (icon in menu bar)
2. Talon is awake (say **"wake up"**)
3. The community folder is in the right location (`~/.talon/user/community/`)

To see what Talon is doing behind the scenes, check the log:
- Say **"talon open log"** (the easiest way)
- Or right-click the Talon menu bar icon → Scripting → View Log

Look for `[+]` lines (file loaded successfully) or `ERROR` lines (something needs fixing).

After verifying the community commands work, update the progress table:
mark **Community commands** as `done`.

## Step 3: Personalize the First Settings

Once Talon and the community repo are working, walk the user through
personalizing their setup conversationally. The agent collects what the user
wants and writes the files — the user just answers questions.

### Prerequisite: Personal Repo

Before writing any settings, check that the user has a personal repo:

```bash
ls "$TALON_HOME/user/" | grep -v community | grep -v rango-talon | grep -v cursorless-talon | grep -v parrot | grep -v talon-ai-tools
```

If no personal repo exists, tell the user: "Before we personalize settings,
you need a folder for your own commands and preferences. Let me set that up
first." Then invoke **talon-create-custom-repo**, mark **Personal repo** as
`done` in the progress table, and return here afterward.

### Present the Menu

Tell the user: "Talon is working. Now let's teach it about you — your
words, your websites, and how you want things to look."

Then use **AskUserQuestion** with two multi-select questions in a single
call:

```
AskUserQuestion({
  questions: [
    {
      question: "Which core settings would you like to set up?",
      header: "Core",
      multiSelect: true,
      options: [
        {
          label: "Vocabulary (Recommended)",
          description: "Words Talon doesn't know yet, like software names or technical terms"
        },
        {
          label: "Words to replace",
          description: "Words Talon hears but keeps spelling wrong, like a name with an uncommon spelling"
        },
        {
          label: "Websites",
          description: "Spoken names for sites you visit often — say 'open gmail' to go straight there"
        },
        {
          label: "Search engines",
          description: "Spoken names for searches — say 'pubmed hunt reversal learning' to search directly"
        }
      ]
    },
    {
      question: "Any additional settings?",
      header: "Additional",
      multiSelect: true,
      options: [
        {
          label: "Subtitles / display",
          description: "Control whether subtitles appear on screen, and customize font size and position"
        },
        {
          label: "System paths",
          description: "Give spoken names to folders on your computer for path-aware commands"
        }
      ]
    }
  ]
})
```

Process the selected options in the order listed above (vocabulary first,
system paths last). Skip any options the user didn't select.

### Walk Through Each Choice

Process the user's selections in order. For each one:
1. Ask a short, conversational question to collect entries
2. Write them to the correct file
3. Update the progress table in `profile.md` (mark the row `done` with
   today's date)
4. Confirm what was added
5. Move to the next choice (or ask if they want to continue)

**Important:** The agent writes the files directly. Do not ask the user to
open a text editor or edit files themselves.

If the user says "skip", "nothing right now", or "I don't have any" for an
option, mark it `skipped` in the progress table and move to the next one
without commentary.

When presenting the menu, check the progress table first. If some
personalization options are already marked `done`, show which ones are
complete and only offer the remaining options.

#### Vocabulary

**Ask:** "What words would you want Talon to recognize more reliably?
These are usually things like software names, project names, or technical
terms — anything Talon doesn't know yet. For example, if Talon keeps
stumbling on a word like `SuperWhisper`, that's a good one to add."

**After the user responds:**
- Append each word (one per line) to
  `<user_repo>/settings/vocabulary.talon-list`
- For words with specific capitalization (brand names, acronyms), use the
  `spoken: Written` format — e.g., `superwhisper: SuperWhisper` or
  `pubmed: PubMed`. For plain terms that just need recognition, use the
  word alone.
- If the file doesn't exist, create it with header `list: user.vocabulary`
  followed by a `-` separator line, then the entries
- Check the existing file first to avoid adding duplicates
- Confirm: "Added [words]. Talon will pick these up automatically — no
  restart needed. Try saying one of the new words to verify."

#### Words to Replace

**Ask:** "What words does Talon keep getting wrong for you? This is for
words Talon hears correctly but spells the wrong way. For example, if
someone's name is spelled `Ryon` but Talon always writes `Ryan`, you'd
add that here."

**After the user responds:**
- Append each pair as `correct,incorrect` to
  `<user_repo>/settings/words_to_replace.csv`
- **Column order matters:** the word you *want* written comes first, the
  misrecognized spelling comes second. For example, `Ryon,Ryan` means
  "when Talon writes Ryan, replace it with Ryon."
- Check the existing file first to avoid adding duplicates
- Confirm: "Added [pairs]. Next time Talon hears [incorrect], it'll write
  [correct] instead."

#### Websites

**Ask:** "What websites would you want to open by voice? Give me a short
name and the URL for each one. Once they're added, you can say things like
`open gmail` and the browser will go straight there."

**After the user responds:**
- Append each entry as `spoken name: https://...` to the websites
  `.talon-list` file in the user's settings
- Confirm: "Added [sites]. Try saying `open [name]` to test it."

**Note:** Check both the community defaults and the user's existing personal
settings before adding duplicates. Community defaults are at:
`$TALON_HOME/user/community/core/websites_and_search_engines/website.talon-list`
(includes gmail, github, youtube, google, wikipedia, etc.)

**URL lookup:** The user will often just give a name (e.g. "Notion") without
the URL. Look up or construct the URL yourself — don't make them find it.
For example, "Notion" → `https://notion.so`.

#### Search Engines

**Ask:** "Are there any searches you use a lot that you'd want to run by
voice? The community already includes google, amazon, scholar, wiki, and
map. But if you use something like PubMed or Stack Overflow, you could add
those — then you'd say something like `pubmed hunt reversal learning` and
it opens the search results."

**After the user responds:**
- Check both community defaults and the user's existing personal settings
  to avoid adding duplicates
- Append each entry as `spoken name: https://...%s` to the search engines
  `.talon-list` file in the user's settings
- Confirm: "Added [engines]. Try saying `[name] hunt [your query]` to
  test it."

**URL construction:** The user will usually just say a name like "PubMed" or
"Stack Overflow." Construct the search URL yourself — the `%s` is where the
query goes. For example, "PubMed" →
`https://pubmed.ncbi.nlm.nih.gov/?term=%s`.

#### Subtitles / Display Preferences

**Ask:** "Do you want subtitles on, off, or adjusted? There are two
subtitle systems: Talon's built-in subtitles (toggled from the Talon menu
bar), and a community plugin that's more customizable — you can change the
font size and position on screen."

**Based on the user's response:**
- If **off entirely:** Create or update a `.talon` file with a
  `settings():` block setting `user.subtitles_show = false`. Mention they
  can also turn off Talon's built-in subtitles from the menu bar under
  Speech Recognition → Show Subtitles. **Always mention** that if they
  change their mind later, the community plugin can be adjusted rather
  than just on/off — for example, they could make the text smaller or
  move it to a different position on screen (`user.subtitles_size` and
  `user.subtitles_y`).
- If **adjust:** Ask what they want to change (size, position), then set
  the relevant settings (`user.subtitles_size`, `user.subtitles_y`) in a
  `.talon` file with a `settings():` block.
- Confirm what was changed.

#### System Paths

**Ask:** "System paths let you give spoken names to folders on your
computer, so path-aware commands can use them. What folders would you want
to refer to by voice? Give me a short name and the full path for each."

**After the user responds:**
- Append each entry as `spoken name: /full/path` to
  `<user_repo>/settings/system_paths-<hostname>.talon-list`
- If the file doesn't exist, create it with header
  `list: user.system_paths` followed by a `-` separator line, then the
  entries
- Confirm: "Added [paths]."

### After Each Option

After completing an option, if the user had more choices queued up, move to
the next one. If they've finished all their choices, ask:

> "Want to set up any of the others, or are you good for now?"

### Voice Commands for Customizing Settings Later

Once personalization is complete, let the user know they can update these
settings anytime by voice — no need to ask the assistant again. The
community repo includes built-in commands for this:

| What to say | What it does |
|---|---|
| `help customize` | Shows a list of all files you can customize by voice |
| `customize vocabulary` | Opens the vocabulary file in your text editor |
| `customize words to replace` | Opens the words-to-replace file in your text editor |
| `customize websites` | Opens the websites list in your text editor |
| `customize search engines` | Opens the search engines list in your text editor |
| `customize settings` | Opens the main settings file in your text editor |

There are also quick-add commands you can use while working — just select
some text and say:

| What to say | What it does |
|---|---|
| `copy to vocab` | Adds the selected text to vocabulary |
| `copy to vocab as <word>` | Adds the selected text with a specific spoken form |
| `copy name to vocab` | Adds the selected text as a name (includes possessive form) |
| `copy to replacements as <word>` | Adds the selected text as a word replacement |

These are especially handy for vocabulary — if Talon stumbles on a word in
something you're reading, just select it and say `copy to vocab`.

## Step 4: Install Rango (Optional — Browser Voice Control)

Only proceed if the user opted for Rango in the initial question.

Rango adds clickable letter hints to web pages so the user can navigate browsers entirely by voice.

### Install the Browser Extension

Direct the user to install Rango from their browser's extension store:
- **Chrome**: Search "Rango" in the Chrome Web Store
- **Firefox**: Search "Rango" in Firefox Add-ons
- **Safari**: Search "Rango" in the App Store (macOS); then enable in Safari > Preferences > Extensions
- **Edge**: Search "Rango" in the Microsoft Edge Add-ons store

### Install Rango's Talon Commands

Run this directly (Claude Code has terminal access):

```bash
git clone https://github.com/david-tejada/rango-talon "$HOME/.talon/user/rango-talon"
```

Talon will auto-load the new commands. The user should now see small letter hints overlaid on clickable elements in their browser.

### Verify Rango

Tell the user to:
1. Open their browser and navigate to any webpage
2. Look for small letter labels on links and buttons
3. Say the letters to click — for example, **"air cap"** clicks the element labeled "ac"

After verifying Rango works, update the progress table: mark **Rango** as
`done`. If the user skipped Rango, mark it `skipped`.

## Step 5: Learn the Basics

See also: [Basic Usage](https://talon.wiki/Basic%20Usage/basic_usage)

Point the user to these essential first commands:

| What to say | What it does |
|---|---|
| `wake up` | Start listening |
| `go to sleep` | Stop listening |
| `help alphabet` | Show the spelling alphabet |
| `help active` | Show commands for current app |
| `help search <phrase>` | Search for a specific command |
| `command history` | See recent commands |
| `undo that` | Undo the last action |

Recommend learning order: alphabet first, then keys and symbols, then formatters (like `snake hello world` to type `hello_world`), then mouse and editor commands.

This plugin also includes an interactive training page for practicing the alphabet, spelling, numbers, symbols, and formatters in the browser. Tell the user they can ask to "open the training page" anytime to try it — it's at `resources/talon-training.html`.

### Why a Command Might Not Work

This is a common sticking point for new users — explain it proactively,
but keep it short. Lead with the key insight and the three most likely
causes. Hold the rest back unless the user is actually having trouble.

**What to tell the user upfront:**

> Two things to know about how Talon works. First, Talon only responds to
> commands that exist — if you say something that isn't a defined command,
> nothing happens. No error, no feedback, just silence. Second, Talon can
> sometimes misrecognize what you said as a similar-sounding command, which
> can cause something unexpected to happen.
>
> If a command isn't working, the three most common reasons are:
>
> 1. **The command doesn't exist** — say `help search <word>` to find
>    commands, or `help active` to see what's available
> 2. **Talon is asleep** — say `wake up`
> 3. **Wrong app** — some commands only work in specific apps
>
> If you run into trouble, let me know and I can help diagnose it.

**If the user reports a problem**, consult `references/troubleshooting.md`
for additional causes — microphone issues, wrong mode, speech timeout,
and more.

### Checking the Log

Anytime the user wants to see what Talon is doing — whether something isn't working or they're just curious — show them how to check the log:

- Say **"talon open log"** (the easiest way)
- Or right-click the Talon menu bar icon → Scripting → View Log

The log shows when files load (`[+]`), errors to fix (`ERROR`), and which commands are active. This is the first tool to reach for when debugging.

After covering the basics, update the progress table: mark **Learn the
basics** as `done`.

## Troubleshooting

Consult `references/troubleshooting.md` for common setup issues and their solutions.
