import pyautogui
import random

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


def humanMove(x, y, doubleClick=False):
  """
  Moves like a human to the coordinate (x, y) and 
  clicks on the coordinate.

  Randomizes move time and the move type.

  Visits one intermediate coordiante close to the target before
  fine correcting and clicking on the target coordinates.
  """
  close_x, close_y = someWhereRandomClose(x, y, 100)

  # move to an intermediate target close to the destination
  # start fast, end slow
  pyautogui.moveTo(close_x, close_y, random.uniform(0.19, .75), pyautogui.easeOutQuad)

  # click on the main target
  pyautogui.moveTo(x, y, random.uniform(0.25, .65))

  if doubleClick:
    pyautogui.click(clicks=2)
  else:
    pyautogui.click()
