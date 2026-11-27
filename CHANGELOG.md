# 更新记录

## v2.0 — 2026-11-27

- 资讯模板恢复固定 3 秒/镜：`durationInFrames = shots.length * 90`，总时长=镜头数×3 秒。
- Starter 与 ThemeKit 同步固定 90 帧/镜；移除按脚本改单镜时长的字段。
- 新增 `references/self-check.md`：素材对应、素材异常、字幕闪动、封面、抖音安全区五项自检。
- 新增 `references/theme-system.md` 与 `assets/theme-kit/` 主题工程。
- 新增 `scripts/qc_video.py`、`scripts/safe_area_check.py`；`verify_video.py` 支持 `--shots N` 固定 3 秒校验。
- TP01 标题 `top≥240`、底部卡/字幕底边 `y≤1620`；T04 卡片 `top1088`、底边 `1620`。
- 封面 3:4：TP01 标题 `top≥240`，T04/TP02 `top≥120`；TP01 必须隐藏信息卡后单独渲染。
- 交付规则改为：用户确认后只保留最终版，删除过程版本；参考过往视频只使用最后版本。
- 本仓库轻量包更新文本/脚本；完整字体、样片、BGM 素材见 CDN 完整包。

## v1.1 — 2026-11-26

- 首次发布资讯视频 Skill：固定 3 秒/镜、T01–T03、Remotion starter、环境检查与校验脚本。
