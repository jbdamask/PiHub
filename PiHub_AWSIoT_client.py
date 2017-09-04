# -*- coding: utf-8 -*-
"""
Client that connects together AWS IoT with Bluefruit devices. Generally speaking,
this client attaches several bluetooth low energy (BLE) devices to a single internet-connected hub,
I'm using a Raspberry Pi 3. The upshot is that each BLE device acts as a controller to
all of the other BLE devices. Communication goes through AWS IoT so that other hubs connected to
other BLE devices can join in the fun


Author:
    John B Damask

Synopsis:
    sudo python PiHub_AWSIoT_client

Todo:
    Externalize shadow connection information (right now it's connecting to my device
    Buggy BLE stuff. Mis-connects and disconnects

"""

from AWSIoTMQTTShadowClientGenerator import AWSIoTMQTTShadowClientGenerator
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException
from BluefruitMonitor import BluefruitMonitor
from BLEDeviceScanner import DeviceScanner
from datetime import datetime
import threading
import sys
from AWSIoTNotificationDelegate import AWSIoTNotificationDelegate
from BluefruitNotificationDelegate import BluefruitNotificationDelegate


class BleNotificationThread (threading.Thread):
    # Currently only tx, rx and NOTIFY are supported
    rxUUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
    txUUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

    def __init__(self, peripheral_addr, deviceShadow):
        threading.Thread.__init__(self)
        self.peripheral_addr = peripheral_addr
        self.shadow = deviceShadow

    def run(self):
        peripheral = peripherals[self.peripheral_addr]
        try:
            peripheral.setDelegate(AWSIoTNotificationDelegate(self.peripheral_addr))
            self.rxh = peripheral.getCharacteristics(uuid=self.rxUUID)[0]
            print "Configuring RX to notify me on change"
            peripheral.writeCharacteristic(35, b"\x01\x00", withResponse=True)
            while True:
                if peripheral.waitForNotifications(1):
                    pass

        except BTLEException:
            print BTLEException.message


shadow = AWSIoTMQTTShadowClientGenerator("a2i4zihblrm3ge.iot.us-east-1.amazonaws.com",
                                         "/home/pi/PiHub/root-CA.crt",
                                         "/home/pi/PiHub/pi-ble-broker-1.cert.pem",
                                         "/home/pi/PiHub/pi-ble-broker-1.private.key",
                                         "pi-ble-broker-1",
                                         "pi",
                                         False
                                         )

_deviceNamesToFind = { "Adafruit Bluefruit LE": "" }
peripherals = {}
scanner = Scanner(0)

# Device scanner object for its own thread
#deviceScanner = DeviceScanner()
#deviceScanner.start()
#lock = threading.RLock()

# Set up a dictionary to track BluefruitMonitors
#bleMonitors = {}

# Configure bluetooth notification delegate
blmNotificationDelegate = BluefruitNotificationDelegate()

# Pass it to the shadow so the deviceShadow can call it
shadow.registerNotificationDelegate(blmNotificationDelegate)

while True:
    print str(peripherals.__len__()) + " connected devices"
    print 'Scanning...'
    devices = scanner.scan(2)
    for d in devices:
        try:
            # If scan returns a known addr that's already in the collection, it means it disconnected
            # Remove record and treat it as new
            # Note, it would be nice to remove a device when it goes offline as opposed to when it comes back
            # To do this I'd need something like a ping...dunno what best practice is
            if d.addr in peripherals:
                del peripherals[d.addr]

            for (adtype, desc, value) in d.getScanData():
                if value in _deviceNamesToFind.keys():
                    try:
                        p = Peripheral(d)
                        print "Created Peripheral object for device: " + d.addr
                      #  p.setDelegate(AWSIoTNotificationDelegate(d.addr, shadow))
                    except BTLEException:
                        print BTLEException.message
                        break
                    peripherals[d.addr] = p
                    t = BleNotificationThread(d.addr, shadow)
                    t.start()
        except:
            print sys.exc_info()[0]

# Loop forever
# while True:
#     with lock:
#         registeredDevices = deviceScanner.getDevices().keys()
#     for k in registeredDevices:
#         if k not in bleMonitors:
#             with lock:
#                 shadow.registerDeviceAddress(k)
#             blm = BluefruitMonitor(k, AWSIoTNotificationDelegate(k, shadow))
#             if(blm is None):
#                 print(str(datetime.now()) + " Failed to connect to device. Will try again")
#                 continue
#             blmNotificationDelegate.bleDevices.append(blm)
#             bleMonitors[k] = blm
#             print "Starting thread for device: " + blm.addr
#             if blm.start() == 0:
#                 deviceScanner.removeDevice(k)
#     blms = bleMonitors.keys()
#     for b in blms:
#         if b not in registeredDevices:
#             del bleMonitors[b]