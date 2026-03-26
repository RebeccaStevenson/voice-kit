# Rango Voice Command Reference

Complete list of voice commands available after installing Rango and rango-talon. Commands are grouped by category.

In the tables below, `<target>` means a hint label (e.g., `air`, `bat bat`), `<number>` is an optional count, and `<text>` is free-form dictated text.

## Clicking and Focusing

| Command | What it does |
|---|---|
| `<target>` | Click element (direct mode — say the hint letters) |
| `click <target>` | Click element (explicit mode) |
| `focus <target>` | Focus element without clicking |
| `go input` | Focus the first input field on the page |
| `flick <target>` | Focus element and press Enter |
| `follow <text>` | Click element matching text (prioritizes visible area) |
| `button <text>` | Click element matching text (searches full page) |

### Multi-Target Clicking

Combine hints with "and" to click several elements in sequence:

```
air and bat and cap
```

With number hints, use "plus" instead of "and":

```
five plus twelve plus three
```

## Opening Links

| Command | What it does |
|---|---|
| `blank <target>` | Open link in a new foreground tab |
| `stash <target>` | Open link in a new background tab |

## Tab Navigation

| Command | What it does |
|---|---|
| `go tab <marker>` | Switch to tab by its marker letter |
| `slot <marker>` | Same as `go tab` |
| `tab back` | Switch to the previously focused tab |
| `tab hunt <text>` | Find and switch to a tab by title or URL text |
| `tab ahead` | Cycle forward through tabs matching a previous search |
| `tab behind` | Cycle backward through tabs matching a previous search |
| `tab marker refresh` | Refresh tab marker assignments |
| `visit <website>` | Focus or open a tab from the active `user.website` list (commonly fed by `websites.talon-list`) |

## Tab Management

| Command | What it does |
|---|---|
| `tab clone` | Duplicate the current tab |
| `tab split` | Move the current tab to a new window |
| `tab close other` | Close all other tabs in the window |
| `tab close left` | Close all tabs to the left |
| `tab close right` | Close all tabs to the right |
| `tab close first [<number>]` | Close N tabs from the left end (default 1) |
| `tab close final [<number>]` | Close N tabs from the right end (default 1) |
| `tab close previous [<number>]` | Close N tabs to the left of current (default 1) |
| `tab close next [<number>]` | Close N tabs to the right of current (default 1) |

## Page Navigation

| Command | What it does |
|---|---|
| `go root` | Navigate to the site's root URL |
| `page next` | Go to the next page (pagination) |
| `page last` | Go to the previous page (pagination) |

## Scrolling — Main Page

| Command | What it does |
|---|---|
| `upper [<number>]` | Scroll up (default 1 unit) |
| `upper all` | Scroll to top of page |
| `tiny up` | Scroll up a small amount |
| `downer [<number>]` | Scroll down (default 1 unit) |
| `downer all` | Scroll to bottom of page |
| `tiny down` | Scroll down a small amount |
| `scroll left [all]` | Scroll left |
| `scroll right [all]` | Scroll right |
| `tiny left` | Scroll left a small amount |
| `tiny right` | Scroll right a small amount |

## Scrolling — Side Panels

| Command | What it does |
|---|---|
| `upper left [all]` | Scroll up in left panel |
| `downer left [all]` | Scroll down in left panel |
| `upper right [all]` | Scroll up in right panel |
| `downer right [all]` | Scroll down in right panel |

## Scrolling — At a Specific Element

Target a scrollable container by its hint:

| Command | What it does |
|---|---|
| `upper <target>` | Scroll up inside element |
| `downer <target>` | Scroll down inside element |
| `tiny up <target>` | Small scroll up inside element |
| `tiny down <target>` | Small scroll down inside element |
| `scroll left <target>` | Scroll left inside element |
| `scroll right <target>` | Scroll right inside element |

### Repeat Previous Scroll

| Command | What it does |
|---|---|
| `up again` | Repeat last scroll-up action |
| `down again` | Repeat last scroll-down action |
| `left again` | Repeat last scroll-left action |
| `right again` | Repeat last scroll-right action |

## Snap Scrolling (Scroll to Position)

| Command | What it does |
|---|---|
| `crown <target>` | Scroll so element is at the top of the viewport |
| `center <target>` | Scroll so element is centered |
| `bottom <target>` | Scroll so element is at the bottom |

## Saved Scroll Positions

| Command | What it does |
|---|---|
| `scroll save <word>` | Save the current scroll position with a name |
| `scroll to <word>` | Restore a previously saved scroll position |

## Hovering

| Command | What it does |
|---|---|
| `hover <target>` | Hover over element (reveals tooltips, menus) |
| `hover text <text>` | Hover over element matching text |
| `dismiss` | Clear all hover states |

## Showing and Hiding

| Command | What it does |
|---|---|
| `show <target>` | Display where a link leads |
| `hide <target>` | Hide the hint for an element |

## Copying

| Command | What it does |
|---|---|
| `copy <target>` | Copy the URL of a link |
| `copy text <target>` | Copy the visible text of an element |
| `copy mark <target>` | Copy as a Markdown link `[text](url)` |
| `copy page address` | Copy the current page URL |
| `copy page host name` | Copy the hostname |
| `copy page origin` | Copy the origin |
| `copy page path` | Copy the pathname |
| `copy mark address` | Copy current URL as a Markdown link |

## Form Input

| Command | What it does |
|---|---|
| `paste to <target>` | Paste clipboard contents into an input |
| `insert <text> to <target>` | Type text into an input field |
| `enter <text> to <target>` | Type text and press Enter |
| `change <target>` | Select all text in an input (ready to overwrite) |
| `pre <target>` | Place cursor before element text |
| `post <target>` | Place cursor after element text |

## Hint Display Controls

| Command | What it does |
|---|---|
| `hint bigger` | Increase hint size |
| `hint smaller` | Decrease hint size |
| `hint extra` | Show extra hints for elements normally hidden |
| `hint more` | Show excluded single-letter hints |
| `hint less` | Show fewer hints |
| `hint exclude singles` | Remove all one-letter hints |
| `hint include singles` | Restore one-letter hints |
| `hints refresh` | Force-refresh all hints |

## Hint Visibility Toggles

| Command | What it does |
|---|---|
| `hints toggle` / `hints switch` | Toggle hints on or off |
| `hints on [<level>]` | Enable hints at a specific scope |
| `hints off [<level>]` | Disable hints at a specific scope |
| `hints reset <level>` | Reset a toggle level to default |
| `toggle show` | Display current toggle settings |

**Levels:** `everywhere`, `global`, `tab`, `host`, `page`, `now`

- `everywhere` — All browsers, all tabs
- `global` — All tabs in the current browser
- `tab` — Current tab only
- `host` — Current domain (e.g., all of github.com)
- `page` — Current URL only
- `now` — Temporary, until next navigation

## Custom Hint Selectors

| Command | What it does |
|---|---|
| `include <target>` | Add a CSS selector to show hints on this element type |
| `exclude <target>` | Remove hints from this element type |
| `exclude all` | Remove all custom hint inclusions |
| `some more` | Broaden the selector match |
| `some less` | Narrow the selector match |
| `custom hints save` | Confirm custom selector changes |
| `custom hints reset` | Reset to default selectors |

## Saved References (Bookmarked Elements)

| Command | What it does |
|---|---|
| `mark <target> as <word>` | Save an element with a name |
| `mark this as <word>` | Save the currently focused element |
| `mark show` | List all saved references |
| `mark clear <word>` | Remove a saved reference |
| `click mark <word>` | Click a saved reference |
| `focus mark <word>` | Focus a saved reference |
| `hover mark <word>` | Hover a saved reference |

## Tab Markers

| Command | What it does |
|---|---|
| `markers toggle` / `markers switch` | Toggle tab markers on or off |

## Clicking Mode

| Command | What it does |
|---|---|
| `rango direct` | Switch to direct clicking mode (say hint letters to click) |
| `rango explicit` | Switch to explicit mode (say "click" before hint letters) |
| `keyboard toggle` / `keyboard switch` | Toggle keyboard clicking mode |

## URL in Title Bar

| Command | What it does |
|---|---|
| `address in title on` | Show the page URL in the window title |
| `address in title off` | Hide the URL from the window title |

## Settings and Info Pages

| Command | What it does |
|---|---|
| `rango settings` | Open the Rango settings page |
| `rango open read me` | Open rango.click documentation |
| `rango open issues` | Open the GitHub issues page |
| `rango open new issue` | Open a new GitHub issue |
| `rango open changelog` | Open the changelog |
| `rango open sponsor` | Open the sponsor page |

## Tags and Settings Reference

These tags can be set in a `.talon` file to change Rango's default behavior:

| Tag | Effect |
|---|---|
| `user.rango_direct_clicking` | Enable direct clicking mode (default — already on) |
| `user.rango_explicit_clicking` | Enable explicit clicking mode |
| `user.rango_number_hints` | Use numbers instead of letters for hints |
| `user.rango_exclude_singles` | Hide single-letter hints to reduce accidental clicks |
| `user.rango_disabled` | Disable all Rango commands |

Example — put this in a file like `talon_yourname/rango_settings.talon`:

```talon
# Use number hints and exclude singles
tag(): user.rango_number_hints
tag(): user.rango_exclude_singles
```

## Browser Support

Rango works in these browsers (all via the `tag: browser` context):

- Google Chrome
- Brave
- Microsoft Edge
- Vivaldi
- Opera
- Firefox
- Safari (uses `Ctrl-Shift-3` hotkey instead of `Ctrl-Shift-Insert`)
