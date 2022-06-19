import json
import os
import random
import re
import subprocess
import time

import pyautogui

import constants
from behavior.behavior import human_move

"""
Important: 

1. Update the coordinates of the browser url address bar. Use the key 
  stroke combo `cmd + shift + 4` to detect coordinates on your screen. 
2. Do not change the zoom level for the page in the browser! This will mess 
  with coordinates! Default level must be 100% zoom level.
3. I assume that the binary name of Google Chrome is `google-chrome`. 
  Change the code if your binary name is different.
4. Make sure the browser window is started in your leftmost screen!
   I have a dual screen setup and sometimes I need to manually move 
   my browser window to the correct screen ;)
"""

# collect keys
keys = []


def get_coords(n):
    cmd = f'node cdp/coords.js "p:nth-of-type({n}) > a"'
    # print(cmd)
    coords = subprocess.check_output(cmd, shell=True).decode("utf8").strip()
    # print(coords)
    return json.loads(coords)


def get_key():
    cmd = "/usr/bin/node cdp/page_source"
    ps = subprocess.check_output(cmd, shell=True).decode("utf8").strip()
    if "Not found" in ps:
        return "done"
    key = re.search(r"[0-9a-z]{32}", ps)
    return key[0]


def visit_page():
    # @UPDATE COORDINATES HERE
    human_move(333, 88)  # click on the address bar to enter URL
    pyautogui.typewrite("google.com")  # There is no indication what url this is supposed to be.
    pyautogui.press("enter")
    # the following is not necessary, because JavaScript cannot record
    # keydown/keyup events in the address bar
    # humanTyping(target, speed=None, doubleHit=False)
    time.sleep(random.uniform(1.95, 2.95))


def main():
    """
    Get pixel coords with: cmd + shift + 4
    """
    os.system(
        f"{constants.CHROME_PATH} --remote-debugging-port=9222 --start-maximized --disable-notifications &"
    )
    time.sleep(4)

    try:
        while True:
            time.sleep(random.uniform(0.95, 1.25))
            visit_page()
            parsed = get_coords(random.randrange(1, 11))
            keys.append(get_key())

            for _ in range(11):
                x = parsed["x"] + random.randrange(0, int(parsed["width"]))
                y = parsed["y"] + random.randrange(0, int(parsed["height"]))
                # print(f'x={x}, y={y}')
                human_move(x, y)
                time.sleep(random.uniform(1.15, 1.74))
                key = get_key()
                if key == "done":
                    break
                else:
                    keys.append(key)
                parsed = get_coords(random.randrange(1, 11))
                print(f"Got {len(set(keys))} unique keys")
    except (Exception, KeyboardInterrupt) as e:
        print(f"Error: {e}")
        print(keys)


if __name__ == "__main__":
    main()
