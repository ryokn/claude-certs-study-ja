#!/bin/bash
# Start VOICEVOX engine (CPU, v0.26.0) on 127.0.0.1:50021
cd /workspace/voicevox/linux-cpu-x64 && nohup ./run --host 127.0.0.1 --port 50021 > /workspace/voicevox/engine.log 2>&1 &
for i in $(seq 1 60); do curl -sf localhost:50021/version && exit 0; sleep 1; done; echo "engine failed to start"; exit 1
