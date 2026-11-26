#!/usr/bin/env python3
"""Verify a news video master: 1080x1920 / 30fps / 12Mbps / N*3s, with audio."""
import argparse
import json
import subprocess
import sys
from fractions import Fraction


def ffprobe(path):
    cmd = [
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", path,
    ]
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    return json.loads(out)


def rate(value):
    try:
        return float(Fraction(value))
    except Exception:
        return 0.0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--shots", type=int, default=0, help="number of 3-second shots")
    p.add_argument("--fps", type=float, default=30.0)
    p.add_argument("--width", type=int, default=1080)
    p.add_argument("--height", type=int, default=1920)
    p.add_argument("--min-bitrate", type=float, default=10.0)
    p.add_argument("--max-bitrate", type=float, default=14.0)
    p.add_argument("--allow-no-audio", action="store_true")
    p.add_argument("--no-duration-check", action="store_true", help="skip 3-second duration rules for voice-paced edits")
    args = p.parse_args()

    info = ffprobe(args.video)
    streams = info.get("streams", [])
    fmt = info.get("format", {})
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)

    errors = []
    checks = {}

    if not video:
        errors.append("no video stream")
    else:
        w, h = int(video.get("width", 0)), int(video.get("height", 0))
        fps = rate(video.get("avg_frame_rate") or video.get("r_frame_rate"))
        duration = float(fmt.get("duration") or video.get("duration") or 0)
        size = int(fmt.get("size") or 0)
        bitrate = float(fmt.get("bit_rate") or 0)
        if not bitrate and duration > 0:
            bitrate = size * 8 / duration
        frames = int(round(duration * fps)) if fps else 0

        checks.update({
            "width": w, "height": h, "fps": round(fps, 4),
            "duration": round(duration, 3), "frames": frames,
            "bitrate_mbps": round(bitrate / 1e6, 3) if bitrate else 0,
            "shots": args.shots or None,
        })

        if w != args.width or h != args.height:
            errors.append(f"resolution {w}x{h}, expected {args.width}x{args.height}")
        if abs(fps - args.fps) > 0.01:
            errors.append(f"fps {fps:.4f}, expected {args.fps}")

        if not args.no_duration_check:
            if args.shots:
                expected = args.shots * 3.0
                checks["expected_duration"] = expected
                checks["expected_frames"] = args.shots * 90
                if abs(duration - expected) > 0.15:
                    errors.append(f"duration {duration:.3f}s, expected {expected:.3f}s for {args.shots} shots")
                if frames and abs(frames - args.shots * 90) > 2:
                    errors.append(f"frames {frames}, expected {args.shots * 90}")
            else:
                if abs(duration - round(duration / 3) * 3) > 0.2:
                    errors.append(f"duration {duration:.3f}s is not a multiple of 3s")

        if args.min_bitrate and checks["bitrate_mbps"] < args.min_bitrate:
            errors.append(f"bitrate {checks['bitrate_mbps']} Mbps below {args.min_bitrate}")
        if args.max_bitrate and checks["bitrate_mbps"] > args.max_bitrate:
            errors.append(f"bitrate {checks['bitrate_mbps']} Mbps above {args.max_bitrate}")

    if audio:
        checks["audio"] = {
            "codec": audio.get("codec_name"),
            "sample_rate": audio.get("sample_rate"),
            "channels": audio.get("channels"),
        }
    elif not args.allow_no_audio:
        errors.append("no audio stream")

    result = {"ok": not errors, "video": args.video, "checks": checks, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
