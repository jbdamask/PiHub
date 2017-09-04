# DEPRECATED
# This class was never used anyway. Blow it away in next push
# September 2017 - JBD

from BluefruitUARTNotificationDelegate import BluefruitUARTNotificationDelegate
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