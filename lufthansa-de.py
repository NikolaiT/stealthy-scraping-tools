import random
import time

from behavior.behavior import *
from behavior.sst_utils import *

"""
this is an example how to scrape www.lufthansa.de with stealthy-scraping-tools
"""


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


def main():
    if os.getenv("DOCKER") == "1":
        startFluxbox()
        startVNC()

    start_browser(args=[])

    if os.getenv("DOCKER") == "1":
        # close the annoying chrome error message bar
        # it skews with coordinates
        # x:1903 y:114 screen:0 window:195035139
        # x:1889 y:113 screen:0 window:195035139
        human_move(1893, 103)
        human_move(1889, 103)
        time.sleep(random.uniform(2.5, 3.5))

    for i in range(150):
        print(f"[{i}] Searching for flights...")
        time.sleep(random.uniform(0.5, 1.0))

        goto("https://www.lufthansa.com/de/de/homepage")
        time.sleep(random.uniform(4, 6))

        # accept cookies?
        if i == 0:
            try:
                cookie_accept = get_coords("#cm-acceptAll")
                if cookie_accept:
                    human_move(*cookie_accept, clicks=1)
                    time.sleep(random.uniform(0.25, 1.25))
            except Exception as e:
                print("No cookies to accept, #cm-acceptAll not found")

        # enter where to go
        try:
            input_loc = get_coords('input[placeholder="Nach"]')
            print("Enter Departure " + str(input_loc))
            human_move(*input_loc, clicks=2)
            time.sleep(random.uniform(0.25, 1.25))
            type_normal(
                random.choice(
                    [
                        "Berlin",
                        "Paris",
                        "Tel Aviv",
                        "Stockholm",
                        "Bogota",
                        "Bangkok",
                        "New York",
                    ]
                )
            )
            time.sleep(random.uniform(1.5, 2.5))
            press("down")
            time.sleep(random.uniform(0.5, 1.0))
            press("enter")
            time.sleep(random.uniform(0.5, 1.0))
        except Exception as e:
            print(f"[{i}] Could not enter flight destination. Blocked?")
            continue

        # input return date
        try:
            backdate = get_coords('input[placeholder="Rückflugdatum"]')
            print("backdate " + str(backdate))
            human_move(*backdate, clicks=1)
            time.sleep(random.uniform(4.55, 5.55))
        except Exception as e:
            print(f"[{i}] Could not click on return value. Leaving untouched.")

        # enter departure date
        try:
            datetile = get_coords(
                random.choice(
                    [
                        '[aria-label^="Choose Samstag, 25 Dezember 2021"]',
                        '[aria-label^="Choose Sonntag, 26 Dezember 2021"]',
                    ]
                )
            )
            print("datetile " + str(datetile))
            human_move(*datetile, clicks=1)
            time.sleep(random.uniform(2.25, 3.25))
        except Exception as e:
            print(f"[{i}] Could not select return date. Keeping default value.")

        # submit
        try:
            submit = get_coords('[type="submit"]')
            print("Submit " + str(submit))
            human_move(*submit)
        except Exception as e:
            print(f"[{i}] Could not submit search. Blocked?")
            continue

        # wait for quite some time
        time.sleep(random.uniform(10, 14))
        human_scroll(2, (5, 20), -1)

        try:
            calendar = get_coords("#page .calendarTab")
            if calendar:
                print(f"[{i}] Flight Results loaded!")
        except Exception as e:
            print(f"[{i}] Could not find calendar for flights. Page load to slow?")


if __name__ == "__main__":
    main()
