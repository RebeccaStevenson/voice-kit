# Voice-Kit

This directory collects voice-control tooling, notes, and packaging assets for Talon and SuperWhisper work.

## Contents

- `talon-voice-assistant/` — source for a beginner-friendly Talon assistant plugin, including setup/debugging skills and a browser training page
- `talon-voice-assistant.plugin` — packaged plugin build
- `superwhisper/` — SuperWhisper skill and reference material for configuring custom dictation modes

## Voice Control Resources

### Voice dictation (speech-to-text into apps)

- **[Wispr Flow](https://wisprflow.ai)** — AI dictation across apps; cleans up filler words; adapts tone; 100+ languages; free tier (~$12–15/mo paid)
- **[Superwhisper](https://superwhisper.com)** — AI voice-to-text for macOS/iOS; customizable; optional offline models; free tier (~$8.49/mo paid)
- **[Apple Dictation](https://support.apple.com/guide/mac-help/use-dictation-mchlp2298/mac)** — built-in on Mac/iPhone/iPad; works in most text fields; enable in Keyboard settings (Mac) or on-device in newer versions
- **[Type with your voice (Google Docs)](https://support.google.com/docs/answer/4492226)** — voice typing in Google Docs; Chrome works well with Google's engine

### Full computer control (voice as keyboard + mouse)

- **[Talon Voice](https://talonvoice.com)** — hands-free keyboard/mouse replacement via voice, noise commands (pop/hiss), optional eye tracking; Python-scriptable; Mac, Windows, Linux; local Conformer engine (no audio sent to the cloud); extremely fast and reliable
- **[Talon Community Wiki](https://talon.wiki)** — setup, voice coding, and community documentation
- **[Voice access (Windows 11)](https://support.microsoft.com/en-us/topic/use-voice-access-to-control-your-pc-author-text-with-your-voice-4dcd23ee-f1b9-4fd1-bacc-862ab611f55d)** — control the PC and dictate with your voice; on-device recognition on current Windows 11 builds

### iOS Control

- **[Apple Voice Control](https://support.apple.com/guide/iphone/use-voice-control-on-iphone-iph2a64b1018/ios)** — hands-free control on iPhone/iPad with spoken commands, overlays, and custom commands; also available on [Mac](https://support.apple.com/guide/mac-help/use-voice-control-mh40719/mac)
- **[Siri](https://support.apple.com/guide/iphone/use-siri-iph83aad8922/ios)** — voice assistant for launching apps, dictating messages, timers, smart home, and more
- **[Shortcuts](https://support.apple.com/guide/shortcuts/welcome/ios)** — automate sequences and run them from the app, widgets, or Siri

### Whisper-based (OpenAI Whisper and clients)

- **[OpenAI Whisper](https://github.com/openai/whisper)** — open-source speech-to-text model; used by many apps and scripts; run locally or via APIs depending on integration
- **[MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper)** — macOS and iOS app built around Whisper-class models; strong for transcribing recordings and file-based workflows

### Other

- **[Dragon](https://www.nuance.com/dragon.html)** — long-standing dictation product, still useful for text editing workflows, especially on Windows

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
