import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {Audio} from "@remotion/media";

// EDIT BLOCK 1: output identity
export const SCREENSHOT_LIST_SLUG = "screenshot-list";
export const SCREENSHOT_LIST_OUTPUT =
  `out/golden-shorts/${SCREENSHOT_LIST_SLUG}/video.mp4`;

// EDIT BLOCK 2: screenshot source and intrinsic dimensions
const SCREENSHOT = {
  src: "images/product-shot.png",
  width: 1440,
  height: 900,
};

// EDIT BLOCK 3: hook
const COPY = {
  eyebrow: "AI 工具实测",
  title: "这个功能值不值得用",
  outro: "看结果，再决定要不要装",
};

// EDIT BLOCK 4: use 3-4 concise highlights
const POINTS = [
  {number: "01", title: "结果更直观", detail: "先展示输出，再解释操作"},
  {number: "02", title: "步骤更精简", detail: "复杂流程压缩成关键动作"},
  {number: "03", title: "适合快速判断", detail: "八秒看懂核心价值"},
];

// Shared layout contract: references/layout-rules.md
const SAFE_TOP = 100;
const SAFE_BOTTOM = 150;
const SAFE_LR = 20;
const W = 1080;
const H = 1920;
const CENTER_X = W / 2;
const CENTER_Y = H / 2;
const TYPE = {H1: 144, H2: 96, H3: 60, L: 44};

export const SCREENSHOT_LIST_FRAMES = 270;

const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
};

const Background = () => (
  <AbsoluteFill style={{backgroundColor: "#090d18", overflow: "hidden"}}>
    <div
      style={{
        position: "absolute",
        inset: 0,
        background:
          "radial-gradient(circle at 50% 28%, rgba(96,165,250,0.18), transparent 34%), radial-gradient(circle at 50% 76%, rgba(245,158,11,0.12), transparent 42%)",
      }}
    />
  </AbsoluteFill>
);

const Highlight = ({point, index, frame, fps}) => {
  const enter = spring({
    frame: Math.max(0, frame - 54 - index * 28),
    fps,
    config: {damping: 18, stiffness: 110, mass: 0.7},
  });
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "88px 1fr",
        gap: 22,
        alignItems: "center",
        minHeight: 150,
        padding: "20px 28px",
        borderRadius: 24,
        backgroundColor: "rgba(255,255,255,0.045)",
        outline: "2px solid rgba(96,165,250,0.34)",
        opacity: enter,
        transform: `translateX(${(1 - enter) * 36}px)`,
      }}
    >
      <div
        style={{
          width: 74,
          height: 74,
          borderRadius: 18,
          display: "grid",
          placeItems: "center",
          color: "#7dd3fc",
          backgroundColor: "rgba(96,165,250,0.13)",
          fontSize: 44,
          fontWeight: 900,
        }}
      >
        {point.number}
      </div>
      <div>
        <div style={{color: "#f4f7fb", fontSize: TYPE.H3, fontWeight: 850, lineHeight: 1.08}}>
          {point.title}
        </div>
        <div style={{marginTop: 10, color: "#b6c2d8", fontSize: TYPE.L, lineHeight: 1.18}}>
          {point.detail}
        </div>
      </div>
    </div>
  );
};

export const ScreenshotList = () => {
  if (POINTS.length < 3 || POINTS.length > 4) {
    throw new Error("ScreenshotList requires 3-4 highlights");
  }

  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const headerIn = spring({frame, fps, config: {damping: 20, stiffness: 100}});
  const screenshotIn = spring({
    frame: Math.max(0, frame - 8),
    fps,
    config: {damping: 18, stiffness: 90},
  });
  const outro = interpolate(frame, [228, 252], [0, 1], clamp);
  const screenshotWidth = 860;
  const screenshotHeight = Math.round(
    screenshotWidth * SCREENSHOT.height / SCREENSHOT.width,
  );

  return (
    <AbsoluteFill style={{fontFamily: "Microsoft YaHei, sans-serif"}}>
      <Background />
      <Audio
        src={staticFile("audio/goodfeel.mp3")}
        loop
        volume={(audioFrame) =>
          interpolate(audioFrame, [0, 15, 235, 269], [0, 0.24, 0.24, 0], clamp)
        }
      />

      <div
        style={{
          position: "absolute",
          top: SAFE_TOP,
          left: SAFE_LR,
          right: SAFE_LR,
          textAlign: "center",
          opacity: headerIn,
        }}
      >
        <div style={{color: "#7dd3fc", fontSize: TYPE.L, letterSpacing: 8}}>
          {COPY.eyebrow}
        </div>
        <div
          style={{
            marginTop: 24,
            color: "#f4f7fb",
            fontSize: TYPE.H2,
            fontWeight: 900,
            lineHeight: 1.05,
          }}
        >
          {COPY.title}
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          top: 380,
          left: CENTER_X,
          width: screenshotWidth,
          height: screenshotHeight,
          overflow: "hidden",
          borderRadius: 24,
          outline: "3px solid rgba(96,165,250,0.5)",
          boxShadow: "0 24px 80px rgba(37,99,235,0.3)",
          opacity: screenshotIn,
          transform: `translateX(-50%) scale(${0.94 + screenshotIn * 0.06})`,
        }}
      >
        <Img
          src={staticFile(SCREENSHOT.src)}
          style={{width: "100%", height: "100%", objectFit: "cover"}}
        />
      </div>

      <div
        style={{
          position: "absolute",
          top: 990,
          left: 56,
          right: 56,
          display: "flex",
          flexDirection: "column",
          gap: 22,
        }}
      >
        {POINTS.map((point, index) => (
          <Highlight
            key={point.number}
            point={point}
            index={index}
            frame={frame}
            fps={fps}
          />
        ))}
      </div>

      <div
        style={{
          position: "absolute",
          left: 60,
          right: 60,
          bottom: SAFE_BOTTOM,
          color: "#fbbf24",
          fontSize: TYPE.L,
          fontWeight: 800,
          textAlign: "center",
          opacity: outro,
          transform: `translateY(${(1 - outro) * 20}px)`,
        }}
      >
        {COPY.outro}
      </div>
    </AbsoluteFill>
  );
};
