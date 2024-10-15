import cv2  # Import OpenCV for image processing
import mediapipe as mp  # Import MediaPipe for hand tracking
import time  # Import time for FPS calculation


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # Initialize parameters for hand detection
        self.mode = mode  # Static image mode or video mode
        self.maxHands = maxHands  # Maximum number of hands to detect
        self.detectionCon = detectionCon  # Minimum detection confidence
        self.trackCon = trackCon  # Minimum tracking confidence

        # Initialize MediaPipe Hands module
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        # Initialize MediaPipe drawing utilities
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        # Convert the image from BGR to RGB format
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process the image to find hands
        self.results = self.hands.process(imgRGB)

        # If hands are detected, draw landmarks on the image
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)  # Draw hand connections
        return img  # Return the modified image

    def findPosition(self, img, handNo=0, draw=True):
        # Find the position of landmarks of a specific hand
        lmList = []  # List to store landmark positions
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]  # Select the specified hand
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape  # Get image dimensions
                cx, cy = int(lm.x * w), int(lm.y * h)  # Calculate landmark coordinates
                lmList.append([id, cx, cy])  # Append ID and coordinates to the list
        return lmList  # Return the list of landmarks