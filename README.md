# rvr

A Python3 package for the Sphero RVR.

_Please note: this code is still in the middle of the development process!_

[![GitHub issues](https://img.shields.io/github/issues/markusk/rvr)](https://github.com/markusk/rvr/issues) [![GitHub stars](https://img.shields.io/github/stars/markusk/rvr)](https://github.com/markusk/rvr/stargazers) [![GitHub license](https://img.shields.io/github/license/markusk/rvr)](https://github.com/markusk/rvr/blob/master/LICENSE)

---

## Step 1: OS Setup

- Install Ubuntu Mate on your Raspberry Pi ([Instruction](https://ubuntu-mate.org/download/)).
- Enable SSH (explanation see [here](https://askubuntu.com/questions/626372/could-not-load-host-key-etc-ssh-ssh-host-ed25519-key-in-var-log-auth-log/649782)):

```bash
sudo ssh-keygen -A
```

- Start ssh:

```bash
sudo systemctl restart ssh.service
```

#### Setup the Raspbery Pi serial port

```bash
sudo raspi-config
```

Choose:

- Interfacing Options
- P5 Serial
- No (No Login shell over serial port)
- Yes (Enable serial port hardware)

Do _not_ reboot now!

- Change /boot/cmdline.txt file regarding tty-entries to this (credits to [richard_mark](https://ubuntu-mate.community/t/writing-to-the-serial-port-gpio-tx-rx/4632/3)):

[...] console=tty1 [...]

```bash
sudo nano /boot/cmdline.txt
```

- Add your user to the dialout group:

```bash
sudo gpasswd --add ${USER} dialout
```

- Now reboot the Raspberry Pi!

## Step 2: Joystick/Gamepad OS support

```bash
sudo apt-get install joystick
```

### Microsoft XBOX Wireless Controller

- Supported by the Kernel - if used with the USB connector.

### Gamepad/Joystick test

- Connect a Gamepad to the Pi, start the following command and press any buttons or move some axes:

```bash
jstest --normal /dev/input/js0
```

## Step 3: Create a central place for this repository

- Create your own development directory "develop"

```bash
mkdir ~/develop
cd ~/develop
```

- Clone this repository

```bash
git clone https://github.com/markusk/rvr.git
```

## Step 4: Setup Sphero Public SDK

### Long version

- Setup SDK with method 2: [Instructions](https://sdk.sphero.com/docs/getting_started/raspberry_pi/raspberry_pi_setup/#using-git)

### Short version

- _Without_ [pipenv](https://github.com/pypa/pipenv):

```bash
pip3 install aiohttp pyserial_asyncio
cd ~/develop
git clone https://github.com/sphero-inc/sphero-sdk-raspberrypi-python
```

### Make the Sphero Public SDK accessible

- Create symbolic link, pointing to the 'sphero_sdk' folder:

```bash
ln -s ~/develop/sphero-sdk-raspberrypi-python/sphero_sdk/ ~/develop/rvr/lib/
```

#### Turn on the RVR and test the SDK

- Start the test program:

```bash
cd ~/.../test
./test.py
```

- The output should look something like this:

```bash
Checking RVR firmware versions...
Checking CMS firmware versions...
Firmware check complete.
Battery percentage:  90 %
Voltage state:  1
Voltage states:  [unknown: 0, ok: 1, low: 2, critical: 3]
```

_Note: The firmware check seems to pop up from time to time._

## Step 5: Run XXX



## _**to do:**_ Step 6: Setting up some code for autostart

### systemd under Ubuntu

```bash
sudo cp raspi/etc__systemd__system__rvr-ros-start.service /etc/systemd/system/rvr-ros-start.service
sudo systemctl daemon-reload
sudo systemctl start rvr-ros-start.service
sudo systemctl enable rvr-ros-start.service
```
