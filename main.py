from gpiozero import Button, LED, Buzzer
import paho.mqtt.client as mqtt
from time import sleep
from signal import pause
import Adafruit_DHT

def on_connect(client, userdata, flags, rc):
    print("Connected to Smart Home with result code: " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global message
    message = msg.payload.decode()

    if message == 'ac_indicator':
        buzzer.on()
        sleep(0.5)
        buzzer.off()
        sleep(0.5)

    elif message == 'inside_light':
        inside_light.toggle()

    elif message == 'outside_light':
        outside_light.toggle()

message = ''

hostname = "mqtt.dioty.co"
broker_port = 1883
topic = "smart-home"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(hostname, broker_port, 60)

buzzer = Buzzer(14)

inside_light = LED(17)    # Yellow LED
ac_indicator = LED(18)    # Red LED
outside_light = LED(22)   # Green LED

inside_button = Button(23)
ac_button = Button(25)
outside_button = Button(2)

outside_button.when_pressed = outside_light.toggle      # msg: outside_light
inside_button.when_pressed = inside_light.toggle    # msg: inside_light
ac_button.when_pressed = ac_indicator.toggle       # msg: ac_indicator


client.loop_start()
pause()