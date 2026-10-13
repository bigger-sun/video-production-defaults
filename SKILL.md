---
name: video-production-defaults
description: "Route and govern the user's two default AI video formats: (1) 16:9 narrated tutorials, product introductions, and feature demonstrations with screenshots, screen recordings, smart zoom, annotations, captions, and a digital human; (2) 8-10-second Golden Shorts for lists, feature highlights, warnings, rankings, and steps, using the best executor or supplied template rather than a fixed renderer. Use whenever Codex plans, scripts, captures, edits, renders, reviews, packages, or delivers video. Enforce shared BGM, center-first safe-area layout, evidence-carousel motion boundaries, Video Account metric design, and delivery QA. Do not generate cover images unless explicitly requested."
---

# Video Production Defaults

Use this skill as the routing and quality layer for every video. Use the specialist video
skills as executors; do not duplicate their implementation details here.

## Select the Format

Choose exactly one primary format before scripting:

| Format | Use for | Default output | Required reference |
| --- | --- | --- | --- |
| Narrated demo | Tutorials, product introductions, new-feature introductions, workflows that need explanation or screen demonstration | 16:9, normally 30-120 seconds, cloned narration, digital human, screenshots or screen recording | `references/narrated-demo.md` |
| Golden Short / 黄金短视频 | Lists, rankings, steps, compact feature highlights, warnings, and quick tips | Usually 8-10 seconds, text-led, best-fit executor, 9:16 by default for Video Account | `references/remotion-short.md` |

Use the narrated format when understanding depends on explanation, a real UI workflow, or
voice. Use the Golden Short format when the idea can be understood from concise animated text
and graphics. Respect an explicit user choice over these defaults.

## Apply the Metric Gate

Read `references/video-account-ai.md` for every video before writing the script or storyboard.
Apply it to the topic, hook, pacing, cover, interaction design, ending, and delivery plan.

Create a compact pre-production card that states:

- format, target viewer, concrete problem, duration, aspect ratio, and executor;
- answers to the five Video Account questions;
- primary metric layer and the intended action for the other three layers;
- first-three-second hook, mid-video payoff, ending, and cover promise.

Do not approve a concept for production when it cannot answer at least three of the five
questions. Revise the topic or treatment first.

## Apply Layout Rules

Read `references/layout-rules.md` before drawing any frame. Apply it across every executor and
template. Use the fixed priority **Center First → Safe Areas → Modular Type Scale**. Restore
centering before shrinking text, use only approved type levels, and split scenes before using
body text below 44 px on a 1080×1920 frame.
No visible content, decorative line, logo, title, or control may enter the top safe area; for
9:16 videos the first visible element starts at least 200 px from the top edge.

## Scope Boundary

Stop at validated MP4 delivery. Publishing, comment monitoring, comment replies,
account operation, and post-release metric review belong to the user. Do not perform or report
them as video-production tasks.

## Shared Non-Negotiable Defaults

1. Do not generate a cover image unless the user explicitly asks for one.
2. Use `/Users/biggersun/.workbuddy/skills/ip-ppt-video-pipeline/bgm/goodfeel.m4a` unless the user
   specifies another track.
3. Keep every second necessary while preserving comprehension and emotional completeness.
4. Lead with a result, conflict, contrast, concrete problem, or curiosity gap.
5. Validate video, audio, text layout, and representative stills before delivery.
6. Enforce `references/layout-rules.md` on every frame and representative still.
7. Synthesize narration with the local VoiceStudio channel unless the user explicitly chooses
   another engine. See `## Narration (Local TTS)`.

## Evidence Carousel and Motion Boundaries

- For evidence-carousel layouts, show one evidence asset at a time in the central viewport.
  The central evidence viewport is fixed at 16:9 in every short-video template. Normalize each
  screenshot, image, or video to that viewport before rendering: preserve aspect ratio and show
  the complete source by default. Use proportional letterboxing whenever the source does not
  match 16:9; never crop text, UI edges, logos, or other evidence-bearing content. Never stretch,
  squeeze, or otherwise distort the source. Do not
  place multiple evidence screenshots side by side unless the user explicitly asks for a
  comparison.
- Keep headline, subtitle, explanatory copy, table rows, and footer static by default.
  Restrict motion to the evidence viewport. A ranking/count sequence may additionally animate
  only its numerals or rank chips; do not animate the surrounding text or containers.
- Load complete explanatory text once. Do not use typewriter, per-line entrance, or staggered
  body-copy animation unless explicitly requested.

The default horizontal safe distance is 0 px for 9:16 short-video templates; use edge-to-edge
content where the template calls for full-bleed evidence or a clean editorial layout.

## Clean Editorial Layout

- For software screenshots and evidence-led list videos, prefer a light, airy background,
  black or near-black primary text, restrained blue/cyan accents, thin dividers, and minimal
  borders. Avoid heavy cards, dense decoration, and unnecessary headings.
- Let the central evidence asset occupy the largest visual area. Keep the lower explanation as
  a simple numbered list or compact table with clear spacing.

## Shared BGM Rules

- Trim or loop the BGM to the exact final duration.
- Apply a short fade in and fade out.
- Keep it below narration in narrated videos; voice clarity wins.
- In Golden Shorts, keep it energetic but below clipping and distracting loudness.
- Verify the final mix with `ffprobe` and FFmpeg volume detection.

Start narrated mixes around `volume=0.16`, then adjust from measured output rather than treating
that value as fixed.

## Narration (Local TTS)

Narrated videos use the local VoiceStudio channel by default. Synthesis runs on this machine and
the audio never leaves it. Do not call a cloud TTS provider unless the user explicitly approves it.

- **Engine**: VoiceStudio desktop app, local MCP at `http://127.0.0.1:3900/mcp`.
- **Voice**: the user's cloned profile `08085b08`, `language=zh`. Other available profiles:
  `7a870671` (平淡声音, steady/flat delivery — preferred for dry explainer narration) and
  `4f9caa01` (声音二).
- **Speed**: `1.5`, the user's default pace for Chinese narration.
- **Skill**: narration is owned by the `voiceover-tts` skill — load it instead of re-deriving
  the procedure. Script writing is owned by `voiceover-script`.
- **Config**: read the `tts` block in
  `~/.workbuddy/skills/voiceover-tts/config.json`
  (`engine` / `profile_id` / `speed` / `language`) instead of hardcoding values.
- **Runner**: the local executor already exists — do not write a second VoiceStudio client.
  `python3 ~/.workbuddy/skills/voiceover-tts/scripts/tts_voicestudio.py --project <dir>`
  reads `<dir>/voiceovers.txt` (one sentence per line) and writes `<dir>/audio/vo_NN.wav` plus
  `<dir>/audio/durations.json`. `--speed` / `--profile` / `--lang` override the config.
- **Tool call**: `generate_speech(text, language, profile_id, speed)` returns a base64 WAV and
  `audio_duration_s`.
- **Prerequisite**: the VoiceStudio app must be running and the MCP endpoint reachable. Probe it
  first; if it is down, stop and tell the user to launch VoiceStudio instead of silently switching
  engines.
- **Fallback**: the Doubao TTS script at `~/.workbuddy/skills/voiceover-tts/scripts/tts_doubao.py`
  only when VoiceStudio is unavailable and the user approves the switch. Never substitute another
  provider on your own.
- **Timing**: measure the rendered WAVs with `ffprobe`, then lock scene cuts, captions, and the
  digital-human timing to the final voice track.

## Cover Rules

- Cover generation is off by default. Only use `imagegen` when the user explicitly requests a
  cover, thumbnail, or封面图.
- When explicitly requested, match the final ratio and keep all key content inside platform-safe
  areas; otherwise deliver only the validated MP4 and project source as applicable.

## Execution Routing

### Narrated demo

1. Read `references/narrated-demo.md`.
2. Synthesize narration with the local VoiceStudio channel (see `## Narration (Local TTS)`):
   profile `08085b08`, `language=zh`, `speed=1.5`. Fall back to Doubao TTS only when VoiceStudio is
   unavailable and the user approves.
3. Use `jianying-editor` for screen recording, smart zoom, annotations, editing, captions, and
   export unless the project has a better established toolchain.
4. Add the digital-human layer after narration timing is final and the user-provided API is
   configured. Until then, prepare the integration package described in the branch reference and
   stop before final digital-human assembly.

### Golden Short / 黄金短视频

1. Read `references/remotion-short.md`.
2. If the user supplies a template, preserve its native structure and executor unless there is a
   concrete incompatibility.
3. Select the best-fit executor from Remotion, HyperFrames, Jianying, FFmpeg, or the project's
   established tooling. Do not force Remotion.
4. Load the selected executor's skill or documentation, then render representative frame checks
   before the final MP4.

For `six-card-list`, use its structured card schema by default. Keep hook-list rows vertically
separated, place each question/title above and outside its card, pack explanation bullets
continuously, size the card to its actual content, and default each card to 3 seconds. Preserve
source wording exactly when the user locks question text or punctuation; provide explicit
`question_lines` when an inseparable phrase must stay together.

## Delivery QA

Verify all of the following:

- MP4 exists; a separate cover is required only when explicitly requested.
- Duration, aspect ratio, frame rate, and audio streams match the chosen format.
- `goodfeel.m4a` was used unless explicitly overridden.
- Audio is audible, balanced, and free of clipping.
- Titles, captions, UI targets, annotations, and the digital human do not overlap or overflow.
- Every representative frame passes center alignment, safe-area, and type-scale checks.
- The first visible element clears the format-specific top safe area; no title or decoration is
  hidden under platform status-bar or app-chrome regions.
- The first three seconds establish relevance or curiosity and contain visual change.
- The middle has no obvious information-density drop.
- The ending stops promptly and provides the intended interaction, forwarding, or follow reason.
- If a cover was explicitly requested, it is legible, accurate, inspected at full size, and
  saved with the video; otherwise do not create or report one.
- A narrated demo is not final until the digital-human API output has been integrated and
  validated.

## Delivery Summary

Report:

- chosen format and executor;
- MP4 path (and cover path only when explicitly requested);
- duration, aspect ratio, and frame rate;
- BGM, narration, and digital-human status;
- metric strategy and five-question gate result;
- validation results and any unresolved caveat.
