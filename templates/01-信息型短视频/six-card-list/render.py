"""Six Card List Template - 宽松首屏问题列表 + N 张紧凑自适应卡片
N 自适应,默认 6 卡 × 3.0s + 钩子 4.0s = 22s,无收尾段
1080×1920 / 30fps / Mac 本地 Python + Pillow + FFmpeg
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

# ============ 编辑区 1:基本路径 ============
WORK_DIR = "/tmp/six-card-list"
BGM_PATH = "/Users/biggersun/.workbuddy/skills/ip-ppt-video-pipeline/bgm/goodfeel.m4a"
BGM_VOLUME = 0.48

# ============ 编辑区 2:内容(基于 ChatCut 6 场景示例)============
# 标题严格保留原主题一字不变(英文破折号 —、逗号 ,)
TITLE_BRAND = "ChatCut"
TITLE_REST1 = "—Codex 里的可视化剪辑工具,"
TITLE_REST2 = "从素材到成片只需一句话"
SUBTITLE = "6 个创作场景,一句话出片"

ITEMS = [
    {
        "question": "1、口播剪辑能自动完成什么？",
        "tag": "短视频",
        "conclusion": ["录完口播，一句话剪完"],
        "bullets": [["自动转写并删除停顿"], ["生成字幕与重点强调"], ["适合口播账号日常更新"]],
        "takeaway": ["把重复剪辑交给自动化"],
    },
    {
        "question": "2、MG 动画解决什么问题？",
        "tag": "可视化",
        "conclusion": ["让抽象信息跟着内容动起来"],
        "bullets": [["生成标题条和步骤卡"], ["数据图随讲解同步出现"], ["视觉表达不再与内容脱节"]],
        "takeaway": ["动效是信息，不是装饰"],
    },
    {
        "question": "3、长视频怎么变成短视频？",
        "tag": "二次创作",
        "conclusion": ["自动提取高光并拆成多条短片"],
        "bullets": [["识别可独立传播的片段"], ["重新组织节奏与字幕"], ["适合矩阵账号持续分发"]],
        "takeaway": ["一份素材，多次复用"],
    },
    {
        "question": "4、产品宣传片怎么快速制作？",
        "tag": "营销",
        "conclusion": ["录屏、旁白和重点标注一次完成"],
        "bullets": [["展示核心使用流程"], ["自动补充讲解和放大"], ["不用外包也能快速上线"]],
        "takeaway": ["先展示结果，再解释功能"],
    },
    {
        "question": "5、AI 短片可以做到什么？",
        "tag": "创意",
        "conclusion": ["从提示词生成一条完整创意片"],
        "bullets": [["生成画面与镜头变化"], ["补充旁白、字幕和音乐"], ["快速验证创意方向"]],
        "takeaway": ["先低成本验证，再精细制作"],
    },
    {
        "question": "6、讲解视频怎么更容易看懂？",
        "tag": "知识",
        "conclusion": ["用动态图形承接关键解释"],
        "bullets": [["把步骤和关系直接画出来"], ["重点结论单独形成视觉层"], ["降低抽象概念理解成本"]],
        "takeaway": ["看得见，才更容易记住"],
    },
]

# 6 色(顺序对应 ITEMS;边框/名称/进度条均用此色)
COLORS = [
    (255, 140, 60),    # 橙 — 口播
    (180, 130, 255),   # 紫 — MG
    (80, 220, 240),    # 青 — 长转短
    (255, 200, 60),    # 金 — 产品
    (255, 100, 180),   # 粉 — AI 短片
    (120, 220, 100),   # 绿 — 讲解
]

# ============ 编辑区 3:时序常量 ============
HOOK_DUR = 4.0        # 钩子时长
CARD_DUR = 3.0        # 每张卡片默认时长
SUMMARY_DUR = 0       # 不使用收尾段

W, H = 1080, 1920
CENTER_X = W // 2
SAFE_TOP = 200
SAFE_BOTTOM = 150
SAFE_LR = 60
TYPE = {"H1": 130, "H2": 96, "H3": 64, "H4": 60, "L": 44, "BADGE": 36, "LIST_NAME": 56, "LIST_TAG": 36}

BG = (10, 14, 26)
WHITE = (245, 247, 252)
GRAY = (160, 170, 190)
DIM = (60, 70, 90)
CARD_DARK = (24, 28, 44)
ACCENT = (255, 140, 60)

FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_REG = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_FB = "/System/Library/Fonts/PingFang.ttc"

# 卡片布局：问题标题在卡片外上方，卡片高度按正文自动收缩
QUESTION_TOP = 220
QUESTION_LINE_H = 72
QUESTION_CARD_GAP = 28
CARD_TOP = 360
CARD_W = W - SAFE_LR * 2
CARD_H = 1040
CARD_PAD_X = 56
CARD_RADIUS = 32
CARD_BORDER_W = 4      # 边框粗细

# 卡内图片(上半部分配图,fill cover 避免黑边)
CARD_IMG_H = 320           # 可选图区高度；结构化文字卡默认不启用
CARD_IMG_RADIUS = 24       # 图圆角
CARD_IMG_MARGIN = 36       # 图到卡片边距

# 模式开关:True=上图下文(图必填),False=纯文字顶置(v7 行为)
USE_IMAGES = False         # 结构化文字卡默认关闭图片；旧四元组仍支持图片模式

# 卡片内文字(图下方)
NAME_SIZE = 80             # 名称(图下方,字号从 120 降到 80 让图片有更多视觉重心)
TAG_SIZE = 40
QUOTE_SIZE = 56
DESC_SIZE = 42

# 无图模式下的字号(v7 风格的"顶置大字")
NAME_SIZE_NO_IMG = 120     # 名称大字顶置
QUOTE_SIZE_NO_IMG = 64     # 金句
DESC_SIZE_NO_IMG = 46      # 描述

# 钩子列表行
LIST_LINE_H = 54
LIST_PAD_Y = 20
LIST_GAP = 24

PROGRESS_Y = H - 340      # 距卡片底 180px 呼吸距(用户指定)
PROGRESS_BLOCK_W = 140
PROGRESS_BLOCK_H = 14
PROGRESS_BLOCK_GAP = 16

SLIDE_DIST = 60
SLIDE_DUR = 0.4

DURATION = HOOK_DUR + len(ITEMS) * CARD_DUR   # 去掉收尾
FPS = 30

def get_font(size, bold=True):
    paths = [FONT_BOLD if bold else FONT_REG, FONT_FB]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), size], radius=radius, fill=255)
    return mask

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def ease_out_cubic(p):
    return 1 - (1 - p) ** 3


def as_lines(value):
    """Normalize a string or line collection without changing its characters."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [str(line) for line in value]


def wrap_exact(draw, text, font, max_width):
    """Wrap text by measured width while preserving every source character."""
    if not text:
        return [""]
    lines = []
    current = ""
    for char in text:
        candidate = current + char
        if current and text_size(draw, candidate, font)[0] > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    assert "".join(lines) == text
    return lines


def normalize_item(raw):
    """Support both the structured card schema and the legacy four-tuple schema."""
    if isinstance(raw, dict):
        question = str(raw["question"])
        provided_question_lines = as_lines(raw.get("question_lines"))
        if provided_question_lines:
            assert "".join(provided_question_lines) == question, question
        return {
            "question": question,
            "question_lines": provided_question_lines,
            "tag": str(raw.get("tag", "")),
            "conclusion": as_lines(raw.get("conclusion")),
            "bullets": [as_lines(lines) for lines in raw.get("bullets", [])],
            "takeaway": as_lines(raw.get("takeaway")),
        }

    name, tag, quote, desc = raw
    return {
        "question": str(name),
        "question_lines": [],
        "tag": str(tag),
        "conclusion": [str(quote)],
        "bullets": [[str(desc)]] if desc else [],
        "takeaway": [],
    }


def question_lines(draw, card, font, max_width):
    lines = card["question_lines"] or wrap_exact(draw, card["question"], font, max_width)
    assert "".join(lines) == card["question"], card["question"]
    return lines

def draw_hook_list_style(canvas, t):
    draw = ImageDraw.Draw(canvas)

    title_a = min(1.0, max(0.0, t / 0.55))
    sub_a = min(1.0, max(0.0, (t - 0.35) / 0.55))
    list_start = 0.65

    f_h1 = get_font(TYPE["H1"], bold=True)
    f_h3 = get_font(TYPE["H3"], bold=True)
    f_sub = get_font(TYPE["H4"], bold=False)
    f_question = get_font(TYPE["L"], bold=True)

    a_h1 = tuple(int(c * title_a) for c in ACCENT)
    a_white = tuple(int(c * title_a) for c in WHITE)

    title_y = 200
    cursor_y = title_y
    title_rows = [
        (TITLE_BRAND, f_h1, a_h1, 16),
        (TITLE_REST1, f_h3, a_white, 14),
        (TITLE_REST2, f_h3, a_white, 14),
    ]
    for text, font, fill, gap in title_rows:
        if not text:
            continue
        width, _ = text_size(draw, text, font)
        draw.text((CENTER_X - width // 2, cursor_y), text, font=font, fill=fill)
        cursor_y += font.size + gap

    if SUBTITLE:
        sw, _ = text_size(draw, SUBTITLE, f_sub)
        a_sub = tuple(int(c * sub_a) for c in GRAY)
        cursor_y += 12
        draw.text((CENTER_X - sw // 2, cursor_y), SUBTITLE, font=f_sub, fill=a_sub)
        cursor_y += f_sub.size

    list_top = cursor_y + 54
    list_w = W - SAFE_LR * 2
    current_y = list_top

    for i, (raw, color) in enumerate(zip(ITEMS, COLORS)):
        card = normalize_item(raw)
        lines = question_lines(draw, card, f_question, list_w - 64)
        row_h = LIST_PAD_Y * 2 + len(lines) * LIST_LINE_H
        row_t = list_start + i * 0.18
        p = min(1.0, max(0.0, (t - row_t) / 0.28))
        if p <= 0:
            current_y += row_h + LIST_GAP
            continue
        alpha = p
        slide = int(20 * (1 - ease_out_cubic(p)))
        y_pos = current_y + slide
        row_box = [SAFE_LR, y_pos, SAFE_LR + list_w, y_pos + row_h]
        draw.rounded_rectangle(
            row_box,
            radius=20,
            fill=tuple(int(c * alpha) for c in CARD_DARK),
            outline=tuple(int(c * alpha) for c in color),
            width=3,
        )
        a_w = tuple(int(c * alpha) for c in WHITE)
        text_y = y_pos + LIST_PAD_Y
        for line in lines:
            draw.text((SAFE_LR + 32, text_y), line, font=f_question, fill=a_w)
            text_y += LIST_LINE_H
        current_y += row_h + LIST_GAP

    if current_y - LIST_GAP > H - SAFE_BOTTOM:
        raise ValueError("首屏列表超出安全区：请缩短标题/问题，或减少条目数。")

def fit_image_cover(path, target_w, target_h):
    """等比 cover:填满目标框,超出的部分裁掉"""
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    scale = max(target_w / sw, target_h / sh)
    new_w, new_h = int(sw * scale), int(sh * scale)
    src = src.resize((new_w, new_h), Image.LANCZOS)
    # 中心裁剪
    x0 = (new_w - target_w) // 2
    y0 = (new_h - target_h) // 2
    return src.crop((x0, y0, x0 + target_w, y0 + target_h))


def draw_card(card_idx, local_t):
    if local_t < 0:
        return None
    card = normalize_item(ITEMS[card_idx])
    color = COLORS[card_idx]

    if local_t < SLIDE_DUR:
        p = local_t / SLIDE_DUR
        alpha = p
        slide = int(SLIDE_DIST * (1 - ease_out_cubic(p)))
    else:
        alpha = 1.0
        slide = 0

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)

    f_question = get_font(TYPE["H4"], bold=True)
    f_label = get_font(TYPE["L"], bold=True)
    f_conclusion = get_font(TYPE["H4"], bold=True)
    f_body = get_font(TYPE["L"], bold=False)
    f_takeaway = get_font(TYPE["L"], bold=True)

    q_lines = question_lines(ld, card, f_question, CARD_W - 72)
    question_y = QUESTION_TOP + slide
    question_end = question_y + len(q_lines) * QUESTION_LINE_H
    card_top = question_end + QUESTION_CARD_GAP
    card_left = SAFE_LR
    card_right = SAFE_LR + CARD_W

    img_path = os.path.join(WORK_DIR, f"img_{card_idx}.jpg")
    has_image = USE_IMAGES and os.path.exists(img_path)

    tag_y = card_top + 38
    if has_image:
        img_y = card_top + 105
        content_y = img_y + CARD_IMG_H + 32
    else:
        content_y = card_top + 108

    conclusion_label_y = content_y
    conclusion_y = conclusion_label_y + 62
    conclusion_lines = []
    for source_line in card["conclusion"]:
        conclusion_lines.extend(wrap_exact(ld, source_line, f_conclusion, CARD_W - 104))
    bullets_top = conclusion_y + len(conclusion_lines) * QUESTION_LINE_H + 24

    bullet_layout = []
    bullet_y = bullets_top
    for source_lines in card["bullets"]:
        lines = []
        for source_line in source_lines:
            lines.extend(wrap_exact(ld, source_line, f_body, CARD_W - 166))
        bullet_layout.append((bullet_y, lines))
        bullet_y += len(lines) * 56 + 46

    takeaway_lines = []
    for source_line in card["takeaway"]:
        takeaway_lines.extend(wrap_exact(ld, source_line, f_takeaway, CARD_W - 136))

    if takeaway_lines:
        takeaway_top = bullet_y + 20
        takeaway_bottom = takeaway_top + 76 + len(takeaway_lines) * 52 + 30
        card_bottom = takeaway_bottom + 55
    else:
        takeaway_top = None
        takeaway_bottom = None
        card_bottom = bullet_y + 35

    if card_bottom > PROGRESS_Y - 50:
        raise ValueError(
            f"第 {card_idx + 1} 张卡片超出安全区：请缩短正文、减少行数或拆分场景。"
        )

    # 问题标题固定放在卡片外上方。
    ld.rounded_rectangle(
        [(SAFE_LR, question_y + 5), (SAFE_LR + 10, question_end - 12)],
        radius=5,
        fill=color + (int(255 * alpha),),
    )
    text_question_y = question_y
    for line in q_lines:
        ld.text(
            (SAFE_LR + 32, text_question_y),
            line,
            font=f_question,
            fill=WHITE + (int(255 * alpha),),
        )
        text_question_y += QUESTION_LINE_H

    ld.rounded_rectangle(
        [(card_left, card_top), (card_right, card_bottom)],
        radius=CARD_RADIUS,
        fill=CARD_DARK + (int(242 * alpha),),
        outline=color + (int(255 * alpha),),
        width=CARD_BORDER_W,
    )

    if has_image:
        img_x = card_left + CARD_IMG_MARGIN
        img_w = CARD_W - CARD_IMG_MARGIN * 2
        img = fit_image_cover(img_path, img_w, CARD_IMG_H)
        if alpha < 1.0:
            bg_layer = Image.new("RGB", img.size, CARD_DARK)
            img = Image.blend(bg_layer, img, alpha)
        i_mask = rounded_mask((img_w, CARD_IMG_H), CARD_IMG_RADIUS)
        layer.paste(img, (img_x, img_y), i_mask)

    ld.text(
        (card_left + 52, tag_y),
        f"问题 {card_idx + 1:02d} · {card['tag']}",
        font=f_label,
        fill=color + (int(255 * alpha),),
    )
    ld.text(
        (card_left + 52, conclusion_label_y),
        "核心结论",
        font=f_label,
        fill=color + (int(255 * alpha),),
    )
    draw_y = conclusion_y
    for line in conclusion_lines:
        ld.text(
            (card_left + 52, draw_y),
            line,
            font=f_conclusion,
            fill=WHITE + (int(255 * alpha),),
        )
        draw_y += QUESTION_LINE_H

    for current_bullet_y, lines in bullet_layout:
        ld.ellipse(
            [(card_left + 56, current_bullet_y + 12), (card_left + 80, current_bullet_y + 36)],
            fill=color + (int(255 * alpha),),
        )
        draw_y = current_bullet_y
        for line in lines:
            ld.text(
                (card_left + 106, draw_y),
                line,
                font=f_body,
                fill=GRAY + (int(255 * alpha),),
            )
            draw_y += 56

    if takeaway_top is not None:
        ld.rounded_rectangle(
            [(card_left + 36, takeaway_top), (card_right - 36, takeaway_bottom)],
            radius=24,
            fill=color + (int(35 * alpha),),
            outline=color + (int(230 * alpha),),
            width=3,
        )
        ld.text(
            (card_left + 68, takeaway_top + 20),
            "记住",
            font=f_label,
            fill=color + (int(255 * alpha),),
        )
        draw_y = takeaway_top + 76
        for line in takeaway_lines:
            ld.text(
                (card_left + 68, draw_y),
                line,
                font=f_takeaway,
                fill=WHITE + (int(255 * alpha),),
            )
            draw_y += 52

    return layer

def draw_progress(draw, current_idx):
    blocks = len(ITEMS)
    total_w = blocks * PROGRESS_BLOCK_W + (blocks - 1) * PROGRESS_BLOCK_GAP
    start_x = (W - total_w) // 2
    for i in range(blocks):
        x = start_x + i * (PROGRESS_BLOCK_W + PROGRESS_BLOCK_GAP)
        y = PROGRESS_Y
        color = COLORS[i] if i <= current_idx else DIM
        draw.rectangle(
            [(x, y), (x + PROGRESS_BLOCK_W, y + PROGRESS_BLOCK_H)],
            fill=color,
        )

def make_frame(t):
    canvas = Image.new("RGB", (W, H), BG)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    if t < HOOK_DUR:
        draw_hook_list_style(canvas, t)
    elif t < HOOK_DUR + len(ITEMS) * CARD_DUR:
        local_t = t - HOOK_DUR
        card_idx = int(local_t // CARD_DUR)
        card_local = local_t - card_idx * CARD_DUR
        card_layer = draw_card(card_idx, card_local)
        if card_layer:
            overlay = Image.alpha_composite(overlay, card_layer)
        d = ImageDraw.Draw(canvas)
        draw_progress(d, card_idx)
    # 去掉收尾段

    if overlay.mode == "RGBA":
        canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    return canvas

def render_frames():
    os.makedirs(WORK_DIR, exist_ok=True)
    total_frames = int(DURATION * FPS)
    print(f"生成 {total_frames} 帧 @ {FPS}fps ({DURATION}s) → {WORK_DIR}")
    for i in range(total_frames):
        t = i / FPS
        img = make_frame(t)
        img.save(os.path.join(WORK_DIR, f"frame_{i:04d}.png"), optimize=True)
        if i % 30 == 0:
            print(f"  t={t:.2f}s ({i}/{total_frames})")
    print("帧生成完毕")

def encode_video():
    video_path = os.path.join(WORK_DIR, "video.mp4")
    print(f"合成视频:{video_path}")
    frames_pattern = os.path.join(WORK_DIR, "frame_%04d.png")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-start_number", "0",
        "-i", frames_pattern,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "slow", "-crf", "22",
        "-vf", "fps=" + str(FPS),
        video_path,
    ], check=True, capture_output=True)
    return video_path

def mix_bgm(video_path):
    if not os.path.exists(BGM_PATH):
        print(f"⚠️ 未找到 BGM:{BGM_PATH},跳过混音")
        return None
    bgm_path = os.path.join(WORK_DIR, "bgm.m4a")
    subprocess.run([
        "ffmpeg", "-y", "-ss", "0", "-t", str(DURATION), "-i", BGM_PATH,
        "-af", f"afade=t=in:st=0:d=0.3,afade=t=out:st={DURATION - 0.5}:d=0.5,volume={BGM_VOLUME}",
        "-c:a", "aac", "-b:a", "128k", bgm_path,
    ], check=True, capture_output=True)
    final_path = os.path.join(WORK_DIR, "final.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path, "-i", bgm_path,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", final_path,
    ], check=True, capture_output=True)
    print(f"✅ 成品:{final_path}")
    return final_path

def cleanup_frames():
    for name in os.listdir(WORK_DIR):
        if name.startswith("frame_") and name.endswith(".png"):
            os.remove(os.path.join(WORK_DIR, name))

def main():
    os.makedirs(WORK_DIR, exist_ok=True)
    render_frames()
    video_path = encode_video()
    final = mix_bgm(video_path)
    cleanup_frames()
    if final:
        print(f"\n最终视频:{final}")

if __name__ == "__main__":
    main()
