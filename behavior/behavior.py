import random
import time
import os

if os.getenv('DOCKER') == '1':
  from pyvirtualdisplay.display import Display
  import os 
  import time

  disp = Display(visible=True, size=(1920, 1080), backend="xvfb", use_xauth=True)
  disp.start()

  print('Started display!')
  print('DISPLAY={}'.format(os.environ['DISPLAY']))

  import Xlib.display
  import pyautogui
  pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
else:
  import pyautogui
  pyautogui.FAILSAFE = False


def tinySleep():
  time.sleep(random.uniform(0.075, 0.329))


def someWhereRandomClose(x, y, max_dist=120):
  """
  Find a random position close to (x, y)
  with maximal dist @max_dist
  """
  shape = pyautogui.size()
  cnt = 0

  while True:
    randX = random.randrange(1, max_dist)
    randY = random.randrange(1, max_dist)

    if random.random() > 0.5:
      randX *= -1

    if random.random() > 0.5:
      randY *= -1

    if x + randX in range(0, shape.width) and y + randY in range(0, shape.height):
      return (x + randX, y + randY)

    cnt += 1

    if cnt > 15:
      return (x, y)


def humanMove(x, y, clicks=1):
  """
  Moves like a human to the coordinate (x, y) and 
  clicks on the coordinate.

  Randomizes move time and the move type.

  Visits one intermediate coordiante close to the target before
  fine correcting and clicking on the target coordinates.
  """
  if random.random() < 0.13:
    far_x, far_y = someWhereRandomClose(x, y, 400)
    pyautogui.moveTo(far_x, far_y, random.uniform(0.35, .55), pyautogui.easeOutQuad)
    tinySleep()
    closer_x, closer_y = someWhereRandomClose(x, y, 250)
    pyautogui.moveTo(closer_x, closer_y, random.uniform(0.25, .40), pyautogui.easeOutQuad)

    if random.random() < 0.5 and closer_x > 50 and closer_y > 150:
      tinySleep()
      pyautogui.click(clicks=1)

  # move to an intermediate target close to the destination
  # start fast, end slow
  close_x, close_y = someWhereRandomClose(x, y, 50)
  pyautogui.moveTo(close_x, close_y, random.uniform(.25, .45), pyautogui.easeOutQuad)

  # click on the main target
  pyautogui.moveTo(x, y, random.uniform(.22, .35))
  tinySleep()
  pyautogui.click(clicks=clicks)


def humanScroll(steps, clicks=(5, 20), direction=1):
  for i in range(steps):
    ran_click = random.uniform(*clicks)
    pyautogui.scroll(direction * ran_click)
    time.sleep(random.uniform(0.5, 1.329))


def tinySleep():
  time.sleep(random.uniform(0.005, 0.009))


def doubleHit(key1, key2):
  """
  Sometimes press two keys down at the same time and randomize the 
  order of the corresponding key up events to resemble 
  human typign closer.
  """
  pyautogui.keyDown(key1)
  tinySleep()
  pyautogui.keyDown(key2)
  tinySleep()
  if random.random() > 0.5:
    pyautogui.keyUp(key1)
    tinySleep()
    pyautogui.keyUp(key2)
  else:
    pyautogui.keyUp(key2)
    tinySleep()
    pyautogui.keyUp(key1)


def humanTyping(text, speed=(0.01, 0.025), double_hit=False):
  """
  Mostly the keydown/keyup pairs are in order, but
  sometimes we want two keydown's at the same time.

  text: the text to be written in a human fashion.

  speed: the gap between key presses in seconds. Random number between
    (low, high)
  """
  i = 0
  while i <= len(text):
    if speed:
      time.sleep(random.uniform(*speed))

    if double_hit is True and random.random() < .3 and i+1 < len(text):
      doubleHit(text[i], text[i+1])
      i += 2
    else:
      pyautogui.keyDown(text[i])
      # tinySleep()
      pyautogui.keyUp(text[i])
      i += 1

    if i >= len(text):
      break


def clickNormal(clicks=1):
  pyautogui.click(clicks=clicks, interval=0.25)


def typeNormal(text):
  pyautogui.write(text, interval=random.uniform(0.15, 0.25))


def fastwrite(text):
  pyautogui.write(text, interval=random.uniform(0.045, 0.075))


def press(char):
  pyautogui.press('char', presses=1)


def typeWrite(l):
  pyautogui.typewrite(l, interval=0.22)


def press(key):
  pyautogui.press(key)