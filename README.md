# 资讯视频制作 Skill

从飞书脚本到 Remotion 成片的竖屏资讯短视频工作流，可跨环境安装。

- 技能名：`news-video-production`
- 中文名：资讯视频制作
- 调用：`$news-video-production`
- 核心规则：每镜固定 3 秒；1080×1920 / 30fps / 12Mbps；T01/T02/T03 包装；Remotion 合成；抖音热门 BGM；本地保留 v1/v2 全部版本。

## 快速安装

```bash
git clone https://github.com/wuxi293-maker/news-video-production-skill.git
cd news-video-production-skill
```

把 `news-video-production` 整个文件夹放到目标环境的用户技能目录：

```text
<workspace>/.user_skills/news-video-production
```

不要只复制 `SKILL.md`；`agents/`、`references/`、`scripts/`、`assets/` 要一起保留。

## 环境检查

```bash
export SKILL_DIR="$PWD/news-video-production"
python3 "$SKILL_DIR/scripts/check_env.py"
```

需要 Node 18+、FFmpeg、ffprobe、npm/npx；Chromium 可由 `npx remotion browser ensure` 自动准备。

## 初始化并渲染 starter

```bash
bash "$SKILL_DIR/scripts/scaffold_remotion.sh" ./remotion-news-video
cd ./remotion-news-video
npm run render
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File "$env:SKILL_DIR\scripts\scaffold_remotion.ps1" ".\remotion-news-video"
```

starter 会自动生成静音 `public/bgm.wav` 占位；正式制作时替换为抖音热门音乐，音量 0.20。

## 目录

```text
news-video-production/
├── SKILL.md
├── agents/
├── references/
├── scripts/
└── assets/remotion-starter/
```

## AI 助手安装提示词

见 [`安装提示词.md`](./安装提示词.md)。核心是：解压/克隆后把整个 `news-video-production` 放到 `.user_skills`，运行 `check_env.py`，再用 `scaffold_remotion.sh` 初始化并验证 starter。

## 许可

本仓库是个人工作流模板；使用第三方字体、音乐、素材时请自行确认授权。
