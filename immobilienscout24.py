import time
import random
import json
import pprint
from webbrowser import get
from behavior.sst_utils import *
from behavior.behavior import humanMove, humanScroll, press, typeNormal, typeWrite, press
import immo_env

"""
this is an example how to scrape www.immobilienscout24.de with stealthy-scraping-tools

www.immobilienscout24.de is protected by advanced bot protection: Imperva

advanced?

Let's see ;)
"""

if not os.path.exists('apartments.json'):
  with open('apartments.json', 'w') as f:
    json.dump(dict(), f)

apartments = json.load(open('apartments.json', 'r'))

SEARCH_URL = immo_env.SEARCH_URL


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


def contact(listing):
  """
  contact listing
  """
  goto('https://www.immobilienscout24.de' + listing.get('url'))

  # move a bit around like a hobo
  for i in range(3):
    humanMove(*(random.randrange(100, 800), random.randrange(100, 1000)), clicks=0)
    time.sleep(random.uniform(0.5, 1))

  already_contacted = getCoords('.is24-icon-heart-Favorite-glyph') is not None

  already_contacted = False

  if already_contacted:
    return True

  # contact
  contact_button = getCoords("a span.palm-hide.email-button-desk-text.font-standard")
  humanMove(*contact_button, clicks=1)
  time.sleep(random.uniform(4, 5.5))

  evalJS('document.getElementById("contactForm-Message").value = `{}`'.format(''))
  # input message
  input = getCoords("#contactForm-Message")
  humanMove(*input, clicks=3)
  press('backspace')
  time.sleep(random.uniform(0.5, 1.1))
  evalJS('document.getElementById("contactForm-Message").value = `{}`'.format(immo_env.MESSAGE))
  time.sleep(random.uniform(0.5, 1.1))

  submit = getCoords('button[data-qa="sendButtonBasic"]')
  humanMove(*submit, clicks=1)
  time.sleep(random.uniform(3, 5))
  return True


def main():
  if os.getenv('DOCKER') == '1':
    startFluxbox()
    startVNC()

  startBrowser(args=[])

  if os.getenv('DOCKER') == '1':
    # close the annoying chrome error message bar
    # it skews with coordinates
    # x:1903 y:114 screen:0 window:195035139
    # x:1889 y:113 screen:0 window:195035139
    humanMove(1893, 103)
    humanMove(1889, 103)
    time.sleep(random.uniform(2.5, 3.5))

  goto('https://www.immobilienscout24.de')
  # this is where the bot check is happening
  # move the mouse a bit
  for i in range(3):
    humanMove(*(random.randrange(100, 800), random.randrange(100, 1000)), clicks=0)
    time.sleep(random.uniform(0.5, 1))

  # are there cookies to accept?
  # cookie consent is in an iframe with id '#gdpr-consent-notice'
  # coords = getCoords('button#save', '#gdpr-consent-notice')
  coords = 1099, 859
  print(f'Accept Cookies by clicking at {coords}')
  humanMove(*coords)
  time.sleep(random.uniform(3.5, 4.5))

  # login with username and password
  profile_button = getCoords('#link_loginAccountLink')
  humanMove(*profile_button, clicks=0)
  time.sleep(random.uniform(0.5, 2))

  login_button = getCoords("#is24-dropdown > div.MyscoutDropdownV2_LoginContainer__3X0hy.topnavigation__sso-login__link-list--logged-out > a")
  # if login button not visible, we are logged in probably
  if login_button:
    humanMove(*login_button, clicks=1)

    time.sleep(random.uniform(2.5, 4))

    user_input = getCoords('#username')
    humanMove(*user_input, clicks=1)
    time.sleep(random.uniform(0.25, 1.25))
    typeNormal(immo_env.EMAIL)
    time.sleep(random.uniform(0.25, 1.25))

    humanMove(*getCoords('#submit'), clicks=1)
    time.sleep(random.uniform(2.25, 3.25))

    humanMove(*getCoords('#password'), clicks=1)
    time.sleep(random.uniform(0.25, 1.25))
    typeNormal(immo_env.PASSWORD)
    time.sleep(random.uniform(1.25, 2.25))

    humanMove(*getCoords('#loginOrRegistration'), clicks=1)
    time.sleep(random.uniform(1.25, 2.25))

  goto(SEARCH_URL)
  # this is where the bot check is happening
  # move the mouse a bit
  for i in range(3):
    humanMove(*(random.randrange(100, 800), random.randrange(100, 1000)), clicks=0)
    time.sleep(random.uniform(0.5, 1.25))

  humanScroll(7, (5, 20), -1)

  # finally parse the listings
  parse_listings = """var res = [];
document.querySelectorAll(".result-list__listing").forEach((el) => {
let title = el.querySelector(".result-list-entry__brand-title");
let details = el.querySelector(".result-list-entry__criteria");

if (title) {
  let obj = {
    contacted: false,
    title: title.textContent,
    url: el.querySelector("a.result-list-entry__brand-title-container").getAttribute("href"),
  };
  if (details) {
    obj.location = el.querySelector(".result-list-entry__map-link.link-text-secondary.font-normal.font-ellipsis").textContent;
    obj.price = details.querySelector("dl.grid-item:nth-child(1)").textContent;
    obj.area = details.querySelector("dl.grid-item:nth-child(2)").textContent;
    obj.rooms = details.querySelector("dl.grid-item:nth-child(3)").textContent;
  }
  res.push(obj);
}
});
JSON.stringify(res);"""

  output = evalJS(parse_listings)
  listings = json.loads(output)
  # pprint.pprint(listings)
  filtered_listings = {}
  for el in listings:
    if el.get('url'):
      key = el.get('url')
      location = el.get('location', '').lower().strip()
      for pref in immo_env.PREFERRED_LOCATIONS:
        if pref.lower().strip() in location:
          filtered_listings[key] = el

  # remove listings we already contacted
  for key in apartments:
    if key in filtered_listings:
      if apartments[key].get('contacted', False):
        print('already contacted listing ' + key)
        del filtered_listings[key]

  pprint.pprint(filtered_listings)

  print('contacting {} listings'.format(len(filtered_listings)))
  for key in filtered_listings:
    contacted = contact(filtered_listings[key])
    filtered_listings[key]['contacted'] = contacted
    time.sleep(random.uniform(0.5, 1.25))

  # update?
  for k, v in filtered_listings.items():
    apartments[k] = v

  with open('apartments.json', 'w') as f:
    json.dump(apartments, f)


if __name__ == '__main__':
  main()