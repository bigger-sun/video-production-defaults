"""
封面 v11：去小标题 + 加图2
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
CENTER_X = W // 2
CENTER_Y = H // 2
SAFE_TOP = 100
SAFE_BOTTOM = 150
SAFE_LR = 20
TYPE = {"H1": 144, "H2": 96, "H3": 60, "L": 44, "BADGE": 36}

BG = (10, 14, 26)
ACCENT = (255, 165, 0)
CYAN = (74, 158, 255)
WHITE = (245, 247, 252)
GRAY = (140, 150, 170)

CARD_COLORS = [
    (255, 122, 0),
    (88, 199, 88),
    (162, 96, 240),
    (74, 158, 255),
    (88, 199, 88),
]

FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_REG = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_FB = "/System/Library/Fonts/PingFang.ttc"


def get_font(size, bold=True):
    paths = [FONT_BOLD if bold else FONT_REG, FONT_FB, "/System/Library/Fonts/Hiragino Sans GB.ttc"]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def fit_contain(path, max_w, max_h):
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    scale = min(max_w / sw, max_h / sh)
    new_w, new_h = int(sw * scale), int(sh * scale)
    src = src.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (max_w, max_h), BG)
    canvas.paste(src, ((max_w - new_w)//2, (max_h - new_h)//2))
    return canvas


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), size], radius=radius, fill=255)
    return mask


# ===== 封面 =====
canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

# 主标题 3 行（H3=60）
title_lines = [
    ("GPT 额度不够用？", ACCENT, TYPE["H3"]),
    ("Codex 无缝接入", WHITE, TYPE["H3"]),
    ("国内大模型 / 随时切换", WHITE, TYPE["H3"]),
]
y = 220
for text, color, size in title_lines:
    f = get_font(size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text((CENTER_X - tw // 2 - bbox[0], y - bbox[1]), text, font=f, fill=color)
    y += size + 12

# 两张图
UNIFIED_W = 900
UNIFIED_H = int(UNIFIED_W * 383 / 900)
IMG_TOP = 460
IMG_X = CENTER_X - UNIFIED_W // 2

# 图1
img1 = fit_contain("/tmp/zcode-short/img1.jpg", UNIFIED_W, UNIFIED_H)
mask1 = rounded_mask((UNIFIED_W, UNIFIED_H), 28)
canvas.paste(img1, (IMG_X, IMG_TOP), mask1)

# 列表 5 条
LIST_Y0 = IMG_TOP + UNIFIED_H + 50
LIST_ROW_H = 110
LIST_GAP = 28

highlights = [
    ("01", "突破额度", "流量分流给国内模型，token不再省着用"),
    ("02", "各取所长", "推理靠 DeepSeek，看图靠 MiniMax，GPT 打硬仗"),
    ("03", "无需 CC Switch", "模型菜单直接选，一次配置永久生效"),
    ("04", "高频无压力", "价格极低，每天跑几百次也不心疼"),
    ("05", "不锁定模型", "智谱/千问/豆包随时接，改一行配置就好"),
]
card_w = W - SAFE_LR * 2
card_x = SAFE_LR

for i, (num, t1, t2) in enumerate(highlights):
    row_y = LIST_Y0 + i * (LIST_ROW_H + LIST_GAP)
    color = CARD_COLORS[i % len(CARD_COLORS)]

    # 卡片背景（无边框）
    card_bg = Image.new("RGBA", (card_w, LIST_ROW_H), (15, 20, 35, 140))
    cmask = rounded_mask((card_w, LIST_ROW_H), 16)
    canvas.paste(card_bg, (card_x, row_y), cmask)

    # 编号块
    num_size = 64
    num_x = card_x + 22
    num_y = row_y + (LIST_ROW_H - num_size) // 2
    num_bg = Image.new("RGBA", (num_size, num_size), color)
    nmask = rounded_mask((num_size, num_size), 10)
    canvas.paste(num_bg, (num_x, num_y), nmask)

    nf = get_font(int(num_size * 0.5), bold=True)
    n_bbox = draw.textbbox((0, 0), num, font=nf)
    n_w = n_bbox[2] - n_bbox[0]
    n_h = n_bbox[3] - n_bbox[1]
    n_tx = num_x + (num_size - n_w) // 2 - n_bbox[0]
    n_ty = num_y + (num_size - n_h) // 2 - n_bbox[1]
    draw.text((n_tx, n_ty), num, font=nf, fill=WHITE)

    # 标题 + 副标（靠左）
    text_x = num_x + num_size + 22
    title_font = get_font(TYPE["L"], bold=True)
    t_bbox = draw.textbbox((0, 0), t1, font=title_font)
    t_color = (255, 200, 80) if num in ("01", "02") else WHITE
    draw.text((text_x - t_bbox[0], row_y + 14 - t_bbox[1]), t1, font=title_font, fill=t_color)

    desc_font = get_font(TYPE["BADGE"])
    d_bbox = draw.textbbox((0, 0), t2, font=desc_font)
    draw.text((text_x - d_bbox[0], row_y + LIST_ROW_H - 32 - d_bbox[1]),
              t2, font=desc_font, fill=color)

# 底部装饰
bar_y = H - SAFE_BOTTOM + 20
draw.rectangle([(CENTER_X - 80, bar_y), (CENTER_X + 80, bar_y + 4)], fill=ACCENT)
wm_font = get_font(TYPE["BADGE"])
draw.text((SAFE_LR + 30, H - SAFE_BOTTOM + 35), "@AI落地应用实干家", font=wm_font, fill=GRAY)
cta_font = get_font(TYPE["BADGE"], bold=True)
cta_text = "→ 视频详解"
c_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
c_w = c_bbox[2] - c_bbox[0]
draw.text((W - SAFE_LR - 30 - c_w - c_bbox[0], H - SAFE_BOTTOM + 35 - c_bbox[1]),
          cta_text, font=cta_font, fill=ACCENT)

canvas.save("/tmp/zcode-short/cover.jpg", quality=92, optimize=True)
print("封面保存")
