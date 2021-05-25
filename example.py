import time
import os
import random
import json
import subprocess
from mouse import humanMove
from typing import humanTyping


def getCoords(selector, randomize_within_bcr=True):
  cmd = f'/usr/bin/node coords.js "{selector}"'
  coords = subprocess.check_output(cmd, shell=True)
  parsed = json.loads(coords)

  x = parsed['x'] + random.randrange(0, parsed['width'])
  y = parsed['y'] + random.randrange(0, parsed['height'])

  if randomize_within_bcr:
    x += random.randrange(0, parsed['width'])
    y += random.randrange(0, parsed['height'])

  return x, y


def main():
  """
  Get pixel coords with: `xdotool getmouselocation`
  """
  os.system('google-chrome --remote-debugging-port=9222 --start-maximized --disable-notifications &')
  time.sleep(4)

  # visit https://bot.incolumitas.com/#botChallenge
  humanMove(168, 79)
  time.sleep(random.uniform(0.5, 1.5))
  humanTyping('bot.incolumitas.com\n', speed=(0.005, 0.008))
  time.sleep(random.uniform(1.5, 2.5))

  # click link to get to the challenge
  coords = getCoords('li:nth-of-type(3)')
  print(coords)
  humanMove(*coords)

  # enter username
  username = getCoords('input[name="userName"]')
  humanMove(*username)

  # enter email
  email = getCoords('input[name="eMail"]')
  humanMove(*email)

  # agree to the terms
  terms = getCoords('input[name="terms"]')
  humanMove(*terms)

  # select cats
  cat = getCoords('#bigCat')
  humanMove(*cat)

  # submit
  submit = getCoords('#submit')
  humanMove(*submit)


if __name__ == '__main__':
  main()