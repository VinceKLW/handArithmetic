from flask import Flask, jsonify, render_template, Response
import cv2
import HandTrackingModule as htm  # Import a custom hand tracking module

# Create a Flask application instance
app = Flask(__name__) 

# Set the width and height of the webcam feed
wCam, hCam = 640, 480

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Set the width of the frame
cap.set(4, hCam)  # Set the height of the frame

# Create an instance of the hand detector with a specified detection confidence
detector = htm.HandDetector(detectionCon=0.75)

# Define tip IDs for the fingers (index of landmark positions)
tipIds = [4, 8, 12, 16, 20]

# Initialize a variable to keep track of the total fingers detected
totalFingers = 0

def generate_frames():
    global totalFingers  # Use the global variable for totalFingers
    try:
        while True:  # Continuous loop for frame generation
            success, img = cap.read()  # Capture frame from webcam
            if not success:  # Check if frame was captured successfully
                break
            else:
                # Process the captured image to find hands and landmarks
                img = detector.findHands(img)
                lmList = detector.findPosition(img, draw=False)  # Get landmark positions
                img = cv2.flip(img, 1)  # Flip the image horizontally for a mirror effect

                if len(lmList) != 0:  # Check if any landmarks were detected
                    fingers = []  # List to store the state of each finger (up or down)

                    # Check if the thumb is raised
                    if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                        fingers.append(1)  # Thumb is up
                    else:
                        fingers.append(0)  # Thumb is down

                    # [0,0,0,0,0]

                    # Check for the other fingers (1 to 4)
                    for id in range(1, 5):
                        if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                            fingers.append(1)  # Finger is up
                        else:
                            fingers.append(0)  # Finger is down

                    # Count the number of fingers that are up
                    totalFingers = fingers.count(1) 

                # Encode the processed image as a JPEG byte array
                ret, buffer = cv2.imencode('.jpg', img)
                img_bytes = buffer.tobytes()  # Convert to bytes
                # Yield the image as part of a multipart response
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
                
    except Exception as e:  # Handle any exceptions that occur during processing
        print(f"Error occurred: {e}")
    finally:
        # Release the webcam and destroy any OpenCV windows when done
        cap.release()
        cv2.destroyAllWindows()

@app.route('/')  # Route for the homepage
def index():
    return render_template('index.html')  # Render the index.html template

@app.route('/video_feed')  # Route for the video feed
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # Stream video frames

@app.route('/finger_count')  # Route to get the finger count
def finger_count():
    return jsonify(count=totalFingers)  # Return the total fingers detected as JSON

if __name__ == "__main__":  # Entry point for the application
    app.run(debug=True)  # Run the app in debug mode
