import time
import os
import random
import subprocess
import json
import re
from mouse import humanMove
from typing import humanTyping
from target import target

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
  humanMove(168, 79)
  humanTyping(target, doubleHit=False)
  time.sleep(random.randrange(3, 4))


def main():
  """
  Get pixel coords with: `xdotool getmouselocation`
  """
  os.system('google-chrome --remote-debugging-port=9222 --start-maximized --disable-notifications &')
  time.sleep(4)

  try:
    while True:
      visitPage()
      parsed = getCoords(random.randrange(1, 11))
      keys.append(getKey())

      for i in range(11):
        x = parsed['x'] + random.randrange(0, int(parsed['width'] / 2))
        y = parsed['y'] + random.randrange(0, int(parsed['height'] / 2))
        # print(f'x={x}, y={y}')
        humanMove(x, y)
        time.sleep(random.randrange(1, 3))
        keys.append(getKey())
        parsed = getCoords(random.randrange(1, 11))
        print(f'Got {len(set(keys))} unique keys')
  except (Exception, KeyboardInterrupt) as e:
    print(f'Error: {e}')
    print(keys)


if __name__ == '__main__':
  main()