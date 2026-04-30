# Cursorless Command Reference

This is a curated, verified subset of Cursorless commands. The
**canonical, complete reference** is the in-app cheatsheet — open it by
saying `cursorless cheatsheet`. It reflects the user's actual configured
spoken forms (including overrides) and stays in sync with the installed
version.

## Mental Model

Every Cursorless command is `<action> <target>`.

A **target** is a **mark** (a hat — color + shape + character) plus
optional **modifiers**:

```
[<modifier>...] <hat>
```

Examples:

| Target | Means |
|---|---|
| `air` | Token under the gray `a` hat |
| `blue bat` | Token under the blue `b` hat |
| `funk air` | The whole function containing the gray `a` |
| `next funk` | The next function from cursor |
| `air past blue bat` | Range from `a` to `b` |
| `every arg blue bat` | Every argument in the call where `b` lives |

## Hats: Phonics, Colors, and Shapes

The phonic alphabet matches the standard Talon community alphabet
(`air`, `bat`, `cap`, `drum`, `each`, ...). On top of that:

- **Colors** prefix the phonic — `blue`, `green`, `red`, etc. (the
  exact set is configurable).
- **Shapes** also prefix — `fox`, `wing`, `frame`, etc. (configurable).

Color + shape combinations let Cursorless give every visible character
a unique hat. The user only says color/shape when the bare phonic
is ambiguous on screen.

## Verified Actions

These are confirmed from the Cursorless `spoken_forms.json` source of
truth. The full list is much larger — `cursorless cheatsheet` shows
everything.

| Spoken | Effect |
|---|---|
| `take <target>` | Select the target |
| `chuck <target>` | Delete the target |
| `bring <target>` | Replace current selection with the target's contents |
| `bring <target_a> to <target_b>` | Replace `target_b` with `target_a`'s contents |
| `copy <target>` | Copy target to clipboard |
| `pre <target>` | Move cursor before the target |
| `post <target>` | Move cursor after the target |
| `drink <target>` | Insert a new line above the target's line; cursor there |
| `pour <target>` | Insert a new line below the target's line; cursor there |

For the full action list (clear, change, scout/find, format,
breakpoint, fold, etc.), use the in-app cheatsheet.

## Verified Scope Modifiers

Confirmed from `spoken_forms.json`:

| Spoken | Scope |
|---|---|
| `funk` | Named function |
| `arg` | Argument or parameter |
| `line` | Line |

Other scopes documented across Cursorless: `token` (default), `word`,
`file`, `block`, `paint` (paragraph), `state` (statement), `value`
(right-hand side), `key`, `item`, `class`, `name`, `type`, `string`,
`comment`. Spoken forms for these may vary across releases — confirm
via the cheatsheet rather than this doc.

## Verified Position Modifiers

From `spoken_forms.json`:

| Spoken | Means |
|---|---|
| `next` | The next instance of the scope from cursor |
| `every` | Every instance of the scope in the parent |
| `first` | The first instance |

Standard companions — `last`, `previous`, ordinals (`second`, `third`),
counts (`two`, `three`) — are documented in the cheatsheet.

## Customization

Cursorless reads spoken-form overrides from CSV files. The recommended
override workflow:

1. Locate the default CSVs:

   ```bash
   ls ~/.talon/user/cursorless-talon/cursorless_default_settings/
   ```

2. Copy the file you want to override into the user's personal repo.
   The standard location is `<user_repo>/cursorless_settings/`:

   ```bash
   mkdir -p "$HOME/.talon/user/<user_repo>/cursorless_settings"
   cp ~/.talon/user/cursorless-talon/cursorless_default_settings/actions.csv \
      "$HOME/.talon/user/<user_repo>/cursorless_settings/"
   ```

3. Edit the user-repo copy. Each row maps a spoken phrase to an
   internal Cursorless ID. Empty the spoken-form column to disable a
   command; change it to remap.

4. Reload — Cursorless picks up CSV changes within a few seconds; no
   restart required.

Authoritative customization guide: <https://www.cursorless.org/docs/user/customization/>

## Hat Appearance

Hat colors, shapes, and sizes are configured via VSCode settings (not
Talon). Open VSCode settings → search for `cursorless.hatStyles`.
Common adjustments:

- `cursorless.hatSizeAdjustment` — make hats bigger or smaller
- `cursorless.hatVerticalOffset` — push hats up or down
- `cursorless.colors.dark` / `cursorless.colors.light` — color hex
  values per theme

## Voice Toggle Commands

| Spoken | Effect |
|---|---|
| `hats off` | Hide all hats globally |
| `hats on` | Show hats again |
| `cursorless cheatsheet` | Open the in-browser command reference |

## Supported Languages

Cursorless supports 36 languages with varying depth. Tree-sitter-backed
languages get the full scope vocabulary (`funk`, `class`, `arg`, etc.);
plaintext-style languages get the basics (`token`, `line`, `word`,
`paint`).

Tree-sitter-backed: C, C++, C#, Clojure, CSS, Dart, Go, HTML, Java,
JavaScript, JavaScript React (JSX), JSON, JSONC, JSONL, Kotlin, Lua,
Markdown, PHP, Python, R, Ruby, Rust, Scala, SCSS, Talon, Talon-list,
Tree-sitter query, TypeScript, TypeScript React (TSX), XML, YAML.

Lighter support: LaTeX, Plaintext, Properties.

Per-language notes: <https://www.cursorless.org/docs/user/languages/>

## When to Reach for Cursorless vs. Plain Talon

- **Plain Talon / community commands** — best for "type this", "press
  that key", "open this app", general OS-level workflow.
- **Cursorless** — best for *editing existing code structure*: select
  this argument, replace this function call, delete this string,
  insert above that line.

The two compose: a typical voice-coding session uses Talon for
navigation and dictation, Cursorless for surgical edits, and snippets
for boilerplate. They aren't competing tools.
