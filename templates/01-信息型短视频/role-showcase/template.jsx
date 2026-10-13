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
export const GOLDEN_SHORT_ROLES_SLUG = "golden-roles";
export const GOLDEN_SHORT_ROLES_OUTPUT =
  `out/golden-shorts/${GOLDEN_SHORT_ROLES_SLUG}/video.mp4`;

// EDIT BLOCK 2: hook and payoff
const COPY = {
  eyebrow: "不同岗位怎么选",
  title: "2 类人，工具完全不同",
  outro: "选对工具，比装得多更重要",
};

// EDIT BLOCK 3: use exactly 2 roles and no more than 3 items per role.
const ROLES = [
  {
    label: "内容创作者",
    kicker: "写作 · 视频 · 发布",
    accent: "#60a5fa",
    items: ["公众号文章", "黄金短视频", "图像封面"],
  },
  {
    label: "产品运营",
    kicker: "分析 · 演示 · 转化",
    accent: "#f59e0b",
    items: ["功能演示", "数据复盘", "流程自动化"],
  },
];

export const GOLDEN_SHORT_ROLES_FRAMES = 270;

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
          "radial-gradient(circle at 15% 15%, rgba(96,165,250,0.2), transparent 38%), radial-gradient(circle at 85% 82%, rgba(245,158,11,0.18), transparent 40%)",
      }}
    />
  </AbsoluteFill>
);

const RolePage = ({role, localFrame, fps}) => {
  const enter = interpolate(localFrame, [0, 14], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  const exit = interpolate(localFrame, [88, 104], [1, 0], {
    ...clamp,
    easing: Easing.in(Easing.cubic),
  });
  const opacity = enter * exit;

  return (
    <AbsoluteFill style={{padding: "190px 76px 160px", opacity}}>
      <div style={{color: role.accent, fontSize: TYPE.L, letterSpacing: 7}}>{role.kicker}</div>
      <div style={{marginTop: 24, color: "#f4f7fb", fontSize: TYPE.H2, fontWeight: 900, lineHeight: 1.04}}>
        {role.label}
      </div>
      <div style={{width: 180, height: 5, marginTop: 34, borderRadius: 999, backgroundColor: role.accent}} />
      <div style={{display: "flex", flexDirection: "column", gap: 30, marginTop: 110}}>
        {role.items.map((item, index) => {
          const itemEnter = spring({
            frame: Math.max(0, localFrame - 12 - index * 9),
            fps,
            config: {damping: 18, stiffness: 115, mass: 0.65},
          });
          return (
            <div
              key={item}
              style={{
                display: "grid",
                gridTemplateColumns: "92px 1fr",
                alignItems: "center",
                minHeight: 190,
                padding: "28px 34px",
                borderRadius: 28,
                backgroundColor: "rgba(255,255,255,0.045)",
                outline: `2px solid ${role.accent}55`,
                opacity: itemEnter,
                transform: `translateX(${(1 - itemEnter) * 42}px)`,
              }}
            >
              <div style={{color: role.accent, fontSize: TYPE.H3, fontWeight: 900}}>0{index + 1}</div>
              <div style={{color: "#f4f7fb", fontSize: TYPE.H3, fontWeight: 780}}>{item}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

export const GoldenShortRoles = () => {
  if (ROLES.length !== 2 || ROLES.some((role) => role.items.length > 3)) {
    throw new Error("GoldenShortRoles requires exactly 2 roles with up to 3 items each");
  }

  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const hookOpacity = interpolate(frame, [0, 10, 28, 42], [0, 1, 1, 0], clamp);
  const outro = interpolate(frame, [246, 264], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  const firstStart = 36;
  const secondStart = 141;

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

      <AbsoluteFill style={{padding: "250px 70px", justifyContent: "center", opacity: hookOpacity}}>
        <div style={{color: "#7dd3fc", fontSize: TYPE.L, letterSpacing: 8}}>{COPY.eyebrow}</div>
        <div style={{marginTop: 42, color: "#f4f7fb", fontSize: TYPE.H2, fontWeight: 900, lineHeight: 1.06}}>
          {COPY.title}
        </div>
        <div style={{display: "flex", gap: 22, marginTop: 70}}>
          {ROLES.map((role) => (
            <div
              key={role.label}
              style={{
                flex: 1,
                padding: "22px 18px",
                borderRadius: 20,
                color: role.accent,
                backgroundColor: `${role.accent}12`,
                outline: `2px solid ${role.accent}60`,
                fontSize: TYPE.L,
                fontWeight: 750,
                textAlign: "center",
              }}
            >
              {role.label}
            </div>
          ))}
        </div>
      </AbsoluteFill>

      {frame >= firstStart && frame < secondStart && (
        <RolePage role={ROLES[0]} localFrame={frame - firstStart} fps={fps} />
      )}
      {frame >= secondStart && (
        <RolePage role={ROLES[1]} localFrame={frame - secondStart} fps={fps} />
      )}

      <div
        style={{
          position: "absolute",
          left: 62,
          right: 62,
          bottom: 60,
          padding: "24px 30px",
          borderRadius: 999,
          backgroundColor: "rgba(9,13,24,0.9)",
          outline: "2px solid rgba(251,191,36,0.48)",
          color: "#fbbf24",
          fontSize: TYPE.L,
          fontWeight: 760,
          textAlign: "center",
          opacity: outro,
          transform: `translateY(${(1 - outro) * 22}px)`,
        }}
      >
        {COPY.outro}
      </div>
    </AbsoluteFill>
  );
};
