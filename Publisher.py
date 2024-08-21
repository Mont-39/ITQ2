import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

WIFI_SSID = "MontPi"
WIFI_PASSWORD = "MontPi39"

MQTT_BROKER = "10.42.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "taekwondo/alpha"
#MQTT_TOPIC = "taekwondo/beta"
#MQTT_TOPIC = "taekwondo/gamma"
CLIENT_ID = "pico1"

blu1 = Pin(15, Pin.IN, Pin.PULL_UP)
blu2 = Pin(14, Pin.IN, Pin.PULL_UP)
blu3 = Pin(13, Pin.IN, Pin.PULL_UP)
rbu1 = Pin(16, Pin.IN, Pin.PULL_UP)
rbu2 = Pin(17, Pin.IN, Pin.PULL_UP)
rbu3 = Pin(18, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)
led1 = Pin(2, Pin.OUT)

buttons = [
    (rbu1, "Red1"),
    (rbu2, "Red2"),
    (rbu3, "Red3"),
    (blu1, "Blue1"),
    (blu2, "Blue2"),
    (blu3, "Blue3")
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
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    led1.value(0)
    connect_wifi()
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Connected to MQTT broker")
    debounce_time = 0

    while True:
        if not wlan.isconnected():
            print("WiFi disconnected")
            connect_wifi()
        else:
            led.value(1)
            for button, message in buttons:
                if button.value() == 0 and (time.ticks_ms() - debounce_time) > 500:
                    client.publish(MQTT_TOPIC, message)
                    print("Published: {}".format(message))
                    debounce_time = time.ticks_ms()

if __name__ == "__main__":
    main()
