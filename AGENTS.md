# Voice-Kit — Agent Instructions

## What This Repo Is

A toolkit for voice control beginners containing:

- **talon-voice-assistant/** — Claude Code plugin with 7 skills that walk users through installing and customising Talon voice control
- **superwhisper-assistant/** — standalone skill for configuring SuperWhisper dictation modes

## Repo Structure

```
voice-kit/
├── AGENTS.md                  ← you are here
├── CLAUDE.md                  ← points here
├── LICENSE                    ← MIT
├── README.md                  ← public-facing overview
├── talon-voice-assistant/
│   ├── .claude-plugin/plugin.json
│   ├── README.md
│   ├── skills/<skill>/SKILL.md
│   ├── skills/<skill>/references/*.md
│   └── resources/talon-training.html
└── superwhisper-assistant/
    ├── SKILL.md
    └── references/mode-schema.md
```

## Skill File Conventions

Each skill lives in its own directory under `skills/` (plugin) or at the top level (standalone skill).

- **SKILL.md** — the skill definition. Must include YAML frontmatter with `name` and `description` fields.
- **references/** — optional supporting docs read by the skill at runtime.
- Filenames use lowercase-kebab-case.
- Skills are self-contained: each SKILL.md includes all instructions an agent needs to execute the skill. Do not split logic across files — keep reference docs factual, not procedural.

## Naming

- Skill directories: `lowercase-kebab-case`
- Skill names in frontmatter: match the directory name exactly
- Voice commands: object-verb phrasing (`file save`, `tab close`)

## What Not to Modify

- Do not edit files inside `talon-voice-assistant/resources/` without being asked — the training page is hand-authored HTML.
- Do not change SKILL.md frontmatter `name` fields — other systems reference them.
- Do not add dependencies or build tooling unless requested. This is a documentation-only repo (Markdown + one HTML file).

## Editing Skills

When editing a SKILL.md:

1. Preserve the YAML frontmatter block.
2. Keep the proficiency-adaptation pattern — skills read the user profile and adjust tone/detail.
3. Maintain the "search before creating" and "test after creating" rules in command-creation skills.
4. Reference docs go in `references/`, not inline in SKILL.md.

## Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter.
2. Add a reference doc in `references/` if the skill needs factual lookup material.
3. Update the skill table in `talon-voice-assistant/README.md`.
4. If the skill has prerequisites, document them and add it to the dependency diagram in the start skill's generated CLAUDE.md.

## License

MIT — see LICENSE in the repo root.
