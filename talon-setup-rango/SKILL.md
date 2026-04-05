---
name: talon-setup-rango
description: >
  Walk the user through installing and configuring Rango, the browser
  voice-control extension for Talon. Use when the user asks to "set up
  Rango", "install Rango", "use voice control in the browser", "click
  links with my voice", or wants to navigate websites hands-free.
---

# Setting Up Rango for Browser Voice Control

Guide the user through installing the Rango browser extension and its Talon integration so they can click links, navigate tabs, scroll pages, and fill forms entirely by voice. Assume Talon and the community command set are already installed. No programming experience is required.

**Prerequisite:** Requires Claude Code (not Cowork) for filesystem and git
access. Use absolute paths (`$HOME/.talon/user/...`) for all file operations
and commands. Claude Code can be launched from any directory — do not ask the
user to relaunch.

<!-- SYNC: This "Discover Repo & Load Profile" block is shared with
     talon-create-basic-command, talon-create-python-command, and talon-create-custom-repo.
     Keep all four copies in sync when editing. -->

## Discover Repo & Load Profile (FIRST STEP — do both before anything else)

1. **Find the user's custom repo.** List `~/.talon/user/` and identify the folder that is NOT `community`, `rango-talon`, `cursorless-talon`, `parrot`, or any other well-known shared repo. The remaining folder is the user's personal repo (e.g., `talon-rebecca`, `talon-john`, `my-commands`, etc.).

   ```bash
   ls ~/.talon/user/
   ```

   Store this name and use it everywhere this skill says `<user_repo>`. If you can't determine the repo name, ask the user: "What's the name of your personal Talon commands folder?"

2. **Load the profile.** Immediately after discovering the repo, read the profile:

   ```bash
   cat ~/.talon/talon-assistant/profile.md
   ```

   If the file exists, adapt your explanations for the rest of this session:
   - **Beginner (Talon):** Explain each concept step by step. Spell out what voice commands will do before suggesting them.
   - **Intermediate (Talon):** Skip basic explanations; focus on setup steps and useful commands.
   - **Advanced (Talon):** Be concise — just the install steps and command highlights.
   - **None / Basic (Coding):** Avoid jargon; explain any technical concepts used.
   - **None (Git):** Don't include Git commands without explaining them first.

   If no profile exists, mention: "I don't see a profile yet — you can run the **talon-start** skill to set one up, but we can keep going for now." Then default to intermediate-level explanations.

## Section 1 — Installation

Walk the user through two parts: the browser extension and the Talon-side commands.

### 1a. Install the Browser Extension

Rango is available for all major browsers. Have the user install from their browser's extension store:

- **Chrome / Brave / Edge / Vivaldi / Opera** — Search "Rango" in the Chrome Web Store, or visit [rango.click](https://rango.click) and follow the install link.
- **Firefox** — Search "Rango" in Firefox Add-ons.
- **Safari** — Available on the Mac App Store. After installing, the user must **also** enable it in Safari → Settings → Extensions → check "Rango". Safari uses a different keyboard shortcut (`Ctrl-Shift-3` instead of `Ctrl-Shift-Insert`), but this is handled automatically by rango-talon.

After installing, the user should see small letter hints overlaid on clickable elements when they visit any web page. If hints don't appear, have them click the Rango extension icon and confirm it's enabled.

### 1b. Install rango-talon (the Voice Commands)

The Rango extension alone only shows hints — the *voice commands* come from the `rango-talon` repository. Have the user clone it into their Talon user directory:

```bash
cd ~/.talon
git clone https://github.com/david-tejada/rango-talon.git user/rango-talon
```

Talon will auto-reload and pick up the new commands within a few seconds. No restart is needed.

### 1c. Verify It Works

Have the user open any web page in their browser and try:

1. **Look for hints** — Small one- or two-letter labels should appear on links and buttons.
2. **Say a hint** — For example, say `air` (the letter A) if a link is labeled "A". The link should be clicked.
3. **Say `upper`** — The page should scroll up.

If hints appear and clicking works, Rango is set up correctly. If not, check:
- The extension is enabled (click its toolbar icon).
- The `rango-talon` folder is inside `~/.talon/user/`.
- The Talon log (`Scripting → View Log`) shows no errors related to rango.

## Section 2 — Your First 15 Minutes

Once installation is verified, walk the user through everyday commands so they can start browsing immediately. Present these as a natural flow, not a reference list.

### Clicking Things

Rango works in **direct clicking mode** by default — just say the hint letters to click:

| You say | What happens |
|---|---|
| `air` | Clicks the element labeled "A" |
| `bat bat` | Clicks "BB" |
| `air and bat` | Clicks both A and B in sequence |

If the user prefers to say "click" before each hint, they can switch to explicit mode with `rango explicit`. Switch back with `rango direct`.

### Opening in New Tabs

| You say | What happens |
|---|---|
| `blank air` | Opens link "A" in a new foreground tab |
| `stash air` | Opens link "A" in a background tab |

### Navigating Tabs

| You say | What happens |
|---|---|
| `tab back` | Switches to the previously focused tab |
| `tab hunt gmail` | Finds and switches to a tab containing "gmail" |
| `go tab air` | Switches to the tab whose marker is "A" |

### Scrolling

| You say | What happens |
|---|---|
| `downer` | Scrolls down one unit |
| `downer three` | Scrolls down three units |
| `upper` | Scrolls up one unit |
| `downer all` | Scrolls to the bottom of the page |
| `upper all` | Scrolls to the top |
| `tiny down` / `tiny up` | Small scroll nudges |

### Snap Scrolling

These are especially useful for reading long articles or scanning search results:

| You say | What happens |
|---|---|
| `crown air` | Scrolls so element "A" is at the top of the viewport |
| `center air` | Scrolls so element "A" is centered |
| `bottom air` | Scrolls so element "A" is at the bottom |

### Showing Link Destinations

| You say | What happens |
|---|---|
| `show air` | Displays where link "A" leads |
| `hover air` | Hovers over element "A" (reveals tooltips, dropdowns) |
| `dismiss` | Clears all hover states |

### Copying

| You say | What happens |
|---|---|
| `copy air` | Copies the URL of link "A" |
| `copy text air` | Copies the visible text of element "A" |
| `copy mark air` | Copies as a Markdown link `[text](url)` |
| `copy page address` | Copies the current page URL |

### Working with Forms

| You say | What happens |
|---|---|
| `go input` | Focuses the first input field on the page |
| `focus air` | Focuses the specific input labeled "A" |
| `paste to air` | Pastes clipboard contents into input "A" |
| `change air` | Selects all text in input "A" (ready to overwrite) |

## Section 3 — Common Settings (Q&A Format)

Present these as answers to questions the user is likely to have. Don't dump them all at once — offer them when relevant or if the user asks about customization.

### "The hints are too small / too big"

Say `hint bigger` or `hint smaller` to adjust hint size. This takes effect immediately and persists across page loads.

### "I want to hide hints on a specific site"

Say `hints off host` to disable hints on the current domain (e.g., all of youtube.com). Other levels are available:

- `hints off page` — Just this URL
- `hints off tab` — Just this tab
- `hints off now` — Temporarily, until you navigate away
- `hints off` (no level) — Everywhere, globally

Re-enable with `hints on` plus the same level, e.g. `hints on host`. Check what's currently toggled with `toggle show`.

### "I want to say 'click' before each hint instead of just the letters"

Say `rango explicit` to switch to explicit clicking mode. You'll then say `click air` instead of just `air`. Switch back with `rango direct`.

### "I'd prefer number hints instead of letters"

Add this line to a `.talon` file in your personal commands folder (e.g., `talon-yourname/rango_settings.talon`):

```talon
tag(): user.rango_number_hints
```

With number hints, say the number directly: `five`, `twelve`, etc. When targeting multiple hints, use "plus" instead of "and": `five plus twelve`.

### "Single-letter hints keep triggering accidentally"

Say `hint exclude singles` to remove all one-letter hints, leaving only two-letter combinations. This reduces accidental activations. Undo with `hint include singles`.

Or set it permanently in a `.talon` file:

```talon
tag(): user.rango_exclude_singles
```

### "How do I control scroll speed?"

Each `upper` or `downer` command scrolls by a fixed viewport fraction. Say a number after the command to multiply: `downer five` scrolls five times the normal amount. For fine control, use `tiny up` and `tiny down` (about one-fifth of a normal scroll).

### "Can I scroll a sidebar or panel instead of the main page?"

Yes — for pages with left/right aside panels:

- `upper left` / `downer left` — Scrolls the left panel
- `upper right` / `downer right` — Scrolls the right panel

For any scrollable element, target it directly: `downer air` scrolls the container at hint "A".

### "How do I save a frequently used element?"

Use references to bookmark elements by name:

- `mark air as search` — Saves element "A" with the name "search"
- `click mark search` — Clicks the saved reference
- `mark show` — Lists all saved references
- `mark clear search` — Removes the saved reference

## External Resources

Always link the user to these when appropriate:

- **Rango documentation**: [rango.click](https://rango.click)
- **Rango GitHub**: [github.com/david-tejada/rango](https://github.com/david-tejada/rango)
- **rango-talon commands**: [github.com/david-tejada/rango-talon](https://github.com/david-tejada/rango-talon)
- **Practice in the browser**: [Talon Practice — Browser Lesson](https://chaosparrot.github.io/talon_practice/lessons/browser.html) — An interactive drill page where you practice Rango commands on a live web page with guided prompts.
- **Full command reference**: See `references/rango-commands.md` in this skill for every available voice command.
