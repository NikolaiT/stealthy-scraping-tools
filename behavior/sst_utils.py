import time
import os
import random
import math
import json
import subprocess
from behavior.behavior import humanMove, humanTyping
from pathlib import Path

def goto(url):
  script_path = getScriptPath('goto.js')
  cmd = f"node {script_path} '{url}'"
  ps = subprocess.check_output(cmd, shell=True)
  return ps

def getScriptPath(name):
  return os.path.join(
    Path(__file__).parent.parent,
    'cdp/' + name
  )

def getPageSource():
  cmd = 'node ' + getScriptPath('page_source.js')
  ps = subprocess.check_output(cmd, shell=True)
  return ps

def evalJS(command):
  with open('/tmp/evalCommand.txt', 'w') as f:
    f.write(command)

  script_path = getScriptPath('eval_js.js')
  cmd = f"node {script_path}"
  ps = subprocess.check_output(cmd, shell=True)
  return ps

def getCoords(selector, randomize_within_bcr=True):
  """
  Example: `node coords.js "li:nth-of-type(3) a"`
  """
  script_path = getScriptPath('coords.js')
  cmd = f"node {script_path} '{selector}'"
  coords = subprocess.check_output(cmd, shell=True)
  coords = coords.decode()

  x, y = 0, 0

  try:
    parsed = json.loads(coords)
    x = parsed['x']
    y = parsed['y']

    # this is fucking inaccurate. WHY???
    # is el.getBoundingClientRect() fucky?
    if randomize_within_bcr:
      # print(x, y, parsed['width'], parsed['height'])
      x += random.randint(math.floor(parsed['width'] / 4), math.floor(parsed['width'] / 2))
      y += random.randint(math.floor(parsed['height'] / 4), math.floor(parsed['height'] / 2))
  except Exception as e:
    print('getCoords() failed with Error: {}'.format(e))
    return None

  return x, y


def startBrowser(args=[]):
  arg_str = ' '.join(args)
  startCmd = f'google-chrome --remote-debugging-port=9222 --start-maximized --disable-notifications {arg_str} &'
  
  if os.getenv('DOCKER') == '1':
    startCmd = 'google-chrome --remote-debugging-port=9222 --no-sandbox --disable-notifications --start-maximized --no-first-run --no-default-browser-check &'
    # startCmd = 'google-chrome --remote-debugging-port=9222 --no-sandbox --disable-notifications --start-maximized --no-first-run --no-default-browser-check --incognito &'
  
  os.system(startCmd)
  time.sleep(random.uniform(4, 5))
