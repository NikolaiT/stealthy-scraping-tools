# Stealthy Scraping Tools

Do not use puppeteer and playwright for scraping.

We only use the CDP to obtain the page source and to get the absolute coordinates for a CSS selector.

Mouse movements and typing is handled by `pyautogui` or other means, but not with JavaScript or with the CDP!

## Theory 

1. Analyzing key strokes: **TypeNet: Deep Learning Keystroke Biometrics**
2. Research how to mimic human mouse movements: **BeCAPTCHA-Mouse: Synthetic Mouse Trajectories and Improved Bot Detection**

## Full Example

The bot challenge that can be found here [bot.incolumitas.com/#botChallenge](https://bot.incolumitas.com/#botChallenge) will be solved in the following quick tutorial.

The example code can be found in `example.py`.


