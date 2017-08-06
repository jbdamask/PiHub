from AWSIoTMQTTShadowClientGenerator import AWSIoTMQTTShadowClientGenerator, ShadowCallbackContainer
from BluefruitMonitor import BluefruitMonitor
from BLEDeviceScanner import DeviceScanner
from datetime import datetime
import threading
from AWSIoTNotificationDelegate import AWSIoTNotificationDelegate
from BluefruitNotificationDelegate import BluefruitNotificationDelegate


shadow = AWSIoTMQTTShadowClientGenerator("a2i4zihblrm3ge.iot.us-east-1.amazonaws.com",
                                         "/home/pi/PiHub/root-CA.crt",
                                         "/home/pi/PiHub/pi-ble-broker-1.cert.pem",
                                         "/home/pi/PiHub/pi-ble-broker-1.private.key",
                                         "pi-ble-broker-1",
                                         "pi",
                                         False
                                         )

# Device scanner object for its own thread
deviceScanner = DeviceScanner()
deviceScanner.start()
lock = threading.RLock()

# Set up a dictionary to track BluefruitMonitors
bleMonitors = {}

# Configure bluetooth notification delegate
blmNotificationDelegate = BluefruitNotificationDelegate()

# Pass it to the shadow so the deviceShadow can call it
shadow.registerNotificationDelegate(blmNotificationDelegate)

# Loop forever
while True:
    with lock:
        registeredDevices = deviceScanner.getDevices().keys()
    for k in registeredDevices:
        if k not in bleMonitors:
            with lock:
                shadow.registerDeviceAddress(k)
            blm = BluefruitMonitor(k, AWSIoTNotificationDelegate(k, shadow))
            if(blm is None):
                print(str(datetime.now()) + " Failed to connect to device. Will try again")
                continue
            blmNotificationDelegate.bleDevices.append(blm)
            bleMonitors[k] = blm
            print "Starting thread for device: " + blm.addr
            if blm.start() == 0:
                deviceScanner.removeDevice(k)
    blms = bleMonitors.keys()
    for b in blms:
        if b not in registeredDevices:
            del bleMonitors[b]
        #print bleMonitors[b].getLastMessage()

    # blm1Msg = blm1.getLastMessage()
    # if blm1Msg != 0 and blm1Msg is not None:
    #     print("Received message from E0:F2:72:20:15:43")
    #     blm2.txCharacteristic.write(blm1.getLastMessage())
    #     print("     wrote message to FB:E4:1D:F1:22:96")
    #     blm1.clearMessage()
    #
    # blm2Msg = blm2.getLastMessage()
    # if blm2Msg != 0 and blm2Msg is not None:
    #     print("Received message from FB:E4:1D:F1:22:96")
    #     blm1.txCharacteristic.write(blm2.getLastMessage())
    #     print("     wrote message to E0:F2:72:20:15:43")
    #     blm2.clearMessage()
    #	time.sleep(1)