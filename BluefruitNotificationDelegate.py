from NotificationDelegate import NotificationDelegate
import json
import sys

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
                        print ("DEBUGGING: I turned off txh.write")
                        colorString = json.dumps(s["color"])
                        # BluePy write takes a string. See https://github.com/IanHarvey/bluepy/issues/20
                        blm.txh.write(colorString.encode('utf-8'))
                        print("     New color sent to device: " + s["MAC"])
                    except:
                        e = sys.exc_info()[0]
                        print("BluefruitMonitor Error on call to TX: %s" % e)
                        try:
                            self.p.disconnect()
                        except:
                            return 0


