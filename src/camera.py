import cv2

# 0 refers to the first camera or webcam
camera = cv2.VideoCapture(0)

print("Press 'c' to capture an image. Press 'q' to quit.")

while True:
    # Read a frame
    ret, frame = camera.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Display the frame
    cv2.imshow("USB Camera", frame)

    key_press = cv2.waitKey(1) & 0xFF

    # Press 'q' to quit
    if key_press == ord('c'):
        filename = 'captured_image.jpg'
        cv2.imwrite(filename,frame)
        print(f"Image captured and saved as {filename}")
    elif key_press == ord('q'):  # If 'q' is pressed, quit the loop
        print("Exiting...")
        break


# Release the camera and close the window
camera.release()
cv2.destroyAllWindows()