#!/bin/bash
# usage: scripts/rerender.sh 01 03 ... — (re)start background renders for the given episodes
cd "$(dirname "$0")/.."
for e in "$@"; do
  pkill -f "script_ep$e.md" ; sleep 0.5
  python3 scripts/lint_script.py script_ep$e.md >/dev/null
  nohup python3 scripts/render.py script_ep$e.md ep$e.mp4 --work build_ep$e > build_ep$e.log 2>&1 &
done
