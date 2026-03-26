# Voice Kit

This directory collects voice-control tooling, notes, and packaging assets for Talon and SuperWhisper work.

## Contents

- `talon-voice-assistant/` — source for a beginner-friendly Talon assistant plugin, including setup/debugging skills and a browser training page
- `talon-voice-assistant.plugin` — packaged plugin build
- `superwhisper/` — SuperWhisper skill and reference material for configuring custom dictation modes
- `voice_control_resources.md` — curated links for dictation, hands-free control, and Whisper-based tools

## Typical Use

- Edit plugin skills or resources in `talon-voice-assistant/`
- Rebuild the plugin after changes:

```bash
cd talon-voice-assistant
zip -r ../talon-voice-assistant.plugin . -x '*.git*' -x '*.DS_Store'
```

- Refer to `superwhisper/SKILL.md` when creating or updating SuperWhisper modes

## Notes

The detailed plugin documentation lives in `talon-voice-assistant/README.md`.
