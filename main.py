from gpiozero import Button, LED, Buzzer
from flask import Flask, render_template
import Adafruit_DHT
from time import sleep
from signal import pause

led_state=False



def toggle_outside():
    global led_state
    led_state = not led_state
    outside_light.toggle()



def toggle_inside():
    global led_state
    led_state = not led_state
    inside_light.toggle()



def toggle_ac():
    global led_state
    led_state = not led_state
    ac_indicator.toggle()
    buzzer = Buzzer(16)
    
    buzzer.on()
    sleep(0.5)
    buzzer.off()


inside_light = LED(17)    # Yellow LED
ac_indicator = LED(18)    # Red LED
outside_light = LED(22)   # Green LED

inside_button = Button(23)
ac_button = Button(25)
outside_button = Button(2)

inside_button.when_pressed = toggle_inside
outside_button.when_pressed = toggle_outside
ac_button.when_pressed =toggle_ac






pause()