# Narrated Horizontal Demo

Use this branch for tutorials, product introductions, new-feature introductions, and other
videos that depend on spoken explanation or a real product workflow.

## Output Contract

- Use 16:9 horizontal composition, normally 1920x1080.
- Target 30-120 seconds. Extend only when the workflow cannot remain understandable after
  removing repetition, pauses, and nonessential steps.
- Include cloned narration, captions, screen evidence, BGM, and a digital human. Add a separate
  16:9 cover only when explicitly requested.
- Prefer real screenshots and screen recordings over simulated UI.

## Plan Before Capture

Write a scene table with these columns:

| Time | Narration | Screen action or screenshot | Zoom or annotation | Digital-human position | Caption emphasis |
| --- | --- | --- | --- | --- | --- |

Plan around the viewer's problem and result:

1. Show the outcome or conflict in the first three seconds.
2. State what the viewer will learn or gain.
3. Demonstrate only the steps that change the result.
4. Show a clear before/after, completed output, or practical payoff.
5. End immediately after a useful judgment, open question, forwarding reason, or follow-up
   promise.

## Script and Narration

- Rewrite source material into concise spoken Chinese; do not read an article verbatim.
  **Exception — a script the user wrote or hand-edited is final and must be used verbatim, not one
  character changed** (rules and the `split_script.py` / `check_verbatim.py` tooling live in the
  `voiceover-script` skill).
- Give every sentence one job. Delete it if removal does not harm understanding, emotion, or
  action.
- Put a small payoff, change, or useful detail every 5-8 seconds.
- Remove filler words, repeated transitions, breaths, dead air, and trailing endings.
- Use the local VoiceStudio channel for narration (procedure owned by the `voiceover-tts` skill):
  the user's cloned profile `08085b08`, `language=zh`, `speed=1.5`. Read the values from the `tts`
  block in `~/.workbuddy/skills/voiceover-tts/config.json` instead of hardcoding them.
  VoiceStudio must be running; fall back to Doubao TTS only when it is unavailable and the user
  approves.
- Run `python3 ~/.workbuddy/skills/voiceover-tts/scripts/tts_voicestudio.py --project <dir>`
  to synthesize `<dir>/voiceovers.txt` into `<dir>/audio/vo_NN.wav` and `<dir>/audio/durations.json`.
  Do not write a second VoiceStudio client.
- Generate narration first, measure it, and lock scene timing to the final voice track.

## Screenshots and Screen Recording

Use screenshots for static proof, comparisons, settings, and final results. Use screen recording
when cursor movement, state change, timing, or interaction sequence matters.

Before capture:

- close irrelevant windows and hide notifications, personal data, tokens, and account details;
- set a stable 16:9 viewport and readable UI scale;
- prepare the exact demo state, sample data, and expected result;
- record short clean segments instead of one long error-prone take;
- capture the initial state, key actions, and final result separately when useful.

During editing:

- accelerate routine operations and loading periods;
- cut mistakes and waiting instead of narrating around them;
- preserve enough context that viewers know where the highlighted control lives;
- use a screenshot hold when the viewer needs time to read a dense result.

Use `jianying-editor` recording guidance for recording and smart zoom.

## Smart Zoom and Annotation

- Zoom only when it directs attention to a real target.
- Ease into the target, hold long enough to understand it, then return to context.
- Avoid rapid repeated zooms that create motion without information.
- Use arrows, circles, highlights, numbered steps, or short labels to identify the action.
- Keep annotations away from captions, cursor targets, and the digital-human layer.
- Do not crop menus, dialogs, confirmation messages, or the final result.

## Digital Human

Treat the digital human as a required layer for this format.

- Finalize narration before generating or syncing the digital human.
- Reserve a safe corner or dedicated presenter region in the storyboard from the start.
- Keep the presenter away from active UI, annotations, captions, and critical results.
- Use the presenter most strongly for the hook, transitions, judgments, and ending; let the UI
  dominate detailed demonstrations.
- Match lip sync to the final cloned narration and cut the presenter with the same timing edits.
- Use a transparent-background asset when available; otherwise key a clean green-screen asset.

The digital-human API is pending from the user. Until the user provides it:

- do not choose another provider, fabricate an API, request credentials repeatedly, or generate
  a substitute presenter;
- prepare the final narration audio, exact transcript, captions, scene timing, presenter-safe
  region, target resolution, and preferred transparent or green-screen background;
- keep the edit digital-human-ready, but do not put a presenter placeholder into a final MP4;
- report final digital-human assembly as pending rather than calling the narrated video complete.

After the user provides the API:

- keep secrets in environment variables or the provider's secure configuration, never in this
  skill or project documentation;
- test a short sample before submitting the full narration;
- validate lip sync, duration, resolution, background handling, crop, and download integrity;
- integrate the returned asset only after it passes validation.

## Captions and Visual Rhythm

- Generate captions from the final narration, not an earlier script draft.
- Keep captions concise and synchronized; emphasize keywords without turning every word into an
  effect.
- Keep captions inside the safe area and separate from product UI and the digital human.
- Change framing, crop, annotation, screenshot, or visual emphasis every 5-8 seconds when the
  content allows it.
- Add sound effects only when they clarify an action or transition.

## Branch QA

- Confirm 16:9 output and readable UI at normal playback size.
- Inspect the first frame, hook, every zoom target, major annotation, digital-human entry, final
  result, and ending.
- Confirm the digital human never obscures the demonstrated control or caption.
- Confirm narration remains clear over BGM and contains no long silence or clipped phrase.
- Confirm the tutorial can be followed without guessing an omitted critical step.
