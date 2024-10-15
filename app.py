from flask import Flask, jsonify, render_template, Response
import cv2
import HandTrackingModule as htm

app = Flask(__name__)

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]

totalFingers = 0

def generate_frames():
    global totalFingers
    try:
        while True:
            success, img = cap.read()
            if not success:
                break
            else:
                img = detector.findHands(img)
                lmList = detector.findPosition(img, draw=False)
                img = cv2.flip(img, 1)

                if len(lmList) != 0:
                    fingers = []
                    if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    for id in range(1, 5):
                        if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    totalFingers = fingers.count(1) 


                ret, buffer = cv2.imencode('.jpg', img)
                img_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
                
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/finger_count')
def finger_count():
    return jsonify(count=totalFingers)

if __name__ == "__main__":
    app.run(debug=True)
