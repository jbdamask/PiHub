from BluefruitMonitor import BluefruitMonitor
from NotificationDelegate import NotificationDelegate


class BluefruitNotificationDelegate(NotificationDelegate):

    def __init__(self):
        pass

    def notify(self, data):
        print("Received a call to update Bluefruit!")      
        print("Write the payload to TX...")
        newPayload = data #convert data to binary payload here (or string?)#
        self.bluefruitMonitor.txh.write(newPayload)
        #self.notificationInstance.notify(newPayload)
        print("Sent.")


