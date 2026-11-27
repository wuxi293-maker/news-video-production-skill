# 资讯视频制作 Skill

从飞书脚本到 Remotion 成片的竖屏资讯短视频工作流，可跨环境安装。

- 版本：v2.0（2026-11-27）
- 技能名：`news-video-production`
- 中文名：资讯视频制作
- 调用：`$news-video-production`
- 核心规则：资讯模板**固定 3 秒/镜**（总时长=镜头数×3 秒）；1080×1920 / 30fps / 12Mbps；T01–T04 包装；Remotion 合成；抖音热门 BGM 增益约 0.20；成片后强制素材、字幕、封面、抖音安全区自检；用户确认后只保留最终版，删除过程版本；参考过往视频只用最后版本。

## 直接给 AI 助手

- 仓库主页：https://github.com/wuxi293-maker/news-video-production-skill
- 一键下载 zip：https://github.com/wuxi293-maker/news-video-production-skill/archive/refs/heads/main.zip
- 原始 `SKILL.md`：https://raw.githubusercontent.com/wuxi293-maker/news-video-production-skill/main/news-video-production/SKILL.md
- 安装提示词索引：https://github.com/wuxi293-maker/news-video-production-skill/blob/main/%E5%AE%89%E8%A3%85%E6%8F%90%E7%A4%BA%E8%AF%8D.md
- 更新记录：[CHANGELOG.md](./CHANGELOG.md)（当前 [VERSION](./VERSION) = 2.0.0）
- v2.0 完整包（含 theme-kit 字体/样片）：https://aka.doubaocdn.com/s/9Y8e9mPxBs

## 两种安装提示词

- [只安装新版（不删除旧版）](./安装提示词_仅安装新版.md)
- [删除旧版并全新安装](./安装提示词_删除旧版重装.md)

不要混用两种模式：A 会保留旧版并改名备份；B 会先删除旧版目标目录，再全新安装。

## 快速安装

```bash
git clone --depth 1 https://github.com/wuxi293-maker/news-video-production-skill.git
cd news-video-production-skill
```

把 `news-video-production` 整个文件夹放到目标环境的用户技能目录：

```text
<workspace>/.user_skills/news-video-production
```

不要只复制 `SKILL.md`；`agents/`、`references/`、`scripts/`、`assets/` 要一起保留。`assets/theme-kit` 的字体/样片体积较大，若 GitHub 轻量包中缺失，用上面的完整包补入。

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

starter 会自动生成静音 `public/bgm.wav` 占位；正式制作时替换为抖音热门音乐，音量约 0.20。

## 目录

```text
news-video-production/
├── SKILL.md
├── agents/
├── references/
├── scripts/
└── assets/
    ├── remotion-starter/
    └── theme-kit/          # T01–T04 主题与封面工程（字体/样片见完整包）
```

## v2.0 主要更新

- 资讯时长从“按分镜/脚本”恢复为**固定 3 秒/镜**：`durationInFrames = shots.length * 90`。
- 新增抖音安全区、封面、成片五项自检；`safe_area_check.py` 支持 tp01/t04/tp02/cover 预设。
- Starter 与 ThemeKit 统一固定 3 秒；T04 卡片改 `top 1088`、底边 `1620`。
- 新增 `theme-system.md` 与 `theme-kit` 主题工程。
- 交付规则改为：确认后只留最终版，删除过程版本；参考历史视频只用最后版本。

## 许可

本仓库是个人工作流模板；使用第三方字体、音乐、素材时请自行确认授权。
