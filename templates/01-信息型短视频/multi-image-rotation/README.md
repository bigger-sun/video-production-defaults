# Multi-Image Rotation Template
# 多图轮播 + 列表 9:16 黄金短视频模板

适用于"多个产品截图/界面截图轮播展示 + 文案列表"的 8 秒视频。
1080×1920 / 30fps / Mac 本地 Python + FFmpeg 渲染。

## 模板特点

- **顶部**：3 行 H3=60 主标题，依次淡入
- **中部**：1-4 张图同位置轮播（自动接力切换）
- **下部**：5 条彩边列表（左侧编号色块 + 文字靠左）
- **时间**：默认 8s
- **BGM**：自动从 `~/.workbuddy/skills/ip-ppt-video-pipeline/bgm/goodfeel.m4a` 截取 8 秒

## 使用步骤

### 1. 准备素材

把你的图片放到 `/tmp/zcode-short/`（或任意目录），命名 `img1.jpg`、`img2.jpg`...
最多支持 4 张。推荐比例 16:9 或超宽横屏（2:1~3:1）以 contain 显示。

### 2. 改配置

编辑 `render.py` 顶部的 `EDIT BLOCK` 区域：

```python
# === 标题（H3=60，3 行）===
TITLE_LINES = [
    ("GPT 额度不够用？", (255, 165, 0)),       # 橙黄
    ("Codex 无缝接入", (245, 247, 252)),         # 白
    ("国内大模型 / 随时切换", (245, 247, 252)),
]

# === 5 条列表（编号色 + 标题 + 副标）===
LIST_ITEMS = [
    ("01", "突破额度", "流量分流给国内模型，token不再省着用"),
    ...
]

# === 图片轮播时间线 ===
TRANSITIONS = [
    (1.5, 2.0, 1, 2),   # 1.5s-2.0s 切图1→图2
    (3.5, 4.0, 2, 3),   # 3.5s-4.0s 切图2→图3
    (5.5, 6.0, 3, 4),   # 5.5s-6.0s 切图3→图4
]
# 自动按 TRANSITIONS 和图数量分配显示时间
```

### 3. 渲染

```bash
cd /Users/biggersun/.workbuddy/skills/video-production-defaults/templates/01-信息型短视频/multi-image-rotation
python3 render.py    # 生成帧 + 合成视频
```

输出：`/tmp/zcode-short/zcode_final.mp4`

封面单独生成：
```bash
python3 cover.py     # 生成 /tmp/zcode-short/cover.jpg
```

## 布局常量

| 区 | y 范围 | 说明 |
|---|---|---|
| 标题 | 130-334 | H3=60 × 3 行 |
| 图 | 334-759 | 1000×425（按图1 比例） |
| 列表 | 795-1407 | 5 条 × 100 + 4×28 |

## 自定义

- **更多图**：把 TRANSITIONS 改成 `(2.0, 2.5, 1, 2), (4.0, 4.5, 2, 3), (5.5, 6.0, 3, 4), (6.5, 7.0, 4, 5)`，并在 get_current_image 增加分支
- **更少图**：删 TRANSITIONS 行，get_current_image 改回退分支
- **加列表入场动画**：把 LIST_APPEAR_T 改成 2.0，每条 stagger 0.2s

## 依赖

- Python 3 + Pillow
- FFmpeg（系统命令）
- macOS 系统字体（思源黑体 / PingFang）

## 颜色

- 背景：`#0A0E1A` (10, 14, 26)
- 主色橙黄：`#FFA500` (255, 165, 0)
- 辅色青蓝：`#4A9EFF` (74, 158, 255)
- 白：`#F5F7FC` (245, 247, 252)
- 列表编号配色（循环）：橙/绿/紫/蓝/绿
