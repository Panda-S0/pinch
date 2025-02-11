from ctypes import windll
import cv2
from mediapipe import solutions
from math import hypot
from time import sleep

# Initialize the hand solution
mp_hands = solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Open the default camera
video_cap = cv2.VideoCapture(0)
video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Lower resolution for better performance
video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Get screen size
user32 = windll.user32
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print('width: ', screen_width, '\nheight:', screen_height)
mid_x_screen = screen_width // 2
mid_y_screen = screen_height // 2
scale_factor = 1.2  # the higher the number, the higher the sensitivity

# Smoothing variables
SMOOTHING_FACTOR = 0.4  # Adjust this value (0 < SMOOTHING_FACTOR < 1)
Smoothed = [mid_x_screen,mid_y_screen]

clicking = False
frame_time = 1 / 60  # change the 30 to the number of fps you need

while True:
    sleep(frame_time)  # Delay to limit FPS

    # Read a frame from the camera and flip it
    success, img = video_cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)

    # Process hand landmarks
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Check if a hand is detected
    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0].landmark

        # Extract raw coordinates
        raw_index_x = landmarks[8].x * screen_width
        raw_index_y = landmarks[8].y * screen_height
        raw_thumb_x = landmarks[4].x * screen_width
        raw_thumb_y = landmarks[4].y * screen_height

        # Scale the raw coordinates
        raw_index_x = mid_x_screen + (raw_index_x - mid_x_screen) * scale_factor
        raw_index_y = mid_y_screen + (raw_index_y - mid_y_screen) * scale_factor
        raw_thumb_x = mid_x_screen + (raw_thumb_x - mid_x_screen) * scale_factor
        raw_thumb_y = mid_y_screen + (raw_thumb_y - mid_y_screen) * scale_factor

        # Apply low-pass filter to smooth the positions and ensure they are within screen bounds
        smoothed_x = max(0, min(smoothed_x * (1 - SMOOTHING_FACTOR) + raw_thumb_x * SMOOTHING_FACTOR, screen_width))
        smoothed_y = max(0, min(smoothed_y * (1 - SMOOTHING_FACTOR) + raw_thumb_y * SMOOTHING_FACTOR, screen_height))

        # Calculate distance between thumb and index finger
        distance = hypot(smoothed_x - raw_index_x, smoothed_y - raw_index_y)

        # Move mouse to the thumb position
        user32.SetCursorPos(int(smoothed_x), int(smoothed_y))

        # Handle mouse click
        if distance < 65:
            if not clicking:
                clicking = True
                user32.mouse_event(2, 0, 0, 0, 0)  # Left button down
        else:
            if clicking:
                clicking = False
                user32.mouse_event(4, 0, 0, 0, 0)  # Left button up

    else:
        if clicking:
            clicking = False
            user32.mouse_event(4, 0, 0, 0, 0)  # Left button up

video_cap.release()