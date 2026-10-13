"""
Multi-Image Rotation Template
9:16 黄金短视频 · 1080×1920 · 8s

顶部标题 + 中部多图轮播 + 下部列表
Mac 本地 + Python + Pillow + FFmpeg

=== 编辑区（按需修改）===

把下面的 EDIT BLOCK 改了就行，其他不用动。
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

# ============ 编辑区 1：基本路径 ============
WORK_DIR = "/tmp/zcode-short"            # 工作目录（图片、字体都放这）
IMG_DIR = WORK_DIR                       # 图片也放这里，命名 img1.jpg / img2.jpg ...
OUTPUT_DIR = WORK_DIR
IMG_PREFIX = "img"
BGM_PATH = "/Users/biggersun/.workbuddy/skills/ip-ppt-video-pipeline/bgm/goodfeel.m4a"  # BGM 路径

# ============ 编辑区 2：内容 ============
TITLE_LINES = [
    # (文字, 颜色 RGB)
    ("GPT 额度不够用？",          (255, 165, 0)),   # 橙黄
    ("Codex 无缝接入",            (245, 247, 252)), # 白
    ("国内大模型 / 随时切换",     (245, 247, 252)),
]

LIST_ITEMS = [
    # (编号, 标题, 副标)
    ("01", "突破额度",      "流量分流给国内模型，token不再省着用"),
    ("02", "各取所长",      "推理靠 DeepSeek，看图靠 MiniMax，GPT 打硬仗"),
    ("03", "无需 CC Switch", "模型菜单直接选，一次配置永久生效"),
    ("04", "高频无压力",    "价格极低，每天跑几百次也不心疼"),
    ("05", "不锁定模型",    "智谱/千问/豆包随时接，改一行配置就好"),
]

# ============ 编辑区 3：图片与时间线 ============
# TRANSITIONS 中每一项 (start, end, from_img, to_img) 表示在 [start, end] 秒内从 from_img 切到 to_img
# 自动按这些切点划分时间段
# 例：
#   TRANSITIONS = [(1.5, 2.0, 1, 2), (3.5, 4.0, 2, 3), (5.5, 6.0, 3, 4)]
#   → 0-1.5: 图1, 1.5-2.0 切, 2.0-3.5: 图2, 3.5-4.0 切, 4.0-5.5: 图3, 5.5-6.0 切, 6.0-8.0: 图4
TRANSITIONS = [
    (1.5, 2.0, 1, 2),
    (3.5, 4.0, 2, 3),
    (5.5, 6.0, 3, 4),
]

# ============ 常量（一般不用改）============
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

# 列表编号色（循环）
CARD_COLORS = [
    (255, 122, 0),    # 橙
    (88, 199, 88),    # 绿
    (162, 96, 240),   # 紫
    (74, 158, 255),   # 青蓝
    (88, 199, 88),    # 绿
]

FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_REG = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_FB = "/System/Library/Fonts/PingFang.ttc"

# 布局
TITLE_Y0 = 130
UNIFIED_W = 1000
UNIFIED_H = int(UNIFIED_W * 383 / 900)  # 425
IMG_TOP = 334
IMG_X = CENTER_X - UNIFIED_W // 2
LIST_Y0 = IMG_TOP + UNIFIED_H + 36
LIST_ROW_H = 100
LIST_GAP = 28
LIST_APPEAR_T = 1.0
LIST_ANIM_DUR = 0.3


def get_font(size, bold=True):
    paths = [FONT_BOLD if bold else FONT_REG, FONT_FB, "/System/Library/Fonts/Hiragino Sans GB.ttc"]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def fit_image_contain(path, max_w, max_h, bg_color):
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    scale = min(max_w / sw, max_h / sh)
    new_w, new_h = int(sw * scale), int(sh * scale)
    src = src.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (max_w, max_h), bg_color)
    canvas.paste(src, ((max_w - new_w)//2, (max_h - new_h)//2))
    return canvas


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), size], radius=radius, fill=255)
    return mask


def img_path(idx):
    return os.path.join(IMG_DIR, f"{IMG_PREFIX}{idx}.jpg")


def get_current_image(t):
    """根据 TRANSITIONS 返回当前应显示的图。返回 (cur_idx, target_idx, swap_p, in_swap)"""
    for start, end, f, to in TRANSITIONS:
        if start <= t < end:
            swap_p = (t - start) / (end - start)
            return f, to, swap_p, True
    # 不在切换：按时间段确定当前图
    boundaries = [0.0]
    for start, end, f, to in TRANSITIONS:
        boundaries.append(start)
        boundaries.append(end)
    boundaries.append(8.0)
    for j in range(0, len(boundaries), 2):
        seg_start = boundaries[j]
        seg_end = boundaries[j+1] if j+1 < len(boundaries) else 8.0
        if seg_start <= t < seg_end:
            img_idx = (j // 2) + 1
            return img_idx, img_idx, 0, False
    return 1, 1, 0, False


def draw_image(canvas, img_idx, scale, alpha, cur_w, cur_h, cur_x, cur_y):
    src = fit_image_contain(img_path(img_idx), cur_w, cur_h, BG)
    if alpha < 1.0:
        bg_layer = Image.new("RGB", (cur_w, cur_h), BG)
        src = Image.blend(bg_layer, src, alpha)
    mask = rounded_mask((cur_w, cur_h), 28)
    canvas.paste(src, (cur_x, cur_y), mask)


def make_frame(t):
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # ===== 主标题 =====
    y = TITLE_Y0
    for i, (text, color) in enumerate(TITLE_LINES):
        line_t0 = 0.1 + i * 0.15
        line_t1 = line_t0 + 0.3
        if t < line_t0:
            line_alpha = 0
            y_offset = 15
        elif t < line_t1:
            p = (t - line_t0) / 0.3
            line_alpha = p
            y_offset = int(15 * (1 - p))
        else:
            line_alpha = 1.0
            y_offset = 0
        f = get_font(TYPE["H3"], bold=True)
        bbox = draw.textbbox((0, 0), text, font=f)
        tw = bbox[2] - bbox[0]
        a_color = tuple(int(c * line_alpha) for c in color)
        draw.text((CENTER_X - tw // 2 - bbox[0], y + y_offset - bbox[1]),
                  text, font=f, fill=a_color)
        y += TYPE["H3"] + 12

    # ===== 图片轮播 =====
    cur_idx, target_idx, swap_p, in_swap = get_current_image(t)

    if t < 1.0:
        enter_p = t / 1.0
        enter_scale = 0.88 + 0.12 * enter_p
        enter_alpha = enter_p
    else:
        enter_scale = 1.0
        enter_alpha = 1.0

    cur_w = int(UNIFIED_W * enter_scale)
    cur_h = int(UNIFIED_H * enter_scale)
    cur_x = IMG_X + (UNIFIED_W - cur_w) // 2
    cur_y = IMG_TOP + (UNIFIED_H - cur_h) // 2

    if in_swap:
        ease = swap_p * swap_p * (3 - 2 * swap_p)
        s1 = 1.0 - 0.2 * ease
        s1_w = int(UNIFIED_W * s1)
        s1_h = int(UNIFIED_H * s1)
        s1_x = IMG_X + (UNIFIED_W - s1_w) // 2 - int(40 * ease)
        s1_y = IMG_TOP + (UNIFIED_H - s1_h) // 2
        draw_image(canvas, cur_idx, 1.0, 1 - ease, s1_w, s1_h, s1_x, s1_y)
        s2 = 0.8 + 0.2 * ease
        s2_w = int(UNIFIED_W * s2)
        s2_h = int(UNIFIED_H * s2)
        s2_x = IMG_X + (UNIFIED_W - s2_w) // 2 + int(40 * (1 - ease))
        s2_y = IMG_TOP + (UNIFIED_H - s2_h) // 2
        draw_image(canvas, target_idx, 1.0, ease, s2_w, s2_h, s2_x, s2_y)
    else:
        draw_image(canvas, cur_idx, enter_scale, enter_alpha, cur_w, cur_h, cur_x, cur_y)

    # ===== 列表（1s 全部同时入场） =====
    if t >= LIST_APPEAR_T - LIST_ANIM_DUR:
        if t < LIST_APPEAR_T:
            list_alpha = (t - (LIST_APPEAR_T - LIST_ANIM_DUR)) / LIST_ANIM_DUR
        else:
            list_alpha = 1.0

        card_w = W - SAFE_LR * 2
        card_x = SAFE_LR

        for i, (num, title, desc) in enumerate(LIST_ITEMS):
            row_y = LIST_Y0 + i * (LIST_ROW_H + LIST_GAP)
            color = CARD_COLORS[i % len(CARD_COLORS)]

            card_bg = Image.new("RGBA", (card_w, LIST_ROW_H),
                                (15, 20, 35, int(140 * list_alpha)))
            cmask = rounded_mask((card_w, LIST_ROW_H), 18)
            canvas.paste(card_bg, (card_x, row_y), cmask)

            # 编号块
            num_size = 76
            num_x = card_x + 24
            num_y = row_y + (LIST_ROW_H - num_size) // 2
            num_bg = Image.new("RGBA", (num_size, num_size),
                               color + (int(255 * list_alpha),))
            nmask = rounded_mask((num_size, num_size), 13)
            canvas.paste(num_bg, (num_x, num_y), nmask)

            nf = get_font(int(num_size * 0.5), bold=True)
            n_bbox = draw.textbbox((0, 0), num, font=nf)
            n_w = n_bbox[2] - n_bbox[0]
            n_h = n_bbox[3] - n_bbox[1]
            n_tx = num_x + (num_size - n_w) // 2 - n_bbox[0]
            n_ty = num_y + (num_size - n_h) // 2 - n_bbox[1]
            draw.text((n_tx, n_ty), num, font=nf,
                      fill=(int(255*list_alpha), int(255*list_alpha), int(255*list_alpha)))

            # 标题 + 副标（靠左）
            text_x = num_x + num_size + 24
            title_font = get_font(TYPE["L"], bold=True)
            t_bbox = draw.textbbox((0, 0), title, font=title_font)
            t_x = text_x - t_bbox[0]
            t_y = row_y + 14 - t_bbox[1]
            draw.text((t_x, t_y), title, font=title_font,
                      fill=(int(255*list_alpha), int(255*list_alpha), int(255*list_alpha)))

            desc_font = get_font(TYPE["BADGE"])
            d_bbox = draw.textbbox((0, 0), desc, font=desc_font)
            d_color = tuple(int(c * list_alpha) for c in color)
            d_x = text_x - d_bbox[0]
            d_y = row_y + LIST_ROW_H - 36 - d_bbox[1]
            draw.text((d_x, d_y), desc, font=desc_font, fill=d_color)

    # 底部装饰
    bar_y = H - SAFE_BOTTOM + 20
    draw.rectangle([(CENTER_X - 60, bar_y), (CENTER_X + 60, bar_y + 4)], fill=ACCENT)
    wm_font = get_font(TYPE["BADGE"])
    draw.text((SAFE_LR + 20, H - SAFE_BOTTOM + 40),
              "@AI落地应用实干家", font=wm_font, fill=GRAY)

    return canvas


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fps = 30
    duration = 8.0
    total_frames = int(duration * fps)
    print(f"生成 {total_frames} 帧 ...")
    for i in range(total_frames):
        t = i / fps
        img = make_frame(t)
        img.save(os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png"), optimize=True)
        if i % 30 == 0:
            print(f"  t={t:.2f}s ({i}/{total_frames})")
    print("帧生成完毕")

    # 合成视频
    video_path = os.path.join(OUTPUT_DIR, "video.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "30",
        "-i", os.path.join(OUTPUT_DIR, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "slow", "-crf", "22", video_path
    ], check=True, capture_output=True)

    # 合成 BGM
    if os.path.exists(BGM_PATH):
        bgm_path = os.path.join(OUTPUT_DIR, "bgm.m4a")
        subprocess.run([
            "ffmpeg", "-y", "-ss", "0", "-t", "8", "-i", BGM_PATH,
            "-af", "afade=t=in:st=0:d=0.3,afade=t=out:st=7.5:d=0.5,volume=0.16",
            "-c:a", "aac", "-b:a", "128k", bgm_path
        ], check=True, capture_output=True)

        final_path = os.path.join(OUTPUT_DIR, "final.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path, "-i", bgm_path,
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", final_path
        ], check=True, capture_output=True)
        print(f"最终视频：{final_path}")
    else:
        print(f"未找到 BGM：{BGM_PATH}")
        print(f"无音视频：{video_path}")


if __name__ == "__main__":
    main()
