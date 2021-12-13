import time
import os
import random
import json
import subprocess
from mouse import humanMove
from typing import humanTyping

"""
You might have to adjust some coordinates. 

I used a dual screen setup and I started the browser on the
left screen.

You can obtain the coordinates of your current mouse pointer with 
the bash command on Linux `xdotool getmouselocation`
"""

def getPageSource():
  cmd = f'/usr/bin/node page_source.js'
  ps = subprocess.check_output(cmd, shell=True)
  return ps


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
  startBrowser()

  # click link to get to the challenge
  coords = getCoords('li:nth-of-type(3) a')
  print('Clicking on coordinates ' + str(coords))
  humanMove(*coords)
  time.sleep(random.uniform(0.5, 1.0))

  # enter username
  username = getCoords('input[name="userName"]')
  humanMove(*username, clicks=2)
  time.sleep(random.uniform(0.25, 1.25))
  humanTyping('IamNotABotISwear\n', speed=(0.005, 0.008))

  time.sleep(random.uniform(0.5, 1.0))

  # enter email
  email = getCoords('input[name="eMail"]')
  humanMove(*email, clicks=3)
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

  # press the final enter
  time.sleep(random.uniform(2.5, 3.4))
  humanTyping('\n', speed=(0.005, 0.008))

  # finally get the page source
  text = getPageSource()
  print('Got {} bytes of page soure'.format(len(text)))


if __name__ == '__main__':
  main()