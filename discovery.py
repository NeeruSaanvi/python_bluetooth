import gatt
import bluepy.btle as btle
import time
import base64
import sys
import requests
from bluepy.btle import Scanner
from datetime import datetime
from datetime import timedelta


serviceuuid = ""
characteristic_uuid = ""
bleDeviceType = "oxy"

oxiServiceUDID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
oxiCharUDID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

ekgServiceUDID = "14839ac4-7d7e-415c-9a42-167340cf2339"
ekgCharUDID = "8b00ace7-eb0b-49b0-bbe9-9aee0a26e1a3"




class AnyDeviceManager(gatt.DeviceManager):
    def device_discovered(self, device):
        print("[%s] Discovered, alias = %s" % (device.mac_address, device.alias()))
        if(device.alias().find("POD") == 0 or device.alias().find("DuoEK") == 0):
            self.stop_discovery()
            self.stop()
            connect = MyDelegate()
            connect.callcode(device)
            

class MyDelegate(btle.DefaultDelegate):
    
   # serviceuuid = ""
    #characteristic_uuid = ""
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here]
        
    def handleNotification(self, cHandle, data):
        data = bytearray(data)
        print(data)
        try:
            val = base64.b64encode(data)
            url = 'http://raspberrypi.local:3000/sendSPo2'
            myobj = {'data': val,'type':bleDeviceType}
            x = requests.post(url, json = myobj)
            #print(x)
        except:
            print("no connection available")
        
    def callcode(self,device):
        print("call")
        ble_write_uuid_prefix = "8b00ace7"
        get_real_time_wave_bytes = b'\xa5\x01\xfe\x00\x00\x00\x00\xf3'
        get_device_run_state_bytes = b'\xa5\x02\xfd\x00\x00\x00\x00\x2e'
        get_real_time_data_bytes = b'\xa5\x03\xfc\x00\x00\x00\x00\x65'
        ble_notify_uuid_prefix = "00002902"
        subscribe_bytes = b'\x01\x00'
        write_handle = None
        subscribe_handle = None
        
        if device.alias().find("POD") == 0:
            bleDeviceType = "oxy"
        elif device.alias().find("DuoEK") == 0:
            bleDeviceType = "ekg"
            
        if(bleDeviceType == "oxy"):
            p = btle.Peripheral(device.mac_address)
            serviceuuid = oxiServiceUDID
            characteristic_uuid = oxiCharUDID
        else:
            p = btle.Peripheral(device.mac_address,btle.ADDR_TYPE_RANDOM)
            serviceuuid = ekgServiceUDID
            charectoruuid = ekgCharUDID
            
        p.setDelegate( MyDelegate() )
        services=p.getServices()


        for service in services:
            print(service)
            if(serviceuuid == service.uuid):
                for characteristic in service.getCharacteristics():
                    print(characteristic.uuid)
                    if("ekg" == bleDeviceType):
                        str_uuid = str(characteristic.uuid).lower()
                        if str_uuid.startswith(ble_write_uuid_prefix):
                            write_handle = characteristic.handle
                            print("write_handle: " + str(write_handle))
                        elif str_uuid.startswith(ble_notify_uuid_prefix):
                            subscribe_handle = characteristic.handle
                            print("subscribe_handle: " + str(subscribe_handle))
                        
                        if write_handle is not None and subscribe_handle is not None:
                            while True:
                                #last_time = datetime.now()
                                #start_time = datetime.now()
                                
                                #response = p.writeCharacteristic(subscribe_handle, subscribe_bytes, withResponse=True)
                                
                                response = p.writeCharacteristic(write_handle, get_device_run_state_bytes, withResponse=True)
                                
                                if p.waitForNotifications(1.0):
                                    continue
                                sleep(1)
                    elif(characteristic_uuid == characteristic.uuid):
                        p.writeCharacteristic(characteristic.valHandle+1, "\x01\x00".encode())

                        while True:
                            if p.waitForNotifications(1.0):
                                #print("ssss")
                                continue
                            
                    #print(characteristic_uuid)
                            
                    """
                    if(characteristic_uuid == characteristic.uuid):
                        print("characteristic_uuid match")
                        
                            while True:
                                #last_time = datetime.now()
                                #start_time = datetime.now()
                                
                                #response = p.writeCharacteristic(subscribe_handle, subscribe_bytes, withResponse=True)
                                get_real_time_wave_bytes = b'\xa5\x01\xfe\x00\x00\x00\x00\xf3'
                                response = p.writeCharacteristic(get_real_time_wave_bytes, withResponse=True)
                                
                                #p.waitForNotifications(1.0)
                                sleep(2)
                        else:
                            p.writeCharacteristic(characteristic.valHandle+1, "\x01\x00".encode())
                        #print("Hello")
                       
                        # Main loop --------
                        while True:
                            if p.waitForNotifications(1.0):
                                #print("ssss")
                                continue """
                   
        
manager = AnyDeviceManager(adapter_name='hci0')
manager.start_discovery()
manager.run()






    
        
    
