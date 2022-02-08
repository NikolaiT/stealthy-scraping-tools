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
# echo "Starting X virtual framebuffer";
# python3 -u behavior/start_disp.py &
# Xvfb $DISPLAY -ac -screen 0 $XVFB_WHD -nolisten tcp -nolisten unix &
# xvfb=$!

# sleep 3

# GENERATE .Xauthority file
# xauth with complain unless ~/.Xauthority exists
# touch $HOME/.Xauthority
# # only this one key is needed for X11 over SSH 
# xauth generate $DISPLAY . trusted
# # generate our own key, xauth requires 128 bit hex encoding
# xauth add $DISPLAY . $(xxd -l 16 -p /dev/urandom)
# # To view a listing of the .Xauthority file, enter the following 
# xauth list


echo "Blocking all UDP traffic except DNS";
id

# https://serverfault.com/questions/222606/how-can-i-reject-all-incoming-udp-packets-except-for-dns-lookups/716035
# how can I reject all traffic I didn't initiate with Linux netfilter?
sudo iptables --version
sudo iptables -A DOCKER-USER -m state --state ESTABLISHED,RELATED -j ACCEPT

sudo iptables -A DOCKER-USER -p udp --dport 53 -j ACCEPT -m comment --comment "we serve DNS"
sudo iptables -A DOCKER-USER -p tcp --dport 53 -j ACCEPT -m comment --comment "DNS uses TCP too sometimes"

sudo iptables -A DOCKER-USER -j DROP


echo "Starting browser";
# Avoid chrome in docker crashing: https://github.com/stephen-fox/chrome-docker/issues/8
# Option 1: Run chrome with --disable-dev-shm-usage
# Option 2: Set /dev/shm size to a reasonable amount docker run -it --shm-size=1g replacing 1g with whatever amount you want.
# google-chrome --remote-debugging-port=9222 --no-sandbox --disable-notifications --start-maximized --no-first-run --no-default-browser-check --incognito &
# chrome=$!

sleep 5

# https://abhishekvaid13.medium.com/pyautogui-headless-docker-mode-without-display-in-python-480480599fc4
echo "Running bot";
python3 -u immobilienscout24.py &
python=$!

# echo "Starting x11vnc";
# x11vnc -display $DISPLAY.0 -forever -passwd ${X11VNC_PASSWORD:-password} &
# vnc_server=$!

wait $python
echo "bot terminated";
wait $xvfb
wait $chrome
wait $vnc_server
