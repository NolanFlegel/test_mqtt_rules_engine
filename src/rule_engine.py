from paho.mqtt import client as mqtt_client
import json
import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.environ.get('MQTT_BROKER') 
MQTT_PORT = int(os.environ.get('MQTT_PORT') )
MQTT_TOPIC_ID = os.environ.get('MQTT_TOPIC_ID') 

# BRE/calculateWinterSupplementInput/<MQTT topic ID>
# 
# BRE/calculateWinterSupplementOutput/<MQTT topic ID>

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe(MQTT_TOPIC_ID)

def on_message(client, userdata, message):
    print(message.topic+" "+str(message.payload))

def rule_engine(topic_id, message):
    return


client = mqtt_client.Client(client_id='WinterSuppliment', callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect  
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)

try:
    print("Starting MQTT Client")
    client.loop_forever()
except KeyboardInterrupt:
    print("Closing MQTT Client Connection")
    client.disconnect()