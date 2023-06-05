# light.py
# -*- coding: utf-8 -*-
import time
import board
import neopixel
import RPi.GPIO as GPIO
from threading import Thread

# LED strip configuration
LED_COUNT = 30  # Number of LED pixels.
LED_PIN = board.D18  # GPIO pin (must be a PWM GPIO).
LED_BRIGHTNESS = 1  # Set from 0 for off to 1 for max brightness

# Button configuration
BUTTON_PIN = 16  # The GPIO pin the button is connected to

# Create LED strip object
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)

# Initial state of LED strip
led_state = {"on": True, "color": (255, 255, 255)}

def change_color(color):
    """Change the color of all pixels to the given color."""
    for i in range(len(pixels)):
        pixels[i] = color
    pixels.show()

def button_thread():
    # Configure GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Function to handle button event
    def button_callback(channel):
        led_state['on'] = not led_state['on']  # Toggle LED strip state
        change_color((255, 255, 255)) if led_state['on'] else change_color((0, 0, 0))

    # Set up button event
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

    # Keep thread running indefinitely
    while True:
        time.sleep(1)

def main_loop():
    # Keep program running indefinitely
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO resources when program is interrupted

button_t = Thread(target=button_thread)
button_t.start()

main_loop_t = Thread(target=main_loop)
main_loop_t.start()

def get_led_state():
    return led_state

def set_led_state(new_led_state):
    led_state.update(new_led_state)
    change_color((0, 0, 0)) if not led_state['on'] else change_color(tuple(led_state['color']))
