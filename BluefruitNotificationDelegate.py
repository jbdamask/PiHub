from NotificationDelegate import NotificationDelegate
import json


class BluefruitNotificationDelegate(NotificationDelegate):

    def __init__(self):
        # Initialize a list of devices
        self.bleDevices = []

    def notify(self, data):
        print("Received a call to update Bluefruit!")      
        print("Write the payload to TX...")
       # newPayload = data #convert data to binary payload here (or string?)#
       # print json.dumps(data)
        payload = json.loads(d["payload"])["state"]["ble_devices"]
        for blm in self.bleDevices:
            for d in payload:
                if blm.addr == d["MAC"]:
                    blm.txh.write(d["color"])
                    print("New color sent to device: " + d["MAC"])


