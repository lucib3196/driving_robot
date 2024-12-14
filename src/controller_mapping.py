from evdev import InputDevice, ecodes
from gpiozero import Motor, PWMOutputDevice, AngularServo
import cv2
import asyncio
# Replace with the path of the controller
controller_path = "/dev/input/event6"

def map_value(value, a1, a2, b1, b2):
    """
    Maps a value from range [a1, a2] to range [b1, b2].
    """
    return b1 + (value - a1) * (b2 - b1) / (a2 - a1)

# Define Motor Actions
motor = Motor(forward=4, backward=14,enable=22)
# Define Servo
servo = AngularServo(17, min_angle=-90, max_angle=90)

# Checks to ensure controller is found 
try:
    gamepad = InputDevice(controller_path)
    print(f"Connected to: {gamepad.name}")
except FileNotFoundError:
    print("Controller not found. Check the device path.")

# Intialize Camera 
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Failed to open camera")
    exit()

# Button A Honk Noice
def action_button_a():
    print('Button A Pressed: Honking')
    pass

# Break Button
def action_button_b():
    print('Button B Pressed: Braking')
    pass

# Boost Function
def action_button_x():
    print('Button X Pressed: Going Super Turbo!!!!')
    pass

# Toggle Lights
def action_button_y():
    print('Button Y Pressed: Toggle Lights')
    pass

# Capure Image
def action_button_cap():
    ret, frame = camera.read()
    print('Button Z Pressed: Image Capture')
    filename = 'captured_image.jpg'
    cv2.imwrite(filename,frame)
    print(f"Image captured and saved as {filename}")

# Define actions for joystick or axis movements
def action_left_joystick_x(value):
    mapped_speed = map_value(value, -32767, 32767, -255, 255)
    print(f"Action: Left joystick X-axis moved to {mapped_speed}")


def action_left_joystick_y(value):
    mapped_speed = map_value(value, 32767, -32767, -255, 255)
    print(f"Action: Left joystick Y-axis moved to {mapped_speed}")
    if mapped_speed >100:
        motor.forward()
        print("Motor moving forward")
    elif mapped_speed <-9:
        motor.backward()
        print("Motor moving backward")
    else:
        motor.stop()
        print("Motor Stop")

def action_right_joystick_x(value):
    mapped_speed_s = map_value(value, -34000, 34000, -90, 90)
    print(f"Action: Right joystick X-axis moved to {mapped_speed_s}")
    servo.angle = mapped_speed_s


# def action_right_joystick_y(value):
#     mapped_speed = map_value(value, -32767, -1048, -90, 90)
#     print(f"Action: Right joystick y-axis moved to {mapped_speed}")


async def handle_gamepad():
    async for event in gamepad.async_read_loop():
        print(event)
        if event.type == ecodes.EV_KEY:
            if event.code in button_actions:
                if event.value == 1:
                    button_actions[event.code]()
        elif event.type == ecodes.EV_ABS and event.code in abs_actions:
            # Call the function for the axis with its value
            abs_actions[event.code](event.value)

            
async def handle_camera():
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("USB Camera", frame)

        cv2.waitKey(1)
        await asyncio.sleep(0.01)

button_actions = {
    ecodes.BTN_A: action_button_a,
    ecodes.BTN_B: action_button_b,
    ecodes.BTN_X: action_button_x,
    ecodes.BTN_Y: action_button_y,
    ecodes.BTN_Z: action_button_cap,
}

abs_actions = {
    ecodes.ABS_X: action_left_joystick_x,
    ecodes.ABS_Y: action_left_joystick_y,
    ecodes.ABS_RX: action_right_joystick_x,
}

async def main():
    # Run both tasks concurrently
    await asyncio.gather(
        handle_gamepad()
        # handle_camera(),
    )

# Run the main async loop
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program interrupted.")
