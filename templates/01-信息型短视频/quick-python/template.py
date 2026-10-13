"""Render a fixed 9-second Golden Short with Pillow and FFmpeg.

Example:
    uv run --with pillow template.py --project-root /path/to/project --slug quick-ranking
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# EDIT BLOCK 1: output identity
DEFAULT_SLUG = "quick-ranking"

# EDIT BLOCK 2: hook and payoff
COPY = {
    "eyebrow": "快速避坑",
    "title": "3 个视频工具怎么选",
    "accent": "别再重复安装",
    "outro": "按场景选工具，效率最高",
}

# EDIT BLOCK 3: use exactly 3 compact cards.
CARDS = [
    {"number": "01", "title": "FFmpeg", "tag": "基础处理", "detail": "转码、裁剪、混音", "color": (52, 211, 153)},
    {"number": "02", "title": "Remotion", "tag": "模板视频", "detail": "列表、榜单、批量出片", "color": (96, 165, 250)},
    {"number": "03", "title": "HyperFrames", "tag": "网页动效", "detail": "HTML、GSAP、音频响应", "color": (167, 139, 250)},
]


WIDTH = 1080
HEIGHT = 1920
SAFE_TOP = 100
SAFE_BOTTOM = 150
SAFE_LR = 20
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
TYPE = {"H1": 144, "H2": 96, "H3": 60, "L": 44}
FPS = 30
HOOK_FRAMES = 36
CARD_FRAMES = 66
OUTRO_FRAMES = 36
TOTAL_FRAMES = HOOK_FRAMES + len(CARDS) * CARD_FRAMES + OUTRO_FRAMES

BACKGROUND = (9, 13, 24)
PANEL = (19, 27, 47)
TEXT = (244, 247, 251)
MUTED = (156, 174, 203)
GOLD = (251, 191, 36)

# 字体：按平台候选顺序取第一个存在的（macOS 优先，兼容 Windows）
FONT_REGULAR_CANDIDATES = [
    Path("/System/Library/Fonts/STHeiti Light.ttc"),
    Path("/System/Library/Fonts/Supplemental/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("C:/Windows/Fonts/msyh.ttc"),
]
FONT_BOLD_CANDIDATES = [
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/System/Library/Fonts/Supplemental/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("C:/Windows/Fonts/msyhbd.ttc"),
]


def _first_existing(candidates: list[Path], label: str) -> Path:
    for path in candidates:
        if path.exists():
            return path
    tried = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"{label} CJK font not found; tried: {tried}")


FONT_REGULAR = _first_existing(FONT_REGULAR_CANDIDATES, "regular")
FONT_BOLD = _first_existing(FONT_BOLD_CANDIDATES, "bold")
DEFAULT_BGM = Path("/Users/biggersun/.workbuddy/skills/ip-ppt-video-pipeline/bgm/goodfeel.m4a")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--slug", default=DEFAULT_SLUG)
    parser.add_argument("--bgm", type=Path, default=DEFAULT_BGM)
    return parser.parse_args()


def ease(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return 1 - (1 - value) ** 3


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(str(path), size)


def scaled(color: tuple[int, int, int], opacity: float) -> tuple[int, int, int]:
    return tuple(int(BACKGROUND[i] + (color[i] - BACKGROUND[i]) * opacity) for i in range(3))


def draw_centered(draw: ImageDraw.ImageDraw, y: int, text: str, text_font, color) -> None:
    draw.text((WIDTH / 2, y), text, font=text_font, fill=color, anchor="mm")


def new_frame() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.ellipse((-450, 1260, 520, 2230), fill=(12, 42, 58))
    draw.ellipse((690, -320, 1410, 400), fill=(30, 28, 70))
    return image, draw


def hook_frame(local_frame: int) -> Image.Image:
    image, draw = new_frame()
    enter = ease(min(1.0, local_frame / 10))
    exit_opacity = 1.0 if local_frame < 26 else max(0.0, (36 - local_frame) / 10)
    opacity = enter * exit_opacity

    draw_centered(draw, 520, COPY["eyebrow"], font(TYPE["L"], True), scaled((125, 211, 252), opacity))
    draw_centered(draw, 770, COPY["title"], font(TYPE["H2"], True), scaled(TEXT, opacity))
    draw_centered(draw, 990, COPY["accent"], font(TYPE["H3"], True), scaled(GOLD, opacity))
    return image


def card_frame(card_index: int, local_frame: int) -> Image.Image:
    image, draw = new_frame()
    card = CARDS[card_index]
    color = card["color"]
    enter = ease(min(1.0, local_frame / 12))
    exit_opacity = 1.0 if local_frame < CARD_FRAMES - 10 else max(0.0, (CARD_FRAMES - local_frame) / 10)
    opacity = enter * exit_opacity
    offset = int(44 * (1 - enter))

    draw.text((78, 142), COPY["eyebrow"], font=font(TYPE["L"], True), fill=scaled((125, 211, 252), opacity))
    draw.text((78, 205), COPY["title"], font=font(TYPE["H3"], True), fill=scaled(TEXT, opacity))

    top = 470 + offset
    draw.rounded_rectangle((70, top, WIDTH - 70, 1450 + offset), radius=34, fill=PANEL, outline=scaled(color, opacity), width=4)
    draw.rounded_rectangle((122, top + 70, 250, top + 198), radius=28, fill=scaled(color, opacity * 0.24), outline=scaled(color, opacity), width=3)
    draw.text((186, top + 134), card["number"], font=font(48, True), fill=scaled(color, opacity), anchor="mm")
    draw.text((290, top + 98), card["tag"], font=font(TYPE["L"], True), fill=scaled(color, opacity))

    title_size = TYPE["H2"] if len(card["title"]) <= 12 else TYPE["H3"]
    draw.text((122, top + 310), card["title"], font=font(title_size, True), fill=scaled(TEXT, opacity))
    draw.rounded_rectangle((122, top + 465, WIDTH - 122, top + 472), radius=4, fill=scaled(color, opacity))
    draw.text((122, top + 560), card["detail"], font=font(TYPE["L"], True), fill=scaled(MUTED, opacity))

    progress_width = (WIDTH - 180) / len(CARDS)
    progress_y = 1630
    for index in range(len(CARDS)):
        fill = CARDS[index]["color"] if index <= card_index else (55, 69, 96)
        x0 = 90 + index * progress_width
        draw.rounded_rectangle((x0, progress_y, x0 + progress_width - 18, progress_y + 14), radius=7, fill=fill)
    return image


def outro_frame(local_frame: int) -> Image.Image:
    image, draw = new_frame()
    opacity = ease(min(1.0, local_frame / 12))
    draw_centered(draw, 660, "选择工具的标准", font(TYPE["H3"], True), scaled((125, 211, 252), opacity))
    draw_centered(draw, 850, COPY["outro"], font(TYPE["H2"], True), scaled(TEXT, opacity))
    draw_centered(draw, 1090, "收藏这张选择逻辑", font(TYPE["L"], True), scaled(GOLD, opacity))
    return image


def validate_inputs(args: argparse.Namespace) -> None:
    if len(CARDS) != 3:
        raise ValueError("quick-python requires exactly 3 cards for a 9-second timeline")
    if args.slug in {"", ".", ".."} or Path(args.slug).name != args.slug:
        raise ValueError("slug must be one directory-safe name")
    if not FONT_REGULAR.exists() or not FONT_BOLD.exists():
        raise FileNotFoundError(
            "a CJK font is required (STHeiti / Hiragino Sans GB / PingFang / Microsoft YaHei)"
        )
    if not args.bgm.exists():
        raise FileNotFoundError(f"BGM not found: {args.bgm}")
    if shutil.which("ffmpeg") is None:
        raise FileNotFoundError("ffmpeg is not available on PATH")


def frames():
    for local_frame in range(HOOK_FRAMES):
        yield hook_frame(local_frame)
    for card_index in range(len(CARDS)):
        for local_frame in range(CARD_FRAMES):
            yield card_frame(card_index, local_frame)
    for local_frame in range(OUTRO_FRAMES):
        yield outro_frame(local_frame)


def render_video(output_file: Path, bgm: Path) -> None:
    duration = TOTAL_FRAMES / FPS
    fade_out_start = duration - 1
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-pixel_format",
        "rgb24",
        "-video_size",
        f"{WIDTH}x{HEIGHT}",
        "-framerate",
        str(FPS),
        "-i",
        "pipe:0",
        "-stream_loop",
        "-1",
        "-i",
        str(bgm),
        "-filter_complex",
        f"[1:a]volume=0.24,afade=t=in:st=0:d=0.5,afade=t=out:st={fade_out_start}:d=1[a]",
        "-map",
        "0:v",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-r",
        str(FPS),
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        f"{duration:.3f}",
        "-movflags",
        "+faststart",
        str(output_file),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        if process.stdin is None:
            raise RuntimeError("ffmpeg stdin is unavailable")
        for image in frames():
            process.stdin.write(image.tobytes())
        process.stdin.close()
        return_code = process.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, command)
    except Exception:
        if process.stdin is not None and not process.stdin.closed:
            process.stdin.close()
        process.kill()
        process.wait()
        raise


def main() -> None:
    args = parse_args()
    validate_inputs(args)
    output_dir = args.project_root.resolve() / "out" / "golden-shorts" / args.slug
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "video.mp4"

    render_video(output_file, args.bgm.resolve())

    print(f"video={output_file}")
    print(f"duration={TOTAL_FRAMES / FPS:.1f}s")
    print(f"cover={output_dir / 'cover.png'} (generate separately with ImageGen)")


if __name__ == "__main__":
    main()
