import time
import random
from behavior.behavior import humanMove
from behavior.sst_utils import *

"""
Very simple HTML crawl of a website.
"""


def main():
    print('Trying to start browser')
    startBrowser(['www.hetzner.com\n'])

    # do a bit of random moving around
    # to fool bot systems
    coords = getCoords('body')
    print('Clicking on coordinates ' + str(coords))
    humanMove(*coords)
    time.sleep(random.uniform(0.5, 1.0))

    # finally get the page source
    text = getPageSource()
    print('Got {} bytes of HTML data'.format(len(text)))

    # close the browser
    closeBrowser()


if __name__ == '__main__':
    main()
