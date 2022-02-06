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

RUN apt-get install -y fonts-roboto fonts-ubuntu ttf-bitstream-vera fonts-crosextra-caladea fonts-cantarell fonts-open-sans ttf-wqy-zenhei

# install debs error if combine together
RUN apt install -y --no-install-recommends --allow-unauthenticated x11vnc fluxbox xxd \
    && apt autoclean -y \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*


RUN apt-get update -y && apt install -y iptables sudo

# RUN npm install chrome-remote-interface

COPY . .

# https://dev.to/emmanuelnk/using-sudo-without-password-prompt-as-non-root-docker-user-52bg
# Create new user `docker` and disable 
# password and gecos for later
# --gecos explained well here:
# https://askubuntu.com/a/1195288/635348
RUN adduser --force-badname --disabled-password --gecos '' browserUser

# Add a user to run the browser as non-root
RUN mkdir -p /home/browserUser/Downloads \
  && chown -R browserUser:browserUser /home/browserUser

RUN adduser browserUser sudo

# Ensure sudo group users are not 
# asked for a password when using 
# sudo command by ammending sudoers file
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> \
/etc/sudoers

RUN chmod 755 start.sh

# Run everything after as non-privileged user.
USER browserUser

# Application specific environment variables
# disp = Display(visible=True, size=(1920, 1080), backend="xvfb", use_xauth=True); disp.start()
# set's DISPLAY=:1
ENV DISPLAY=:1
# By default, only screen 0 exists and has the dimensions 1280x1024x8
ENV XVFB_WHD=1920x1080x24
# x11vnc password
ENV X11VNC_PASSWORD=test
# This variable tells our source code that its invoked within a Docker container
ENV DOCKER=1

ENTRYPOINT [ "./start.sh" ]