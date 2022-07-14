import paho.mqtt.client as mqtt
import bme680
import time
import json
from datetime import datetime
BROKER_ADDRESS = "broker.hivemq.com"
DEVICE_LOCATION = "GreyCourt"
client = mqtt.Client("P2")
client.connect(BROKER_ADDRESS)

sensor = bme680.BME680()

# define the sampling rate for individual paramters
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)

# filter out noises
sensor.set_filter(bme680.FILTER_SIZE_3)

client.loop_start()
try:
    while True:
        print("in loop")
        if sensor.get_sensor_data():#we first need to chekc if any data is present
            pres = sensor.data.pressure
            hum = sensor.data.humidity
            temp = sensor.data.temperature
            
            now = datetime.now()
            
            date_string = now.strftime("%Y/%m/%d")
            time_string = now.strftime("%H:%M:%S")
            
            data = f"{date_string}?{time_string}?{temp:.2f}?{pres:.1f}?{hum:.2f}?0?{DEVICE_LOCATION}" 

            print(data)
            print(date_string)
            print(time_string)
            client.publish("Bee/Data",data)
        time.sleep(3)
except KeyboardInterrupt:
    pass        
client.loop_stop()
