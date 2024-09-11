import threading
import cv2
from deepface import DeepFace

# Initialize video capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0
face_match = False

# Load reference image
reference_img = cv2.imread("C:\intern\intern\assets\1.jpg")
if reference_img is None:
    raise ValueError("Reference image could not be loaded. Check the file path and ensure the image exists.")

def check_face(frame):
    global face_match
    try:
        # DeepFace requires image paths or file-like objects
        result = DeepFace.verify(frame, reference_img)
        face_match = result['verified']
    except Exception as e:
        print(f"Error during face verification: {e}")
        face_match = False

while True:
    ret, frame = cap.read()
    if ret:
        if counter % 30 == 0:
            # Check face in the main thread
            check_face(frame.copy())
            counter += 1
        
        # Display match status
        if face_match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        # Display the frame
        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
