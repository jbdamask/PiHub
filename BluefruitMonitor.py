from bluepy.btle import DefaultDelegate, Peripheral, BTLEException
import binascii
from datetime import datetime
import threading
import sys



class BluefruitDelegate(DefaultDelegate):

    message = 0

    # Constructor. Takes the RX handle, the MAC address of the Peripheral and a NotificationDelegate
    def __init__(self, handle, addr, notificationDelgate):
        print addr + ": Creating BluefruitDelegate"
        DefaultDelegate.__init__(self)
        self.hndl=handle
        self.addr=addr
        self.notificationDelegate=notificationDelgate

    def handleNotification(self, cHandle, data):    
        self.message = data
        print(str(datetime.now()) + " Notification from: " + self.addr)
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
        self.daemon = True
        self.addr = mac
        try:
            self.p = Peripheral(mac, "random")
            self.notificationDelgate = notificationDelgate
            print("New BluefruitMonitor created for device: " + self.p.addr)
        except:
            print "Not connected"
            return None

    #def startMonitor(self):
    def run(self):
        print self.addr + ": In run method for BluefruitMonitor"
        try:
            self.rxh = self.p.getCharacteristics(uuid=self.rxUUID)[0]
        except AttributeError as a:
            print(str(datetime.now()) + " AttributeError: " + a.message)
            print(str(datetime.now()) + " Will try to connect to Peripheral...")
            try:
                self.p = Peripheral(self.addr, "random")
                self.notificationDelgate = self.notificationDelgate
                print(str(datetime.now()) + " Peripheral connected successfully!")
                self.rxh = self.p.getCharacteristics(uuid=self.rxUUID)[0]
            except BTLEException as e:
                print(str(datetime.now()) + " BTLEException: " + e.message)
                return 0
            except:
                e2 = e = sys.exc_info()[0]
                print(str(datetime.now()) + " BluefruitMonitor Error on call to TX: %s" % e.message)
                return 0
        except:
            e = sys.exc_info()[0]
            print(str(datetime.now()) + " BluefruitMonitor Error on call to TX: %s" % e)
            return 0


        self.txCharacteristic = self.p.getCharacteristics(uuid=self.txUUID)[0]
        print("RX handle: " + str(self.rxh.getHandle()))
        # Note setDelegate method has been replaced by withDelegate. Change this
        self.p.setDelegate(BluefruitDelegate(self.rxh.getHandle(), self.addr, self.notificationDelgate))
        try:
            # Turn on notifications. If 35 isn't your handle run hcidump in one window, bluetoothctl in another
            # then connect, select-atrribute for RX then set "notify on". 
            # Inspect the hcidump log for the handle associated with "Write req" 
            print "Configuring RX to notify me on change"
            self.p.writeCharacteristic(35, b"\x01\x00", withResponse=True)
            self.monitor = "ON"
            #return 0
        except:
            e = sys.exc_info()[0]
            print("BluefruitMonitor Error: %s" % e)
            try:
                self.p.disconnect()
            except:
                return 0
        while True:
            try:
                if self.p.waitForNotifications(1):
                    msg = self.p.delegate.getLastMessage()
                    if msg != 0 and msg is not None:
                        self.txCharacteristic.write(msg)
                        self.clearMessage()
            except BTLEException:
                print BTLEException.message
                return 0
                # Add callback to remove device


    def clearMessage(self):
        self.p.delegate.clearMessage()

    def stopMonitor(self):
        self.monitor="OFF"
        self.p.writeCharacteristic(35, '\x00', withResponse=False)

    # Trying some error handling...dunno if it will work
    def reconnect(self):
        try:
            self.p.connect(self.addr, "random")
        except:
            print BTLEException.message
            return 0