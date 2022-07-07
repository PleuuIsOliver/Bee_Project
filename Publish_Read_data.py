import paho.mqtt.client as mqtt
import bme680
import time
import json
BROKER_ADDRESS = "broker.hivemq.com"
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
            output = "{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH".format(sensor.data.temperature,sensor.data.pressure,sensor.data.humidity)
            print("{0},{1}  Ohms".format(output, sensor.data.gas_resistance))
            if sensor.data.heat_stable: #checks if it is stable for reading
                print("{0},{1}  Ohms".format(output, sensor.data.gas_resistance))
        client.publish("Bee/Data",output)
        time.sleep(3)
except KeyboardInterrupt:
    pass        
client.loop_stop()
