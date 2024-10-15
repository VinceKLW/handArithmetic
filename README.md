# handArithmetic

handArithmetic is a web application that utilizes hand gesture recognition to help users solve elementary math questions. The application uses a camera to detect the number of fingers being held up, translating hand gestures into numerical inputs for simple arithmetic operations.

## Features

- **Webcam Integration**: Stream live video feed to detect hand gestures.
- **Finger Counting**: Count the number of fingers displayed by the user.
- **Elementary Math Questions**: Pose simple math problems (e.g., addition, subtraction) and validate user input via gestures.
- **User-Friendly Interface**: Easy to use and visually appealing layout.

## Technologies Used
- **Flask**: A lightweight WSGI web application framework in Python for the backend.
- **OpenCV**: A computer vision library for capturing and processing images from the webcam.
- **MediaPipe**: A library for hand tracking and gesture recognition.
- **HTML/CSS**: For the frontend user interface.
- **JavaScript**: For handling user interactions and dynamic content updates.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/VinceKLW/handArithmetic.git
   cd handArithmetic

2. Install the required packages:
    pip install -r requirements.txt

3. Run the application:
    python app.py

4. Open your web browser and navigate to:
    http://127.0.0.1:5000