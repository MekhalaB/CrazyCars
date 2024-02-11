import cv2
import cvzone
import pyautogui
from cvzone.HandTrackingModule import HandDetector

# Initialize video capture
cap = cv2.VideoCapture(0)

# Create hand detector object
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Function to check for open palm or closed fist
def check_gesture(lmList):
    dist_index = lmList[4][1] - lmList[8][1]
    dist_pinky = lmList[4][1] - lmList[20][1]
    threshold_open = 15
    threshold_closed = 50
    if dist_index > threshold_open and dist_pinky > threshold_open:
        return "Open Palm"
    elif dist_index < threshold_closed and dist_pinky < threshold_closed:
        return "Closed Fist"
    else:
        return "Unknown Gesture"

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Detect hands
    hands, img = detector.findHands(img)

    left_gesture = None
    right_gesture = None

    # Iterate over detected hands
    for hand in hands:
        lmList = hand["lmList"]
        gesture = check_gesture(lmList)

        # Determine hand side
        if hand["type"] == "Left":
            left_gesture = gesture
        else:
            right_gesture = gesture

        # Draw bounding box
        #cv2.rectangle(img, (hand["bbox"][0], hand["bbox"][1]), (hand["bbox"][2], hand["bbox"][3]), (255, 0, 255), 2)

        # Display gesture text
        cv2.putText(img, gesture, (hand["bbox"][0], hand["bbox"][1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    # Keyboard control based on gestures
    if left_gesture == "Open Palm" and right_gesture == "Closed Fist":
        for i in range(5):
            pyautogui.keyDown('left')
        pyautogui.keyUp('left')
        # Left arrow key
    elif left_gesture == "Closed Fist" and right_gesture == "Open Palm":
        for i in range(5):
            pyautogui.keyDown('right')
        pyautogui.keyUp('right')  # Right arrow key
    elif left_gesture == "Open Palm" and right_gesture == "Open Palm":
        for i in range(5):
            pyautogui.keyDown('up')
        pyautogui.keyUp('up')
        # Forward arrow key
    elif left_gesture == "Closed Fist" and right_gesture == "Closed Fist":
        for i in range(5):
            pyautogui.keyDown('down')
        pyautogui.keyUp('down')# Backward arrow key

    # Display the image
    cv2.imshow("Hand Gesture Control", img)

    # Exit on 'q' key press
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
