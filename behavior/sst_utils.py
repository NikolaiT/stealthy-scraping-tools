import time
import os
import random
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
  command = command.replace('\n', '')
  script_path = getScriptPath('eval_js.js')
  cmd = f"node {script_path} '{command}'"
  ps = subprocess.check_output(cmd, shell=True)
  return ps

def getCoords(selector, randomize_within_bcr=True):
  """
  Example: `node coords.js "li:nth-of-type(3) a"`
  """
  script_path = getScriptPath('coords.js')
  cmd = f'node {script_path} "{selector}"'
  coords = subprocess.check_output(cmd, shell=True)
  print(coords)
  parsed = json.loads(coords)

  x = parsed['x']
  y = parsed['y']

  if randomize_within_bcr:
    x += random.randrange(0, int(parsed['width']))
    y += random.randrange(0, int(parsed['height']))

  return x, y


def startBrowser(address_bar, args=[]):
  arg_str = ' '.join(args)
  startCmd = f'google-chrome --remote-debugging-port=9222 --start-maximized --disable-notifications {arg_str} &'
  os.system(startCmd)
  time.sleep(6)
  
  humanMove(168, 79)
  time.sleep(random.uniform(0.5, 1.5))
  humanTyping(address_bar, speed=(0.005, 0.008))
  time.sleep(random.uniform(1.5, 2.5))