from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from NotificationDelegate import NotificationDelegate
import sys
import logging
import time
import json
import argparse


class ShadowCallbackContainer:
    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance

    # Custom Shadow callback
    def customShadowCallbackDelta(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        print("Received a delta message:")
        payloadDict = json.loads(payload)
        deltaMessage = json.dumps(payloadDict["state"])
        print(deltaMessage)
        print("Request to update the reported state...")
        newPayload = '{"state":{"reported":' + deltaMessage + '}}'
        self.deviceShadowInstance.shadowUpdate(newPayload, None, 5)
        print("Sent.")

    # Notification delegate knows how to notify other stuff
    def setNotificationDelegate(self, notificationDelegate):
        self.notificationDelegate = notificationDelegate


class AWSIoTMQTTShadowClientGenerator:

    def __init__(self, host, rootCAPath, certificatePath, privateKeyPath, thingName, clientId, useWebsocket=False):
        self.host = host
        self.rootCAPath = rootCAPath
        self.certificatePath = certificatePath
        self.privateKeyPath = privateKeyPath
        self.useWebsocket = useWebsocket
        self.thingName = thingName
        self.clientId = clientId

        if useWebsocket and certificatePath and privateKeyPath:
            print("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
            exit(2)

        if not useWebsocket and (not certificatePath or not privateKeyPath):
            print("Missing credentials for authentication.")
            exit(2)

        # Configure logging
        logger = logging.getLogger("AWSIoTPythonSDK.core")
        logger.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

        # Init AWSIoTMQTTShadowClient
        self.myAWSIoTMQTTShadowClient = None
        if useWebsocket:
            self.myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId, useWebsocket=True)
            self.myAWSIoTMQTTShadowClient.configureEndpoint(host, 443)
            self.myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath)
        else:
            self.myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
            self.myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
            self.myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTShadowClient configuration
        self.myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect to AWS IoT
        self.myAWSIoTMQTTShadowClient.connect()

        # Create a deviceShadow with persistent subscription
        self.deviceShadowHandler = self.myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
        self.shadowCallbackContainer_Bot = ShadowCallbackContainer(self.deviceShadowHandler)

        # Listen on deltas
        self.deviceShadowHandler.shadowRegisterDeltaCallback(self.shadowCallbackContainer_Bot.customShadowCallbackDelta)

        # Create the initial State
        self._desired_state = {}
        self._reported_state = {}


    def getState(self):
        _r = '{"reported": {"ble_devices": ' + json.dumps(self._reported_state.values()) + '}'
        _d = '{"desired": {"ble_devices": ' + json.dumps(self._reported_state.values()) + '}'
        return '{"state": ' + _r + ', ' + _d + '}'


    def updateState(self, value):
        print "updateState() msg:"
        print "  " + json.dumps(value)

        self._reported_state[value["MAC"]] = value
        self._desired_state[value["MAC"]] = value
        print "Desired state values: " + json.dumps(self._desired_state.values())
        print "Reported state values: " + json.dumps(self._reported_state.values())
        if len(self._desired_state) > 1:
            for x in self._desired_state.keys():
                if x != value["MAC"]:
                    self._desired_state[x]["color"] = value["color"]
        else:
            self._desired_state[value["MAC"]] = value
        return self.getState()


    def registerDeviceAddress(self, address):
        self._desired_state["address"] = ""
        self._reported_state["address"] = ""


