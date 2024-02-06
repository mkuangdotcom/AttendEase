import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json",)

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendanceproject-b8993-default-rtdb.firebaseio.com/",
    'storageBucket': "attendanceproject-b8993.appspot.com"
})


folderPathImages = 'Images'
listPathImages = os.listdir(folderPathImages)
imgListImages = []

#Extracting Student Ids
studentIDs = []
print(listPathImages)

for path in listPathImages:
    imgListImages.append(cv2.imread(os.path.join(folderPathImages,path)))
    #taking only the first element after splitting text and storing 
    #that into student IDs
    studentIDs.append(os.path.splitext(path)[0])

    # you're already going through the images one by one here, so you might as well use this loop to store them as well
    # join together the full filename using folderPathImages as well as each individual path
    fileName = f'{folderPathImages}/{path}'
    # the following code will retrieve a reference to your established cloud storage
    bucket = storage.bucket()
    # a reference to a specific object is created
    blob = bucket.blob(fileName)
    # the file with the fileName is uploaded to reference "blob" created in your cloud storage
    blob.upload_from_filename(fileName)


def generateEncodings(images):
    encodingsList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)       # converting color format RGB (default BGR)
        encode = face_recognition.face_encodings(img)[0]    
        encodingsList.append(encode)

    return encodingsList

encodingsListKnown = generateEncodings(imgListImages)
encodingsListWithIDs = [encodingsListKnown, studentIDs]

# opening a new file called EncodingsFile.p in WRITE MODE
encodingFile = open("EncodingsFile.p","wb")
# using pickle to dump into the file your encodings list
pickle.dump(encodingsListWithIDs, encodingFile)
# closing the file 
encodingFile.close()

    
print(studentIDs)