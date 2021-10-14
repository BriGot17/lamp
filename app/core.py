from flask import Flask, redirect, request, render_template
import random

from coap_handler import coap_handler
app = Flask(__name__)
app.config["DEBUG"] = True

value = 0
coap = coap_handler('cisco', '1vB3D29hz7Uja2wS', '192.168.1.10')
@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

app.add_url_rule("/", "index", home)

@app.route('/api/off', methods=['PUT', 'GET'])
def lamp_off():
    coap.turn_off()
    return redirect("http://localhost:5000/")

@app.route('/api/on', methods=['PUT', 'GET'])
def lamp_on():
    coap.turn_on()
    return redirect("http://localhost:5000/")
@app.route('/api/on/level', methods=['PUT', 'GET'])
def lamp_light_change():
    try:
        level = int(request.args['lightlevel'])
        coap.change_level(level)
    except:
        print('Not a number between 1 and 254')
    return redirect("http://localhost:5000/")

@app.route('/api/moisturedata', methods=['PUT', 'GET'])
def get_moisture():
    value = int(request.args['moisture'])
    f = open('value.txt', 'w')
    f.write(str(value)  )
    f.close()
    if int(value) <= 60:
        coap.turn_on()
    return '{"result": "success"}'

@app.route('/api/moistureout')
def return_moisture():
    f = open('value.txt', 'r')
    value = f.read()
    f.close()
    
    return '{"moisture": "' + str(value) + '"}'

@app.route('/api/ciscodisco/on', methods=['PUT', 'GET'])
def disco_on():
    print('corehello')
    coap.ciscodisco()
    return 'Success'


app.run(host = "0.0.0.0")

