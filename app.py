from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

app = Flask(__name__)

mqtt = Mqtt(app)
socketio = SocketIO(app)

app.config['MQTT_BROKER_URL'] = 'mqtt.dioty.co'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'smart-home'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
app.config['MQTT_KEEPALIVE'] = 5

mqtt = Mqtt(app)

@app.route('/')
def index():
    return render_template('index.html')

