from paho.mqtt import client as mqtt_client
import json
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

MQTT_BROKER = os.environ.get('MQTT_BROKER') 
MQTT_PORT = int(os.environ.get('MQTT_PORT') )
MQTT_TOPIC_ID = os.environ.get('MQTT_TOPIC_ID')
MQTT_INPUT_TOPIC = f"BRE/calculateWinterSupplementInput/{MQTT_TOPIC_ID}"
MQTT_OUTPUT_TOPIC = f"BRE/calculateWinterSupplementOutput/{MQTT_TOPIC_ID}"
CLIENT_ID = f"WinterSupplement-{uuid.uuid4()}"

# Prefer to use StrEnum for python 3.11+
FAMILY_COMPOSITION = {
    "single": "single",
    "couple": "couple"
}

def new_mqtt_client() -> mqtt_client:
    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        client.subscribe(MQTT_INPUT_TOPIC)

    def on_subscribe(client, userdata, mid, granted_qos):
        for sub_result in granted_qos:
            print(sub_result)

    def on_message(client, userdata, message):
        output_message = json.dumps(rule_engine(message.payload))
        if output_message is not None:
            response = client.publish(topic=MQTT_OUTPUT_TOPIC, payload=output_message)

    def on_subscribe(client, userdata, mid, reason_codes, properties):
        print(f"Subscribed with reason code {reason_codes}")

    def on_publish(client, userdata, mid, reason_codes, properties):
        print(f"Published message with reason code {reason_codes} ")
        
    client = mqtt_client.Client(client_id=CLIENT_ID, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_publish = on_publish
    return client



def rule_engine(message):
    print(f"message payload: {message}")
    required_keys = ["id", "familyUnitInPayForDecember", "numberOfChildren", "familyComposition"]
    message_body = json.loads(message)

    # If any keys are missing or id is empty return without publishing
    # could expand this to cover cases where any dependent field is empty
    if not set(required_keys).issubset(message_body):
        print(f"message body missing required keys")
        return None
    
    if message_body['id'] is None or message_body['id'] == "":
        return None
    
    if message_body == None or message_body == {}:
        print(f"Message body empty, return")
        return None
    
    default_output_message = {
        "id": message_body["id"], 
        "isEligible": False,
        "baseAmount": 0.0,
        "childrenAmount": 0.0,
        "supplementAmount": 0.0
        }

    # set default values
    is_eligible = message_body["familyUnitInPayForDecember"]
    number_of_children = int(message_body["numberOfChildren"])
    family_composition = message_body["familyComposition"]
    base_amount = 0.0
    children_amount = 0.0
    supplement_amount = 0.0

    if is_eligible == False:
        return default_output_message
    
    # handle edge case of invalid data
    if number_of_children < 0 or family_composition not in FAMILY_COMPOSITION:
        return default_output_message

    if is_eligible and number_of_children > 0:
        base_amount = 120.00
        children_amount = 20.00 * number_of_children
    elif is_eligible and family_composition == FAMILY_COMPOSITION["couple"]:
        base_amount = 120.00
    elif is_eligible and family_composition == FAMILY_COMPOSITION["single"]:
        base_amount = 60.00
    else:
        is_eligible = False

    supplement_amount = base_amount + children_amount
    output_message = {
        "id": message_body["id"], 
        "isEligible": is_eligible,
        "baseAmount": base_amount,
        "childrenAmount": children_amount,
        "supplementAmount": supplement_amount
        }
    return output_message

def start_rule_engine():
    client = new_mqtt_client()
    client.connect(MQTT_BROKER, MQTT_PORT)
    
    try:
        print("Starting MQTT Client")
        client.loop_forever()
    except KeyboardInterrupt:
        print("Closing MQTT Client Connection")
        client.disconnect()


if __name__ == '__main__':
    start_rule_engine()