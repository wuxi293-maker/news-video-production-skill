# Remotion 合成指南

## 0. 快速起步

```bash
bash "$SKILL_DIR/scripts/scaffold_remotion.sh" ./remotion-news-video
cd ./remotion-news-video
npm run render
```

- 脚本会复制 `assets/remotion-starter/`，安装依赖，并尝试下载 Chromium。
- Windows 用 `scripts/scaffold_remotion.ps1`。
- 离线环境设置 `SKIP_INSTALL=1`、`SKIP_BROWSER=1`，手动准备 `node_modules` 和浏览器。

## 1. 工程初始化（手动）

目标环境需具备 Node 18+、Chromium、FFmpeg；先运行 `python3 "$SKILL_DIR/scripts/check_env.py"` 检查。每个新片建独立 Remotion 工程，不要把素材写死在代码里。

```bash
mkdir project && cd project
npm init -y
npm i remotion @remotion/cli react react-dom
npm i -D typescript @types/react @types/react-dom
```

目录约定：

```text
project/
├── public/            # 素材、字体、BGM、音效；用 staticFile() 引用
├── src/
│   ├── index.ts       # registerRoot
│   ├── Root.tsx       # Composition
│   ├── NewsVideo.tsx  # 主合成
│   └── types.ts
├── out/
└── remotion.config.ts
```

## 2. 帧数与镜头

```tsx
// Root.tsx
import { Composition } from "remotion";
import { NewsVideo } from "./NewsVideo";
import { shots } from "./data";

export const Root = () => (
  <Composition
    id="NewsVideo"
    component={NewsVideo}
    durationInFrames={shots.length * 90} // 每镜 3 秒 = 90 帧
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{ shots }}
  />
);
```

```tsx
// NewsVideo.tsx（示意；FixedTitle/FixedLowerTitle/InfoCard/Shot 需自行实现）
import { AbsoluteFill, Sequence, useCurrentFrame } from "remotion";

export const NewsVideo = ({ shots }) => {
  const frame = useCurrentFrame();
  const current = Math.min(Math.floor(frame / 90), shots.length - 1);

  return (
    <AbsoluteFill style={{ backgroundColor: "#05070c" }}>
      {shots.map((shot, i) => (
        <Sequence key={i} from={i * 90} durationInFrames={90}>
          <Shot shot={shot} index={i} total={shots.length} />
        </Sequence>
      ))}
      <FixedTitle />
      <FixedLowerTitle />
      <InfoCard shot={shots[current]} />
    </AbsoluteFill>
  );
};
```

- `durationInFrames` 必须是 `shots.length * 90`。
- 每镜 `Sequence` 的 `from` 必须是 `i*90`；不要用 100、120 等时长。
- 总时长改不了单镜；只能增删 `shots`。

## 3. 固定标题与卡片

标题、下方标题、资讯卡都放在所有 `Sequence` 之外，保证全片固定：

```tsx
<AbsoluteFill>
  <FixedTitle text={scriptTitle} />
  <FixedLowerTitle text={scriptTitle} />
  <InfoCard shot={shots[currentShotIndex]} />
</AbsoluteFill>
```

- 主标题与下方标题都左对齐、加粗、固定。
- 每镜只替换 `InfoCard` 的正文与重点词。
- 字幕圆角底板常驻；卡片无描边；时间轴放在卡片内。

## 4. 素材与转场

```tsx
<Img
  src={staticFile(shot.src)}
  style={{ width: "100%", height: "100%", objectFit: "cover" }}
/>
```

```tsx
<Video
  src={staticFile(shot.src)}
  startFrom={shot.startFrom ?? 0}
  muted
  style={{ width: "100%", height: "100%", objectFit: "cover" }}
/>
```

交叉淡入：在每镜开头 4–8 帧做透明度过渡，不改变 90 帧切点。

```tsx
import { interpolate } from "remotion";

const fade = interpolate(localFrame, [0, 6], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
<AbsoluteFill style={{ opacity: fade }}>...</AbsoluteFill>
```

轻微放大：`interpolate(localFrame, [0, 90], [1.0, 1.06])`。

## 5. 实拍视频运动插帧

进 Remotion 前，把 24/25fps 实拍统一转 30fps：

```bash
ffmpeg -y -i input.mp4 \
  -vf "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1" \
  -c:v libx264 -crf 16 -preset medium -an output_30fps.mp4
```

检查：快速运动处不出现鬼影/撕裂；有严重伪影时降低 `mi_mode` 或换素材。

## 6. 声音

BGM 与音效直接用 Remotion `Audio`，避免二次混音：

```tsx
<Audio src={staticFile("bgm.mp3")} volume={0.20} />
```

```tsx
<Sequence from={sectionStartFrame}>
  <Audio src={staticFile("sfx/whoosh.wav")} volume={0.35} />
</Sequence>
```

- BGM 音量 0.20；口播清晰优先。
- 音效只在段落起点、数据卡、结尾；约 10 处/100 秒。
- 不逐镜加音效。

## 7. 渲染与封装

先渲染高质量母版：

```bash
npx remotion render src/index.ts NewsVideo out/master.mp4 \
  --codec=h264 --crf=16 --pixel-format=yuv420p --concurrency=1
```

再用 FFmpeg 封装成 12Mbps：

```bash
ffmpeg -y -i out/master.mp4 \
  -c:v libx264 -preset medium \
  -b:v 12M -minrate 12M -maxrate 12M -bufsize 24M \
  -x264-params "nal-hrd=cbr:force-cfr=1" \
  -pix_fmt yuv420p -c:a aac -b:a 192k \
  -movflags +faststart out/final.mp4
```

- `--concurrency=1` 降低内存峰值，避免单帧泛白/崩溃。
- 如果 Chromium 报错，先运行 `npx remotion browser ensure`。
- 抽一帧封面：`npx remotion still src/index.ts NewsVideo out/cover.png --frame=0`。

## 8. 字体与授权

- 中文用 Noto Sans CJK / 思源黑体；把字体文件放 `public/fonts/` 并在 CSS 里显式 `fontFamily`，避免目标环境字体缺失。
- Remotion 商用授权按团队规模确认；团队超过 3 人通常需要商业许可。
- 不要把未授权字体、音乐、素材打进成片。
