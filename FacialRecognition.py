import cv2
import os

# Captures video (0 for )
capture  = cv2.VideoCapture(0) 

capture.set(3, 1280) #Window size (3 for width)
capture.set(4, 720)  #Window size (4 for height)
backgroundImg = cv2.imread(r'Resources/Background.png')

folderPathMode = 'Resources/Modes'
listPathMode = os.listdir(folderPathMode)
imageListMode = []


for path in listPathMode:
    imageListMode.append(cv2.imread(os.path.join(folderPathMode, path)))

print(imageListMode)

while True:
    success, image = capture.read()

    image = cv2.resize(image, (640, 480))

    #onto the position of 162:162 + 480, 55:55 + 640, you are pasting your web cam over the background image
    backgroundImg[162:162 + 480, 55:55 + 640] = image

    backgroundImg[44:44+633, 808:808 +414] = imageListMode[0]


    # show a window for your webcam
    # cv2.imshow("My WebCam", image)

    # show a window for your system
    cv2.imshow("Attendance System", backgroundImg)
    cv2.waitKey(1)
