#!/bin/bash
set -e

# When docker restarts, this file is still there,
# so we need to kill it just in case
[ -f /tmp/.X99-lock ] && rm -f /tmp/.X99-lock

_kill_procs() {
  kill -TERM $python
  kill -TERM $xvfb
}

# Relay quit commands to processes
trap _kill_procs SIGTERM SIGINT

echo "Starting X virtual framebuffer";
# https://github.com/browserless/chrome/blob/307fa139b4c65f314a083891e1dbdb2dddeafcb7/start.sh

# Alternatively:
# xvfb-run -e /dev/stdout --server-num=99 --server-args="-ac -screen 0 $XVFB_WHD -nolisten tcp -nolisten unix" python3 -u immobilienscout24.py

Xvfb $DISPLAY -ac -screen 0 $XVFB_WHD -nolisten tcp -nolisten unix &
xvfb=$!

sleep 1

# https://abhishekvaid13.medium.com/pyautogui-headless-docker-mode-without-display-in-python-480480599fc4
echo "Running bot";
python3 -u immobilienscout24.py
python=$!

wait $python
wait $xvfb
