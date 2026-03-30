# Voice-Kit — Agent Instructions

## What This Repo Is

A toolkit for voice control beginners containing:

- `talon-start/`, `talon-setup-talon/`, `talon-setup-rango/`, `talon-create-custom-repo/`, `talon-create-basic-command/`, `talon-create-python-command/`, and `talon-test-and-debug/` — root-level Talon skills that walk users through installing and customising Talon voice control
- **superwhisper-assistant/** — standalone skill for configuring SuperWhisper dictation modes

## Repo Structure

```
voice-kit/
├── AGENTS.md                  ← you are here
├── CLAUDE.md                  ← points here
├── LICENSE                    ← MIT
├── README.md                  ← public-facing overview
├── resources/
│   └── talon-training.html    ← training page
├── talon-start/
│   └── SKILL.md
├── talon-setup-talon/
│   ├── SKILL.md
│   └── references/*.md
├── talon-setup-rango/
│   ├── SKILL.md
│   └── references/*.md
├── talon-create-custom-repo/
│   ├── SKILL.md
│   └── references/*.md
├── talon-create-basic-command/
│   ├── SKILL.md
│   └── references/*.md
├── talon-create-python-command/
│   ├── SKILL.md
│   └── references/*.md
├── talon-test-and-debug/
│   ├── SKILL.md
│   └── references/*.md
└── superwhisper-assistant/
    ├── SKILL.md
    └── references/mode-schema.md
```

## Skill File Conventions

Each skill lives in its own directory at the top level.

- **SKILL.md** — the skill definition. Must include YAML frontmatter with `name` and `description` fields.
- **references/** — optional supporting docs read by the skill at runtime.
- Filenames use lowercase-kebab-case.
- Skills are self-contained: each SKILL.md includes all instructions an agent needs to execute the skill. Do not split logic across files — keep reference docs factual, not procedural.

## Naming

- Skill directories: `lowercase-kebab-case`
- Skill names in frontmatter: match the directory name exactly
- Voice commands: object-verb phrasing (`file save`, `tab close`)

## What Not to Modify

- Do not edit `resources/talon-training.html` unless the task specifically calls for changing the training page.
- Do not change SKILL.md frontmatter `name` fields — other systems reference them.
- Do not add dependencies or build tooling unless requested. This is a documentation-only repo (Markdown + one HTML file).

## Editing Skills

When editing a SKILL.md:

1. Preserve the YAML frontmatter block.
2. Keep the proficiency-adaptation pattern — skills read the user profile and adjust tone/detail.
3. Maintain the "search before creating" and "test after creating" rules in command-creation skills.
4. Reference docs go in `references/`, not inline in SKILL.md.

## Adding a New Skill

1. Create `<skill-name>/SKILL.md` with frontmatter.
2. Add a reference doc in `references/` if the skill needs factual lookup material.
3. Update the skill table in `README.md`.
4. If the skill has prerequisites, document them and add it to the dependency diagram in the `talon-start` skill's generated `CLAUDE.md`.

## License

MIT — see LICENSE in the repo root.
