import time
import random
from mouse import humanMove, humanScroll
import json 
import pprint
from typing import typeNormal
from sst_utils import *
import os

if os.getenv('DOCKER') == '1':
  from pyvirtualdisplay.display import Display
  disp = Display(visible=True, size=(1920, 1080), backend="xvfb", use_xauth=True)
  disp.start()

  import Xlib.display
  import pyautogui
  pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
else:
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

  humanMove(315, 255, clicks=1)
  time.sleep(random.uniform(0.5, 1.0))

  # input price
  input_price = getCoords('#oss-price')
  humanMove(*input_price, clicks=1)
  time.sleep(random.uniform(0.25, 1.25))
  typeNormal('700')

  # input area
  input_area = getCoords('#oss-area')
  humanMove(*input_area, clicks=1)
  time.sleep(random.uniform(0.25, 1.25))
  typeNormal('45')

  humanMove(1217, 495, clicks=1)
  time.sleep(random.uniform(0.5, 1.0))

  # submit
  submit = getCoords('button.oss-main-criterion.oss-button.button-primary.one-whole')
  humanMove(*submit)

  time.sleep(random.uniform(4, 5.0))

  humanScroll(7, (5, 20), -1)

  # finally parse the listings
  parse_listings = """var res = [];
document.querySelectorAll(".result-list__listing").forEach((el) => {
let title = el.querySelector(".result-list-entry__brand-title");
let details = el.querySelector(".result-list-entry__criteria");

if (title) {
  let obj = {
    title: title.textContent,
    url: el.querySelector("a.result-list-entry__brand-title-container").getAttribute("href"),
  };
  if (details) {
    obj.price = details.querySelector("dl.grid-item:nth-child(1)").textContent;
    obj.area = details.querySelector("dl.grid-item:nth-child(2)").textContent;
    obj.rooms = details.querySelector("dl.grid-item:nth-child(3)").textContent;
  }
  res.push(obj);
}
});
JSON.stringify(res);"""

  listings = evalJS(parse_listings)
  # print(listings)
  pprint.pprint(json.loads(listings))


if __name__ == '__main__':
  main()