import pytest
import sys
sys.path.append(".")
from src.rule_engine import new_mqtt_client
from paho.mqtt import client as mqtt_client

# Test client connection
def test_client_init():
    client = new_mqtt_client()
    assert isinstance (client, mqtt_client.Client)


# For a more robust testing solution, it would be ideal
# to build a mock client to test this library however
# for the purposes of this assignment using test.mosquitto.org 
# demonstates functionality

# Test subscribe
def test_subscribe():
    client = new_mqtt_client()
    result = client.connect("test.mosquitto.org", 1883)
    client.disconnect()
    assert result == 0

# Test publish
def test_publish():
    client = new_mqtt_client()
    client.connect("test.mosquitto.org", 1883)
    result = client.publish(topic="winterSupplementTest", payload=("Test"))
    client.disconnect()
    assert result.rc == 0