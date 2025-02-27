
# pinch

This project allows you to control the mouse cursor using your hand gestures through a webcam. It uses **OpenCV**, **MediaPipe**, and **ctypes** to detect the hand, smooth the movements, and simulate mouse actions. When the thumb and index finger get close, a mouse click is triggered.

## Features

- **Hand Tracking**: Uses MediaPipe to detect and track the position of the hand and its fingers in real-time.
- **Mouse Movement**: The mouse cursor follows the thumb's position, with sensitivity adjusted by a scale factor.
- **Mouse Click Simulation**: When the thumb and index finger are close enough (threshold distance), the left mouse button is clicked.
- **Smoothing**: The mouse movement is smoothed to avoid jerky movements.

## Requirements

To run the project, you need the following libraries:

- **OpenCV**: For capturing the webcam feed and processing the images.
- **MediaPipe**: For hand tracking and landmark detection.
- **ctypes**: For interacting with Windows APIs to control the mouse cursor.

### Install Dependencies

Use the following commands to install the required Python libraries:

```bash
pip install opencv-python mediapipe
```

## Setup

1. **Webcam**: Make sure you have a webcam connected to your computer.
2. **Permissions**: On Windows, the script uses the `windll` library to access system metrics and control the mouse. Make sure you are running the script on a Windows system.

## How It Works

### Hand Tracking

- The script uses **MediaPipe Hands** to detect the hand landmarks.
- The thumb (landmark 4) and index finger (landmark 8) are tracked to control the mouse position.
- The positions are scaled and smoothed for smoother cursor movement.

### Mouse Control

- The `user32.SetCursorPos` function is used to move the mouse cursor to the calculated position.
- If the distance between the thumb and index finger is below a certain threshold (65 pixels), it simulates a mouse click using `user32.mouse_event`.

### Smoothing

- A low-pass filter is applied to the cursor's movement to make the tracking smoother and more responsive.

### Screen Size

- The screen size is automatically detected using `windll.user32.GetSystemMetrics`.
- The cursor is constrained to the screen bounds, ensuring it does not move off-screen.

## How to Run

1. **Run the Script**: Execute the script directly in your terminal or an IDE.
   ```bash
   python pinch.py
   ```

2. **Pointing**: The mouse cursor will follow your thumb’s position.
   
3. **Clicking**: When your thumb and index finger get close to each other (within 65 pixels), a click will be triggered.

4. **Exit**: To stop the program, simply close the terminal or interrupt the execution.

## Adjustments

- **Sensitivity**: You can adjust the sensitivity of the hand tracking by changing the `scale_factor` variable. A higher value increases the cursor's movement sensitivity.
  
- **Smoothing Factor**: The smoothness of the cursor movement can be controlled via the `SMOOTHING_FACTOR` variable. A value between 0 and 1 (e.g., `0.4`) determines how much smoothing is applied.

## Troubleshooting

- **No Hand Detection**: Ensure your hand is clearly visible to the webcam. If the hand is out of frame or too far from the camera, the hand might not be detected.
- **Low Sensitivity**: Try increasing the `scale_factor` to make the cursor movement more sensitive to your hand's position.
- **No Clicks**: If the thumb and index finger are not registering clicks, try adjusting the threshold distance by changing the `distance < 65` condition in the code.

## License
This project is open-source. Feel free to modify and improve it!

