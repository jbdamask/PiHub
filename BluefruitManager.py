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
    * Externalize device type so we can search for different stuff

"""

from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException
import threading
import time


class DeviceScanner(threading.Thread):

    # Limit the number of ble devices per Pi
    _deviceLimit = 8
    _registeredDevices = {}
    _deviceNamesToFind = { "Adafruit Bluefruit LE": "" }

    lock = threading.RLock()

    def __init__(self):
        threading.Thread.__init__(self)
        self.scanner = Scanner(0)
        self.daemon = True

    def run(self):
        print "Starting scanner thread"
        while True:
            print "Scanning..."
            try:
                _devices = self.scanner.scan(10.0)
            except BTLEException:
                continue
            _onlineDeviceAddresses = {}
            #_counter = 0
            print "Iterating over devices..."
            for d in _devices:
                # If we're over the limit just stop
                #if _counter < self._deviceLimit:
                #    print _counter
                for (adtype, desc, value) in d.getScanData():
                    if value in self._deviceNamesToFind.keys():
                        print "Found Bluefruit with address: " + d.addr
                        _onlineDeviceAddresses[d.addr] = ""
                            # Check only to avoid unnecessary locking
                            #if d.addr not in self._registeredDevices:
                            #    print d.addr + " is online!"
                                #_onlineDeviceAddresses[d.addr] = ""
                                #_counter += 1
                            #_counter += 1

            # Replace registered devices with ones that are currently online
            # Remove devices we can't see
            with self.lock:
                for r in self._registeredDevices.keys():
                    if r not in _onlineDeviceAddresses:
                        del self._registeredDevices[r]
                # Add devices we can (provided there's still space)
                for n in _onlineDeviceAddresses:
                    if (n not in self._registeredDevices) and (len(self._registeredDevices) < self._deviceLimit):
                        self._registeredDevices[n] = ""

        time.sleep(2)

    def getDeviceLimit(self):
        return self._deviceLimit

    def getDevices(self):
        return self._registeredDevices