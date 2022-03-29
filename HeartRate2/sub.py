# python3.6

import random
from datetime import datetime as dt

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'iot'
password = 'public'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect("localhost", 1883, 60)
    # client.connect("192.168.1.77", 1883, 60)
    return client

import datetime
dt = datetime.datetime.now()
import test
import statistics as s
window = []
def subscribe(client: mqtt_client):
    import datetime
    def on_message(client, userdata, msg):
        global window,dt
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        #print(msg.payload.decode(), dt.now())
        x = msg.payload.decode()
        data = x.split('-')
        #print(data)
        if data[0] == '1':
            test.write_data( data[1], (datetime.datetime.now()-dt).microseconds, datetime.datetime.now(), data[2], 'all')
                    
            if len(window) < 5:
                window.append(int(data[1]))
            else:
                window.append(int(data[1]))
                window.pop(0)
                if s.stdev(window) < 10:                    
                    print("Mean:\t", data[1], '\t', (datetime.datetime.now()-dt).microseconds,'\t',datetime.datetime.now())
                    test.write_data( data[1], (datetime.datetime.now()-dt).microseconds, datetime.datetime.now(), data[2], 'window')
                    dt = datetime.datetime.now()
                    print("="*20)
                    window = []
	#print(x.split(',', maxsplit=4))

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()

