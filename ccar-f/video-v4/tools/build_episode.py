#!/usr/bin/env python3
"""One-shot entry: TTS → frames → assemble → mix BGM → chapters.txt.

Usage (from kit root):
  python3 tools/build_episode.py episodes/ep02
  python3 tools/build_episode.py episodes/ep01 --max-slides 2   # smoke test
  python3 tools/build_episode.py episodes/ep01 --slides-only
"""
from __future__ import annotations
from pathlib import Path
import argparse, re, sys, json

KIT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT_ROOT))
from tools.render import run as render_run  # noqa: E402
from tools.mix_bgm import mix  # noqa: E402
from tools.write_chapters import write_chapters  # noqa: E402


def ep_num(ep: Path) -> str:
    m = re.search(r"ep(\d+)$", ep.name)
    assert m, f"episode dir must be named epNN, got {ep}"
    return m.group(1)


def build(ep_dir: Path, *, slides_only=False, tts_only=False, max_slides=None,
          skip_bgm=False) -> Path | None:
    ep = ep_dir.resolve()
    assert (ep / "script.md").exists(), f"Need {ep}/script.md"
    n = ep_num(ep)
    voice_name = f"ccar-f-s{n}-voice.mp4"
    final_name = f"ccar-f-s{n}.mp4"

    tl, t = render_run(
        ep,
        slides_only=slides_only,
        tts_only=tts_only,
        max_slides=max_slides,
        out_voice=voice_name,
    )
    if slides_only or tts_only:
        return None

    if not skip_bgm:
        mix(ep, voice_mp4=voice_name, out_mp4=final_name)
    else:
        # copy voice-only as final for debugging
        import shutil
        shutil.copy2(ep / voice_name, ep / final_name)

    # chapters need full timeline; for max_slides subset still write what we have
    try:
        write_chapters(ep)
    except Exception as e:
        print("chapters warning:", e, file=sys.stderr)
        # fallback: duration only
        (ep / "chapters.txt").write_text(f"0:00 第1回\n", encoding="utf-8")

    out = ep / final_name
    meta = {
        "episode": ep.name,
        "duration_s": t + 4,  # + end card
        "out": str(out),
        "voicevox": __import__("tools.common", fromlist=["voicevox_url"]).voicevox_url(),
    }
    (ep / "build" / "build_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    print("DONE", out, f"~{meta['duration_s']:.1f}s")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build one CCAR-F series episode")
    ap.add_argument("episode_dir", type=Path, help="e.g. episodes/ep02")
    ap.add_argument("--slides-only", action="store_true")
    ap.add_argument("--tts-only", action="store_true")
    ap.add_argument("--max-slides", type=int, default=None)
    ap.add_argument("--skip-bgm", action="store_true")
    a = ap.parse_args()
    build(a.episode_dir, slides_only=a.slides_only, tts_only=a.tts_only,
          max_slides=a.max_slides, skip_bgm=a.skip_bgm)
