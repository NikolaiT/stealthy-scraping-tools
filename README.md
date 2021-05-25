# Stealthy Scraping Tools

Do not use puppeteer and playwright for scraping.

We only use the CDP to obtain the page source and to get the absolute coordinates for a CSS selector.

Mouse movements and typing is handled by `pyautogui` or other means, but not with JavaScript or with the CDP!

## Full Example

