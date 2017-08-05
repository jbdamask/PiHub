from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import binascii
from datetime import datetime
import threading
import sys



class BluefruitDelegate(DefaultDelegate):

    message = 0

    # Constructor. Takes the RX handle, the MAC address of the Peripheral and a NotificationDelegate
    def __init__(self, handle, addr, notificationDelgate):
        DefaultDelegate.__init__(self)
        self.hndl=handle
        self.addr=addr
        self.notificationDelegate=notificationDelgate

    def handleNotification(self, cHandle, data):    
        self.message = data
        print("Notification from: " + self.addr)
        print( str(datetime.now()) )        
        print(binascii.b2a_hex(data))
        self.notificationDelegate.notify(data)


    def getLastMessage(self):
        return self.message

    def clearMessage(self):
        self.message = 0


class BluefruitMonitor(threading.Thread):

    monitor = "OFF"
    txUUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
    rxUUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    def __init__(self, mac, notificationDelgate):
        threading.Thread.__init__(self)
        try:
            self.p = Peripheral(mac, "random")
            self.notificationDelgate = notificationDelgate
            print("New BluefruitMonitor created for device: " + self.p.addr)
        except:
            print "Not connected"
            return None

    #def startMonitor(self):
    def run(self):
        self.rxh = self.p.getCharacteristics(uuid=self.rxUUID)[0]
        self.txh = self.p.getCharacteristics(uuid=self.txUUID)[0]
        print("RX handle: " + str(self.rxh.getHandle()))
        # Note setDelegate method has been replaced by withDelegate. Change this
        self.p.setDelegate(BluefruitDelegate(self.rxh.getHandle(), self.p.addr, self.notificationDelgate))
        try:
            # Turn on notifications. If 35 isn't your handle run hcidump in one window, bluetoothctl in another
            # then connect, select-atrribute for RX then set "notify on". 
            # Inspect the hcidump log for the handle associated with "Write req" 
            print(self.p.writeCharacteristic(35, b"\x01\x00", withResponse=True))
            self.monitor = "ON"
            return 0
        except:
            e = sys.exc_info()[0]
            print("BluefruitMonitor Error: %s" % e)
            try:
                self.p.disconnect()
            except:
                return 0
        while True:
            if self.p.waitForNotifications(1):
                msg = self.p.delegate.getLastMessage()
                if msg != 0 and msg is not None:
                    self.txh.write(msg)
                    self.clearMessage()

#    def getLastMessage(self):
#         try:
#             self.p.waitForNotifications(1.0)
#             return self.p.delegate.getLastMessage()
#         except:
#             #return 0
#             return

    def clearMessage(self):
        self.p.delegate.clearMessage()

    def stopMonitor(self):
        self.monitor="OFF"
        self.p.writeCharacteristic(35, '\x00', withResponse=False)