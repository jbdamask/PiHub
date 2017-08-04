from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import binascii
from NotificationDelegate import NotificationDelegate

class AWSIoTNotificationDelegate(NotificationDelegate):


    def __init__(self, deviceId, deviceShadowInstance):
        self.deviceId = deviceId
        self.deviceShadowInstance = deviceShadowInstance
        print("Created an AWSIoTNotificationDelegate for " + self.deviceId)

    def notify(self, data):
        print("Received a call to update the shadow!")
        print("Current state: " + self.deviceShadowInstance.getState())
        print("Request to update the reported state...")
        #newPayload = '{"state":{"reported":' + binascii.b2a_hex(data) + '}}'
        _s = self.deviceShadowInstance.updateState(binascii.b2a_hex(data))
        print("New state: " + _s)
        self.deviceShadowInstance.shadowUpdate(_s, None, 5)
        #self.notificationInstance.notify(newPayload)
        print("Sent.")

