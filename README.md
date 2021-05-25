# Stealthy Scraping Tools

Do not use puppeteer and playwright for scraping.

We only use the [CDP](https://developer.chrome.com/docs/devtools/) to obtain the page source and to get the absolute coordinates for a CSS selector.

Mouse movements and typing is handled by `pyautogui` or other means, but not with JavaScript or with the CDP! Reason: Browser based mouse and keyboard emulation is very easy detectable!

## Theory 

1. Analyzing key strokes: **TypeNet: Deep Learning Keystroke Biometrics**
2. Research how to mimic human mouse movements: **BeCAPTCHA-Mouse: Synthetic Mouse Trajectories and Improved Bot Detection**

## Full Example

The bot challenge that can be found here [bot.incolumitas.com/#botChallenge](https://bot.incolumitas.com/#botChallenge) will be solved in the following quick tutorial.

The example code can be found in `example.py`.

## TODO

+ Look at Kernel/OS level mouse/keyboard control commands (Ditch `pyautogui`)
+ Use the math from [ghost-cursor](https://github.com/Xetera/ghost-cursor)
+ Create a set of typign recordings and use it to derive rules for bot writing


