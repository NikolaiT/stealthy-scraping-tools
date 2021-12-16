import time
import random
from behavior.behavior import humanMove
from typing import humanTyping
from behavior.sst_utils import *

"""
You might have to adjust some coordinates. 

I used a dual screen setup and I started the browser on the
left screen.

You can obtain the coordinates of your current mouse pointer with 
the bash command on Linux `xdotool getmouselocation`
"""

def main():
  startBrowser('bot.incolumitas.com\n')

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