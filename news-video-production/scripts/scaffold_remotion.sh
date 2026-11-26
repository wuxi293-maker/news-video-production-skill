#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-./remotion-news-video}"

if [ -e "$TARGET" ]; then
  echo "Target already exists: $TARGET"
  echo "Move it away or pass a different target path."
  exit 1
fi

mkdir -p "$TARGET"
cp -R "$SKILL_DIR/assets/remotion-starter/." "$TARGET/"
cd "$TARGET"

if [ "${SKIP_INSTALL:-0}" != "1" ]; then
  npm install
fi

if [ -f scripts/ensure-bgm.mjs ]; then
  node scripts/ensure-bgm.mjs
fi

if [ "${SKIP_BROWSER:-0}" != "1" ]; then
  npx remotion browser ensure
fi

echo "Starter created at: $TARGET"
echo "Next:"
echo "  cd \"$TARGET\""
echo "  npm run render"
