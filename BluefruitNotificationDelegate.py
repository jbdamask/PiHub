from NotificationDelegate import NotificationDelegate
import json


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
                    print s["MAC"] + " : " + s["color"]
                    blm.txh.write(s["color"])
                    print("     New color sent to device: " + s["MAC"])


