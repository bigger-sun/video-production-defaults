"""
Title Card + Image 封面 v1
5 行主标题（全部橙黄高亮）+ 中部实拍图（contain 完整显示）+ 无公众号引导
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ============ 编辑区 1：路径 ============
WORK_DIR = "/tmp/title-card-image"
IMG_DIR = WORK_DIR
COVER_PATH = os.path.join(WORK_DIR, "cover.png")

# ============ 编辑区 2：内容（主标题）============
TITLE_LINES = [
    ("GPT额度不够用？",                  (255, 165, 0)),
    ("Codex 原生无缝接入国内大模型",      (255, 165, 0)),
    ("可随时切换模型",                    (255, 165, 0)),
    ("无需 Codex++",                     (255, 165, 0)),
    ("无需 CC switch",                   (255, 165, 0)),
]

# ============ 常量（一般不用改）============
W, H = 1080, 1920
CENTER_X = W // 2
SAFE_TOP = 100
SAFE_BOTTOM = 150
SAFE_LR = 20
TYPE = {"H3": 60}

BG = (10, 14, 26)
ACCENT = (255, 165, 0)
WHITE = (245, 247, 252)
GRAY = (140, 150, 170)

FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_REG = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_FB = "/System/Library/Fonts/PingFang.ttc"
FONT_FALLBACK = "/System/Library/Fonts/Hiragino Sans GB.ttc"

TITLE_MAX_W = W - SAFE_LR * 2 - 20
TITLE_ROW_GAP = TYPE["H3"] + 14

# ============ 工具函数 ============
def get_font(size, bold=True):
    paths = [FONT_BOLD if bold else FONT_REG, FONT_FB, FONT_FALLBACK]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def fit_contain(path, max_w, max_h, bg_color=BG):
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    scale = min(max_w / sw, max_h / sh)
    new_w, new_h = int(sw * scale), int(sh * scale)
    src = src.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (max_w, max_h), bg_color)
    canvas.paste(src, ((max_w - new_w) // 2, (max_h - new_h) // 2))
    return canvas


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), size], radius=radius, fill=255)
    return mask


def measure_text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def fit_line(draw, text, font):
    if measure_text_width(draw, text, font) <= TITLE_MAX_W:
        return [text]
    if "/" in text:
        parts = text.split("/")
        head = parts[0].rstrip()
        rest = "/".join(parts[1:]).strip()
        if head and rest:
            return [head, rest]
    mid = len(text) // 2
    return [text[:mid], text[mid:]]


def text_center(draw, text, y, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((CENTER_X - tw // 2 - bbox[0], y - bbox[1]), text, font=font, fill=color)


# ============ 封面绘制 ============
def main():
    os.makedirs(WORK_DIR, exist_ok=True)
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    f = get_font(TYPE["H3"], bold=True)
    wrapped = [(fit_line(draw, t, f), c) for t, c in TITLE_LINES]
    total_rows = sum(len(rows) for rows, _ in wrapped)
    block_h = total_rows * TYPE["H3"] + (total_rows - 1) * 14

    IMG_W = W
    IMG_H = int(IMG_W / (833 / 533))   # 691
    IMG_GAP = 60
    total_content_h = block_h + IMG_GAP + IMG_H

    # 整体垂直居中
    content_y0 = (H - total_content_h) // 2

    y = content_y0
    for rows, color in wrapped:
        for row in rows:
            text_center(draw, row, y, f, color)
            y += TITLE_ROW_GAP

    # 中部图（contain）
    IMG_TOP = content_y0 + block_h + IMG_GAP
    img1_path = os.path.join(IMG_DIR, "img1.jpg")
    if not os.path.exists(img1_path):
        print(f"⚠️ 找不到 {img1_path},封面将只渲染标题")
        out = COVER_PATH
    else:
        img1 = fit_contain(img1_path, IMG_W, IMG_H)
        mask = rounded_mask((IMG_W, IMG_H), 24)
        canvas.paste(img1, (0, IMG_TOP), mask)
        out = COVER_PATH
    canvas.save(out, quality=92, optimize=True)
    print(f"封面已保存：{out}")


if __name__ == "__main__":
    main()
