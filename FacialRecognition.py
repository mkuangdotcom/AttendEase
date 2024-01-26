
# python library to import and used here
import cv2
import os
capture = cv2.VideoCapture(0)

# width capturing
capture.set(3, 1280)
# height capturing
capture.set(4, 720)
# state variable
backgroundImg = cv2.imread('Resources/Background.png')

folderPathMode = 'Resources/Modes'
listPathMode = os.listdir(folderPathMode)
imgListMode = []

for path in listPathMode:
    imgListMode.append(cv2.imread(os.path.join(folderPathMode, path)))
    
print(listPathMode)

# conditional capture  
while True:
    success, image = capture.read()

    # webcam over the background
    image = cv2.resize(image,(640,480))
    backgroundImg[162: 162+480, 55: 55+640] = image
    backgroundImg[44: 44+633, 808: 808+414 ] = imgListMode[0]

    # showing a window for webcam 
    # cv2.imshow("My Webcam", image)

    # showing window for background image
    cv2.imshow("Attendance System", backgroundImg)
    cv2.waitKey(1)
