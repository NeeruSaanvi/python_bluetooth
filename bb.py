import bluepy.btle as btle
#from bluepy.btle import Perpheral, DefaultDelegate
import time
import sys
from bluepy.btle import Scanner
import gatt
from datetime import datetime
from datetime import timedelta
# import scandevice
#from scandevice import AnyDeviceManager
        

class MyDelegate(btle.DefaultDelegate):
    
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here]
                                        
    def handleNotification(self, cHandle, data):
        data = bytearray(data)
        print("Developer: do what you want with the data.")
        print(data)
        #headertrate = data[1] & 255;
        #print(headertrate)
        if (len(data) > 4):
            #str = data[3] & 255
            
            if(data[4] == 1):
                if (data[2] == 15):
                    # token
                    totalSize = data[5] & 255;
                    temp1 = data[6] & 255;
                    temp2 = data[7] & 255;
                    temp1 += temp2 << 8;
                    j = temp1;
                    year = data[8] & 255;
                    temp2 = data[9] & 255;
                    #month = (temp2 & 2) >>> 1;
                    #day = (temp2 & 192) >>> 6;
                    temp1 = data[10] & 255;
                    hour = temp1 & 31;
                    min1 = temp1 >> 6 & 3;

                    #_status = month == 0;
                    print("spo2")
                    print(totalSize)
                    #print(temp1)
            elif(data[4] == 2):
                if(data[2] == 15):
                    units = []
                    rang = len(data) - 2
                    #print(rang)
                    for j in range(rang):
                      temp1 = data[j] & 255;
                      value = (temp1 & 127) / 100;
                      units.append(value)
                      #units.add(value);
            

                    #if (len(units) > 210):
                      #  units.removeRange(0, 4)

                    
                    #print(units)
                      
                
def sleep(period):
    msperiod = period * 1000
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    sleep = msperiod - (ms % msperiod)
    time.sleep(sleep/1000)
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    sleep = msperiod - (ms % msperiod)
    time.sleep(sleep/1000)
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.>

  
        
#oxcimeter      
#p = btle.Peripheral("c0:00:00:00:02:82")
#ekg 
p = btle.Peripheral("df:45:05:21:d2:65",btle.ADDR_TYPE_RANDOM)

p.setDelegate( MyDelegate() )
services=p.getServices()

ble_uuid = "14839ac4-7d7e-415c-9a42-167340cf2339"
ble_write_uuid_prefix = "8b00ace7"
get_real_time_wave_bytes = b'\xa5\x01\xfe\x00\x00\x00\x00\xf3'
get_device_run_state_bytes = b'\xa5\x02\xfd\x00\x00\x00\x00\x2e'
get_real_time_data_bytes = b'\xa5\x03\xfc\x00\x00\x00\x00\x65'
ble_notify_uuid_prefix = "00002902"
subscribe_bytes = b'\x01\x00'
write_handle = None
subscribe_handle = None

for service in services:
    #print(service)
    #for desc in service.getDescriptors():
        #descuuid = desc.uuid
    print(service.uuid)
        #print(desc.handle)
    
    #for characteristic in service.getCharacteristics():
        #print( "===> " + " udid: "+ str(characteristic.uuid))
        #if("8b00ace7-eb0b-49b0-bbe9-9aee0a26e1a3" == characteristic.uuid):
            #p.writeCharacteristic(characteristic.valHandle+1, "\x01\x00".encod>
        #if("0734594a-a8e7-4b1a-a6b1-cd5243059a57" == characteristic.uuid):
            #p.writeCharacteristic(characteristic.valHandle+1, "\x01\x00".encod>
        
        
    #oxcimeter
    #if("6e400001-b5a3-f393-e0a9-e50e24dcca9e" == service.uuid):
    #ekg
    if(ble_uuid == service.uuid):
        #print("  Service [%s]" % (service.uuid))
        #c = service.getCharacteristics()
        
        descs = service.getDescriptors()
        
        for desc in descs:
            
            str_uuid = str(desc.uuid).lower()
            if str_uuid.startswith(ble_write_uuid_prefix):
                write_handle = desc.handle
                print("write_handle: " + str(write_handle))
            elif str_uuid.startswith(ble_notify_uuid_prefix):
                subscribe_handle = desc.handle
                print("subscribe_handle: " + str(subscribe_handle))
        
        
        if write_handle is not None and subscribe_handle is not None:
            print("if block run")
            
            while True:
                last_time = datetime.now()
                start_time = datetime.now()
                
                response = p.writeCharacteristic(subscribe_handle, subscribe_by>
                
                response = p.writeCharacteristic(write_handle, get_device_run_s>
                
                p.waitForNotifications(1.0)
                sleep(2)
        
        #for characteristic in service.getCharacteristics():
            #print(characteristic)
            #print(characteristic.uuid)
            #ble oximeter
            #if("6e400003-b5a3-f393-e0a9-e50e24dcca9e" == characteristic.uuid):
            #EKG reading
            #if("8b00ace7-eb0b-49b0-bbe9-9aee0a26e1a3" == characteristic.uuid):
                
                #svc = p.getServiceByUUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e>
                #ch = svc.getCharacteristics("6e400003-b5a3-f393-e0a9-e50e24dcc>
                #characteristic.write(characteristic.getHandle() + 1, b"\x01\x0>
                
                #print("Hello ", characteristic.handle)
                #pp = p.waitForNotifications(10)
                #pp = characteristic.getHandle()
                #print(pp)
                
                #p.writeCharacteristic(characteristic.valHandle+1, "\x01\x00".e>
                #if(characteristic.suppotsRead()):
                    #print("Hello ", notify)
                    #characteristic.notify()
                #if(characteristic.isnotify):
                    #print("dddd")
                # Enable the sensor, start notifications
                # Writing x01 is the protocol for all BLE notifications.
                #characteristic.write(bytes("0001".encode())) 
                #p.connect(service);
                #ppp = characteristic.write(b"\x01\x00")
                #print(ppp)
                #time.sleep(1.0) # Allow sensor to stabilise

                # Main loop --------
                #while True:
                    #if p.waitForNotifications(1.0):
                        #print("ssss")
                        # handleNotification() was called
                        #continue
                        #print("Waiting...")
                #print(characteristic.uuid)
                


    


