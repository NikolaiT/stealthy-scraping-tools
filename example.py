import time
import os
import random
import json
import subprocess
from mouse import humanMove
from typing import humanTyping


def getCoords(selector, randomize_within_bcr=True):
  """
  Example: `node coords.js "li:nth-of-type(3) a"`
  """
  cmd = f'/usr/bin/node coords.js "{selector}"'
  coords = subprocess.check_output(cmd, shell=True)
  parsed = json.loads(coords)

  x = parsed['x']
  y = parsed['y']

  if randomize_within_bcr:
    x += random.randrange(0, int(parsed['width']))
    y += random.randrange(0, int(parsed['height']))

  return x, y


def startBrowser():
  os.system('google-chrome --remote-debugging-port=9222 --start-maximized --disable-notifications &')
  time.sleep(4)

  # visit https://bot.incolumitas.com/#botChallenge
  humanMove(168, 79)
  time.sleep(random.uniform(0.5, 1.5))
  humanTyping('bot.incolumitas.com\n', speed=(0.005, 0.008))
  time.sleep(random.uniform(1.5, 2.5))


def main():
  """
  Get pixel coords with: `xdotool getmouselocation`
  """
  startBrowser()

  # click link to get to the challenge
  coords = getCoords('li:nth-of-type(3) a')
  print('Clicking on coordinates ' + str(coords))
  humanMove(*coords)
  time.sleep(random.uniform(0.5, 1.0))

  # enter username
  username = getCoords('input[name="userName"]')
  humanMove(*username)
  time.sleep(random.uniform(0.25, 1.25))
  humanTyping('IamNotABotISwear\n', speed=(0.005, 0.008))

  time.sleep(random.uniform(0.5, 1.0))

  # enter email
  email = getCoords('input[name="eMail"]')
  humanMove(*email)
  time.sleep(random.uniform(0.25, 1.25))
  humanTyping('bot@spambot.com\n', speed=(0.005, 0.008))

  time.sleep(random.uniform(0.5, 1.0))

  # agree to the terms
  terms = getCoords('input[name="terms"]')
  humanMove(*terms)

  # select cats
  cat = getCoords('#bigCat')
  humanMove(*cat)

  # submit
  submit = getCoords('#submit')
  humanMove(*submit)

  time.sleep(random.uniform(1.5, 2.0))

  humanTyping('\n', speed=(0.005, 0.008))


if __name__ == '__main__':
  main()