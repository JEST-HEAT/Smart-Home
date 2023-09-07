from flask import Flask, render_template, request, redirect, url_for
from gpiozero import Button, LED, Buzzer
import Adafruit_DHT
from time import sleep
from threading import Thread

app = Flask(__name__)

# Initialize GPIO components and variables
led_state_out = False
led_state_in = False
led_state_ac = False
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
    global led_state_out
    led_state_out = not led_state_out
    outside_light.toggle()
 


# Function to toggle inside light
def toggle_inside():
    global led_state_in
    led_state_in = not led_state_in
    inside_light.toggle()

# Function to toggle AC and sound buzzer
def toggle_ac():
    global led_state_ac
    led_state_ac = not led_state_ac
    ac_indicator.toggle()
    buzzer.on()
    sleep(0.5)
    buzzer.off()

def temperature_check():
    sensor = Adafruit_DHT.DHT11
    pin = 21
    humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
    # print("Temperature:  {}".format(temperature))
    return temperature 
temp_value= temperature_check()
# Function to read temperature and humidity
def read_temperature_humidity():
    global temperature
    global humidity
    while True:
        humidity, temp = Adafruit_DHT.read_retry(sensor, temp_pin)
        if temp is not None:
            temperature = temp
            #humidity    =hum

        
            
        
    

def ac_auto_toggle():
   
   if temp_value>=28.0 :
       toggle_ac()   
   else: 
       toggle_ac()



inside_button.when_pressed = toggle_inside
outside_button.when_pressed = toggle_outside
ac_button.when_pressed =toggle_ac
ac_auto_toggle()

# Start a thread to continuously read temperature and humidity
temp_thread = Thread(target=read_temperature_humidity)
temp_thread.daemon = True
temp_thread.start()

# Routes for the web interface
@app.route('/', methods=['GET', 'POST'])
def index():
    led_states=[led_state_out,led_state_in,led_state_ac]
    
    return render_template('index.html',led_states= led_states,temperature=temperature, humidity=humidity)
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
    app.run(debug= True, host='192.168.24.166' , port = 5001)
