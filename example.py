from behavior.behavior import human_move, human_typing
from behavior.sst_utils import *

"""
You might have to adjust some coordinates. 

I used a dual screen setup and I started the browser on the
left screen.

You can obtain the coordinates of your current mouse pointer with 
the bash command on Linux `xdotool getmouselocation`
"""


def main():
    start_browser("bot.incolumitas.com\n")
    coords = get_coords("li:nth-of-type(3) a")
    print(f"Clicking on coordinates {str(coords)}")
    human_move(*coords)
    time.sleep(random.uniform(0.5, 1.0))

    # enter username
    username = get_coords('input[name="userName"]')
    human_move(*username, clicks=2)
    time.sleep(random.uniform(0.25, 1.25))
    human_typing("IamNotABotISwear\n", speed=(0.005, 0.008))

    time.sleep(random.uniform(0.5, 1.0))

    # enter email
    email = get_coords('input[name="eMail"]')
    human_move(*email, clicks=3)
    time.sleep(random.uniform(0.25, 1.25))
    human_typing("bot@spambot.com\n", speed=(0.005, 0.008))

    time.sleep(random.uniform(0.5, 1.0))

    # agree to the terms
    terms = get_coords('input[name="terms"]')
    human_move(*terms)

    # select cats
    cat = get_coords("#bigCat")
    human_move(*cat)

    # submit
    submit = get_coords("#submit")
    human_move(*submit)

    # press the final enter
    time.sleep(random.uniform(2.5, 3.4))
    human_typing("\n", speed=(0.005, 0.008))

    # finally get the page source
    text = get_page_source()
    print(f"Got {len(text)} bytes of page source")


if __name__ == "__main__":
    main()
