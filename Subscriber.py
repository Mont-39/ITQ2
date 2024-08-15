import paho.mqtt.client as mqtt

class MQTTHandler:
    def __init__(self, host, port, topics):
        self.MQTT_HOST = host
        self.MQTT_PORT = port
        self.MQTT_KEEPALIVE_INTERVAL = 5
        self.message1="1"
        self.message2="2"
        self.message3="3"
        self.topics = topics
        self.received_messages = {}  
        
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        
        self.mqttc.connect(self.MQTT_HOST, self.MQTT_PORT, self.MQTT_KEEPALIVE_INTERVAL)
        self.mqttc.loop_start()

    def on_connect(self, mosq, obj, flags, rc):
        
        for topic in self.topics:
            self.mqttc.subscribe(topic, 0)
            print(f"Subscribed to MQTT Topic: {topic}")

    def on_message(self, mosq, obj, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Received message on topic '{topic}': {payload}")

        self.received_messages[topic] = payload
        self.hand_msg(topic, payload)
        self.check_msg()
        
    def hand_msg(self, topic, payload):
        if topic == "taekwondo/alpha":
            self.message1 = payload
            pass
        elif topic == "taekwondo/beta":
            self.message2 = payload
            pass
        elif topic == "taekwondo/gamma":
            self.message3 = payload
            pass
    
    def check_msg(self):
        temp_message = set([self.message1, self.message2, self.message3])
        if len(temp_message) == 1:
            print("all message are the same")
        elif len(temp_message) == 2:
            print("Two message are the same")
        else:
            print("Message are unique")

if __name__ == "__main__":
    mqtt_topics = ["taekwondo/alpha", "taekwondo/beta", "taekwondo/gamma"]
    mqtt_handler = MQTTHandler(host="10.42.0.1", port=1883, topics=mqtt_topics)
    
    mqtt_handler.check_msg()
