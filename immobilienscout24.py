import pprint
import sys

import constants
from behavior.behavior import *
from behavior.sst_utils import *

"""
this is an example how to scrape www.immobilienscout24.de 
with stealthy-scraping-tools
www.immobilienscout24.de is protected by advanced bot protection: 
Imperva advanced?

Let's see ;)
"""

# if not os.path.exists("apartments.json"):
#     with open("apartments.json", "w") as f:
#         json.dump({"data": []}, f)

apartments = json.load(open("apartments.json", "r"))
if not apartments:
    apartments = json.load(open("apartments.json", "w"))


def startFluxbox():
    # start fluxbox
    os.system("fluxbox &")
    time.sleep(3)


def startVNC():
    # and a vnc server for debugging remotely
    vnc_cmd = "x11vnc -display {}.0 -forever -passwd {} &".format(
        os.environ["DISPLAY"],
        os.environ["X11VNC_PASSWORD"],
    )
    print(vnc_cmd)
    os.system(vnc_cmd)


def moveRandomly(steps=5):
    width, height = get_dim()
    width = min(1920, width)
    # this is where the bot check is happening
    # move the mouse a bit
    for i in range(steps):
        human_move(
            *(random.randrange(0, width - 50), random.randrange(0, height - 50)),
            clicks=0,
            steps=2,
        )
        time.sleep(random.uniform(0.25, 1.0))


def contact(listing):
    """
    contact the listing. This is where I get mostly blocked.
    """
    goto("https://www.immobilienscout24.de" + listing.get("url"))
    moveRandomly(steps=4)

    already_contacted = get_coords(".is24-icon-heart-Favorite-glyph") is not None
    if already_contacted:
        print("Listing {} already contacted".format(listing.get("url")))
        return True

    # contact
    contact_button = get_coords("a span.palm-hide.email-button-desk-text.font-standard")
    human_move(*contact_button, clicks=1)
    time.sleep(random.uniform(4, 5.5))

    # check if message already entered
    already_entered = (
        json.loads(
            eval_js(
                'document.getElementById("contactForm-Message").value.includes("und Langfristiges")'
            )
        )
        is True
    )
    if not already_entered:
        eval_js('document.getElementById("contactForm-Message").value = `{}`'.format(""))
        # input message
        input = get_coords("#contactForm-Message")
        human_move(*input, clicks=3)
        type_normal("Guten Tag, ")
        time.sleep(random.uniform(0.5, 1.1))
        eval_js(
            'document.getElementById("contactForm-Message").value = `{}`'.format(
                constants.MESSAGE
            )
        )
        time.sleep(random.uniform(0.5, 1.1))

    time.sleep(random.uniform(0.5, 1.1))

    no_pets = get_coords('[for="contactForm-hasPets.no"]')
    if no_pets:
        human_scroll(4, (5, 20), -1)
        time.sleep(random.uniform(1.5, 1.5))
        no_pets = get_coords('[for="contactForm-hasPets.no"]')
        human_move(*no_pets, clicks=1)
        submit = get_coords("button.button-primary.padding-horizontal-m")
        human_move(*submit, clicks=1)
    else:
        submit = get_coords('button[data-qa="sendButtonBasic"]')
        human_move(*submit, clicks=1)

    time.sleep(random.uniform(3.9, 5.9))
    return True


def is_detected():
    detected = (
        json.loads(
            eval_js(
                "JSON.stringify(document.body.textContent.includes('Warum haben wir deine Anfrage blockiert?'));"
            )
        )
        == True
    )
    other = (
        json.loads(
            eval_js(
                "JSON.stringify(document.body.textContent.includes('Sicherheitsabfrage'));"
            )
        )
        == True
    )
    if detected or other:
        print("Got detected as a bot. Aborting.")
        sys.exit(0)
        return True
    else:
        return False


def main():
    if os.getenv("DOCKER") == "1":
        startFluxbox()
        startVNC()

    # startBrowser(args=['--incognito'])
    start_browser(args=[])

    if os.getenv("DOCKER") == "1":
        # close the annoying chrome error message bar
        # it skews with coordinates
        # x:1903 y:114 screen:0 window:195035139
        # x:1889 y:113 screen:0 window:195035139
        human_move(1893, 103)
        human_move(1889, 103)
        time.sleep(random.uniform(2.5, 3.5))

    try:
        human_move(333, 88)  # click on the address bar to enter URL
        pyautogui.typewrite("https://www.immobilienscout24.de")  # There is no indication what url this is supposed to be.
        pyautogui.press("enter")
        # goto("https://www.immobilienscout24.de")
        moveRandomly()

        # are there cookies to accept?
        # cookie consent is in an iframe with id '#gdpr-consent-notice'
        # coords = getCoords('button#save', '#gdpr-consent-notice')
        coords = 1099, 859
        print(f"Accept Cookies by clicking at {coords}")
        human_move(*coords)
        time.sleep(random.uniform(3.5, 4.5))

        # login with username and password
        profile_button = get_coords("#link_loginAccountLink")
        human_move(*profile_button, clicks=0)
        time.sleep(random.uniform(0.5, 2))

        login_button = get_coords(
            "#is24-dropdown > div.MyscoutDropdownV2_LoginContainer__3X0hy.topnavigation__sso-login__link-list--logged-out > a"
        )
        # if login button not visible, we are logged in probably
        if login_button:
            human_move(*login_button, clicks=1)

            time.sleep(random.uniform(2.5, 4))

            user_input = get_coords("#username")
            if not user_input:
                raise Exception("Cannot find username input field by id #username")

            human_move(*user_input, clicks=1)
            time.sleep(random.uniform(0.25, 1.25))
            type_normal(constants.EMAIL)
            time.sleep(random.uniform(0.25, 1.25))

            human_move(*get_coords("#submit"), clicks=1)
            time.sleep(random.uniform(2.25, 3.25))

            human_move(*get_coords("#password"), clicks=1)
            time.sleep(random.uniform(0.25, 1.25))
            type_normal(constants.PASSWORD)
            time.sleep(random.uniform(1.25, 2.25))

            human_move(*get_coords("#loginOrRegistration"), clicks=1)
            time.sleep(random.uniform(2.25, 3.55))

        goto(constants.SEARCH_URL)

        human_scroll(8, (5, 20), -1)

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

        output = eval_js(parse_listings)
        listings = json.loads(output)
        # pprint.pprint(listings)
        filtered_listings = {}
        for el in listings:
            if el.get("url"):
                key = el.get("url")
                location = el.get("location", "").lower().strip()
                for pref in constants.PREFERRED_LOCATIONS:
                    if pref.lower().strip() in location:
                        filtered_listings[key] = el

        # remove listings we already contacted
        for key in apartments:
            if key in filtered_listings:
                if apartments[key].get("contacted", False):
                    print("already contacted listing " + key)
                    del filtered_listings[key]

        pprint.pprint(filtered_listings)

        print("contacting {} listings".format(len(filtered_listings)))
        for key in filtered_listings:
            try:
                contacted = contact(filtered_listings[key])
            except Exception as e:
                print("Failed to contact {}. Blocked? Error: {}".format(key, str(e)))
                is_detected()

            filtered_listings[key]["contacted"] = contacted
            time.sleep(random.uniform(0.5, 1.25))

        # update?
        for k, v in filtered_listings.items():
            apartments[k] = v

        with open("apartments.json", "w") as f:
            json.dump(apartments, f)

        os.system("pkill -f 'chrome'")
    except Exception as e:
        print("Error: {}".format(e))
        is_detected()


if __name__ == "__main__":
    main()
