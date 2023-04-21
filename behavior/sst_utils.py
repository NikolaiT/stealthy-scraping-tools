import time
import os
import sys
import random
import math
import json
import subprocess
import subprocess
from pathlib import Path


def goto(url):
    script_path = getScriptPath('goto.js')
    cmd = f"node {script_path} '{url}'"
    ps = subprocess.check_output(cmd, shell=True)
    return ps


def getScriptPath(name):
    return os.path.join(
        Path(__file__).parent.parent,
        'cdp/' + name
    )


def getPageSource():
    cmd = 'node ' + getScriptPath('page_source.js')
    ps = subprocess.check_output(cmd, shell=True)
    return ps


def evalJS(command):
    with open('/tmp/evalCommand.txt', 'w') as f:
        f.write(command)

    script_path = getScriptPath('eval_js.js')
    cmd = f"node {script_path}"
    ps = subprocess.check_output(cmd, shell=True)
    return ps


def getCoords(selector, randomize_within_bcr=True, highlight_bb=True):
    """
    - selector: The CSS selector to get the coords for
    - randomize_within_bcr: select a random coordinate within the bounding box
    hight
    - highlight_bb: visually highlight the bounding box for debugging purposes
    """
    script_path = getScriptPath('coords.js')
    cmd = f"node {script_path} '{selector}'"
    coords = subprocess.check_output(cmd, shell=True)
    coords = coords.decode()

    x, y = 0, 0

    try:
        parsed = json.loads(coords)
        x, y, width, height = parsed['x'], parsed['y'], parsed['width'], parsed['height']

        if randomize_within_bcr:
            # print(x, y, parsed['width'], parsed['height'])
            x += random.randint(0, math.floor(parsed['width'] / 4))
            y += random.randint(0, math.floor(parsed['height'] / 4))

        if highlight_bb:
            # Just add a red thick border around the CSS selector
            cmd = """var el = document.querySelector('""" + selector + \
                """'); if (el) { el.style.border = "2px solid #ff0000"; }"""
            evalJS(cmd)

    except Exception as e:
        print('getCoords() failed with Error: {}'.format(e))
        return None

    return x, y


def startBrowser(args=[], startInTempDir=True):
    """
    ping google.com 1>out.log 2>err.log &
    """
    tempDirStr = ' '
    if startInTempDir:
        tempDirStr = f' --user-data-dir=/tmp '

    arg_str = ' '.join(args)
    if sys.platform == 'darwin':
        chromePath = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'
        # On MacOS Monterey, we need to start Google Chrome
        # in fullscreen mode to get the correct coordinates.
        startCmd = f'{chromePath} --remote-debugging-port=9222 --start-maximized{tempDirStr}--disable-notifications --start-fullscreen {arg_str} 1>out.log 2>err.log &'
    else:
        startCmd = f'google-chrome --remote-debugging-port=9222 --start-maximized --disable-notifications {arg_str} 1>out.log 2>err.log &'

    if os.getenv('DOCKER') == '1':
        startCmd = 'google-chrome --remote-debugging-port=9222 --no-sandbox --disable-notifications --start-maximized --no-first-run --no-default-browser-check 1>out.log 2>err.log &'

    subprocess.Popen([startCmd], shell=True)
    time.sleep(random.uniform(3, 4))


def closeBrowser():
    print('closing browser')
    if sys.platform == 'darwin':
        os.system("killall -9 'Google Chrome'")
    else:
        os.system("killall -9 'google-chrome'")
