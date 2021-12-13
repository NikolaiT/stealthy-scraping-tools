import time
import random
from mouse import humanMove
from typing import humanTyping
from sst_utils import *

"""
this is an example how to scrape www.immobilienscout24.de with stealthy-scraping-tools

www.immobilienscout24.de is protected by advanced bot protection

advanced?
"""

def main():
  startBrowser('www.immobilienscout24.de\n')

  time.sleep(random.uniform(3, 5))

  # are there cookies to accept?
  # cookie consent is in an iframe with id '#gdpr-consent-notice'
  coords = getCoords('button#save')
  print('Accept to Cookies ' + str(coords))
  humanMove(*coords)
  time.sleep(random.uniform(0.5, 1.0))

  # # enter username
  # username = getCoords('input[name="userName"]')
  # humanMove(*username, clicks=2)
  # time.sleep(random.uniform(0.25, 1.25))
  # humanTyping('IamNotABotISwear\n', speed=(0.005, 0.008))

  # time.sleep(random.uniform(0.5, 1.0))

  # # enter email
  # email = getCoords('input[name="eMail"]')
  # humanMove(*email, clicks=3)
  # time.sleep(random.uniform(0.25, 1.25))
  # humanTyping('bot@spambot.com\n', speed=(0.005, 0.008))

  # time.sleep(random.uniform(0.5, 1.0))

  # # agree to the terms
  # terms = getCoords('input[name="terms"]')
  # humanMove(*terms)

  # # select cats
  # cat = getCoords('#bigCat')
  # humanMove(*cat)

  # # submit
  # submit = getCoords('#submit')
  # humanMove(*submit)

  # # press the final enter
  # time.sleep(random.uniform(2.5, 3.4))
  # humanTyping('\n', speed=(0.005, 0.008))

  # # finally get the page source
  # text = getPageSource()
  # print('Got {} bytes of page soure'.format(len(text)))


if __name__ == '__main__':
  main()