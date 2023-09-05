from gpiozero import Button, LED, Buzzer
from flask import Flask, render_template
import Adafruit_DHT
from time import sleep
from signal import pause

def switch_up(status, led):
    if status == "on":
        LED(led).on()
    else:
        LED(led).off()


inside_light = LED(17)    # Yellow LED
ac_indicator = LED(18)    # Red LED
outside_light = LED(22)   # Green LED

inside_button = Button(23)
ac_button = Button(25)
outside_button = Button(2)

outside_button.when_pressed = outside_light.on
inside_button.when_pressed = inside_light.on
ac_button.when_pressed = ac_indicator.on



# ac_indicator.on()
# sleep(3)
# buzzer = Buzzer(17)
# while True:
#     buzzer.on()

pause()