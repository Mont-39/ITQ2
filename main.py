import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

WIFI_SSID = "MontPi"
WIFI_PASSWORD = "MontPi39"

MQTT_BROKER = "10.42.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "taekwondo/gamma"
CLIENT_ID = "pico1"

blu1 = Pin(15, Pin.IN, Pin.PULL_UP)
blu2 = Pin(14, Pin.IN, Pin.PULL_UP)
blu3 = Pin(13, Pin.IN, Pin.PULL_UP)
rbu1 = Pin(16, Pin.IN, Pin.PULL_UP)
rbu2 = Pin(17, Pin.IN, Pin.PULL_UP)
rbu3 = Pin(18, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

buttons = [
    (rbu1, "Red, 1,1"),
    (rbu2, "Red, 1,2"),
    (rbu3, "Red, 1,3"),
    (blu1, "Blue, 2,1"),
    (blu2, "Blue, 2,2"),
    (blu3, "Blue, 2,3")
]

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("Connecting..",end="")
    while not wlan.isconnected():
        print(".",end="")
        led.value(0)
        time.sleep(1)
    print("\nConnected to WiFi")

def main():
    connect_wifi()
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Connected to MQTT broker")
    debounce_time = 0

    while True:
        led.value(1)
        for button, message in buttons:
            if button.value() == 0 and (time.ticks_ms() - debounce_time) > 500:
                client.publish(MQTT_TOPIC, message)
                print("Published: {}".format(message))
                # if sp.is_connected():
                #     sp.send(message)
                debounce_time = time.ticks_ms()

if __name__ == "__main__":
    main()

        # message = "Hello from {}!".format(CLIENT_ID)
        # client.publish(MQTT_TOPIC, message)
        # print("Published: {}".format(message))
        # time.sleep(5)
        # message = "Goodbye from {}!".format(CLIENT_ID)
        # client.publish(MQTT_TOPIC, message)
        # print("Published: {}".format(message))
        # time.sleep(5)