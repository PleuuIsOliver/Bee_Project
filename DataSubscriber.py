import paho.mqtt.client as mqtt #import the client
import time
import uuid
import sqlite3
import os.path

def create_data_base(db_name: str):
    con = sqlite3.connect(db_name+".db")
    con.close()

def create_table(db_name: str, table_name : str):
    con = sqlite3.connect(db_name+".db")
    cur = con.cursor()
    cur.execute(f"CREATE TABLE {table_name} (date TEXT, time Text, temperature REAL, humidity REAL, air_pressure REAL, illuminance REAL, location TEXT)")     
    con.commit()
    con.close()
    
def append_table(db_name : str,table_name : str,Data):
    con = sqlite3.connect(db_name+".db")
    cur = con.cursor()
    FormatedData = (tuple(Data))
    cur.execute(f"INSERT INTO {table_name} VALUES (?,?,?,?,?,?,?)",FormatedData)
    con.commit()
    con.close()

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_message(client,userdata,message):
    print("message:",str(message.payload.decode("utf-8")))
    print("message topic: ",message.topic)

broker_address="broker.hivemq.com"
print("creating new instance")


def on_log(client, userdata, level, buf):
    print("log: ",buf)
    print("client: ",client)
    print("userdata: ",userdata)
    print("level: ",level)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
        print(client)
        client.subscribe("Bee/Data")
    else:
        print("Bad connection Returned code=",rc)

def on_message(client,userdata,message):
    mess = str(message.payload.decode("utf-8")).split("?")
    for item in mess:
        print(item)
    print("message:",str(message.payload.decode("utf-8")))
    print("message topic: ",message.topic)
    append_table("Bee_Data_Base","BeeData",mess)
def on_disconnect(client, userdata, rc):
   print("Client Got Disconnected")
   print('rc value '+str(rc))

   if rc != 0:
       print('Unexpected MQTT disconnection. Will auto-reconnect')

   else:
       print('rc value:' + str(rc))

if os.path.isfile("Bee_Data_Base.db") == False:
    print("no db found making new one\n")
    create_data_base("Bee_Data_Base")
    create_table("Bee_Data_Base","BeeData")
else:
    print("db found\n")
client = mqtt.Client("P1") #create new instance

client.on_message = on_message #connects function to callback
client.on_log=on_log
print("connecting to broker")
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.connect(broker_address) #connect to broker
client.loop_start()
print("Subscribing to topic","Bee/Data")
client.subscribe("Bee/Data")

time.sleep(1000)
client.loop_stop()
