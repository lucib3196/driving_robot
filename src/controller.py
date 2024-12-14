from evdev import InputDevice, categorize, ecodes
from gpiozero import Motor, PWMOutputDevice



# Replace with the path of your controller (e.g., /dev/input/eventX)
controller_path = "/dev/input/event6"

try:
    gamepad = InputDevice(controller_path)
    print(f"Connected to: {gamepad.name}")
except FileNotFoundError:
    print("Controller not found. Check the device path.")

# Define the motor
# enable_pin1 = PWMOutputDevice(15)
motor = Motor(forward=4, backward=14,enable=22)
# Define Key Actions
# Each button is associated to a code ex Button y is associated with code 308
key_actions = {
    ecodes.BTN_A: "Button A pressed",
    ecodes.BTN_B: "Button B pressed",
    ecodes.BTN_X: "Button X pressed",
    ecodes.BTN_Y: "Button Y pressed",
    ecodes.BTN_TR: 'Right Trigger 1 pressed',
    ecodes.BTN_TR2: 'Right Trigger 2 pressed',
    ecodes.BTN_TL: 'Right Trigger 1 pressed',
    ecodes.BTN_TL2: 'Right Trigger 2 pressed',
    ecodes.BTN_Z: 'Capture pressed',
    ecodes.BTN_START: "Start button pressed",
    ecodes.BTN_SELECT: "Select button pressed",
}

abs_actions = {
    # ecodes.ABS_X: "Left joystick X-axis moved",
    # ecodes.ABS_Y: "Left joystick Y-axis moved",
    # ecodes.ABS_RX: "Right joystick X-axis moved",
    # ecodes.ABS_RY: "Right joystick Y-axis moved",
    # ecodes.ABS_Z: "Left trigger pressed",
    # ecodes.ABS_RZ: "Right trigger pressed",
}
JOYSTICK_THRESHOLD = 10000

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:  # Button press/release
        if event.code in key_actions:
            if event.value == 1:
                print(key_actions[event.code])
            elif event.value == 0:
                print(f"{key_actions[event.code]} released")
        else:
            print(f"Unknown key event: {event.code} must add {categorize(event)}")
    
    
    elif event.type == ecodes.EV_ABS:  # Joystick or trigger movement
        if event.code in abs_actions:
            action = abs_actions[event.code]
            # Position of the joystick
            action_value = event.value 
            print(f"{action}: {action_value}")
            if event.code == ecodes.ABS_Y:
                print('should move motor')
                if action_value <128 - JOYSTICK_THRESHOLD:
                    motor.forward()
                    print("Motor moving forward")
                elif action_value >128 + JOYSTICK_THRESHOLD:
                    motor.backward()
                    print("Motor moving backward")
            
        else:
            print(f"Unknown ABS event: {event.code}, value: {event.value}")
