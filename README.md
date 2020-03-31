# rvr

A ROS Python package for the Sphero RVR.

_Please note: this code is still in the middle of the development process!_

[![GitHub issues](https://img.shields.io/github/issues/markusk/rvr)](https://github.com/markusk/rvr/issues) [![GitHub stars](https://img.shields.io/github/stars/markusk/rvr)](https://github.com/markusk/rvr/stargazers) [![GitHub license](https://img.shields.io/github/license/markusk/rvr)](https://github.com/markusk/rvr/blob/master/LICENSE)

---

## Step 1: OS Setup

- Install Ubuntu Mate on your Raspberry Pi ([Instruction](https://ubuntu-mate.org/download/))
- Install ROS on your Ubuntu Mate ([Instruction](http://wiki.ros.org/melodic/Installation/Ubuntu/))

- Enable SSH (explanation see [here](https://askubuntu.com/questions/626372/could-not-load-host-key-etc-ssh-ssh-host-ed25519-key-in-var-log-auth-log/649782)):

```bash
sudo ssh-keygen -A
```

- Start ssh

```bash
sudo systemctl restart ssh.service
```

#### Setup Raspbery Pi

sudo raspi-config

Choose:
- Interfacing Options
- P5 Serial
- No (No Login shell over serial port)
- Yes (Enable serial port hardware)
Reboot your Raspberry Pi


## Step 2: Joystick/Gamepad OS support

```bash
sudo apt-get install joystick
```

### Microsoft XBOX Wireless Controller

Supported by the Kernel - if used with the USB connector.

### Gamepad/Joystick test

```bash
jstest --normal /dev/input/js0
```

## Step 3: ROS Setup

- Install ROS

```bash
sudo apt-get install ros-melodic-ros-base
```

- Install ROS packages

```bash
sudo apt-get install ros-melodic-urg-node ros-melodic-teleop-twist-keyboard joystick ros-melodic-joystick-drivers ros-melodic-teleop-twist-joy
```

- create your own development directory "develop"

```bash
mkdir ~/develop
cd ~/develop
```

- clone this repository

```bash
git clone https://github.com/markusk/rvr.git
```

- Create a catkin workspace without 'src' folder:

```bash
mkdir ~/catkin_ws
cd ~/catkin_ws
```

- Create symbolic link with the name 'src', pointing to the 'src' folder in the ROS directory from this repository:

```bash
ln -s /home/$USERNAME/develop/rvr/ROS/catkin_workspace/src/ src
catkin_make
```

## Step 4: ROS Python support

```bash
sudo apt install python-rosinstall python-rosinstall-generator python-wstool build-essential
```

## Step 5: Setup Sphero Public SDK

#### Long version
- Setup SDK with method 2: [Instructions](https://sdk.sphero.com/docs/getting_started/raspberry_pi/raspberry_pi_setup/#using-git)

#### Short version
- _Without_ [pipenv](https://github.com/pypa/pipenv):
```bash
pip3 install aiohttp pyserial_asyncio
cd ~/develop
git clone https://github.com/sphero-inc/sphero-sdk-raspberrypi-python
```

#### ~~"Fix" the serial port path and~~ Give yourself permission for the serial port

- Test SDK / Connection to RVR

Turn on the RVR and run on of the provided examples:

```bash
cd ~/develop/sphero-sdk-raspberrypi-python/getting_started/asyncio/leds/
python3 set_single_led.py
```
All RVR LEDs should glow now!


## Step 6: Run ROS

### The main launch file

On the robot (Raspberry Pi):

```bash
roslaunch rvr rvr.launch
```

On another computer (the ground control center):

```bash
export ROS_MASTER_URI=http://<hostname>:11311
rosparam set joy_node/dev "/dev/input/js1"
roslaunch rvr ground_control_center.launch
```

## _**to do:**_ Step 6: Setting up ROS for autostart

### systemd under Ubuntu

```bash
sudo cp raspi/etc__systemd__system__rvr-ros-start.service /etc/systemd/system/rvr-ros-start.service
sudo systemctl daemon-reload
sudo systemctl start rvr-ros-start.service
sudo systemctl enable rvr-ros-start.service
```

---

## The ROS launch files

### K

#### keyboard_control_test

Listens to a teleop_twist_keyboard node and prints out the data/messages. Uses:

- _teleop_twist_keyboard_
- _nodes/keyboard_listener.py_

### M

#### motor_server

Controls the motors on the robot. Uses:

- _motor_server.py_

### R

#### rvr

Controls the whole robot. To be started on the robot. Uses:

- _motor_server.py_
_**to do:**_
- _tf_broadcaster.py_
- _battery_publisher.py_
- _imu_bno055.py_
- _base_controller.py_
- _minibot_camera_
- _urg_node_
