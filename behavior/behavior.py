import os
import random
import time
from turtle import width

if os.getenv("DOCKER") == "1":
    import os
    import time

    from pyvirtualdisplay.display import Display

    disp = Display(visible=True, size=(1920, 1080), backend="xvfb", use_xauth=True)
    disp.start()

    print("Started display!")
    print(f'DISPLAY={os.environ["DISPLAY"]}')

    import pyautogui
    import Xlib.display

    pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ["DISPLAY"])
else:
    import pyautogui

    pyautogui.FAILSAFE = False


def tiny_sleep():
    time.sleep(random.uniform(0.075, 0.329))


def get_dim():
    # current screen resolution width and height
    return pyautogui.size()


def some_where_random_close(x, y, max_dist=120):
    """
    Find a random position close to (x, y)
    with maximal dist @max_dist
    """
    shape = pyautogui.size()
    cnt = 0

    while True:
        rand_x = random.randrange(1, max_dist)
        rand_y = random.randrange(1, max_dist)

        if random.random() > 0.5:
            rand_x *= -1

        if random.random() > 0.5:
            rand_y *= -1

        if x + rand_x in range(shape.width) and y + rand_y in range(shape.height):
            return x + rand_x, y + rand_y

        cnt += 1

        if cnt > 15:
            return (x, y)


def human_move(x, y, clicks=1, steps=1):
    """
    Moves like a human to the coordinate (x, y) and
    clicks on the coordinate.

    Randomizes move time and the move type.

    Visits one intermediate coordinate close to the target before
    fine correcting and clicking on the target coordinates.
    """
    width, height = get_dim()

    if steps > 1:  # kek
        far_x, far_y = some_where_random_close(x, y, min(width, 600))
        pyautogui.moveTo(
            far_x, far_y, random.uniform(0.35, 0.55), pyautogui.easeOutQuad
        )
        tiny_sleep()

    if steps > 0:
        closer_x, closer_y = some_where_random_close(x, y, min(width, 400))
        pyautogui.moveTo(
            closer_x, closer_y, random.uniform(0.25, 0.40), pyautogui.easeOutQuad
        )

    # move to an intermediate target close to the destination
    # start fast, end slow
    close_x, close_y = some_where_random_close(x, y, 50)
    pyautogui.moveTo(
        close_x, close_y, random.uniform(0.25, 0.45), pyautogui.easeOutQuad
    )

    # click on the main target
    pyautogui.moveTo(x, y, random.uniform(0.22, 0.35))
    tiny_sleep()
    pyautogui.click(clicks=clicks)


def human_scroll(steps, clicks=(5, 20), direction=1):
    for _ in range(steps):
        ran_click = random.uniform(*clicks)
        pyautogui.scroll(direction * ran_click)
        time.sleep(random.uniform(0.5, 1.329))


def double_hit(key1, key2):
    """
    Sometimes press two keys down at the same time and randomize the
    order of the corresponding key up events to resemble
    human typing closer.
    """
    pyautogui.keyDown(key1)
    tiny_sleep()
    pyautogui.keyDown(key2)
    tiny_sleep()
    if random.random() > 0.5:
        pyautogui.keyUp(key1)
        tiny_sleep()
        pyautogui.keyUp(key2)
    else:
        pyautogui.keyUp(key2)
        tiny_sleep()
        pyautogui.keyUp(key1)


def human_typing(text, speed=(0.01, 0.025), double_hit=False):
    """
    Mostly the keydown/keyup pairs are in order, but
    sometimes we want two keydowns at the same time.

    text: the text to be written in a human fashion.

    speed: the gap between key presses in seconds. Random number between
      (low, high)
    """
    i = 0
    while i <= len(text):
        if speed:
            time.sleep(random.uniform(*speed))

        if double_hit is True and random.random() < 0.3 and i + 1 < len(text):
            double_hit(text[i], text[i + 1])
            i += 2
        else:
            pyautogui.keyDown(text[i])
            # tinySleep()
            pyautogui.keyUp(text[i])
            i += 1

        if i >= len(text):
            break


def click_normal(clicks=1):
    pyautogui.click(clicks=clicks, interval=0.25)


def type_normal(text):
    pyautogui.write(text, interval=random.uniform(0.15, 0.25))


def fast_write(text):
    pyautogui.write(text, interval=random.uniform(0.045, 0.075))


def press(char):
    pyautogui.press("char", presses=1)


def type_write(l):
    pyautogui.typewrite(l, interval=0.22)
