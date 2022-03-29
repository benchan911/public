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
    client.connect("localhost", 1883, 60) # 192.168.1.77
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        #print(msg.payload.decode(), dt.now())
        x = msg.payload.decode()
        data = x.split('-')
        if data[0] == '2':
            process(data[1], data[2]) # Red, IR

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


irDataList = []
redDataList = []

HR_value = 0

window = []

import datetime
dt = datetime.datetime.now()
irDataList = []
redDataList = []

def process(redData, irData):
    from time import time, sleep
    import datetime
    import hrcalc
    import statistics as s
    global HR_value, dt, irDataList, redDataList, window
    import test
    # hr, hr_valid, spo2, spo2_valid
    if len(irDataList) == 100 and len(redDataList) == 100: 
        hr, hr_valid, _, _ = hrcalc.calc_hr_and_spo2(irDataList, redDataList)
        irDataList.append(int(redData))
        redDataList.append(int(irData))
        irDataList.pop(0)
        redDataList.pop(0)
        if hr_valid and HR_value != hr:
            HR_value = hr
            test.write_data(HR_value, (datetime.datetime.now()-dt).microseconds, datetime.datetime.now(), 0,  'all')
                    
            if len(window) < 5:
                window.append(0.9*hr)
            else:
                
                #if s.stdev(window) < 10:
                #print("Mean:\t",s.mean(window))
                #print("Stdev:\t", s.stdev(window))
                print("="*20)
                window.append(0.9*hr)
                window.pop(0)
                if s.stdev(window) < 10:
                    print("Mean:\t", round(s.mean(window)), '\t\t', (datetime.datetime.now()-dt).microseconds ,'\t',datetime.datetime.now())
                    test.write_data(round(s.mean(window)), (datetime.datetime.now()-dt).microseconds, datetime.datetime.now(), 0,  'window')
                    dt = datetime.datetime.now()
                    irDataList = []
                    redDataList = []
                    window = []
    else:
        irDataList.append(int(redData))
        redDataList.append(int(irData))
        
    
    
if __name__ == '__main__':
    run()

