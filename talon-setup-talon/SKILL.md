---
name: talon-setup-talon
description: >
  Step-by-step Talon installation, setup, and personalization for complete
  beginners. Best supported on macOS; Linux and Windows are supported via
  brief install branches that route to the Talon Community Wiki for the
  platform-specific details. Use when the user asks to "install Talon",
  "set up Talon", "get started with voice control", "install community
  commands", "personalize settings", "customize Talon", "resume setup",
  "continue setup", "set up Rango", "install rango", or wants help with
  initial Talon configuration.
---

# Setting Up Talon Voice Control

Walk the user through every step of installing and configuring Talon from scratch. Assume zero prior experience with voice control software. Keep language friendly, jargon-free, and encouraging.

**Platform support.** Talon runs on macOS, Linux, and Windows. This skill
walks macOS users through every step in detail. For Linux and Windows
users the install path differs significantly — those branches give the
essentials and route to the wiki for full instructions, then rejoin the
common steps (community clone, personalization).

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

Explain to the user: Talon is a voice control framework — it listens to
speech and converts it into computer actions.

Before installing, **read the OS** from
`~/.talon/talon-assistant/profile.md` (set during talon-start). Then
follow the matching branch below.

### Branch A: macOS (detailed walkthrough)

1. Confirm the user is on **macOS High Sierra (10.13) or later** — Talon requires this as a minimum. Apple Silicon Macs are natively supported.
2. Direct the user to download Talon from https://talonvoice.com
3. Walk through the macOS installation:
   - Open the downloaded `.dmg` file
   - Drag the Talon app to the Applications folder
   - Launch Talon from Applications
   - Grant macOS accessibility permissions when prompted (System Settings > Privacy & Security > Accessibility)
   - Grant microphone permission when prompted

The macOS-specific "first launch troubleshooting", menu bar icon
explanation, and speech-engine sections below all apply to this branch.

### Branch B: Linux

The Linux install path differs by distro and isn't fully scripted in
this skill. The wiki has the up-to-date instructions for each
distribution:

- **Wiki page:** [Talon Installation — Linux](https://talon.wiki/Resource%20Hub/Talon%20Installation/installation_guide) — WebFetch this and walk the user through the steps that match their distro.

Key differences from macOS:

- Talon ships as a `.tar.xz` archive (and sometimes `.deb` / `.AppImage`); extract it under `~/.talon-bin/` or similar and add `talon` to the user's PATH.
- There is no Applications folder or Gatekeeper. Launch from a terminal (`talon &`) or from the user's DE app menu after installing the `.desktop` file the archive ships with.
- The "menu bar icon" is a status-bar / system-tray icon, depending on the desktop environment (GNOME, KDE, etc.). On GNOME, the user may need the AppIndicator extension to see it.
- Microphone and accessibility permissions are not gated like macOS — they're managed at the PulseAudio / PipeWire and X11 / Wayland layer. Default install usually works without extra setup.

After Talon is running and the tray icon is visible, skip ahead to the
**Speech Engine** subsection below — the menu interaction is the same.

### Branch C: Windows

- **Wiki page:** [Talon Installation — Windows](https://talon.wiki/Resource%20Hub/Talon%20Installation/installation_guide) — WebFetch this and walk the user through.

Key differences from macOS:

- Talon ships as a `.msi` installer; run it as the user's regular account (not Administrator).
- The user's Talon directory is `%AppData%\Talon\` rather than `~/.talon/`. **All commands and file paths below that use `$HOME/.talon` or `~/.talon` need to be translated to the Windows equivalent.** When the agent is helping a Windows user, prefer PowerShell (`$env:APPDATA\Talon\...`) and remember Talon's REPL lives at `%AppData%\Talon\bin\repl.exe`.
- After installing, Talon appears as a **system tray icon** (bottom-right, near the clock), not a menu bar icon.
- Microphone permissions are handled in Windows Settings → Privacy & Security → Microphone — allow desktop apps.

After Talon is running and the tray icon is visible, skip ahead to the
**Speech Engine** subsection below — the menu interaction is the same
once the icon is visible.

### macOS-specific subsections (skip on Linux / Windows)

The following three subsections — "What Talon Looks Like When Running",
"Nothing happened — First Launch Troubleshooting", and the menu-bar
phrasing in the **Speech Engine** section — are written for macOS users.
On Linux or Windows, adapt the tray-icon and permission language to the
user's platform (system tray on Windows, status-bar icon on Linux) and
fall back to the wiki troubleshooting page if anything is unclear:
[Talon Troubleshooting](https://talon.wiki/Resource%20Hub/Speech%20Recognition/troubleshooting).

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
# Clone the community commands into the Talon user directory (macOS / Linux)
git clone https://github.com/talonhub/community "$HOME/.talon/user/community"
```

**Windows users:** the equivalent target is `%AppData%\Talon\user\community`.
In PowerShell:

```powershell
git clone https://github.com/talonhub/community "$env:APPDATA\Talon\user\community"
```

If the user doesn't have `git` installed, help them install it. Install
instructions depend on OS:

- **macOS:** typing `git` in Terminal prompts the Xcode Command Line Tools install. Alternatively run `xcode-select --install`.
- **Linux:** use the system package manager — `sudo apt install git`, `sudo dnf install git`, or `sudo pacman -S git`.
- **Windows:** download from <https://git-scm.com/download/win>.

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

### Walk Through Each Choice — Delegate to talon-customize-settings

The per-setting logic — file paths, duplicate-checking against
community defaults, URL construction, list-header creation, and the
matching Setup Progress row update — all lives in
**talon-customize-settings**. Do not duplicate that logic here. For
each option the user picked, run the customize-settings flow for that
setting type, then come back here for the next one.

**Process options in this order** (most-impactful first):

1. Vocabulary
2. Words to replace
3. Websites
4. Search engines
5. Subtitles / display
6. System paths

**Onboarding-specific behaviour to layer over the customize-settings
flow:**

- **Pre-flight the menu.** Before showing the AskUserQuestion menu above,
  re-read the Setup Progress table. If any personalization rows are
  already `done` from an earlier attempt, surface that and only offer
  the remaining options.
- **Give a beginner-friendly example before delegating.** This is most
  users' first time and they often don't know what to add. Before
  running customize-settings for a given option, offer an example so
  the user has something concrete to react to. Examples to use:
  - **Vocabulary:** "Things like software names, project names, or
    technical terms — anything Talon doesn't know yet. If Talon keeps
    stumbling on a word like `SuperWhisper`, that's a good one to add."
  - **Words to replace:** "Words Talon hears correctly but spells the
    wrong way. For example, if someone's name is spelled `Ryon` but
    Talon always writes `Ryan`, you'd add that here."
  - **Websites:** "Sites you'd want to open by voice — say `open
    gmail` to go straight there. Just give a short name; I'll look up
    the URL."
  - **Search engines:** "Searches you use a lot — say `pubmed hunt
    reversal learning` and it opens the results. Community already
    has google, amazon, scholar, wiki, and map."
  - **Subtitles:** "Talon's built-in subtitles are on/off from the
    menu bar; the community plugin is more customizable (font size,
    on-screen position). Do you want subtitles off, or adjusted?"
  - **System paths:** "Spoken names for folders on your computer —
    short name plus the full path. Useful for path-aware commands."
- **Hand off the user's answer to customize-settings.** Once you have
  the entries the user wants to add, run the customize-settings flow
  for that setting with the entries already collected — don't make
  customize-settings re-ask.
- **Handle "skip" without delegating.** If the user says "skip" /
  "nothing right now" / "I don't have any" for an option, mark the
  matching row `skipped` in the progress table and move on without
  invoking customize-settings for that option.
- **The agent writes files directly.** Never ask the user to open a
  text editor. (customize-settings already enforces this — repeated
  here for clarity.)

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
| `mouse grid` | Show a numbered grid for clicking without a mouse |
| `touch` | Left click |
| `righty` | Right click |
| `scroll down` / `scroll up` | Scroll the page |

Recommend learning order: alphabet first, then keys and symbols, then formatters (like `snake hello world` to type `hello_world`), then mouse and editor commands.

This plugin also includes an interactive training page for practicing the alphabet, spelling, numbers, symbols, and formatters in the browser. Tell the user they can ask to "open the training page" anytime to try it — it's at `resources/talon-training.html`.

Also mention the [Talon Slack](https://talonvoice.com/chat) — it's the
main place to get help from other Talon users. The `#help` channel is
active and welcoming. Let the user know they can join anytime if they
get stuck or want to learn from others.

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

### What's Next

After covering the basics, briefly mention what the user can explore next.
Keep it short — just plant the seeds, don't overwhelm.

> You're set up. As you get comfortable, here are some things worth
> exploring:
>
> - **Better microphone** — a good mic makes a big difference in
>   accuracy. See the [Hardware Guide](https://talon.wiki/Resource%20Hub/Hardware/)
>   for recommendations at every budget.
> - **Cursorless** — structural code editing by voice, if you write code.
> - **Eye tracking** — combine with Talon for hands-free mouse control.
>
> The full list is at [Essential Tools](https://talon.wiki/Integrations/essential-tools)
> on the wiki.

After covering the basics, update the progress table: mark **Learn the
basics** as `done`.

## Troubleshooting

Consult `references/troubleshooting.md` for common setup issues and their solutions.
