import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  Video,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import type { NewsVideoProps, Shot } from "./types";

const SHOT_FRAMES = 90;

const MainTitle = ({ text }: { text: string }) => (
  <div
    style={{
      position: "absolute",
      top: 150,
      left: 80,
      width: 920,
      color: "#ffffff",
      fontFamily: "Noto Sans CJK SC, Source Han Sans SC, sans-serif",
      fontSize: 64,
      fontWeight: 800,
      lineHeight: 1.18,
      textAlign: "left",
      textShadow: "0 4px 24px rgba(0,0,0,.45)",
    }}
  >
    {text}
  </div>
);

const LowerTitle = ({ text }: { text: string }) => (
  <div
    style={{
      position: "absolute",
      left: 56,
      right: 56,
      bottom: 380,
      display: "flex",
      justifyContent: "flex-start",
    }}
  >
    <div
      style={{
        background: "rgba(0,0,0,.62)",
        borderRadius: 22,
        padding: "14px 24px",
        color: "#ffffff",
        fontFamily: "Noto Sans CJK SC, Source Han Sans SC, sans-serif",
        fontSize: 52,
        fontWeight: 700,
        lineHeight: 1.25,
        textAlign: "left",
      }}
    >
      {text}
    </div>
  </div>
);

const InfoCard = ({ shot }: { shot: Shot }) => (
  <div
    style={{
      position: "absolute",
      left: 56,
      right: 56,
      bottom: 40,
      background: "#ffffff",
      borderRadius: 26,
      padding: "24px 28px",
      boxShadow: "0 10px 30px rgba(0,0,0,.18)",
    }}
  >
    <div
      style={{
        color: "#0b1220",
        fontFamily: "Noto Sans CJK SC, Source Han Sans SC, sans-serif",
        fontSize: 48,
        fontWeight: 700,
        lineHeight: 1.25,
        textAlign: "left",
      }}
    >
      {shot.heading}
    </div>
    <div
      style={{
        marginTop: 10,
        color: "#334155",
        fontFamily: "Noto Sans CJK SC, Source Han Sans SC, sans-serif",
        fontSize: 36,
        lineHeight: 1.3,
        textAlign: "left",
      }}
    >
      {shot.body}
    </div>
    <div style={{ marginTop: 18, display: "flex", alignItems: "center", gap: 12 }}>
      <div style={{ height: 6, width: 120, background: "#e11d48", borderRadius: 999 }} />
      <div
        style={{
          color: "#64748b",
          fontFamily: "Noto Sans CJK SC, Source Han Sans SC, sans-serif",
          fontSize: 24,
        }}
      >
        {shot.source ?? "来源"}
      </div>
    </div>
  </div>
);

const ShotLayer = ({ shot }: { shot: Shot }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 6], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const scale = interpolate(frame, [0, SHOT_FRAMES], [1.0, 1.06]);

  return (
    <AbsoluteFill style={{ opacity }}>
      {shot.kind === "video" ? (
        <Video
          src={staticFile(shot.src)}
          startFrom={shot.startFrom ?? 0}
          muted
          style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${scale})` }}
        />
      ) : (
        <Img
          src={staticFile(shot.src)}
          style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${scale})` }}
        />
      )}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(0,0,0,.35), transparent 30%, transparent 55%, rgba(0,0,0,.55))",
        }}
      />
    </AbsoluteFill>
  );
};

export const NewsVideo = ({ title, shots }: NewsVideoProps) => {
  const frame = useCurrentFrame();
  const current = Math.min(Math.floor(frame / SHOT_FRAMES), shots.length - 1);

  return (
    <AbsoluteFill style={{ backgroundColor: "#05070c" }}>
      {shots.map((shot, index) => (
        <Sequence key={index} from={index * SHOT_FRAMES} durationInFrames={SHOT_FRAMES}>
          <ShotLayer shot={shot} />
        </Sequence>
      ))}
      <MainTitle text={title} />
      <LowerTitle text={title} />
      <InfoCard shot={shots[current]} />
      <Audio src={staticFile("bgm.wav")} volume={0.2} />
    </AbsoluteFill>
  );
};
