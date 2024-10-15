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


# Uncomment the following main function to run the hand detection
# def main():
#     pTime = 0  # Previous time for FPS calculation
#     cap = cv2.VideoCapture(0)  # Open the webcam
#     detector = HandDetector()  # Create an instance of HandDetector
    
#     # Check if the video stream opened successfully
#     if not cap.isOpened():
#         print("Error: Could not open video stream.")
#         return

#     while True:  # Continuous loop to process frames
#         success, img = cap.read()  # Capture a frame from the webcam
#         if not success:
#             print("Error: Failed to capture image.")
#             break

#         img = detector.findHands(img)  # Detect hands in the image
#         lmList = detector.findPosition(img)  # Get the landmark positions
#         if lmList:  # If landmarks are found
#             print(lmList[4])  # Print the coordinates of the 5th landmark (thumb tip)

#         cTime = time.time()  # Get current time
#         fps = 1 / (cTime - pTime)  # Calculate frames per second
#         pTime = cTime  # Update previous time

#         # Display FPS on the image
#         cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

#         cv2.imshow("Image", img)  # Show the processed image

#         # Break the loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()  # Release the webcam
#     cv2.destroyAllWindows()  # Close all OpenCV windows


# if __name__ == "__main__":  # Entry point for the application
#     main()  # Run the main function
