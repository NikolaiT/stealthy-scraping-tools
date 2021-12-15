FROM ubuntu:20.04

# Set correct timezone
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install python3 tesseract-ocr python3-pip curl unzip -yf

# Install Chrome
RUN apt-get update -y
RUN apt-get install -y dbus-x11
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb

RUN apt-get install -y poppler-utils
RUN apt-get clean
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-xlib xvfb xserver-xephyr python3-tk python3-dev

# https://github.com/puppeteer/puppeteer/issues/5429
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install wget libcairo2-dev \
   libjpeg-dev libpango1.0-dev libgif-dev build-essential g++ libgl1-mesa-dev libxi-dev \
   libx11-dev pulseaudio udev

RUN apt update && apt install -y postgresql-server-dev-12

RUN curl --silent --location https://deb.nodesource.com/setup_14.x | bash - &&\
  apt-get -y -qq install nodejs

# Move this into requirements.txt at some time
RUN pip3 install pyautogui python-xlib PyVirtualDisplay

COPY . .

RUN apt-get install -y fonts-roboto fonts-ubuntu ttf-bitstream-vera fonts-crosextra-caladea fonts-cantarell fonts-open-sans

RUN npm install chrome-remote-interface

ENTRYPOINT ["python3", "-u", "immobilienscout24.py"]