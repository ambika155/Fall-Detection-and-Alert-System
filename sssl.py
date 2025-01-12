import cv2
import mediapipe as mp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils


# Email Alert Function
def send_alert():
    sender_email = "ambikaacharya155@gmail.com"  # Your email
    receiver_email = "anjalic1402@gmail.com"    # Receiver's email
    password = "njeh ityz zyxq dlgk"  # Use an app-specific password for better security
    
    subject = "Fall Detected!"
    body = "A fall has been detected. Please check immediately."
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)  # Logging into Gmail with the app password
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Alert email sent!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Open webcam
cap = cv2.VideoCapture(0)
fall_detected = False
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Convert to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)
    
    if results.pose_landmarks:
        # Draw landmarks on the frame
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Get key points for detection
        landmarks = results.pose_landmarks.landmark
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        
        # Calculate vertical alignment
        vertical_alignment = abs(nose.y - hip.y)
        if vertical_alignment < 0.1:  # Threshold for fall detection
            fall_detected = True
            print("Fall detected!")
    
    if fall_detected:
        send_alert()
        fall_detected = False  # Reset to avoid repeated alerts

    # Display the video
    cv2.imshow('Fall Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
