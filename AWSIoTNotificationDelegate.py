from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import binascii
from NotificationDelegate import NotificationDelegate
from datetime import datetime

class AWSIoTNotificationDelegate(NotificationDelegate):


    def __init__(self, deviceId, deviceShadowInstance):
        self.deviceId = deviceId
        self.deviceShadowInstance = deviceShadowInstance
        print("Created an AWSIoTNotificationDelegate for " + self.deviceId)

    def notify(self, data):
        print(str(datetime.now()) + " Received a call to update the shadow!")
        d = { "MAC": self.deviceId, "color": binascii.b2a_hex(data)}
        _s = self.deviceShadowInstance.updateState(d)
        self.deviceShadowInstance.deviceShadowHandler.shadowUpdate(_s, None, 5)
        print(str(datetime.now()) + " Sent to deviceShadowHandler")

