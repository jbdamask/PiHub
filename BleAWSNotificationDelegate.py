from BluefruitNotificationDelegate import BluefruitNotificationDelegate
from AWSIoTNotificationDelegate import AWSIoTNotificationDelegate

class BleAWSNotificationDelegate:

	bleNDDict = dict()

	def __init__(self):
		self.iotND = AWSIoTNotificationDelegate()
        
	def notify(self, data):
		for key in self.bleNDDict:
			key.notify(data)
		self.iotND.notify(data)

	def addBleNd(self, id):
		self.bleNDDict[id] = BluefruitNotificationDelgate()