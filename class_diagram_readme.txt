https://yuml.me/diagram/class/draw

[AWSIoTMQTTShadowClientGenerator]<++-1[AWSIoTMQTTShadowClient]
[AWSIoTMQTTShadowClientGenerator]<++-1[ShadowCallbackContainer|customShadowCallbackDelta(payload)]
[AWSIoTMQTTShadowClient]<++-1[AWS:deviceShadow|shadowUpdate(data)]
[AWSIoTNotificationDelegate|deviceId:String|notify(data)]->[AWSIoTMQTTShadowClientGenerator]
[ShadowCallbackContainer|customShadowCallbackDelta(payload)]<->[AWS:deviceShadow|shadowUpdate(data)]
[ShadowCallbackContainer|customShadowCallbackDelta(payload)]->[BluefruitNotificationDelegate|bleDevices:List|notify(data)]
[NotificationDelegate|notify(data)]^-.-[BluefruitNotificationDelegate|bleDevices:List|notify(data)]
[NotificationDelegate|notify(data)]^-.-[AWSIoTNotificationDelegate|deviceId:String|notify(data)]
[BluefruitMonitor]<++-1[Bluepy:Peripheral]
[Bluepy:Peripheral]<++-1[BluefruitDelegate|handleNotification(data)]
[BluefruitDelegate|handleNotification(data)]->[AWSIoTNotificationDelegate|deviceId:String|notify(data)]
[Bluepy:DefaultDelegate|handleNotification(data)]^-.-[BluefruitDelegate|handleNotification(data)]