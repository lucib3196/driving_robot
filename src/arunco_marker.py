# This script detects ArUco markers, annotates their corner coordinates, and visualizes their 3D pose by drawing frame axes.

# Features:
# 1. **Corner Coordinate Annotation**:
#    - Detects the top-left, top-right, bottom-right, and bottom-left corners of the marker.
#    - Displays the coordinates of each corner on the image.

# 2. **3D Frame Axes Visualization**:
#    - Calculates the marker's 3D pose using camera calibration parameters.
#    - Draws the X (red), Y (green), and Z (blue) axes on the marker using `cv2.aruco.drawAxis`.

# 3. **Camera Calibration**:
#    - Uses preloaded `camera_matrix` and `distortion_coeffs` for undistortion and pose estimation.

# 4. **Live Camera Feed**:
#    - Continuously displays the camera feed with annotated markers and 3D axes.
#    - Press 'q' to quit the feed.

# Dependencies:
# - OpenCV (`cv2`)
# - Camera calibration files (`cameraMatrix.pkl`, `dist.pkl`) for accurate pose estimation.


from math import dist
import cv2
import cv2.aruco as aruco
import numpy as np
import pickle


def initialize_camera_live(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Unable to access camera with index {camera_index}")
        exit()
    return cap

def detect_aruco_marker(image_frame, camera_matrix, distortion_coeffs, aruco_dict_type=cv2.aruco.DICT_6X6_250):
    gray = image_frame
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, rejected = detector.detectMarkers(gray)
    print("Detected Marks:", ids)

    if ids is not None:
        for marker_corner, marker_id in zip(corners, ids):
            print(f"[INFO] Marker ID: {marker_id}")

            # Reshape corners for easier handling
            corners_abcd = marker_corner.reshape((4, 2))
            (top_left, top_right, bottom_right, bottom_left) = corners_abcd

            # Convert corner points to integers for drawing
            top_left = (int(top_left[0]), int(top_left[1]))
            top_right = (int(top_right[0]), int(top_right[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
            bottom_left = (int(bottom_left[0]), int(bottom_left[1]))

            # Draw lines between corners
            cv2.line(gray, top_left, top_right, (0, 255, 0), 2)
            cv2.line(gray, top_right, bottom_right, (0, 255, 0), 2)
            cv2.line(gray, bottom_right, bottom_left, (0, 255, 0), 2)
            cv2.line(gray, bottom_left, top_left, (0, 255, 0), 2)

            # Draw corner coordinates as text
            cv2.putText(gray, f"{top_left}", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            cv2.putText(gray, f"{top_right}", top_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            cv2.putText(gray, f"{bottom_right}", bottom_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            cv2.putText(gray, f"{bottom_left}", bottom_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            # Estimate pose of the marker
            marker_length = 0.1  # Replace with the real marker size in meters
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corner, marker_length, camera_matrix, distortion_coeffs)

            # Draw the axes on the marker
            cv2.drawFrameAxes(gray, camera_matrix, distortion_coeffs, rvec, tvec, marker_length)

    return gray


def define_camera_settings():
    with open("cameraMatrix.pkl", "rb") as file:
        camera_matrix = pickle.load(file)

    with open("dist.pkl", "rb") as dist_file:
        camera_distortion = pickle.load(dist_file)

    return camera_matrix, camera_distortion


def main():
    # Load camera settings
    camera_matrix, camera_distortion = define_camera_settings()
    cap = initialize_camera_live(camera_index=1)

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from the camera.")
            break

        # Undistort the frame
        h, w = frame.shape[:2]
        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(
            camera_matrix, camera_distortion, (w, h), 1, (w, h)
        )
        undistorted_frame = cv2.undistort(
            frame, camera_matrix, camera_distortion, None, new_camera_mtx
        )

        x, y, w, h = roi
        undistorted_frame = undistorted_frame[y : y + h, x : x + w]

        # Detect ArUco markers and annotate corners and axes
        frame_with_markers = detect_aruco_marker(undistorted_frame, camera_matrix, camera_distortion)

        cv2.imshow("ArUco Marker Detection with Corner Coordinates and Axes", frame_with_markers)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
