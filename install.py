#!/usr/bin/env python3

import os

user = os.environ.get('USER')
if user is None: user = "pi"

curpath = os.path.dirname(os.path.abspath(__file__))

os.system("sudo apt install git python3 python3-dev python3-pip python3-venv")
os.system("sudo apt install nmap")
os.system("""sudo apt-get install build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-numpy \
    zip""")

os.system("python3 -m venv '%s/slave_venv'" % curpath)

with open("%s/slave_init.sh" % curpath, "w") as f:
    f.write("""#!/bin/sh

. '%s/slave_venv/bin/activate'

# avoid to stuck raspberry cpus
export OPENBLAS_NUM_THREADS=1
export OPENBLAS_MAIN_FREE=1

cd '%s/slave'
python3 find_master.py

python3 main.py
""" % (curpath, curpath))

os.system("chmod +x '%s/slave_init.sh'" % curpath)

with open("%s/slave_service.service" % curpath, "w") as f:
    f.write("""[Unit]
Description=Human Firewall Slave Service

[Service]
Type=simple
# Another Type option: forking
User=%s
WorkingDirectory=/home/%s
ExecStart=%s/slave_init.sh
#Restart=on-failure
# Other Restart options: or always, on-abort, etc

[Install]
WantedBy=multi-user.target""" % (user, user, curpath))

if os.uname()[4][:3] == "arm":
    os.system(""". '%s/slave_venv/bin/activate' && pip install https://github.com/humanfirewall-iot19/dlib-builds/raw/master/dlib-19.17.99-cp35-cp35m-linux_armv7l.whl && \
pip install gpiozero && pip install picamera && pip install rpi.gpio""" % curpath)

    os.system("sudo systemctl enable '%s/slave_service.service'" % curpath)
else:
    os.system(""". '%s/slave_venv/bin/activate' && pip install https://github.com/humanfirewall-iot19/dlib-builds/raw/master/dlib-19.17.99-cp36-cp36m-linux_x86_64.whl && \
pip install opencv-python""" % curpath)

os.system(". '%s/slave_venv/bin/activate' && pip install -r requirements.txt" % curpath)

os.system("cd '%s' && git clone https://github.com/humanfirewall-iot19/slave" % curpath)

