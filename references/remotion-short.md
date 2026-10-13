# 黄金短视频 (Golden Short)

Use this branch for compact text-led list videos, rankings, steps, feature highlights, warnings,
and quick tips.

## Output Contract

- Target 8-10 seconds in normal use; keep a shorter result when the message is complete sooner.
- Default to 9:16 at 1080x1920 for Video Account unless the user specifies another ratio.
- Use animated text, simple graphics, screenshots, icons, or product visuals as the primary
  communication layer.
- Do not use a digital human or long narration. Default to no narration; add only a very short
  voice line when the user requests it or comprehension clearly requires it.
- Use `goodfeel.m4a`. Cover generation is off by default and only happens when explicitly requested.
- Select the executor from the supplied template and actual visual requirements. Do not force a
  particular renderer.

## Template Priority

- Treat user-provided templates as the starting point for structure, timing, visual language,
  reusable components, and executor choice.
- Preserve the template's native technology unless it cannot meet the requested output.
- Separate template constants from per-video content so later Golden Shorts can reuse the same
  structure safely.
- Do not redesign an approved template merely to move it into a preferred tool.

## Output Layout

Use this project-relative layout for every Golden Short:

```text
<project-root>/
├── src/golden-shorts/                 # Remotion source copied from a template
├── public/audio/goodfeel.mp3          # Remotion-compatible transcode of the shared BGM
└── out/golden-shorts/<slug>/
    ├── video.mp4                      # rendered video
    └── cover.png                      # optional; create only when explicitly requested
```

Do not write outputs into the installed skill directory or a hard-coded external project. Save
temporary render files inside the selected output folder and remove them after a successful
render.

## Available Templates

Load the matching source from `templates/` when the content pattern is clear. The templates use
fixed 9-second timelines at 30 fps and contain `EDIT BLOCK` regions for per-video data.

| Template | Executor | Content limit | Use for |
| --- | --- | --- | --- |
| `templates/01-信息型短视频/list-cards/template.jsx` | Remotion | 3-5 compact cards | Tool lists, tips, feature lists |
| `templates/01-信息型短视频/role-showcase/template.jsx` | Remotion | 2 roles, up to 3 items each | Role or industry comparisons |
| `templates/01-信息型短视频/screenshot-list/template.jsx` | Remotion | Screenshot plus 3-4 highlights | AI tools, software tests, feature releases |
| `templates/01-信息型短视频/quick-python/template.py` | FFmpeg + Pillow | Exactly 3 compact cards | Fast list, ranking, or warning videos |
| `templates/01-信息型短视频/multi-image-rotation/render.py` | FFmpeg + Pillow | 3-row title + 1-4 image rotation + 5-item list | Feature comparison, product walkthroughs |
| `templates/01-信息型短视频/title-card-image/render.py` | FFmpeg + Pillow | 5-row highlighted title card + single image | Result-driven hooks, "5 reasons why" style, 8s payoff |
| `templates/01-信息型短视频/six-card-list/render.py` | FFmpeg + Pillow | 4s spaced hook list + N compact adaptive cards at 3s each | Six questions, toolkits, workflows, and multi-item recommendations |

Project template specifications synchronized from the workspace:

| Template | Structure | Use for |
| --- | --- | --- |
| `templates/01-信息型短视频/07-数据爆点-证据轮播/template.md` | Headline + evidence media + full analysis | Data-driven news and product reactions |
| `templates/01-信息型短视频/08-黑底榜单-数据长表/template.md` | High-contrast ranking table with optional scroll/page turns | Rankings, city/company/product comparisons |
| `templates/01-信息型短视频/09-分类工具矩阵-Logo墙/template.md` | Gradient background + category rows + logos | Tool maps, software collections, AI toolkits |

### Remotion Template Usage

1. Copy the selected template to `<project-root>/src/golden-shorts/<slug>.jsx`.
2. Transcode `/Users/biggersun/.workbuddy/skills/ip-ppt-video-pipeline/bgm/goodfeel.m4a` once for
   browser-compatible Remotion audio:

   ```bash
   ffmpeg -y \
     -i /Users/biggersun/.workbuddy/skills/ip-ppt-video-pipeline/bgm/goodfeel.m4a \
     -codec:a libmp3lame -q:a 2 \
     <project-root>/public/audio/goodfeel.mp3
   ```
3. Edit only the marked data blocks.
4. Import the component and exported frame count in the project's `Root.jsx`, then register a
   1080x1920, 30 fps composition.
5. Render to `<project-root>/out/golden-shorts/<slug>/video.mp4`.
6. Generate a separate ImageGen cover only when explicitly requested; otherwise deliver the MP4 without a cover.

For `screenshot-list`, place the source screenshot in `public/images/`, set its filename and
dimensions in the marked edit block, and keep the screenshot plus highlight group centered
inside the safe area.

### Python Template Usage

Run with `uv` so Pillow does not depend on a globally installed Python:

```bash
uv run --with pillow templates/01-信息型短视频/quick-python/template.py \
  --project-root <project-root> \
  --slug <slug>
```

The script streams Pillow frames directly into FFmpeg and writes `video.mp4` to the common output
layout without a temporary frame directory. Generate `cover.png` separately with ImageGen only
when explicitly requested.

## Choose One Content Pattern

- **List:** one promise plus 3-5 concise items.
- **Ranking:** reveal from lower rank to the strongest item; explain the ranking criterion.
- **Steps:** show a clear ordered path with one action per card.
- **Feature:** show the capability, then the practical benefit or before/after.
- **Warning:** state the mistake or risk, show the consequence, then the fix.

Do not combine multiple patterns unless the result remains readable in 8-10 seconds.

## Timing Blueprint

Use this as a starting point, not a rigid template:

| Time | Purpose |
| --- | --- |
| First 10-15% | Hook, result, contradiction, warning, or direct viewer problem |
| Middle 70-75% | 3-5 cards, steps, ranks, or feature beats with continuous progress |
| Final 15-20% | Payoff, compact viewpoint, save/share reason, or open question |

The first frame must already communicate something. Do not spend time on a logo or empty intro.

## Executor Selection and Implementation

Choose based on the actual work:

- **Remotion:** data-driven React templates, reusable components, structured lists, rankings,
  steps, and batch variants.
- **HyperFrames:** HTML/CSS/GSAP motion, rich typography, web-style effects, audio-reactive
  visuals, or an existing HyperFrames template.
- **Jianying:** timeline-led assembly, native effects, screenshots, clips, or an existing Jianying
  draft/template.
- **FFmpeg:** deterministic media assembly, trimming, compositing, audio preparation, or final
  packaging when a higher-level renderer is unnecessary.
- **Project tooling:** preserve an established executor when it already owns the template.

Load the selected executor's rules. If Remotion is selected, use
`remotion:remotion-best-practices`; if HyperFrames is selected, use its authoring and CLI skills.

- Drive animation from the selected executor's deterministic timeline.
- Keep reusable list, ranking, step, feature, and warning data separate from template structure.
- Use one dominant visual hierarchy: hook, current item, supporting detail.
- Keep transitions fast and meaningful; each should reveal progress or a new information point.
- Fit text programmatically and verify that Chinese strings do not overflow.
- Apply `references/layout-rules.md`: center-first composition, proportional safe areas, and the
  H1/H2/H3/L type scale.
- Render representative stills before the final video: opening, densest card, transition, and
  ending.

## Copy and Design Rules

- Use everyday Chinese and concrete outcomes; avoid abstract AI jargon.
- Keep each card to one thought and remove words that do not change meaning.
- Make the item number, rank, step, feature, or warning unmistakable.
- Use visual consistency across cards but create enough change to prevent a static slideshow.
- Show at least one useful or surprising payoff.
- Make the final line strong enough to function as a shareable viewpoint when appropriate.
- **Measure every string before rendering.** A line that is one character too wide silently wraps
  (or the hook subtitle overflows the canvas), and the break lands mid-word. Never estimate from
  the canvas size — use the template's real text box. In `six-card-list`, `CARD_W = W - SAFE_LR * 2`
  (960 px on a 1080-wide frame), so at the fixed type scale the limits are: question ≤ `CARD_W - 72`,
  hook-list question ≤ `CARD_W - 64`, conclusion ≤ `CARD_W - 104`, bullets ≤ `CARD_W - 166`,
  takeaway ≤ `CARD_W - 136`, and the hook subtitle ≤ ~1000 px. Dump every string through
  `ImageDraw.textbbox` with the real font and assert the widths before starting the frame render.

## Audio

- Trim `goodfeel.m4a` to the exact composition duration.
- Apply short fades and avoid clipping.
- Align major visual beats to clear musical changes when practical.
- Use restrained sound effects only when they improve comprehension or emphasis.
- **Do not trust the template's default volume blindly.** Measured on 2026-10-05: `six-card-list`'s
  stock `BGM_VOLUME=0.48` rendered mean −22.9 dB / peak −7.1 dB — too quiet for a text-only short
  that has no narration carrying the audio. `0.7` measured mean −19.6 dB / peak −3.8 dB, which is a
  better starting point when there is no voice track. Verify with `volumedetect` and keep peak below
  about −1 dB.

## Branch QA

- Confirm duration, ratio, fps, and audio metadata.
- Confirm every card can be read at normal playback speed without pausing.
- Inspect the opening, densest card, every transition type, and ending at full resolution.
- Confirm text, numbers, icons, and screenshots remain inside safe areas.
- Confirm the video communicates the intended message from text and visuals alone, even when a
  short optional voice line is present.
- If a cover was explicitly requested, confirm it is not merely a cropped frame and matches the actual payoff.
