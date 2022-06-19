# Stealthy Scraping Tools

Do not use puppeteer and playwright for scraping. Or any other browser automation framework for that matter. [Why?](https://incolumitas.com/2021/05/20/avoid-puppeteer-and-playwright-for-scraping/)

We only use the [CDP](https://developer.chrome.com/docs/devtools/) to obtain the page source and to get the absolute coordinates for an arbitrary CSS selector. That's all what is needed for efficient scraping.

1. To obtain the page source of the browser's current page. Implemented in [page_source.js](https://github.com/NikolaiT/stealthy-scraping-tools/blob/main/page_source.js)
2. To get the absolute coordinates for an arbitrary CSS selector. Implemented in [coords.js](https://github.com/NikolaiT/stealthy-scraping-tools/blob/main/coords.js)

Mouse movements and typing is handled by `pyautogui` or other means, but not with JavaScript or with the CDP! Reason: Browser based mouse and keyboard emulation is very easy detectable!

## Theory 

1. Analyzing key strokes: [TypeNet: Deep Learning Keystroke Biometrics](https://arxiv.org/abs/2101.05570)
2. Research how to mimic human mouse movements: [BeCAPTCHA-Mouse: Synthetic Mouse Trajectories and Improved Bot Detection](https://arxiv.org/abs/2005.00890)

## Full Example

The bot challenge that can be found here [bot.incolumitas.com/#botChallenge](https://bot.incolumitas.com/#botChallenge) will be solved in the following quick tutorial.

The example code can be found in `example.py`.

I am using an Ubuntu 18.04 system with `Python3` (with `pipenv`) and a recent `Node` version.

The browser `google-chrome` must be installed.

Clone the repo:

```
git clone https://github.com/NikolaiT/stealthy-scraping-tools
cd stealthy-scraping-tools
```

Activate an environment with:

```bash
pew new -p python3 sst

pew workon sst
```

Then install `pyautogui`:

```bash
pip install pyautogui
```

Install node modules:

```
npm install chrome-remote-interface
```

And then run the bot with:

```python
python example.py
```

## Docker

The Dockerfile is based on `Ubuntu 20.04`. 

The Dockerfile uses `xvfb` from the python module `PyVirtualDisplay`.

I use `pyautogui` for mouse and keyboard automation. 

I use `fluxbox` as a tiny window manager and `x11vnc` (Virtual Network Computing server program) as a means to inspect the docker image and see what is going on.

Build the Dockerfile:

```
docker build -t sst:0.0.1 .
```

Hint: Avoid chrome in docker crashing: https://github.com/stephen-fox/chrome-docker/issues/8

```
1. Option 1: Run chrome with --disable-dev-shm-usage
2. Option 2: Set /dev/shm size to a reasonable amount `docker run -it --shm-size=1g` replacing 1g with whatever amount you want.
```

The docker option `--shm-size=2g` is really important:

```
docker run --cap-add=NET_ADMIN --network="host" --shm-size=2g sst:0.0.1
```

## TODO

+ Look at Kernel/OS level mouse/keyboard control commands (Ditch `pyautogui`)
+ Use the math from [ghost-cursor](https://github.com/Xetera/ghost-cursor)
+ Create a set of typing recordings and use it to derive rules for bot writing
