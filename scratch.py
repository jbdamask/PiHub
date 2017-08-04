from AWSIoTMQTTShadowClientGenerator import AWSIoTMQTTShadowClientGenerator, ShadowCallbackContainer
from bluepy.btle import Scanner, DefaultDelegate, Peripheral
from BluefruitMonitor import BluefruitMonitor
import time
from AWSIoTNotificationDelegate import AWSIoTNotificationDelegate


shadow = AWSIoTMQTTShadowClientGenerator("a2i4zihblrm3ge.iot.us-east-1.amazonaws.com",
                                         "/home/pi/PiHub/root-CA.crt",
                                         "/home/pi/PiHub/pi-ble-broker-1.cert.pem",
                                         "/home/pi/PiHub/pi-ble-broker-1.private.key",
                                         "pi-ble-broker-1",
                                         "pi",
                                         False
                                         )

blm1 = BluefruitMonitor("E0:F2:72:20:15:43", AWSIoTNotificationDelegate("E0:F2:72:20:15:43", shadow))
blm1.startMonitor()
blm2 = BluefruitMonitor("FB:E4:1D:F1:22:96", AWSIoTNotificationDelegate("FB:E4:1D:F1:22:96", shadow))
blm2.startMonitor()

shadow.registerDeviceAddress("E0:F2:72:20:15:43")
shadow.registerDeviceAddress("FB:E4:1D:F1:22:96")

# Loop forever
while True:
    blm1Msg = blm1.getLastMessage()
    if blm1Msg != 0 and blm1Msg is not None:
        print("Received message from E0:F2:72:20:15:43")
        blm2.txh.write(blm1.getLastMessage())
        print("     wrote message to FB:E4:1D:F1:22:96")
        blm1.clearMessage()

    blm2Msg = blm2.getLastMessage()
    if blm2Msg != 0 and blm2Msg is not None:
        print("Received message from FB:E4:1D:F1:22:96")
        blm1.txh.write(blm2.getLastMessage())
        print("     wrote message to E0:F2:72:20:15:43")
        blm2.clearMessage()
    	time.sleep(1)