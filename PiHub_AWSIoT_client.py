# -*- coding: utf-8 -*-
"""
Client that connects together AWS IoT with Bluefruit devices. Generally speaking,
this client attaches several bluetooth low energy (BLE) devices to a single internet-connected hub,
I'm using a Raspberry Pi 3. The upshot is that each BLE device acts as a controller to
all of the other BLE devices. Communication goes through AWS IoT so that other hubs connected to
other BLE devices can join in the fun


Author:
    John B Damask

Todo:


"""

from AWSIoTMQTTShadowClientGenerator import AWSIoTMQTTShadowClientGenerator
from BluefruitMonitor import BluefruitMonitor
from BLEDeviceScanner import DeviceScanner
from datetime import datetime
import threading
from AWSIoTNotificationDelegate import AWSIoTNotificationDelegate
from BluefruitNotificationDelegate import BluefruitNotificationDelegate


shadow = AWSIoTMQTTShadowClientGenerator("a2i4zihblrm3ge.iot.us-east-1.amazonaws.com",
                                         "/home/pi/PiHub/root-CA.crt",
                                         "/home/pi/PiHub/pi-ble-broker-1.cert.pem",
                                         "/home/pi/PiHub/pi-ble-broker-1.private.key",
                                         "pi-ble-broker-1",
                                         "pi",
                                         False
                                         )

# Device scanner object for its own thread
deviceScanner = DeviceScanner()
deviceScanner.start()
lock = threading.RLock()

# Set up a dictionary to track BluefruitMonitors
bleMonitors = {}

# Configure bluetooth notification delegate
blmNotificationDelegate = BluefruitNotificationDelegate()

# Pass it to the shadow so the deviceShadow can call it
shadow.registerNotificationDelegate(blmNotificationDelegate)

# Loop forever
while True:
    with lock:
        registeredDevices = deviceScanner.getDevices().keys()
    for k in registeredDevices:
        if k not in bleMonitors:
            with lock:
                shadow.registerDeviceAddress(k)
            blm = BluefruitMonitor(k, AWSIoTNotificationDelegate(k, shadow))
            if(blm is None):
                print(str(datetime.now()) + " Failed to connect to device. Will try again")
                continue
            blmNotificationDelegate.bleDevices.append(blm)
            bleMonitors[k] = blm
            print "Starting thread for device: " + blm.addr
            if blm.start() == 0:
                deviceScanner.removeDevice(k)
    blms = bleMonitors.keys()
    for b in blms:
        if b not in registeredDevices:
            del bleMonitors[b]