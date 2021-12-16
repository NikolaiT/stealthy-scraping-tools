#!/bin/bash
set -e

# When docker restarts, this file is still there,
# so we need to kill it just in case
[ -f /tmp/.X99-lock ] && rm -f /tmp/.X99-lock

_kill_procs() {
  kill -TERM $python
  kill -TERM $xvfb
  kill -TERM $chrome
}

# Relay quit commands to processes
trap _kill_procs SIGTERM SIGINT

# https://github.com/browserless/chrome/blob/307fa139b4c65f314a083891e1dbdb2dddeafcb7/start.sh

# Alternatively:
# xvfb-run -e /dev/stdout --server-num=99 --server-args="-ac -screen 0 $XVFB_WHD -nolisten tcp -nolisten unix" python3 -u immobilienscout24.py
echo "Starting X virtual framebuffer";
Xvfb $DISPLAY -ac -screen 0 $XVFB_WHD -nolisten tcp -nolisten unix &
xvfb=$!

sleep 3

echo "Starting browser";
x11vnc -display $DISPLAY.0 -forever -passwd ${X11VNC_PASSWORD:-password} &
vnc_server=$!

sleep 5

echo "Starting browser";
# Avoid chrome in docker crashing: https://github.com/stephen-fox/chrome-docker/issues/8
# Option 1: Run chrome with --disable-dev-shm-usage
# Option 2: Set /dev/shm size to a reasonable amount docker run -it --shm-size=1g replacing 1g with whatever amount you want.
google-chrome --remote-debugging-port=9222 --no-sandbox --disable-notifications --start-maximized --no-first-run --no-default-browser-check --incognito &
chrome=$!

sleep 5

# https://abhishekvaid13.medium.com/pyautogui-headless-docker-mode-without-display-in-python-480480599fc4
# echo "Running bot";
# python3 immobilienscout24.py
# python=$!

# wait $python
wait $xvfb
wait $chrome
wait $vnc_server
