import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {Audio} from "@remotion/media";

const SAFE_TOP = 100;
const SAFE_BOTTOM = 150;
const SAFE_LR = 20;
const W = 1080;
const H = 1920;
const CENTER_X = W / 2;
const CENTER_Y = H / 2;
const TYPE = {H1: 144, H2: 96, H3: 60, L: 44};

// EDIT BLOCK 1: output identity
export const GOLDEN_SHORT_LIST_SLUG = "golden-list";
export const GOLDEN_SHORT_LIST_OUTPUT =
  `out/golden-shorts/${GOLDEN_SHORT_LIST_SLUG}/video.mp4`;

// EDIT BLOCK 2: hook and payoff
const COPY = {
  eyebrow: "AI 工具清单",
  title: "4 个值得收藏的工具",
  accent: "少走弯路",
  outro: "先收藏，需要时直接照着选",
};

// EDIT BLOCK 3: use 3-5 compact cards. Keep every field to one short line.
const CARDS = [
  {number: "01", title: "HyperFrames", detail: "网页动效视频", color: "#34d399"},
  {number: "02", title: "FFmpeg", detail: "稳定处理音视频", color: "#60a5fa"},
  {number: "03", title: "Remotion", detail: "模板批量出片", color: "#a78bfa"},
  {number: "04", title: "Manim", detail: "数学科普动画", color: "#f59e0b"},
];

export const GOLDEN_SHORT_LIST_FRAMES = 270;

const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
};

const fitFontSize = (text, preferred, minimum, threshold) => {
  const overflow = Math.max(0, text.length - threshold);
  return Math.max(minimum, preferred - overflow * 3);
};

const Background = () => (
  <AbsoluteFill style={{backgroundColor: "#090d18", overflow: "hidden"}}>
    <div
      style={{
        position: "absolute",
        width: 760,
        height: 760,
        borderRadius: "50%",
        top: -260,
        right: -280,
        background: "radial-gradient(circle, rgba(52,211,153,0.2), rgba(9,13,24,0))",
      }}
    />
    <div
      style={{
        position: "absolute",
        width: 900,
        height: 900,
        borderRadius: "50%",
        bottom: -420,
        left: -420,
        background: "radial-gradient(circle, rgba(96,165,250,0.18), rgba(9,13,24,0))",
      }}
    />
  </AbsoluteFill>
);

const ListCard = ({card, index, frame, fps}) => {
  const enter = spring({
    frame: Math.max(0, frame - 42 - index * 10),
    fps,
    config: {damping: 18, stiffness: 110, mass: 0.7},
  });
  const y = interpolate(enter, [0, 1], [44, 0]);

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "112px 1fr",
        alignItems: "center",
        minHeight: 176,
        padding: "24px 34px",
        borderRadius: 28,
        backgroundColor: "rgba(255,255,255,0.045)",
        outline: `2px solid ${card.color}55`,
        boxShadow: `0 18px 60px ${card.color}15`,
        opacity: enter,
        transform: `translateY(${y}px) scale(${0.96 + enter * 0.04})`,
      }}
    >
      <div
        style={{
          width: 86,
          height: 86,
          borderRadius: 24,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: card.color,
          backgroundColor: `${card.color}18`,
          outline: `2px solid ${card.color}70`,
          fontSize: TYPE.L,
          fontWeight: 900,
          fontVariantNumeric: "tabular-nums",
        }}
      >
        {card.number}
      </div>
      <div style={{minWidth: 0}}>
        <div
          style={{
            color: "#f4f7fb",
            fontSize: fitFontSize(card.title, TYPE.H3, TYPE.L, 12),
            fontWeight: 850,
            lineHeight: 1.05,
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          {card.title}
        </div>
        <div
          style={{
            marginTop: 12,
            color: card.color,
            fontSize: TYPE.L,
            fontWeight: 650,
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          {card.detail}
        </div>
      </div>
    </div>
  );
};

export const GoldenShortList = () => {
  if (CARDS.length < 3 || CARDS.length > 5) {
    throw new Error("GoldenShortList requires 3-5 cards");
  }

  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const hookOut = interpolate(frame, [24, 42], [1, 0], {
    ...clamp,
    easing: Easing.in(Easing.cubic),
  });
  const contentIn = interpolate(frame, [30, 48], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  const outroIn = interpolate(frame, [228, 248], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });

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

      <AbsoluteFill
        style={{
          padding: "220px 78px",
          justifyContent: "center",
          opacity: hookOut,
          transform: `scale(${0.92 + hookOut * 0.08})`,
        }}
      >
        <div style={{color: "#7dd3fc", fontSize: TYPE.L, letterSpacing: 8}}>{COPY.eyebrow}</div>
        <div style={{marginTop: 42, color: "#f4f7fb", fontSize: TYPE.H1, fontWeight: 900, lineHeight: 1.05}}>
          {COPY.title}
        </div>
        <div style={{marginTop: 38, color: "#fbbf24", fontSize: TYPE.H3, fontWeight: 850}}>
          {COPY.accent}
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{padding: "110px 70px 150px", opacity: contentIn}}>
        <div style={{color: "#7dd3fc", fontSize: TYPE.L, letterSpacing: 7}}>{COPY.eyebrow}</div>
        <div style={{marginTop: 16, color: "#f4f7fb", fontSize: TYPE.H3, fontWeight: 900}}>
          {COPY.title}
        </div>
        <div style={{display: "flex", flexDirection: "column", gap: 24, marginTop: 62}}>
          {CARDS.map((card, index) => (
            <ListCard key={card.number} card={card} index={index} frame={frame} fps={fps} />
          ))}
        </div>
      </AbsoluteFill>

      <div
        style={{
          position: "absolute",
          left: 60,
          right: 60,
          bottom: 58,
          padding: "22px 30px",
          borderRadius: 999,
          backgroundColor: "rgba(9,13,24,0.88)",
          outline: "2px solid rgba(251,191,36,0.45)",
          color: "#fbbf24",
          fontSize: TYPE.L,
          fontWeight: 750,
          textAlign: "center",
          opacity: outroIn,
          transform: `translateY(${(1 - outroIn) * 24}px)`,
        }}
      >
        {COPY.outro}
      </div>
    </AbsoluteFill>
  );
};
