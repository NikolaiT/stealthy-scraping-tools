import time
import random
from mouse import humanMove, humanScroll
from typing import humanTyping, typeNormal
from sst_utils import *
import pyautogui

"""
this is an example how to scrape www.immobilienscout24.de with stealthy-scraping-tools

www.immobilienscout24.de is protected by advanced bot protection

advanced?
"""

def main():
  startBrowser('www.immobilienscout24.de\n', args=['--incognito'])

  time.sleep(random.uniform(3, 5))

  # are there cookies to accept?
  # cookie consent is in an iframe with id '#gdpr-consent-notice'
  # coords = getCoords('button#save', '#gdpr-consent-notice')
  coords = 1099, 859
  print('Accept to Cookies ' + str(coords))
  humanMove(*coords)
  time.sleep(random.uniform(1.5, 2.5))

  # enter City
  input_loc = getCoords('#oss-location')
  humanMove(*input_loc, clicks=1)
  time.sleep(random.uniform(0.25, 1.25))
  typeNormal('K')
  time.sleep(random.uniform(1.5, 2.5))

  pyautogui.press('down')
  time.sleep(random.uniform(0.5, 1.0))
  pyautogui.press('down')
  time.sleep(random.uniform(0.5, 1.0))
  pyautogui.press('enter')

  humanMove(160, 703, clicks=1)
  time.sleep(random.uniform(0.5, 1.0))

  # submit
  submit = getCoords('button.oss-main-criterion.oss-button.button-primary.one-whole')
  humanMove(*submit)

  time.sleep(random.uniform(4, 5.0))

  humanScroll(7, (5, 20), -1)

  # # finally get the page source
  text = getPageSource()
  print('Got {} bytes of page soure'.format(len(text)))


if __name__ == '__main__':
  main()