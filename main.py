import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import credentials
from datetime import datetime
import time

# Initialize variables
modeType = 1  # Initialize to 1 (2.png - scanning mode)
attendance_marked = False  # Track if attendance was marked in this session
transition_time = None  # Track when mode changes occur
DELAY_DURATION = 2  # Seconds to show each transition screen
current_sequence = None  # Track the current transition sequence

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendanceproject-b8993-default-rtdb.firebaseio.com/",
    'storageBucket': "attendanceproject-b8993.appspot.com"
})

bucket = storage.bucket()

def update_attendance(student_id):
    ref = db.reference(f'Students/{student_id}')
    student_info = ref.get()
    
    if student_info is None:
        print(f"Error: Student {student_id} not found in database")
        return False
    
    # Update attendance count and timestamp
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_attendance = student_info.get('total_attendance', 0) + 1
    
    # Update the database
    ref.update({
        'total_attendance': new_attendance,
        'last_attendance_taken': current_time
    })
    
    print(f"Attendance updated successfully. New count: {new_attendance}")
    return True

try:
    # Camera setup
    capture = cv2.VideoCapture(0)
    capture.set(3, 640)
    capture.set(4, 480)

    screenBg = cv2.imread('Resources/background.png')

    # Import mode images
    modeFolderPath = 'Resources/Modes'
    modePathList = os.listdir(modeFolderPath)
    imgModeList = []
    for path in sorted(modePathList):  # Sort to ensure consistent order
        imgModeList.append(cv2.imread(os.path.join(modeFolderPath, path)))

    # Load encodings
    file = open("EncodingsFile.p", 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, studentIds = encodeListKnownWithIds

    # Main loop
    while True:
        success, img = capture.read()
        if not success:
            print("Failed to grab frame")
            break

        imageSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imageSmall = cv2.cvtColor(imageSmall, cv2.COLOR_BGR2RGB)

        # Update the background with camera feed
        screenBg[162:162 + 480, 55:55 + 640] = img
        screenBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        # Only detect faces if we're not in a transition sequence
        if current_sequence is None:
            faceCurrentFrame = face_recognition.face_locations(imageSmall)
            encodeCurrentFrame = face_recognition.face_encodings(imageSmall, faceCurrentFrame)

            if faceCurrentFrame:
                for encodeFace, faceLocation in zip(encodeCurrentFrame, faceCurrentFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
                    matchIndex = np.argmin(faceDistance)

                    if matches[matchIndex]:
                        y1, x2, y2, x1 = faceLocation
                        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                        bbox = 55 + x1, 162 + y1, x2-x1, y2-y1
                        screenBg = cvzone.cornerRect(screenBg, bbox, rt=0)
                        id = studentIds[matchIndex]

                        if not attendance_marked:
                            print("Registered Student Detected.")
                            print(studentIds[matchIndex])
                            
                            if update_attendance(id):
                                # Start transition sequence
                                current_sequence = [
                                    (2, "Attendance Marked"),  # 3.png
                                    (0, "Ready for Next Scan"),  # 1.png
                                    (1, "Back to Scanning")  # 2.png
                                ]
                                transition_time = time.time()
                                modeType = current_sequence[0][0]
                                print(f"Showing: {current_sequence[0][1]}")
                                attendance_marked = True
                                
                                studentInfo = db.reference(f'Students/{id}').get()
                                print(studentInfo)
                        else:
                            modeType = 3  # Show 4.png (attendance already taken)
            else:
                # Only reset if we're not in a transition sequence
                if not current_sequence:
                    modeType = 1
                    attendance_marked = False

        # Handle transition sequence
        if current_sequence:
            current_time = time.time()
            if current_time - transition_time >= DELAY_DURATION:
                current_sequence.pop(0)  # Remove the current mode
                
                if current_sequence:  # If there are more modes to show
                    modeType = current_sequence[0][0]
                    print(f"Showing: {current_sequence[0][1]}")
                    transition_time = current_time
                else:  # End of sequence
                    current_sequence = None
                    modeType = 1  # Back to scanning mode
                    print("Back to scanning mode")

        cv2.imshow("Face Attendance System", screenBg)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Cleanup
    capture.release()
    cv2.destroyAllWindows()
    print("Camera released and windows closed")