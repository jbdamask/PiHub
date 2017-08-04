from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import threading


class DeviceScanner(threading.Thread):

    # Limit the number of ble devices per Pi
    _deviceLimit = 8
    _registeredDevices = {}

    def __init__(self):
        threading.Thread.__init__(self)
        self.scanner = Scanner(0)
        self.daemon = True

    def run(self):
        print "Starting scanner thread"
        while True:
            print "Scanning..."
            _devices = self.scanner.scan(10.0)
            _onlineDeviceAddresses = {}
            _counter = 0
            print "Iterating over devices..."
            for d in _devices:
                # If we're over the limit just stop
                while _counter < self._deviceLimit:
                    _onlineDeviceAddresses[d.addr] = ""
                    for (adtype, desc, value) in d.getScanData():
                        if value == "Adafruit Bluefruit LE":
                            print "Found Bluefruit with address: " + d.addr
                            # Check only to avoid unnecessary locking
                            if d.addr not in self._registeredDevices:
                                print d.addr + " is online!"
                                _onlineDeviceAddresses[d.addr] = ""
                                _counter += 1

            # Replace registered devices with ones that are currently online
            self._registeredDevices = _onlineDeviceAddresses

    def getDeviceLimit(self):
        return self._deviceLimit

    def getDevices(self):
        return self._registeredDevices