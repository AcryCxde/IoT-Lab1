import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_SENSOR = "iot_lab1/smoke_level"
TOPIC_MODE = "iot_lab1/mode"
TOPIC_ACTUATOR = "iot_lab1/actuator"

client = mqtt.Client(client_id="SmokeDetector_001", protocol=mqtt.MQTTv311)
manual_mode = None
fire_suppression_status = None  # ссылка на функцию для активации пожаротушения
start_time = time.time()

def publish_sensor_data(smoke_level):
    current_time = time.time()
    elapsed_time = int(current_time - start_time)
    formatted_time = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
    rounded_smoke_level = round(smoke_level, 1)

    data = {
        "timestamp": formatted_time,
        "elapsed_time": elapsed_time,
        "smoke_level": rounded_smoke_level
    }
    client.publish(TOPIC_SENSOR, json.dumps(data))

def set_manual_mode(mode_var):
    global manual_mode
    manual_mode = mode_var  # устанавливаем ссылку на manual_mode из main.py

def set_fire_suppression_status(status_func):
    global fire_suppression_status
    fire_suppression_status = status_func  # функция для управления пожаротушением из main.py

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC_MODE)
    client.subscribe(TOPIC_ACTUATOR)

def on_message(client, userdata, msg):
    global manual_mode
    payload = msg.payload.decode()

    if msg.topic == TOPIC_MODE:
        if payload == "auto":
            manual_mode.set(0)
            print("Автоматический режим включен")
        elif payload == "manual":
            manual_mode.set(1)
            print("Ручной режим включен")

    elif msg.topic == TOPIC_ACTUATOR and manual_mode.get():
        if payload == "activate" and fire_suppression_status:
            print("Актуатор активирован по команде от сервера")
            fire_suppression_status()  # активирует систему пожаротушения

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()
