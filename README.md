# PiHub

Connecting multiple Bluetooth Low Energy (BLE) devices to the same Raspberry Pi and communicating via AWS IoT.

This initial version uses the Pi as a communication hub between local BLE devices; an event on one will produce an effect on another. Each BLE device is a producer and consumer of events, which mean they can all control each other. 

The benefit of using IoT is that multiple Pis can connect over the internet and each Pi can be connected to multiple BLE devices. Effectively, this lets BLE devices control each other without being connected to the internet themselves. 

## Getting Started

Just starting this project. There are no diagrams, build scripts, requirements.txt or anything that would make it real. As such, installation and getting things working is manual. But that's ok as it's just a home project (for now) ;-)

### Prerequisites

This is more about my setup - some of the hardware can be swapped but I'm not at the point of generalizing 

Raspberry Pi 3 (others may work but I've only tested on a Pi 3)
BluePy
* BlueZ - I'm using 5.46 but an earlier one will do (just not the one that comes with Raspbian)
AWSIoTPythonSDK

Certificates for your Pi - follow AWS IoT tutorial for configuring a device. These should be placed in the same directory as this code.

Bluetooth Low Engergy devices, etc
Adafruit: 
* [Feather Bluefruit 32u4](https://www.adafruit.com/product/2829)
* [NeoPixels](https://www.adafruit.com/product/1376)
* [MPR121 capacitive touch breakout](https://www.adafruit.com/product/1982)
[Arduino IDE](https://www.arduino.cc/en/Main/OldSoftwareReleases)

Install code from [Bluefruit_LE_tx_rx](https://github.com/jbdamask/Adafruit/tree/master/Bluefruit_LE_tx_rx)

### Installing on Raspberry Pi3

Starting with a fresh install of Raspbian, install a newer version of BlueZ using [Martijn Kieboom's Ansible script](https://github.com/mkieboom/raspberrypi-bluez). Note - modify main.yml to install the desired version of BlueZ, e.g.

```
$ sudo su -
$ cd raspberrypi-bluez/roles/bluetooth/tasks
$ sed -ie 's|bluez-5.41|bluez-5.46|g’ main.yml
$ ansible-playbook -i myhosts/raspberrypi_localhost raspberrypi-deployment.yml --connection=local
```

Install BluePy and AWSIoTPython SDK (I installed from source but consider using pip install).

```
$ cd ~
$ git clone <this repo>
```
Edit scratch.py to in include the MAC addresses of you Feather Bluefruit boards (hardcoded for two right now but I'll change this to dynamic scanning/selection in a future version).

Copy your AWS IoT certificates (and root cert) into the newly created PiHub folder.

Execute:
```
$ python scratch.py
```
If things work well, you'll see the little blue LED on your Feathers light up and the console will tell you the Pi is listening.


## Running the tests

Yea no unit tests. Sue me

## Contributing

nothing yet

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

This isn't production-grade code.

## Authors

* **John B Damask** - *Initial work* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Adafruit
* Ian Harvey
* Arduino
