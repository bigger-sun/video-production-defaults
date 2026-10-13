"""
Title Card + Image Template
5 行主标题（高亮/可变色）+ 深色标题卡片 + 中部单图 + 无底部列表
1080×1920 / 30fps / 8s（所有内容 6s 内入场）

=== 编辑区（按需修改）===

把下面的 EDIT BLOCK 改了就行，其他不用动。
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

# ============ 编辑区 1：基本路径 ============
WORK_DIR = "/tmp/title-card-image"          # 工作目录（图片也放这里）
IMG_DIR = WORK_DIR
OUTPUT_DIR = WORK_DIR
IMG_PREFIX = "img"
BGM_PATH = "/Users/biggersun/.workbuddy/skills/ip-ppt-video-pipeline/bgm/goodfeel.m4a"

# ============ 编辑区 2：内容 ============
TITLE_LINES = [
    # (文字, 颜色 RGB)
    ("GPT额度不够用？",                  (255, 165, 0)),  # 橙黄
    ("Codex 原生无缝接入国内大模型",      (255, 165, 0)),
    ("可随时切换模型",                    (255, 165, 0)),
    ("无需 Codex++",                     (255, 165, 0)),
    ("无需 CC switch",                   (255, 165, 0)),
]

# 单张图：默认取 IMG_DIR/img1.jpg
IMG_COUNT = 1

# ============ 编辑区 3：时序常量 ============
TITLE_STAGGER = 0.45     # 标题每行错峰（秒）
TITLE_DUR = 0.40         # 标题每行淡入时长（秒）
IMG_ENTER_T0 = 3.0      # 图片入场开始
IMG_ENTER_T1 = 4.5      # 图片入场结束（4.5s 后保持静态）

# ============ 常量（一般不用改）============
W, H = 1080, 1920
CENTER_X = W // 2
CENTER_Y = H // 2
SAFE_TOP = 100
SAFE_BOTTOM = 150
SAFE_LR = 20
TYPE = {"H1": 144, "H2": 96, "H3": 60, "L": 44, "BADGE": 30}

BG = (10, 14, 26)
ACCENT = (255, 165, 0)
WHITE = (245, 247, 252)
GRAY = (140, 150, 170)

FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_REG = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_FB = "/System/Library/Fonts/PingFang.ttc"
FONT_FALLBACK = "/System/Library/Fonts/Hiragino Sans GB.ttc"

# 布局常量
TITLE_CARD_Y = 180          # 标题卡片顶 y
TITLE_CARD_PAD_X = 36
TITLE_CARD_PAD_Y = 32
TITLE_CARD_RADIUS = 28
TITLE_MAX_W = W - SAFE_LR * 2 - 20
TITLE_ROW_GAP = TYPE["H3"] + 14
TITLE_BAR_W = 6              # 标题左侧装饰条宽
TITLE_BAR_PAD = 16           # 标题条距左边距
TITLE_TAG_W = 108            # 标题右上短装饰条宽
TITLE_TAG_H = 4

IMG_GAP_BELOW_CARD = 80      # 卡片下方间距
IMG_MASK_RADIUS = 24         # 图片圆角

# 时长
DURATION = 8.0
FPS = 30

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


def fit_image_contain(path, max_w, max_h, bg_color):
    """等比缩放并在中间贴到底色画布上。"""
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


def img_path(idx):
    return os.path.join(IMG_DIR, f"{IMG_PREFIX}{idx}.jpg")


def measure_text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def fit_title_line(draw, text, font, max_w):
    """超宽标题按 / 分段或中点切两行。返回行列表（单行或多行）。"""
    if measure_text_width(draw, text, font) <= max_w:
        return [text]
    if "/" in text:
        parts = text.split("/")
        head = parts[0].rstrip()
        rest = "/".join(parts[1:]).strip()
        if head and rest:
            return [head, rest]
    mid = len(text) // 2
    return [text[:mid], text[mid:]]


# ============ 帧绘制 ============
def make_frame(t):
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # ===== 计算标题布局 =====
    f = get_font(TYPE["H3"], bold=True)
    wrapped = [(fit_title_line(draw, txt, f, TITLE_MAX_W), color)
               for txt, color in TITLE_LINES]
    total_rows = sum(len(rows) for rows, _ in wrapped)
    text_block_h = total_rows * TYPE["H3"] + (total_rows - 1) * 14

    # ===== 标题卡片 =====
    card_w = W - SAFE_LR * 2
    card_h = text_block_h + TITLE_CARD_PAD_Y * 2
    card_x = SAFE_LR
    card_y = TITLE_CARD_Y

    # 卡片入场（与首行标题同步淡入）
    if t < 0.1:
        card_alpha = 0.0
    elif t < 0.4:
        card_alpha = (t - 0.1) / 0.3
    else:
        card_alpha = 1.0

    if card_alpha > 0:
        # 卡片底色（深色圆角矩形）
        bg_alpha = int(235 * card_alpha)
        card_bg = Image.new("RGBA", (card_w, card_h), (24, 28, 44, bg_alpha))
        c_mask = rounded_mask((card_w, card_h), TITLE_CARD_RADIUS)
        canvas.paste(card_bg, (card_x, card_y), c_mask)

        # 左侧橙色装饰竖条
        bar_w = TITLE_BAR_W
        bar_x = card_x + TITLE_BAR_PAD
        bar_y0 = card_y + 22
        bar_y1 = card_y + card_h - 22
        draw.rectangle([(bar_x, bar_y0), (bar_x + bar_w, bar_y1)], fill=ACCENT)

        # 右上角短横装饰
        tag_x0 = card_x + card_w - TITLE_TAG_W - 22
        tag_x1 = card_x + card_w - 22
        tag_y = card_y + 22
        draw.rectangle([(tag_x0, tag_y), (tag_x1, tag_y + TITLE_TAG_H)], fill=ACCENT)

    # ===== 标题文字（5 行，逐行淡入） =====
    seg_idx = 0
    y = card_y + TITLE_CARD_PAD_Y
    for rows, color in wrapped:
        line_t0 = 0.1 + seg_idx * TITLE_STAGGER
        line_t1 = line_t0 + TITLE_DUR
        seg_idx += 1
        for row in rows:
            if t < line_t0:
                line_alpha = 0.0
                y_offset = 14
            elif t < line_t1:
                p = (t - line_t0) / TITLE_DUR
                line_alpha = p
                y_offset = int(14 * (1 - p))
            else:
                line_alpha = 1.0
                y_offset = 0
            bbox = draw.textbbox((0, 0), row, font=f)
            tw = bbox[2] - bbox[0]
            a_color = tuple(int(c * line_alpha) for c in color)
            draw.text(
                (CENTER_X - tw // 2 - bbox[0], y + y_offset - bbox[1]),
                row, font=f, fill=a_color,
            )
            y += TITLE_ROW_GAP

    # ===== 单图：3.0-4.5s 入场，4.5-8.0s 静态 =====
    if t < IMG_ENTER_T0:
        enter_p = 0.0
        enter_scale = 0.88
        enter_alpha = 0.0
    elif t < IMG_ENTER_T1:
        p = (t - IMG_ENTER_T0) / (IMG_ENTER_T1 - IMG_ENTER_T0)
        ease = p * p * (3 - 2 * p)  # smoothstep
        enter_scale = 0.88 + 0.12 * ease
        enter_alpha = ease
    else:
        enter_scale = 1.0
        enter_alpha = 1.0

    IMG_W = W                              # 宽度铺满
    IMG_H = int(IMG_W / (833 / 533))       # 691，对应参考图比例
    IMG_TOP = card_y + card_h + IMG_GAP_BELOW_CARD

    # 防溢出底部
    if IMG_TOP + IMG_H > H - 60:
        IMG_TOP = H - 60 - IMG_H

    cur_w = int(IMG_W * enter_scale)
    cur_h = int(IMG_H * enter_scale)
    cur_x = (W - cur_w) // 2
    cur_y = IMG_TOP + (IMG_H - cur_h) // 2

    img1 = fit_image_contain(img_path(1), cur_w, cur_h, BG)
    if enter_alpha < 1.0:
        bg_layer = Image.new("RGB", (cur_w, cur_h), BG)
        img1 = Image.blend(bg_layer, img1, enter_alpha)
    mask = rounded_mask((cur_w, cur_h), IMG_MASK_RADIUS)
    canvas.paste(img1, (cur_x, cur_y), mask)

    return canvas


# ============ 主流程 ============
def render_frames():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total_frames = int(DURATION * FPS)
    print(f"生成 {total_frames} 帧 @ {FPS}fps ({DURATION}s) → {OUTPUT_DIR}")
    for i in range(total_frames):
        t = i / FPS
        img = make_frame(t)
        img.save(os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png"), optimize=True)
        if i % 30 == 0:
            print(f"  t={t:.2f}s ({i}/{total_frames})")
    print("帧生成完毕")


def encode_video():
    video_path = os.path.join(OUTPUT_DIR, "video.mp4")
    print(f"合成视频：{video_path}")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", os.path.join(OUTPUT_DIR, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "slow", "-crf", "22", video_path,
    ], check=True, capture_output=True)
    return video_path


def mix_bgm(video_path):
    if not os.path.exists(BGM_PATH):
        print(f"⚠️ 未找到 BGM：{BGM_PATH},跳过混音")
        return None
    bgm_path = os.path.join(OUTPUT_DIR, "bgm.m4a")
    subprocess.run([
        "ffmpeg", "-y", "-ss", "0", "-t", str(DURATION), "-i", BGM_PATH,
        "-af", "afade=t=in:st=0:d=0.3,afade=t=out:st={:.1f}:d=0.5,volume=0.16".format(DURATION - 0.5),
        "-c:a", "aac", "-b:a", "128k", bgm_path,
    ], check=True, capture_output=True)
    final_path = os.path.join(OUTPUT_DIR, "final.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path, "-i", bgm_path,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", final_path,
    ], check=True, capture_output=True)
    print(f"✅ 成品：{final_path}")
    return final_path


def cleanup_frames():
    for name in os.listdir(OUTPUT_DIR):
        if name.startswith("frame_") and name.endswith(".png"):
            os.remove(os.path.join(OUTPUT_DIR, name))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not os.path.exists(img_path(1)):
        print(f"❌ 缺少图片：{img_path(1)}")
        return
    render_frames()
    video_path = encode_video()
    final = mix_bgm(video_path)
    cleanup_frames()
    if final:
        print(f"\n最终视频：{final}")


if __name__ == "__main__":
    main()
