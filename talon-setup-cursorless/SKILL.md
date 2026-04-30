---
name: talon-setup-cursorless
description: >
  Walk the user through installing and configuring Cursorless, the
  Talon-powered structural code editor for VSCode. Use when the user asks
  to "set up Cursorless", "install Cursorless", "edit code by voice",
  "voice control VSCode", "navigate code with voice", or wants
  hat-and-target-style code editing in VSCode (and Cursor / VSCodium /
  Code OSS, which are compatible). Assumes Talon and the community repo
  are already installed; if not, route to talon-setup-talon first.
---

# Setting Up Cursorless for Voice Coding in VSCode

Cursorless is the most powerful voice-coding tool in the Talon ecosystem.
Instead of moving a cursor and selecting text manually, the user *names*
on-screen targets ("hats" — colored, shaped marks above letters) and
applies actions to them: `take air`, `chuck blue bat`, `bring funk cap`.
This skill installs the pieces, verifies the setup, and gives the user
their first 15 minutes of working commands.

> Based on the [Cursorless docs](https://www.cursorless.org/docs/) and
> the [Talon Community Wiki](https://talon.wiki/Integrations/essential-tools).
> When linking the user to further reading, prefer cursorless.org over
> paraphrasing — it stays current and the in-app `cursorless cheatsheet`
> is the canonical command reference.

**Prerequisite:** Requires Claude Code (not Cowork) for filesystem and git
access. Use absolute paths (`$HOME/.talon/user/...`) for all file
operations and commands. Claude Code can be launched from any directory —
do not ask the user to relaunch.

<!-- SYNC: This "Discover Repo & Load Profile" block is shared with
     talon-create-command, talon-setup-rango, talon-setup-cursorless,
     and talon-test-and-debug. talon-create-custom-repo runs a related
     but distinct check (existing-repo discovery). Keep all copies in
     sync when editing. Cursorless adds skill-specific proficiency tips
     because it has a steeper learning curve than the others. -->

## Discover Repo & Load Profile (FIRST STEP — do both before anything else)

1. **Find the user's custom repo.** List `~/.talon/user/` and identify the
   folder that is NOT `community`, `rango-talon`, `cursorless-talon`,
   `parrot`, or any other well-known shared repo.

   ```bash
   ls ~/.talon/user/
   ```

   Store this name and use it everywhere this skill says `<user_repo>`. If
   unclear, ask the user once.

2. **Load the profile.**

   ```bash
   cat ~/.talon/talon-assistant/profile.md
   ```

   Adapt explanations to the user's proficiency:
   - **Beginner (Talon):** Walk through the mental model carefully.
     Cursorless has a learning curve — explain hats, marks, and the
     action+target structure before showing commands.
   - **Intermediate (Talon):** Skip the basics; focus on install steps and
     the first-15-minutes tour.
   - **Advanced (Talon):** Be concise — install steps, point at the
     cheatsheet, suggest customization paths.
   - **None / Basic (Coding):** Avoid jargon; explain what tree-sitter,
     scopes, and parse trees mean in plain language.
   - **None (Git):** Don't run git commands without explaining them first.

   If no profile exists, offer to run **talon-start** quickly (then resume
   this skill automatically), or default to intermediate-level
   explanations.

## Pre-flight: Confirm Talon and Community

Cursorless rides on Talon and the community repo. Verify both are present
before going further:

```bash
[ -x "$HOME/.talon/bin/repl" ] && echo "talon: ok" || echo "talon: missing"
[ -d "$HOME/.talon/user/community" ] && echo "community: ok" || echo "community: missing"
```

If either is missing, stop and route to **talon-setup-talon** — it
handles the base install and community clone. Once that's done, return
to this skill.

## Section 1 — What Cursorless Adds

Before installing, give the user the mental model. They'll get more out
of the install if they understand what they're getting.

### The Hat System

Cursorless paints small colored, shaped marks ("hats") above letters
across the visible code. Every visible token gets a hat. The user names
a target by saying the **shape** + **color** + **letter phonic**:

- `air` — the gray dot over an `a`
- `blue bat` — the blue dot over a `b`
- `fox cap` — the fox-shape over a `c`

Color and shape are optional — if a letter is unique on screen, the
phonic alone is enough.

### Action + Target

Every Cursorless command is structured: **`<action> <target>`**.

| Spoken | What happens |
|---|---|
| `take air` | Selects the token under the gray-`a` hat |
| `chuck air` | Deletes that token |
| `bring blue bat` | Replaces the *current* selection with the blue-`b` token |

Targets can be expanded by **scope modifiers** (`funk air` = the whole
function containing the `a`-token), **relative position** (`take next
funk`), and **ranges** (`take air past blue bat`).

### Why VSCode

Cursorless plugs into VSCode's parse tree (via tree-sitter) to understand
code structure. That's why "the function" or "the argument" or "the
string" work as targets. It only runs in VSCode-family editors today —
VSCode itself, Cursor, VSCodium, and Code OSS all work; other editors
are not yet supported.

## Section 2 — Installation

Cursorless install is six steps. The first two are already done if the
pre-flight check passed; the rest are below.

### 2a. Install VSCode (if missing)

Check whether VSCode is installed:

```bash
command -v code >/dev/null && echo "vscode: ok" || echo "vscode: missing"
```

If missing, point the user at <https://code.visualstudio.com>. **Cursor**
and **VSCodium** users can skip this — both are drop-in compatible.

### 2b. Install the Talon VSCode Extension Pack

This is `pokey.talon` — the bundle that bridges Talon and VSCode (it
includes the command-server extension Cursorless relies on).

```bash
code --install-extension pokey.talon
```

If `code` isn't on PATH, tell the user to install it from VSCode's
**Extensions** sidebar by searching for `Talon`.

### 2c. Install the Cursorless Extension

```bash
code --install-extension pokey.cursorless
```

Or via the marketplace search: `Cursorless`.

### 2d. Clone cursorless-talon

This is the Talon-side voice command set. It lives in the Talon user
directory alongside `community/` and `rango-talon/`:

```bash
git clone https://github.com/cursorless-dev/cursorless-talon.git \
  "$HOME/.talon/user/cursorless-talon"
```

**Windows path:** `%AppData%\Talon\user\cursorless-talon` (use the same
`git clone` URL but in PowerShell or cmd with the Windows path).

### 2e. Restart Talon

Cursorless is one of the few additions that needs a Talon restart (the
extension and Talon need to handshake on first load). Right-click the
Talon menu bar icon → **Restart**, or quit and relaunch.

## Section 3 — Verify Installation

Walk the user through three checks:

1. **Open any code file in VSCode.** Hats should appear above most
   visible characters within a second or two. Different letters get
   different colors and shapes — that's normal and intentional.

2. **Try selecting.** Pick a visible letter, say `take <phonic>` (e.g.,
   `take air` if there's a gray `a` hat). The token under that hat
   should highlight.

3. **Try deleting.** Type some throwaway code, then `chuck <phonic>`
   on a token. It should disappear.

If hats don't appear:
- Make sure the Cursorless extension is **enabled** (Extensions sidebar
  in VSCode).
- Check the Talon log (`talon open log`) for errors mentioning
  `cursorless` or `command-server`.
- Confirm the `cursorless-talon` folder is at
  `~/.talon/user/cursorless-talon/` (not nested deeper).
- Try toggling hats off/on with `hats off` / `hats on`.

If hats appear but commands don't fire, the most common cause is the
command-server bridge not connecting — restart VSCode *and* Talon.

## Section 4 — Your First 15 Minutes

Once the verify steps pass, walk the user through everyday commands so
they can start coding immediately. Don't dump the cheatsheet — pick the
working subset below and let them try each one.

### Always-Available: The Cheatsheet

Tell the user upfront: **`cursorless cheatsheet`** opens an in-browser,
always-current command reference filtered to their actual configured
spoken forms. This is the canonical reference — `help search` and the
docs come second.

### Selecting and Deleting

| You say | What happens |
|---|---|
| `take <hat>` | Selects the token under the hat |
| `chuck <hat>` | Deletes the token |
| `take air past blue bat` | Selects the range from one hat to another |

### Replacing One Thing With Another

`bring` is the headline action — it replaces the current selection (or
a target) with the contents of another target:

| You say | What happens |
|---|---|
| `bring <hat>` | Replaces current selection with that hat's token |
| `bring air to blue bat` | Replaces the blue-`b` token with the gray-`a` token |

### Scope Modifiers

Expand a hat-target into a larger code unit:

| Modifier | Means | Example |
|---|---|---|
| `funk` | The named function containing the target | `take funk air` |
| `arg` | The argument or parameter | `chuck arg blue bat` |
| `line` | The whole line | `take line air` |
| `block` | The block (if/for/while body, etc.) | `chuck block air` |

Other scopes — `class`, `string`, `comment`, `value`, `key`, `item`,
`name`, `type`, `state` (statement) — work the same way. The
cheatsheet lists them all.

### Relative Position

You can target by position rather than hat:

| You say | What happens |
|---|---|
| `take next funk` | Selects the next function from the cursor |
| `take last arg` | Selects the previous argument |
| `take every arg` | Selects every argument in the current call |
| `take first line block` | Selects the first line of the current block |

### Inserting Around a Target

| You say | What happens |
|---|---|
| `pre <hat>` | Move cursor *before* the target |
| `post <hat>` | Move cursor *after* the target |
| `drink <hat>` | Insert a new line *above* the target's line, cursor there |
| `pour <hat>` | Insert a new line *below* the target's line, cursor there |

### Snippets

If the user has the community snippets installed (the talonhub/community
repo includes them), Cursorless can wrap targets in a snippet:

```
snip funk         # insert a function snippet at cursor
snip funk air     # wrap the target in a function snippet
```

Mention this lightly — `snip` is a separate community feature that pairs
beautifully with Cursorless but isn't strictly Cursorless.

### A Practical Sequence

End the tour with a chained example so the user feels the speed:

> Say you want to extract a hard-coded string into a variable. Position
> the cursor where you want the variable declared. Then:
>
> 1. `take string air` — select the string under the `a`-hat.
> 2. `copy that` — copy it.
> 3. `bring that` — paste it back as the right-hand side of your new
>    line.
> 4. `bring blue bat to air` — replace the original string (now under
>    `a`) with the new variable name (under `b`).

Note: you don't pause between commands. Cursorless commands chain like
any other Talon commands.

## Section 5 — Common Settings (Q&A Format)

Don't dump these. Offer them when relevant or when the user asks about
customization.

### "How do I see all the commands?"

`cursorless cheatsheet`. It opens in the browser and reflects the user's
actual configured spoken forms — including any overrides.

### "I want to change a spoken form (e.g., I keep saying 'select' instead of 'take')"

Cursorless ships customization CSV files inside `cursorless-talon`. The
recommended pattern is to copy the CSVs you want to override into your
**user repo** so updates pull cleanly. The relevant docs page is at
<https://www.cursorless.org/docs/user/customization/>.

For one-off changes, the user can edit
`~/.talon/user/cursorless-talon/cursorless_default_settings/*.csv` —
but warn them that those edits will conflict on next `git pull`. The
better path is the user-repo override.

### "The hats are too small / too distracting"

Two relevant commands:

- `hats off` — hides hats globally; useful for screen-sharing or when
  reading code rather than editing.
- `hats on` — re-enables.

For sizing, color schemes, and shape preferences, see the customization
docs page above. Hat appearance is configured via VSCode settings under
the `cursorless.hatStyles` namespace.

### "Cursorless seems slow on a big file"

Hat allocation is roughly linear in visible tokens. On very large files,
fold blocks the user isn't editing, or scroll so fewer tokens are
visible. The Cursorless team also publishes performance settings in the
extension preferences.

### "Updating cursorless-talon"

```bash
cd ~/.talon/user/cursorless-talon && git pull
```

Then restart Talon. Update the VSCode extension at the same time
(Extensions sidebar → Cursorless → Update, if available).

### "Can I use this in Vim / IntelliJ / Xcode?"

Not yet. Cursorless is VSCode-family-only today. The team has
experimented with other editors but there's nothing production-ready.
For Vim users, the closest equivalent is the community Talon Vim
integration plus regular Talon commands; for JetBrains, there's a
separate `talon-jetbrains` integration but it's not Cursorless.

## After Setup

Update the user's profile if a setup-progress table exists:

```bash
ls ~/.talon/talon-assistant/profile.md
```

If the profile has a `## Setup Progress` table, add a row for
**Cursorless** marked `done` with today's date. (If no row exists,
add one — this skill is post-onboarding so it won't be in the
initial template.)

Suggest the user log a few commands they want to remember in
`~/.talon/talon-assistant/memory.md` under the "Custom Commands
Created" or a new "Cursorless" section — Cursorless commands the user
finds themselves reaching for repeatedly are good candidates for muscle
memory practice.

## External Resources

Always link the user to these when appropriate:

- **Cursorless documentation:** <https://www.cursorless.org/docs/>
- **In-app cheatsheet:** say `cursorless cheatsheet` (canonical
  reference, reflects user's actual configured spoken forms)
- **GitHub:** <https://github.com/cursorless-dev/cursorless>
- **Customization guide:** <https://www.cursorless.org/docs/user/customization/>
- **Supported languages:** <https://www.cursorless.org/docs/user/languages/>
- **Local reference:** see `references/cursorless-commands.md` in this
  skill for the verified action and scope mappings, plus customization
  pointers.
