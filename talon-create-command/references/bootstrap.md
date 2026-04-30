# Bootstrap: Discover Repo & Load Profile

Both `talon-create-command` and `talon-test-and-debug` start with the same
two steps: find the user's custom repo, then adapt to their proficiency
profile. Run both before doing skill-specific work.

## 1. Find the user's custom repo

List `~/.talon/user/` and identify the folder that is NOT `community`,
`rango-talon`, `cursorless-talon`, `parrot`, or any other well-known shared
repo.

```bash
ls ~/.talon/user/
```

Store this name as `<user_repo>`. If unclear, ask the user once.

## 2. Load the profile

```bash
cat ~/.talon/talon-assistant/profile.md
```

Adapt explanations to the user's proficiency:

- **Beginner (Talon):** Explain syntax step by step. For testing, walk
  through log output and REPL commands in detail.
- **Intermediate (Talon):** Skip basics; focus on results and non-obvious
  patterns.
- **Advanced (Talon):** Show commands and results with brief design notes;
  skip the "why."
- **None / Basic (Coding):** Avoid jargon; explain Python and pytest
  concepts, what assertions mean, how to read test output.
- **Comfortable+ (Coding):** Use standard terminology.
- **None (Git):** If debugging involves git status or diffs, explain the
  commands.

If no profile exists, offer to run **talon-start** quickly (then resume
the calling skill automatically), or default to intermediate-level
explanations.
