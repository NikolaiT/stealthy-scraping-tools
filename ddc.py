import time
import os
import random
import subprocess
import json
import re
from mouse import humanMove
from typing import humanTyping
from target import target
import pyautogui

"""
Important: 

1. Update the coordinates of the browser url address bar. Use the command `xdotool getmouselocation` to detect coordinates on your screen. 
2. Do not change the zoom level for the page in the browser! This will mess with coordinates! Default level must be 100% zoom level.
3. I assume that the binary name of Google Chrome is `google-chrome`. Change the code if your binary name is different.
4. Make sure the browser window is started in your leftmost screen!
   I have a dual screen setup and sometimes I need to manually move my browser window to the correct screen ;)
"""

# collect keys
keys = []

def getCoords(n):
  cmd = f'node coords.js "p:nth-of-type({n}) > a"'
  # print(cmd)
  coords = subprocess.check_output(cmd, shell=True).decode('utf8').strip()
  # print(coords)
  return json.loads(coords)


def getKey():
  cmd = f'/usr/bin/node page_source'
  ps =  subprocess.check_output(cmd, shell=True).decode('utf8').strip()
  key = re.search(r'[0-9a-z]{32}', ps)
  return key.group(0)


def visitPage():
  # @UPDATE COORDINATES HERE
  humanMove(168, 79) # click on the address bar to enter URL
  pyautogui.typewrite(target)
  # the following is not necessary, because JavaScript cannot record 
  # keydown/keyup events in the address bar
  # humanTyping(target, speed=None, doubleHit=False)
  time.sleep(random.uniform(1.95, 2.95))


def main():
  """
  Get pixel coords with: `xdotool getmouselocation`
  """
  os.system('google-chrome --remote-debugging-port=9222 --start-maximized --disable-notifications &')
  time.sleep(4)

  try:
    while True:
      time.sleep(random.uniform(.95, 1.25))
      visitPage()
      parsed = getCoords(random.randrange(1, 11))
      keys.append(getKey())
      
      for i in range(11):
        x = parsed['x'] + random.randrange(0, int(parsed['width']))
        y = parsed['y'] + random.randrange(0, int(parsed['height']))
        # print(f'x={x}, y={y}')
        humanMove(x, y)
        time.sleep(random.uniform(1.15, 1.74))
        keys.append(getKey())
        parsed = getCoords(random.randrange(1, 11))
        print(f'Got {len(set(keys))} unique keys')
  except (Exception, KeyboardInterrupt) as e:
    print(f'Error: {e}')
    print(keys)


if __name__ == '__main__':
  main()