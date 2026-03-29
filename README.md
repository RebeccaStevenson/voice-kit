# Voice-Kit

## Talon voice assistant

- [talon-voice-assistant/](talon-voice-assistant/)
- A collection of skills that guides new users through installing, configuring, and creating custom voice commands with [Talon](https://talonvoice.com/), hopefully making the process mostly hands off i.e. the agent does pretty much everything for you. Beginner friendly, no coding experience required.

## Superwhisper-assistant

- [superwhisper-assistant/](superwhisper-assistant/)
- Install, configure, and create custom dictation modes for SuperWhisper, the macOS voice-to-text app. Handles mode JSON files, voice/language model selection, prompt engineering for text formatting, and Talon integration.

## Plugins

- **Claude Cowork plugins:** Easiest for non-programmers. Just ask your agent to add them.  
  [Overview](https://claude.com/docs/plugins/overview)
- **Claude Code plugins:** For installing full-featured plugins (e.g., `talon-voice-assistant`).  
  [Guide](https://code.claude.com/docs/en/plugins)
- **Codex plugins:** For plugin installations in Codex.  
  [Docs](https://developers.openai.com/codex/plugins)

## Skills

- **Claude Code skills:** For adding individual skills (e.g., `superwhisper-assistant`).  
  [Instructions](https://code.claude.com/docs/en/skills)
- **Codex skills:** For adding specific skills in Codex.  
  [Docs](https://developers.openai.com/codex/skills)

## Voice control resources

### Full computer control (voice as keyboard + mouse)

- **[Talon Voice](https://talonvoice.com)** — hands-free keyboard/mouse replacement via voice, noise commands (pop/hiss), optional eye tracking; Python-scriptable; Mac, Windows, Linux; local Conformer engine (no audio sent to the cloud); extremely fast and reliable
  - **[Talon Community Wiki](https://talon.wiki)** — setup, voice coding, Slack community
  - [Talon voice assistant skills](talon-voice-assistant/skills/) — local setup, command-creation, debugging, and Rango skills
- **[Apple Voice Control for Mac](https://support.apple.com/en-us/HT203085)** — built-in hands-free control for macOS with spoken commands, overlays, custom commands, and dictation on device

### Voice dictation (speech-to-text)

- **[Wispr Flow](https://wisprflow.ai)** — AI dictation across apps on Mac, Windows, iOS, and Android; 100+ languages; Flow Pro is $15/user/month monthly or $12/user/month annual, with a free Basic tier and 14-day trial
- **[Superwhisper](https://superwhisper.com)** — AI voice-to-text for macOS, Windows, iPhone, and iPad; customizable modes; local and cloud models; Pro is $8.49/month, $84.99/year, or $249.99 once, with a free tier available
  - [`superwhisper-assistant` skill directory](superwhisper-assistant/) — local skill files and references for dictation modes
- **[Dragon](https://www.nuance.com/dragon.html)** — long-standing dictation product (Windows-focused today); still good for editing text especially in Microsoft Word

### iOS control

- **[Apple Voice Control for iPhone and iPad](https://support.apple.com/en-us/111778)** — hands-free control on iPhone/iPad with spoken commands, overlays, custom commands, and on-device recognition after setup
- **[Siri](https://support.apple.com/guide/iphone/use-siri-iph83aad8922/ios)** — voice assistant for launching apps, dictating messages, timers, smart home, and more
- **[Shortcuts](https://support.apple.com/guide/shortcuts/welcome/ios)** — automate sequences (open apps, text, Home actions) and run them from the app, widgets, or Siri

### Whisper-based (OpenAI Whisper and clients)

- **[OpenAI Whisper](https://github.com/openai/whisper)** — open-source speech-to-text model; used by many apps and scripts; run locally or via APIs depending on integration
- **[MacWhisper](https://macwhisper.com/)** — Mac app for Whisper-based transcription, recording, file export, and optional system-wide dictation; also available on iPhone/iPad; free download with Pro from EUR59 as a one-time purchase

### Other
