from NotificationDelegate import NotificationDelegate
import json
import sys
import binascii

class BluefruitNotificationDelegate(NotificationDelegate):

    def __init__(self):
        # Initialize a list of devices
        self.bleDevices = []

    def notify(self, data):
        print("Received a call to update Bluefruit!")
        print data
       # newPayload = data #convert data to binary payload here (or string?)#
       # print json.dumps(data)
        payloadDict = json.loads(data)
#        deltaMessage = json.dumps(payloadDict["state"])
        # Get the list of device states to modify
        states = payloadDict["state"]["ble_devices"]
        print("Writing the payload to TX for all devices:")
        for blm in self.bleDevices:
            for s in states:
                if blm.addr == s["MAC"]:
          #          print s["MAC"] + " : " + s["color"]
                    try:
                        print("TX handle: " + str(blm.txh.getHandle()))
                        print("Trying to send color to device: " + s["color"])
                        print ("DEBUGGING: I turned off txCharacteristic.write")
                        colorString = json.dumps(s["color"])
                        # BluePy write expects a string that it will turn into hex.
                        # This class assumes a payload is already in hex so we transform back before writing
                        # See code for writeCharacteristic: https://github.com/IanHarvey/bluepy/blob/master/bluepy/btle.py
                        #  See https://github.com/IanHarvey/bluepy/issues/20
                        blm.txCharacteristic.write( binascii.unhexlify(colorString) )
                        print("     New color sent to device: " + s["MAC"])
                    except:
                        e = sys.exc_info()[0]
                        print("BluefruitMonitor Error on call to TX: %s" % e)
                        try:
                            self.p.disconnect()
                        except:
                            return 0


