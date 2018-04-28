from flask import Flask, render_template
import RPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import smtplib # This is the SMTP library we need to send the email notification
import time # This is the time library, we need this so we can use the sleep function

app = Flask(__name__)

# This is our callback function, this function will be called every time there is a change on the specified GPIO channel, in this example we are using 17

LED_status = "not start yet"
def callback(channel):
	global LED_status
	if GPIO.input(channel):
		LED_status = "wet"
		print ("LED on")
	else:
		print ("LED off")
		LED_status = "dry"


@app.route('/')
def index():
	return render_template('index.html',led_status=LED_status)


GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that we have our digital output from our sensor connected to
channel = 17
# Set the GPIO pin to an input
GPIO.setup(channel, GPIO.IN)

# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
GPIO.add_event_callback(channel, callback)



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
    while True:
        # This line simply tells our script to wait 0.1 of a second, this is so the script doesnt hog all of the CPU
        time.sleep(0.1)