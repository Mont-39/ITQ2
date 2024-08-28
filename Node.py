import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

WIFI_SSID = "MontPi"
WIFI_PASSWORD = "MontPi39"

MQTT_BROKER = "10.42.0.1"
MQTT_PORT = 1883
MQTT_TOPIC_ALIVE="taekwondo/alphaa"
# MQTT_TOPIC_ALIVE="taekwondo/betaa"
# MQTT_TOPIC_ALIVE="taekwondo/gammaa"
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

adc = ADC(28)
voltage_per_unit = 0.828 / 14700

powr = Pin(5, Pin.OUT)
powg = Pin(6, Pin.OUT)
conr = Pin(9, Pin.OUT)
cong = Pin(10, Pin.OUT)

msg = "a"

buttons = [
    (rbu1, "Red1"),
    (rbu2, "Red2"),
    (rbu3, "Red3"),
    (blu1, "Blue1"),
    (blu2, "Blue2"),
    (blu3, "Blue3")
]

def read_battery_voltage():
    raw_value = adc.read_u16()
    voltage = raw_value * voltage_per_unit
    return voltage

def battery_percentage(voltage, min_voltage=0.100, max_voltage=0.828):
    percentage = ((voltage - min_voltage) / (max_voltage - min_voltage)) * 100
    return max(0, min(100, percentage))

def battery_led():
    vtime = 0
    if time.ticks_ms() - vtime >= 2000:
        voltage = read_battery_voltage()
        print(f"Battery Voltage: {voltage:.2f}V, Battery Percentage: {battery_percentage(voltage):.2f}%")
        percent = battery_percentage(voltage)
        if percent <= 25:
            powr.value(1)
            powg.value(0)
        else:
            powr.value(0)
            powg.value(1)
        vtime = time.ticks_ms()
    
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("Connecting..",end="")
    while not wlan.isconnected():
        print(".",end="")
        cong.value(0)
        conr.value(1)
        time.sleep(1)
    print("\nConnected to WiFi")

def main():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    powr.value(0)
    conr.value(0)
    powg.value(1)
    cong.value(0)
    connect_wifi()
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Connected to MQTT broker")
    debounce_time = 0
    dtime = 0
    vtime  =0

    while True:
        if time.ticks_ms() - vtime >= 2000:
            voltage = read_battery_voltage()
            print(f"Battery Voltage: {voltage:.2f}V, Battery Percentage: {battery_percentage(voltage):.2f}%")
            percent = battery_percentage(voltage)
            if percent <= 25:
                powr.value(1)
                powg.value(0)
            else:
                powr.value(0)
                powg.value(1)
            vtime = time.ticks_ms()

        if not wlan.isconnected():
            print("WiFi disconnected")
            connect_wifi()
        else:
            conr.value(0)
            cong.value(1)
            if time.ticks_ms() - dtime >= 5000:
                client.publish(MQTT_TOPIC_ALIVE,msg)
                print("Published: {}".format(msg))
                dtime = time.ticks_ms()
                print("Task completed")
            for button, message in buttons:
                if button.value() == 0 and (time.ticks_ms() - debounce_time) > 500:
                    client.publish(MQTT_TOPIC, message)
                    print("Published: {}".format(message))
                    debounce_time = time.ticks_ms()

if __name__ == "__main__":
    main()
