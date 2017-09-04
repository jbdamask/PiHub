from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import binascii
from NotificationDelegate import NotificationDelegate
from datetime import datetime

class AWSIoTNotificationDelegate(NotificationDelegate):

    message = 0

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


    # JBD September 2017. Refactor hack. This class is passed to Blupepy for callbacks based
    # on the DefaultDelegate model. Since I've already made this a subclass of NotificationDelegate
    # and I don't want to make it dual-parent, simply adding a handleNotification() method should suffice
    # This will need to be cleaned up
    def handleNotification(self, cHandle, data):
        self.message = data
        self.notify(data)
        # print(str(datetime.now()) + " Notification from: " + self.deviceId)
        # print(binascii.b2a_hex(data))
        # self.notificationDelegate.notify(data)