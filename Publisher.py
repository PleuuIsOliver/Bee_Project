import paho.mqtt.client as mqtt
import time
def on_message(client,userdata,message):
    print("message:",str(message.payload.decode("utf-8")))
    print("message topic: ",message.topic)
def on_log(client, userdata, level, buf):
    print("log: ",buf)

ACCESS_TOKEN = "BEE_DATA_COLLECTOR_TOKEN_2022"
BROKER_ADDRESS = "broker.hivemq.com"



client = mqtt.Client("P2")
client.on_message = on_message #connects function to callback
client.on_log=on_log
#sets the accses token
#client.username_pw_set(ACCESS_TOKEN)

client.connect(BROKER_ADDRESS)
client.loop_start()
print("Publishing message to topic","house/light/Test-light")
client.publish("Bee/Data",1)
time.sleep(5)
print("Publishing message to topic","house/light/Test-light")
client.publish("Bee/Data",2)
client.loop_stop()
