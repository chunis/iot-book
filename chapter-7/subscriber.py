#!/usr/bin/python3

import paho.mqtt.client as mqtt

# 回调函数，当尝试与 MQTT broker 建立连接时，触发该函数。
# client: 本次连接的客户端实例。
# userdata: 用户信息，一般为空。但如果有需要，也可以通过user_data_set函数设置。
# flags: 保存服务器响应标志的字典。
# rc: 响应码；一般情况下，只需要关注 rc 响应码是否为 0。
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 订阅，需要放在 on_connect 里
    # 如果与 broker 失去连接后重连，仍然会继续订阅 raspberry/topic 主题
    client.subscribe("iot/testmqtt")

# 回调函数，当收到消息时，触发该函数
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 创建连接，参数分别为 broker 地址，broker 端口号，保活时间
client.connect("broker.emqx.io", 1883, 60)

client.loop_forever()
