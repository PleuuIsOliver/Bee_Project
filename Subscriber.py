import paho.mqtt.client as mqtt #import the client1
import time
broker_address="broker.hivemq.com"
print("creating new instance")


def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_message(client,userdata,message):
    print("message:",str(message.payload.decode("utf-8")))
    print("message topic: ",message.topic)

client = mqtt.Client("P1") #create new instance

client.on_message = on_message #connects function to callback
client.on_log=on_log
print("connecting to broker")

client.connect(broker_address) #connect to broker
client.loop_start()
print("Subscribing to topic","house/light/Test-light")
client.subscribe("Bee/Data")

time.sleep(1000)
client.loop_stop()
