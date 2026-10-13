"""
Six Card List Template - 封面生成(可选)
封面通常建议用 imagegen skill,这里是占位实现
"""
import os
from PIL import Image, ImageDraw, ImageFont

WORK_DIR = "/tmp/six-card-list"
TITLE = "Codex 必装的 6 个软件"
SUBTITLE = "装好这 6 个,Codex 直接起飞"

W, H = 1080, 1920
BG = (10, 14, 26)
WHITE = (245, 247, 252)
GRAY = (140, 150, 170)
ACCENT = (255, 140, 60)

FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_REG = "/System/Library/Fonts/STHeiti Light.ttc"


def get_font(size, bold=True):
    p = FONT_BOLD if bold else FONT_REG
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main():
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    f_h1 = get_font(120, bold=True)
    f_h3 = get_font(60, bold=False)

    # 标题(主色高亮)
    bbox = draw.textbbox((0, 0), TITLE, font=f_h1)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2 - bbox[0], 600), TITLE, font=f_h1, fill=ACCENT)

    # 副标题
    bbox = draw.textbbox((0, 0), SUBTITLE, font=f_h3)
    sw = bbox[2] - bbox[0]
    draw.text(((W - sw) // 2 - bbox[0], 780), SUBTITLE, font=f_h3, fill=GRAY)

    os.makedirs(WORK_DIR, exist_ok=True)
    out = os.path.join(WORK_DIR, "cover.png")
    canvas.save(out, optimize=True)
    print(f"封面:{out}")


if __name__ == "__main__":
    main()
