import time
import random
import json
import pprint
from behavior.sst_utils import *
from behavior.behavior import humanMove, humanScroll, press, typeNormal

"""
this is an example how to scrape www.immobilienscout24.de with stealthy-scraping-tools

www.immobilienscout24.de is protected by advanced bot protection

advanced?
"""


def startFluxbox():
  # start fluxbox
  os.system('fluxbox &')
  time.sleep(3)


def startVNC():
  # and a vnc server for debugging remotely
  vnc_cmd = 'x11vnc -display {}.0 -forever -passwd {} &'.format(
    os.environ['DISPLAY'],
    os.environ['X11VNC_PASSWORD'],
  )
  print(vnc_cmd)
  os.system(vnc_cmd)


def main():
  if os.getenv('DOCKER') == '1':
    startFluxbox()
    startVNC()

  startBrowser(args=[])
  time.sleep(random.uniform(3, 5))

  # enter the url
  # humanMove(168, 79)
  # time.sleep(random.uniform(0.5, 1.5))
  # humanTyping('www.immobilienscout24.de\n', speed=(0.005, 0.008))
  # time.sleep(random.uniform(1.5, 2.5))

  if os.getenv('DOCKER') == '1':
    # close the annoying chrome error message bar
    # it skews with coordinates
    # x:1903 y:114 screen:0 window:195035139
    # x:1889 y:113 screen:0 window:195035139
    humanMove(1893, 103)
    humanMove(1889, 103)
    time.sleep(random.uniform(2.5, 3.5))

  for i in range(7):
    time.sleep(random.uniform(0.5, 1.0))

    if os.getenv('DOCKER') == '1':
      goto('https://www.immobilienscout24.de')
      time.sleep(random.uniform(4, 7))

    # are there cookies to accept?
    # cookie consent is in an iframe with id '#gdpr-consent-notice'
    # coords = getCoords('button#save', '#gdpr-consent-notice')
    if i == 0:
      coords = 1099, 859
      print(f'[{i}] Accept to Cookies {coords}')
      humanMove(*coords)
      time.sleep(random.uniform(3.5, 4.5))

    # enter City
    if i == 0:
      input_loc = getCoords('#oss-location')
      print('Enter City ' + str(input_loc))
      humanMove(*input_loc, clicks=2)
      time.sleep(random.uniform(0.25, 1.25))
      typeNormal('K')
      time.sleep(random.uniform(1.5, 2.5))
      press('down')
      time.sleep(random.uniform(0.5, 1.0))
      press('down')
      time.sleep(random.uniform(0.5, 1.0))
      press('enter')
      time.sleep(random.uniform(2.5, 3.5))

    # input price
    input_price = getCoords('input#oss-price')
    print('Enter Max Price ' + str(input_price))
    humanMove(*input_price, clicks=2)
    time.sleep(random.uniform(0.25, 1.25))
    typeNormal('700')

    time.sleep(random.uniform(0.25, 1.25))

    # input area
    input_area = getCoords('input#oss-area')
    print('Enter Area ' + str(input_area))
    humanMove(*input_area, clicks=2)
    time.sleep(random.uniform(0.25, 1.25))
    typeNormal('45')

    # submit
    submit = getCoords('button.oss-main-criterion.oss-button.button-primary.one-whole')
    print('Submit ' + str(submit))
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