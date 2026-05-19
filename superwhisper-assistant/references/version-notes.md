# SuperWhisper Version Notes

Version-gated facts and dated observations that don't belong in the
main `SKILL.md` because they go stale.

**Last verified:** 2026-05-19. If you're reading this much later, treat
items below as historical until re-verified — features may have moved
or behaviors may have changed.

## Version history (per-mode and integration features)

| Version | Released | Capability |
|---|---|---|
| v2.9.0 | — | Per-mode `autoPaste` override field added |
| v2.11.0 | — | Per-mode `autoCapitalize` override field added |
| v2.12.0 | Apr 2026 | Per-mode push-to-talk and toggle-recording shortcut overrides (so a single global hotkey is no longer the only option) |
| v2.13.0 | Apr 2026 | Direct integration with Claude Code and Open Code agents |
| v2.13.2 | — | Support for the Claude `AskUserQuestion` hook (agent can prompt the user and receive a dictated answer) |

The exact JSON keys for per-mode overrides aren't documented publicly.
To see what's set, read an existing mode in
`~/Documents/superwhisper/modes/`, or toggle the override in the UI and
diff the file before/after.

## Filesystem visibility of recording outputs

Since the 2026 release line, per-recording folders under
`~/Documents/superwhisper/recordings/` contain the `.wav` audio, raw
transcripts, and AI-output JSON as plain files — all scriptable. Older
versions kept some of this in the app's SQLite database only.

## Byte-format JSON sensitivity (known issue)

Confirmed on 2026-04-29 and 2026-04-30: SuperWhisper's mode parser
sometimes rejects mode files whose JSON was rewritten via Python's
default `json.dump` (compact `"key":"value"` style, unescaped `/`,
compact empty arrays). It reliably accepts files that match its own
serialization style:

- `"key" : "value"` (space before the colon)
- empty arrays as `[\n\n  ]` (newline, blank line, closing bracket at
  parent indent)
- forward slashes escaped as `\/` inside strings
- trailing newline at end of file

This is why the skill workflow is **byte-copy a donor mode with `cp`,
then surgically `Edit` individual fields** — never round-trip through
`json.load → json.dump`.

If this issue gets fixed in a future SuperWhisper release, the byte-copy
workflow still works (it's strictly more conservative). Update this
note when it's confirmed unnecessary.

## When to re-verify

Re-run the bisection playbook in `SKILL.md` against a known-good donor
mode whenever:

- SuperWhisper has had a major version bump since this file was last
  verified.
- A mode that worked previously starts getting silently rejected after
  an app update.
- The schema reference (`references/mode-schema.md`) disagrees with
  fields you see in an on-disk mode.
