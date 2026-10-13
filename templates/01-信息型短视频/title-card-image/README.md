# Title Card + Image Template
# 5 行主标题 + 中部单图 9:16 黄金短视频模板

适用于"用 5 行精炼标题打中观众 + 中部一张主图"的 8 秒视频。
1080×1920 / 30fps / Mac 本地 Python + Pillow + FFmpeg 渲染。

## 模板特点

- **顶部**：深色标题卡片（圆角 + 左侧橙色装饰条 + 右上短横装饰）
- **标题**：5 行 H3=60，逐行 stagger 0.45s 淡入，全部内容 2.35s 入场完毕
- **中部**：单张主图，3.0s-4.5s 缩放+淡入一次，之后保持静态（4.5s-8s 给观众读图）
- **底部**：无公众号引导、无 CTA、无水印（让画面更聚焦）
- **时长**：8s @ 30fps = 240 帧
- **BGM**：自动从 `~/.workbuddy/skills/ip-ppt-video-pipeline/bgm/goodfeel.m4a` 截取 8 秒并 fade

## 使用步骤

### 1. 准备素材

把你的图片放到 `/tmp/title-card-image/`，命名为 `img1.jpg`。
推荐比例 3:2 ~ 5:3 横版图，以 contain 完整显示。

### 2. 改配置

编辑 `render.py` 顶部的 `EDIT BLOCK` 区域：

```python
# === 路径 ===
WORK_DIR = "/tmp/title-card-image"
BGM_PATH = "/Users/biggersun/.workbuddy/skills/ip-ppt-video-pipeline/bgm/goodfeel.m4a"

# === 5 行标题（H3=60，背景卡片）===
TITLE_LINES = [
    ("GPT额度不够用？",                  (255, 165, 0)),  # 橙黄高亮
    ("Codex 原生无缝接入国内大模型",      (255, 165, 0)),
    ("可随时切换模型",                    (255, 165, 0)),
    ("无需 Codex++",                     (255, 165, 0)),
    ("无需 CC switch",                   (255, 165, 0)),
]

# === 时序（一般不用改）===
TITLE_STAGGER = 0.45  # 标题每行错峰
TITLE_DUR     = 0.40  # 标题每行淡入时长
IMG_ENTER_T0  = 3.0   # 图片入场开始
IMG_ENTER_T1  = 4.5   # 图片入场结束
```

> **超宽标题自动换行**：单行宽度超过 `TITLE_MAX_W` 时，脚本会优先按 `/` 分段；否则中点切两行。
> 示例：`"GPT额度不够用？Codex 国内大模型"` → 自动切两行。

### 3. 渲染

```bash
cd /Users/biggersun/.workbuddy/skills/video-production-defaults/templates/01-信息型短视频/title-card-image
python3 render.py
```

输出：
- `/tmp/title-card-image/video.mp4`（无音视频）
- `/tmp/title-card-image/bgm.m4a`（截取的 8 秒 BGM）
- `/tmp/title-card-image/final.mp4`（最终成品）

封面单独生成（可选，封面通常建议用 imagegen skill 生成，不是这个脚本）：
```bash
python3 cover.py     # 生成 /tmp/title-card-image/cover.png
```

## 布局常量

| 区 | y 范围 | 说明 |
|---|---|---|
| 标题卡片 | 180 - (180+H_card) | 圆角 28，左侧橙色 6px 竖条 + 右上 108px 短横装饰 |
| 标题文字 | 卡片内，padding 32 | 5 行 H3=60，行间距 14，每行 stagger 0.45s |
| 中部主图 | 卡片下方 80px 起 | 1080×691（按 833:533 比例），圆角 24 |
| 底部安全 | 60px | 无水印 |

## 与 multi-image-rotation 的差异

| 维度 | multi-image-rotation | title-card-image |
|---|---|---|
| 标题 | 3 行无容器 | **5 行 + 深色卡片** |
| 主图 | 多图轮播 + 切换 | **单图静态** |
| 列表 | 5 条底部列表 | 无 |
| 信息密度 | 高 | **精炼** |

## 自定义

- **标题配色**：每行可单独指定颜色（RGB 元组），如需变化把每行 color 改不同值即可
- **图片比例**：模板默认按 833:533 显示，如需调整修改 `IMG_H = int(IMG_W / ...)`
- **卡片位置**：调整 `TITLE_CARD_Y` 改变整组位置上移/下移
- **更早静态收尾**：把 `IMG_ENTER_T1` 改小（如 3.5），最后几秒完全静止

## 依赖

- Python 3 + Pillow
- FFmpeg（系统命令）
- macOS 系统字体（STHeiti Medium / Light / Hiragino Sans GB）

## 颜色

- 背景：`#0A0E1A` (10, 14, 26)
- 卡片底：`#181C2C` (24, 28, 44, alpha 235/255)
- 主色橙黄：`#FFA500` (255, 165, 0)
- 白：`#F5F7FC` (245, 247, 252)
