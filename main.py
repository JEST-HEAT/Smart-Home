from gpiozero import Button, LED, Buzzer
import paho.mqtt.client as mqtt
from time import sleep
from signal import pause
import Adafruit_DHT

# Functions
# Toggle AC
def toggle_ac():
    buzzer.on()
    ac_indicator.toggle()
    sleep(0.5)
    buzzer.off()
    client.publish(topic, 'ac_indicator')

# Toggle Inside Light
def toggle_inside():
    inside_light.toggle()
    client.publish(topic, 'inside_light')

# Toggle Outside Light
def toggle_outside():
    outside_light.toggle()
    client.publish(topic, 'outside_light')

# Temperature Check
def temperature_check():
    humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
    return temperature

# AC Auto Toggle with Temperature Check (DHT11)
def ac_auto_toggle():
    temp_value=temperature_check()
    if temp_value >=28.0:
        toggle_ac()
        print("The AC has been Turned On")
    elif temp_value < 28.0:
        toggle_ac()
        print("THE AC has been turned off")
    else:
        print("Temperature can't be detected!!!!")


# MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected to Smart Home with result code: " + str(rc))
    client.subscribe(topic)
    client.publish(topic, temp_value)

def on_message(client, userdata, msg):
    global message
    message = msg.payload.decode()

    if message == 'ac_indicator':
        toggle_ac()

    elif message == 'inside_light':
        toggle_inside()

    elif message == 'outside_light':
        toggle_outside()


# Variables
message = ''

hostname = "mqtt.dioty.co"
broker_port = 1883
topic = "smart-home"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(hostname, broker_port, 60)

# DHT11 sensor
sensor = Adafruit_DHT.DHT11
pin = 21

# GPIO (LED, Buzzer, Button)
inside_light = LED(17)    # Yellow LED
ac_indicator = LED(18)    # Red LED
outside_light = LED(22)   # Green LED

buzzer = Buzzer(14)

inside_button = Button(23)
ac_button = Button(25)
outside_button = Button(2)

# Main Program
outside_button.when_pressed = toggle_outside    # msg: outside_light
inside_button.when_pressed = toggle_inside      # msg: inside_light
ac_button.when_pressed = toggle_ac              # msg: ac_indicator
temp_value = temperature_check()                # msg: temperature_check

# test
print(temp_value)

ac_auto_toggle()

client.loop_start()
pause()