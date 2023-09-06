from flask import Flask, render_template, request, redirect, url_for
from gpiozero import Button, LED, Buzzer
import Adafruit_DHT
from time import sleep
from threading import Thread

app = Flask(__name__)

# Initialize GPIO components and variables
led_state = False
inside_light = LED(17)    # Yellow LED
ac_indicator = LED(18)    # Red LED
outside_light = LED(22)   # Green LED
inside_button = Button(23)
ac_button = Button(25)
outside_button = Button(2)
buzzer = Buzzer(16)
sensor = Adafruit_DHT.DHT11
temp_pin = 21
temperature = None


# Function to toggle outside light
def toggle_outside():
    global led_state
    led_state = not led_state
    outside_light.toggle()
 


# Function to toggle inside light
def toggle_inside():
    global led_state
    led_state = not led_state
    inside_light.toggle()

# Function to toggle AC and sound buzzer
def toggle_ac():
    global led_state
    led_state = not led_state
    ac_indicator.toggle()
    buzzer.on()
    sleep(0.5)
    buzzer.off()

# Function to read temperature and humidity
def read_temperature_humidity():
    global temperature
    global humidity
    while True:
        humidity, temp = Adafruit_DHT.read_retry(sensor, temp_pin)
        if temp is not None:
            temperature = temp
        sleep(10)



inside_button.when_pressed = toggle_inside
outside_button.when_pressed = toggle_outside
ac_button.when_pressed =toggle_ac


# Start a thread to continuously read temperature and humidity
temp_thread = Thread(target=read_temperature_humidity)
temp_thread.daemon = True
temp_thread.start()

# Routes for the web interface
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', led_state=led_state, temperature=temperature, humidity=humidity)

@app.route('/toggle_outside', methods=['POST'])
def toggle_outside_route():
    toggle_outside()
    return redirect("/")

@app.route('/toggle_inside', methods=['POST'])
def toggle_inside_route():
    toggle_inside()
    return redirect("/")


@app.route('/toggle_ac', methods=['POST'])
def toggle_ac_route():
    toggle_ac()
    return redirect("/")


if __name__ == '__main__':
    app.run(host='127.0.0.2')
