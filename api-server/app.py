from crypt import methods
from flask import Flask, request, Request, Response
from flask_mqtt import Mqtt

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = '0.0.0.0'  
app.config['MQTT_BROKER_PORT'] = 1883 
app.config['MQTT_USERNAME'] = ''  
app.config['MQTT_PASSWORD'] = ''  
app.config['MQTT_KEEPALIVE'] = 5  
app.config['MQTT_TLS_ENABLED'] = False  

mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect():
    mqtt.publish("logs", "Connection established")
    mqtt.subscribe("/cycles/cycleResponse")

@app.route("/", methods=["GET"])
def basehit():
    return "Server online"

@app.route("/dispensers/<disp_id>/<cycle_id>", methods=["GET", "POST"])
def requestCycle(disp_id, cycle_id):
    mqtt.publish("/cycles/cycleRequest", "D{}-C{}".format(disp_id, cycle_id))
    return "Request sent"

if __name__ == "__main__":
    app.run()