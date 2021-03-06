# -*- coding: utf-8 -*-
"""
Use this class in its own thread to constantly scan for Adafruit devices.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Todo:
    * Major problem here...once Peripheral is connected it doesn't advertise and
        won't show up in a scan
    * Externalize device type so we can search for different stuff

"""
from bluepy.btle import Scanner, BTLEException
import threading
import time
import json


class DeviceScanner(threading.Thread):

    # Limit the number of ble devices per Pi
    _deviceLimit = 8
    _waitBeforeUnregisteringDevice = 30
    # Devices tracked by this class
    _registeredDevices = {}
    # Devices that are registered but no longer online
    _probationDevices = {}
    _deviceNamesToFind = { "Adafruit Bluefruit LE": "" }

    lock = threading.RLock()

    def __init__(self):
        threading.Thread.__init__(self)
        self.scanner = Scanner(0).withDelegate(ScanDelegate())
        self.daemon = True

    def run(self):
        print "Starting scanner thread"
        while True:
           # print "Scanning..."
            try:
                _devices = self.scanner.scan(10.0)
            except BTLEException:
                continue
            _onlineDeviceAddresses = {}
            #_counter = 0
          #  print "Iterating over devices..."
            for d in _devices:
                # If we're over the limit just stop
                #if _counter < self._deviceLimit:
                #    print _counter
                for (adtype, desc, value) in d.getScanData():
                    if value in self._deviceNamesToFind.keys():
                        _onlineDeviceAddresses[d.addr] = ""

            # Replace registered devices with ones that are currently online
            # Remove devices we can't see anymore
            with self.lock:
                # Add devices we can (provided there's still space)
                for n in _onlineDeviceAddresses:
                    if (n not in self._registeredDevices) and (len(self._registeredDevices) < self._deviceLimit):
                        self._registeredDevices[n] = ""
                    elif (n in self._registeredDevices):
                        # If it's already registered but appears again it must have disconnected. Remove so we can reconnect
                        self.removeDevice(n)

        time.sleep(2)

    def getDeviceLimit(self):
        return self._deviceLimit

    def getDevices(self):
        return self._registeredDevices

    def removeDevice(self, devId):
        with self.lock:
            del self._registeredDevices[devId]


