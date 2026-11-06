#!/usr/bin/env python3
"""Mix BGM under voice at -18 LU, 2s fade-in, 3s fade-out. Writes final mp4.
BGM licence (OpenTracks / KK「昼下がり気分」): free YouTube background use;
NO standalone redistribution, NO AI training, NO Content ID. Keep out of git remotes.
"""
from __future__ import annotations
from pathlib import Path
import argparse, json, re, subprocess, sys

KIT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT_ROOT))
from tools.common import BGM_FILE  # noqa: E402


def loudness(path: Path) -> float:
    x = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    )
    matches = re.findall(r"I:\s*(-?[\d.]+) LUFS", x.stderr)
    return float(matches[-1])


def mix(ep_dir: Path, bgm: Path | None = None, voice_mp4: str = "voice-only.mp4",
        out_mp4: str | None = None) -> dict:
    ep = ep_dir.resolve()
    bgm = (bgm or BGM_FILE).resolve()
    assert bgm.exists(), f"BGM missing: {bgm}"
    voice_wav = ep / "build" / "voice.wav"
    video = ep / voice_mp4
    assert voice_wav.exists(), voice_wav
    assert video.exists(), video
    if out_mp4 is None:
        # episodes/epNN -> ccar-f-sNN.mp4
        m = re.search(r"ep(\d+)$", ep.name)
        out_mp4 = f"ccar-f-s{m.group(1)}.mp4" if m else "out.mp4"
    out = ep / out_mp4
    dur = float(json.loads(
        subprocess.check_output(["ffprobe", "-v", "error", "-show_format", "-of", "json", str(video)])
    )["format"]["duration"])
    v = loudness(voice_wav)
    b = loudness(bgm)
    gain = v - 18 - b
    stem = ep / "build" / "bgm_quiet.wav"
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
        "-stream_loop", "-1", "-i", str(bgm), "-t", str(dur),
        "-af", f"volume={gain}dB,afade=t=in:st=0:d=2,afade=t=out:st={dur-3}:d=3",
        "-ar", "48000", str(stem),
    ], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
        "-i", str(video), "-i", str(voice_wav), "-i", str(stem),
        "-filter_complex",
        "[1:a][2:a]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95:level=0[m]",
        "-map", "0:v:0", "-map", "[m]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-t", str(dur), "-movflags", "+faststart", str(out),
    ], check=True)
    result = {
        "voice_LUFS": v, "original_bgm_LUFS": b, "bgm_gain_dB": gain,
        "quiet_bgm_LUFS": loudness(stem), "duration_s": dur, "out": str(out),
    }
    (ep / "build" / "bgm_measurement.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(result)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode_dir")
    ap.add_argument("--bgm", default=None)
    ap.add_argument("--voice-mp4", default="voice-only.mp4")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    mix(Path(a.episode_dir), Path(a.bgm) if a.bgm else None, a.voice_mp4, a.out)
