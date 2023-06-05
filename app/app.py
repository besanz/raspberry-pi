# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread
import time
import sys
import os
import json
sys.path.append('../sensor')
sys.path.append('../display')  # Add the display directory to the system path
import sensor
import light  # Import light module

app = Flask(__name__)
CORS(app)  # Enable CORS on your Flask application

@app.route('/humidity', methods=['GET'])
def get_humidity():
    humidity, _ = sensor.read_humidity_temp_sensor()
    if humidity is not None:
        return jsonify({'humidity': humidity})
    else:
        return jsonify({'error': 'Failed to read humidity sensor'}), 500

@app.route('/temperature', methods=['GET'])
def get_temperature():
    _, temp = sensor.read_humidity_temp_sensor()
    if temp is not None:
        return jsonify({'temperature': temp})
    else:
        return jsonify({'error': 'Failed to read temperature sensor'}), 500

@app.route('/led', methods=['GET'])
def get_led_state():
    led_state = light.get_led_state()
    return jsonify(led_state)

@app.route('/led', methods=['POST'])
def set_led_state():
    new_led_state = request.get_json()
    light.set_led_state(new_led_state)
    return jsonify({"message": "LED state updated"}), 200

def run_flask_server():
    print("Flask server running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)

def read_sensor_data():
    while True:
        humidity, temp = sensor.read_humidity_temp_sensor()
        if humidity is not None and temp is not None:
            print(f'Humidity: {humidity}%, Temperature: {temp}C')
        else:
            print("Failed to get reading. Try again!")
        
        time.sleep(1)  # Read every 1 second

# Start Flask server in a separate thread
flask_thread = Thread(target=run_flask_server)
flask_thread.start()

# Start sensor reading in a separate thread
sensor_thread = Thread(target=read_sensor_data)
sensor_thread.start()
