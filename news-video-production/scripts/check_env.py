#!/usr/bin/env python3
"""Check the host environment before using the news-video-production skill."""
import json
import shutil
import subprocess
import sys


def run(cmd):
    try:
        out = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15, check=False
        )
        text = (out.stdout or out.stderr or "").strip().splitlines()
        return text[0] if text else ""
    except Exception:
        return ""


def first_on_path(candidates):
    for name in candidates:
        path = shutil.which(name)
        if path:
            return name, path
    return None, None


def main():
    checks = {}
    errors = []
    warnings = []

    checks["python"] = {
        "version": ".".join(str(x) for x in sys.version_info[:3]),
        "executable": sys.executable,
    }
    if sys.version_info < (3, 9):
        warnings.append("Python 3.9+ recommended; verify_video.py may still work.")

    core = {
        "ffmpeg": ["ffmpeg"],
        "ffprobe": ["ffprobe"],
        "node": ["node"],
        "npm": ["npm"],
        "npx": ["npx"],
    }
    for key, candidates in core.items():
        name, path = first_on_path(candidates)
        checks[key] = {"found": bool(path), "path": path}
        if not path:
            errors.append(f"{key} not found on PATH")
        else:
            checks[key]["version"] = run([path, "-version"] if key.startswith("ff") else [path, "-v"])

    _, node_path = first_on_path(["node"])
    node_version = checks.get("node", {}).get("version", "")
    if node_path and node_version:
        try:
            major = int(node_version.lstrip("v").split(".")[0])
            if major < 18:
                errors.append(f"Node {node_version} is too old; Node 18+ required for Remotion")
        except ValueError:
            warnings.append(f"Could not parse Node version: {node_version}")

    chromium_name, chromium_path = first_on_path(
        ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable"]
    )
    checks["chromium"] = {"found": bool(chromium_path), "name": chromium_name, "path": chromium_path}
    if not chromium_path:
        warnings.append("Chromium not found; run `npx remotion browser ensure` inside the project.")

    if shutil.which("zip"):
        checks["zip"] = {"found": True, "path": shutil.which("zip")}
    else:
        checks["zip"] = {"found": False, "path": None}

    fc_list = shutil.which("fc-list")
    checks["cjk_font"] = {"fc_list": bool(fc_list), "found": False}
    if fc_list:
        try:
            out = subprocess.run(
                [fc_list, ":lang=zh", "family"],
                capture_output=True, text=True, timeout=15, check=False,
            )
            families = [line.strip() for line in out.stdout.splitlines() if line.strip()]
            checks["cjk_font"]["found"] = bool(families)
            checks["cjk_font"]["sample"] = families[:5]
            if not families:
                warnings.append("No CJK font found; install Noto Sans CJK / 思源黑体.")
        except Exception:
            warnings.append("Could not query CJK fonts; ensure a CJK font is available.")
    else:
        warnings.append("fc-list not found; ensure a CJK font is available for Chinese titles.")

    try:
        free = shutil.disk_usage(".").free / (1024**3)
        checks["disk_free_gb"] = round(free, 2)
        if free < 2:
            warnings.append("Less than 2GB free; Remotion install/render may fail.")
    except Exception:
        checks["disk_free_gb"] = None

    ok = not errors
    result = {
        "ok": ok,
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "next": [
            "python3 scripts/check_env.py",
            "bash scripts/scaffold_remotion.sh ./remotion-news-video",
            "cd ./remotion-news-video && npm run render",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
