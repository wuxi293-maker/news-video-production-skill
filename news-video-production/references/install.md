# 跨环境安装与使用

## 目标

这个 Skill 不绑定某台机器、某个云主机或某个固定路径。换环境后，只要满足下面的依赖，就能直接制作。

**路径约定**：`SKILL_DIR` = 本 Skill 根目录，也就是包含 `SKILL.md` 的目录。所有命令都用 `$SKILL_DIR` 推导，不写死 `/home`、`/Users`、`/runtime` 或盘符。

## 依赖

| 依赖 | 用途 | 要求 |
|---|---|---|
| Python 3.9+ | 运行 `verify_video.py`、`check_env.py` | 系统自带即可 |
| Node.js 18+ | Remotion 渲染 | 必须 |
| npm / npx | 安装 Remotion 依赖 | 必须 |
| FFmpeg / ffprobe 4+ | 插帧、12Mbps 封装、技术检查 | 必须 |
| Chromium | Remotion 渲染 | 可自动下载；离线环境需预装 |
| 中文字体 | 标题/字幕渲染 | Noto Sans CJK / 思源黑体，缺字会变方框 |
| 磁盘 ≥2GB | 依赖 + 渲染缓存 | 建议 |

## 1. 安装到技能目录

把整个 `news-video-production` 文件夹放到目标环境的用户技能目录：

```text
<workspace>/.user_skills/news-video-production
```

不要只复制 `SKILL.md`；`agents/`、`references/`、`scripts/`、`assets/` 必须一起保留。

## 2. 检查环境

```bash
export SKILL_DIR="/path/to/news-video-production"
python3 "$SKILL_DIR/scripts/check_env.py"
```

Windows：

```powershell
$env:SKILL_DIR = "C:\path\to\news-video-production"
python "$env:SKILL_DIR\scripts\check_env.py"
```

输出 JSON；`ok: true` 才继续。缺 Node/FFmpeg 时先装系统依赖，不要让脚本去改系统。

## 3. 初始化 Remotion 项目

macOS / Linux / WSL / Git Bash：

```bash
bash "$SKILL_DIR/scripts/scaffold_remotion.sh" ./remotion-news-video
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File "$env:SKILL_DIR\scripts\scaffold_remotion.ps1" ".\remotion-news-video"
```

脚本会复制 `assets/remotion-starter/`，执行 `npm install`，再执行 `npx remotion browser ensure`。

- 离线环境：先设置 `SKIP_INSTALL=1` / `SKIP_BROWSER=1`，手动准备 `node_modules` 和 Chromium。
- 不想自动下载浏览器：`SKIP_BROWSER=1`，然后在目标机安装 Chromium，并按 Remotion 文档指定浏览器可执行路径；不要把路径写死。
- 没有 Node 18+：先安装 Node；这是硬依赖，不要退回旧 PIL 流程。
- 没有 FFmpeg：Remotion 先出 master，再把 12Mbps 封装放到有 FFmpeg 的机器/服务；不要把低码率文件当母版。
- 没有中文字体：安装 Noto Sans CJK / 思源黑体，或把有授权的字体放进 `public/fonts/` 并在 CSS 显式指定。

## 4. 替换示例数据

1. 把素材放进 `public/`，保持满幅、无角标、不重复。
2. 改 `src/data.example.json`：`title`、`shots[].src`、`heading`、`body`、`source`。
3. 镜头数 = 总时长 / 3 秒；每个镜头 90 帧，不要改 `durationInFrames`。
4. `public/bgm.wav` 由 `scripts/ensure-bgm.mjs` 自动生成，只是静音占位；换成抖音热门音乐，音量 0.20。

## 5. 渲染

```bash
cd ./remotion-news-video
npm run render
```

产物：`out/master.mp4`。再按 `references/remotion.md` 的 FFmpeg 命令封装 12Mbps 母版，并运行：

```bash
python3 "$SKILL_DIR/scripts/verify_video.py" out/final.mp4 --shots N
```

## 6. 没有飞书 / 没有 CDN 时

- 先本地归档：`日期_脚本名/versions/`，保留全部版本。
- 预览可用本地文件、网盘链接或任意可访问的 mp4 链接；不要依赖某个平台的固定接口。
- 交付前确认：1080×1920、30fps、12Mbps、N×3 秒、有音频。

## 7. 跨环境禁止

- 不把某台机器的绝对路径写进 `SKILL.md`、脚本或数据文件。
- 不假设一定有飞书、抖音、CDN、Chromium 或 FFmpeg；缺什么先检查、再降级。
- 不把预览低码率 mp4 当母版。
- 不删除本地旧版本。
