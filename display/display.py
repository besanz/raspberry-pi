import time
import signal
import sys
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from threading import Lock

# Initialize the OLED display
serial = i2c(port=1, address=0x3C)
device = sh1106(serial, rotate=0)
display_lock = Lock()  # Create a new lock

# Messages to display
messages = ["Benat", "Aritz"]
current_message_index = 0

# Function to display a message
def display_message(message):
    with display_lock:  # Acquire the lock while writing to the display
        with canvas(device) as draw:
            draw.text((0, 0), message, fill="white")

# Function to get the current message
def get_current_message():
    global current_message_index
    return messages[current_message_index]

# Function to handle Ctrl+C interrupt signal
def signal_handler(sig, frame):
    print('Ctrl+C detected! Turning off display.')
    device.cleanup()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Function to loop through messages
def loop_messages():
    global current_message_index
    while True:
        print(f"Displaying message: {messages[current_message_index]}")
        display_message(messages[current_message_index])
        current_message_index = (current_message_index + 1) % len(messages)
        time.sleep(2)

# Start the message loop
loop_messages()
