import json
import math
import os
import random
import subprocess
import time
from pathlib import Path

import constants


def goto(url):
    script_path = get_script_path("goto.js")
    cmd = f"node {script_path} '{url}'"
    return subprocess.check_output(cmd, shell=True)


def get_script_path(name):
    return os.path.join(Path(__file__).parent.parent, f"cdp/{name}")


def get_page_source():
    cmd = "node " + get_script_path("page_source.js")
    return subprocess.check_output(cmd, shell=True)


def eval_js(command):
    with open("/tmp/evalCommand.txt", "w") as f:
        f.write(command)

    script_path = get_script_path("eval_js.js")
    cmd = f"node {script_path}"
    return subprocess.check_output(cmd, shell=True)


def get_coords(selector, randomize_within_bcr=True):
    """
    Example: `node coords.js "li:nth-of-type(3) a"`
    """
    script_path = get_script_path("coords.js")
    cmd = f"node {script_path} '{selector}'"
    coords = subprocess.check_output(cmd, shell=True)
    coords = coords.decode()

    x, y = 0, 0

    try:
        parsed = json.loads(coords)
        x = parsed["x"]
        y = parsed["y"]

        # this is fucking inaccurate. WHY???
        # is el.getBoundingClientRect() fucky?
        if randomize_within_bcr:
            # print(x, y, parsed['width'], parsed['height'])
            x += random.randint(0, math.floor(parsed["width"] / 4))
            y += random.randint(0, math.floor(parsed["height"] / 4))
    except Exception as e:
        print(f"getCoords() failed with Error: {e}")
        return None

    return x, y


def start_browser(args=None):
    if os.getenv("DOCKER") != "1":
        start_cmd = f"{constants.CHROME_PATH} --remote-debugging-port=9222 --start-maximized --disable-notifications"
    if args is None:
        args = []
    if not isinstance(args, list):
        args = [args]
    if isinstance(args, list):
        args = ' '.join(args)

    if os.getenv("DOCKER") == "1":
        start_cmd = "google-chrome --remote-debugging-port=9222 --no-sandbox --disable-notifications --start-maximized --no-first-run --no-default-browser-check & --disable-dev-shm-usage"
        # startCmd = 'google-chrome --remote-debugging-port=9222 --no-sandbox --disable-notifications --start-maximized --no-first-run --no-default-browser-check --incognito &'
    start_cmd += f" {args}"
    os.system(start_cmd)
    time.sleep(random.uniform(4, 5))
