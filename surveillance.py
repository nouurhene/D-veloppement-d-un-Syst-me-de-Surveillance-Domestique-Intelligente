import smtplib
import cv2
import numpy as np
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'koukinourhen03@gmail.com'
EMAIL_PASSWORD = 'qzsk bgmn enms cdbu'
RECIPIENT_EMAIL = 'nourhenekouki016@gmail.com'

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("SMTP connection successful!")
except Exception as e:
    print(f"Error: {e}")


# Function to compare if the image is already saved
def is_face_saved(unknown_face, unknown_faces_dir):
    for filename in os.listdir(unknown_faces_dir):
        saved_image = cv2.imread(os.path.join(unknown_faces_dir, filename), cv2.IMREAD_GRAYSCALE)
        if saved_image is not None:
            # Resize the unknown face to match the saved image's size
            resized_unknown_face = cv2.resize(unknown_face, (saved_image.shape[1], saved_image.shape[0]))

            # Check similarity between the resized unknown face and saved image
            diff = cv2.absdiff(saved_image, resized_unknown_face)
            if np.mean(diff) < 10:  # This threshold can be adjusted based on similarity needed
                return True
    return False

# Function to save the face and send an email
def handle_unknown_face(frame, x, y, w, h):
    unknown_faces_dir = "/home/nounou/surveillance_system/unknown_faces"
    if not os.path.exists(unknown_faces_dir):
        os.makedirs(unknown_faces_dir)
    
    # Extract the detected face from the frame
    unknown_face = gray_frame[y:y+h, x:x+w]

    # Check if the face is already saved
    if not is_face_saved(unknown_face, unknown_faces_dir):
        # Save the unknown face image with a timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        face_path = os.path.join(unknown_faces_dir, f"unknown_face_{timestamp}.jpg")
        cv2.imwrite(face_path, unknown_face)

        # Send an email with the new unknown face
        send_image_email(frame[y:y+h, x:x+w])  # The original frame with the colored face
        print(f"Unknown face saved and email sent: {face_path}")
    else:
        print("Unknown face detected, but email not sent as the face is already saved.")



def send_image_email(image):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = 'Unknown Face Detected'

    body = 'An unknown face was detected. Please find the attached image.'
    msg.attach(MIMEText(body, 'plain'))

    #Convert image to bytes
    img_bytes = cv2.imencode('.jpg', image)[1].tobytes()
    img = MIMEImage(img_bytes, name='unknown_face.jpg')
    msg.attach(img)

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())


# Load the Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Dictionary to store face encodings and labels
known_faces = {}
labels = []
label_names = []

def load_and_encode_faces(directory):
    global labels
    global label_names
    face_count = 0 
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join(directory, filename)
            name = os.path.splitext(filename)[0]  # Name without extension
            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                face = image[y:y+h, x:x+w]
                if name not in label_names:
                    known_faces[name] = face
                    labels.append(len(label_names))
                    label_names.append(name)
                    face_count += 1  # Increment face count    

    print(face_count)
    print(labels)
    print(label_names)

# Load known faces
load_and_encode_faces("known_faces")

# Train the recognizer
faces = [known_faces[name] for name in known_faces]
recognizer.train(faces, np.array(labels))

# Initialize the webcam
cap = cv2.VideoCapture(0)

recording = False
video_writer = None
frames_since_detection = 0

def create_video_directory():
    today = datetime.now().strftime('%Y-%m-%d')
    directory = f'videos/{today}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

video_directory = create_video_directory()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    detected_unknown = False

    for (x, y, w, h) in faces:
        face = gray_frame[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face)

        if confidence < 70:
            name = label_names[label]
            print(f"Recognized: {name} with confidence: {confidence}")
        else:
            name = 'Unknown'
            detected_unknown = True
            print("Unknown face detected")
            #send_image_email(frame[y:y+h, x:x+w])
            handle_unknown_face(frame, x, y, w, h)

            if not recording:
                recording = True
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                video_path = os.path.join(video_directory, f'unknown_face_{timestamp}.avi')
                video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame.shape[1], frame.shape[0]))
            break

        # Draw a rectangle around the face and put the label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if detected_unknown:
        if video_writer is not None:
            video_writer.write(frame)
            frames_since_detection = 0
    elif recording:
        frames_since_detection += 1
        if frames_since_detection >= 20 * 10:  # Record for 10 seconds
            recording = False
            video_writer.release()
          
            video_directory = create_video_directory()  # Create a new directory for the next day
            video_path = os.path.join(video_directory, f'unknown_face_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.avi')

    # Display the video with annotations
    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
