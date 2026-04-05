---
name: talon-setup-talon
description: >
  Step-by-step Talon installation and setup for complete beginners on macOS.
  Use when the user asks to "install Talon", "set up Talon", "get started
  with voice control", "install community commands", "set up Rango",
  "install rango", or wants help with initial Talon configuration.
---

# Setting Up Talon Voice Control

Walk the user through every step of installing and configuring Talon from scratch on macOS. Assume zero prior experience with voice control software. Keep language friendly, jargon-free, and encouraging.

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

### Choose Components

Ask which components the user wants to set up using AskUserQuestion:

- **Talon + Community commands** (recommended minimum)
- **Talon + Community + Rango** (adds browser voice control)

## Step 1: Install Talon

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

## Step 3: Install Rango (Optional — Browser Voice Control)

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

## Step 4: Learn the Basics

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

### Checking the Log

Anytime the user wants to see what Talon is doing — whether something isn't working or they're just curious — show them how to check the log:

- Say **"talon open log"** (the easiest way)
- Or right-click the Talon menu bar icon → Scripting → View Log

The log shows when files load (`[+]`), errors to fix (`ERROR`), and which commands are active. This is the first tool to reach for when debugging.

## Troubleshooting

Consult `references/troubleshooting.md` for common setup issues and their solutions.
