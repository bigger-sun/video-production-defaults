# 排版第一原则 · Layout Rules

Apply these rules to every frame across Remotion, HyperFrames, Jianying, FFmpeg, and custom
renderers.

## Priority

Use this fixed priority:

1. **Center First**
2. **Safe Areas**
3. **Modular Type Scale**

When rules conflict, restore geometric balance first. Then reduce text by one or two approved
type steps. Split the scene before using smaller or arbitrary text.

## Center First

Pull the visual weight of every frame toward the geometric center:

- Anchor horizontal groups around `x = W / 2`.
- Distribute stacked blocks symmetrically around `y = H / 2`.
- Treat titles, card groups, screenshots, and footers as blocks with their own centers.
- For lists longer than five items, use a compact vertical stack while keeping the whole group
  centered.

Frame check: after hiding text, meaningful visual weight must remain within the central ±10% of
the canvas.

## Safe Areas

For a 1080×1920 Video Account frame:

| Edge | Minimum |
| --- | ---: |
| Top | 200 px |
| Bottom | 150 px |
| Left / right | 0 px |

Scale these values proportionally for other resolutions.

When content overflows:

1. Restore center alignment.
2. Drop one or two approved type levels.
3. Shorten copy.
4. Split the content into another scene.

## Modular Type Scale

Use only:

| Level | Size | Use |
| --- | ---: | --- |
| H1 | 144 | Single-line hook or primary title |
| H2 | 96 | Two-line title or page title |
| H3 | 60 | Section or card title |
| L | 44 | Body, label, hint, and footer |

Do not use body text below 44. Badges and number chips may use 36–48 when they are not required
for comprehension.

## Public Template Constants

Expose equivalent constants near the top of every template:

```text
SAFE_TOP = 200
SAFE_BOTTOM = 150
SAFE_LR = 0
W = 1080
H = 1920
CENTER_X = 540
CENTER_Y = 960
TYPE = {H1: 144, H2: 96, H3: 60, L: 44}
```

## Frame Checklist

- Is each major block centered around the canvas geometry?
- Are all required elements inside the safe area?
- Does every meaningful text element use the approved type scale?
- Is there at least 8 px breathing room between text, borders, and adjacent lines?
- Is the largest fitting approved type level being used?

## Evidence Viewport

- The central screenshot/video/animation evidence area is always 16:9.
- Adapt source media with aspect-ratio-preserving `contain` behavior by default; never use
  non-uniform scaling.
- Use proportional letterboxing for non-16:9 sources. Cropping is not allowed when it could
  remove text, UI edges, logos, or other evidence-bearing content.
