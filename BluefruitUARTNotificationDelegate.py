from NotificationDelegate import NotificationDelegate
import json
import sys
import binascii
from bluepy.btle import BTLEException
from datetime import datetime

class BluefruitUARTNotificationDelegate(NotificationDelegate):

    # This class writes to UART.TX characteristic
    txUUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

    def __init__(self):
        # Initialize a list of devices
        self.peripherals = []

    def notify(self, data):
        print(str(datetime.now()) + " Received a call to update Bluefruit!")
        print data
       # newPayload = data #convert data to binary payload here (or string?)#
       # print json.dumps(data)
        payloadDict = json.loads(data)
#        deltaMessage = json.dumps(payloadDict["state"])
        # Get the list of device states to modify
        states = payloadDict["state"]["ble_devices"]
        print(str(datetime.now()) + " Writing the payload to TX for all devices:")
        for p in self.peripherals:
            for s in states:
                if p.addr == s["MAC"]:
                    print(str(datetime.now()) + " Send color to device: " + s["color"])
                    colorString = s["color"]
                    # BluePy write expects a string that it will turn into hex.
                    # This class assumes a payload is already in hex so we transform back before writing
                    # See code for writeCharacteristic: https://github.com/IanHarvey/bluepy/blob/master/bluepy/btle.py
                    #  See https://github.com/IanHarvey/bluepy/issues/20
                    print 'New color: ' + colorString
                    try:
                        #blm.txCharacteristic.write( binascii.unhexlify(colorString), True )
                        # The TX characteristic will be same for all Peripherals (at least i think so...YMMV)
                        tx = p.getCharacteristics(uuid=self.txUUID)[0]
                        tx.write( binascii.unhexlify(colorString), True )
                        print(str(datetime.now()) + " New color sent to device: " + s["MAC"])
                    except BTLEException as e:
                        print(str(datetime.now()) + " BTLEException: " + e.message)
                        print(str(datetime.now()) + " Will try to reconnect...")
                        try:
                            p.reconnect()
#                            p.txCharacteristic.write(binascii.unhexlify(colorString), True)
                            tx = p.getCharacteristics(uuid=self.txUUID)[0]
                            tx.write( binascii.unhexlify(colorString), True )
                            print(str(datetime.now()) + " Reconnect successful!")
                            print(str(datetime.now()) + " New color sent to device: " + s["MAC"])
                        except BTLEException as e2:
                            print(str(datetime.now()) + " BTLException: " + e.message)
                            print(str(datetime.now()) + " Reconnect failed. Sorry")
                        except:
                            e2 = e = sys.exc_info()[0]
                            print(str(datetime.now()) + " BluefruitMonitor Error on call to TX: %s" % e)
                    except:
                        e = sys.exc_info()[0]
                        print(str(datetime.now()) + " BluefruitMonitor Error on call to TX: %s" % e)
                        try:
                            self.p.disconnect()
                        except:
                            return 0


