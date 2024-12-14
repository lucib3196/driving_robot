from gpiozero import Motor,PWMOutputDevice,AngularServo
from time import sleep
# Initialize the motor (IN1 and IN2 pins on GPIO 17 and 18)
motor = Motor(forward=4, backward=14,enable=22)
servo = AngularServo(17, min_angle=-90, max_angle=90)
# # Control the motor
# while True:
#     motor.forward()  # Moves the motor forward
#     motor.backward()  # Moves the motor backward
#     motor.stop()  # Stops the motor
while True:
    servo.angle = -90
    sleep(2)
    servo.angle = 90
    sleep(2)