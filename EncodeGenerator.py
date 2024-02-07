import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json",)
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://attendanceproject-b8993-default-rtdb.firebaseio.com/",
    'storageBucket': "attendanceproject-b8993.appspot.com"
})

ref = db.reference("Students")
# Python dictionary
data = {
    "TP011111":
    {
        "name" : "Lee Wen Han",
        "major" : "CS(AI)",
        "starting_year" : 2021,
        "total_attendance" : 20,
        "grades" : "A",
        "year" : 2,
        "last_attendance_taken" : "2024-01-26 16:10:30",
    },
    "TP012345":
    {
        "name" : "Foo Ming Kuang",
        "major" : "CS(SE)",
        "starting_year" : 2023,
        "total_attendance" : 10,
        "grades" : "A+",
        "year" : 2,
        "last_attendance_taken" : "2024-01-26 16:10:30",
    },
    "TP063338":{
        "name": "Dalton Gan",
        "major": "SE",
        "starting_year": 2024,
        "total_attendance": 4,
        "standing": "A++",
        "year": 2,
        "last_attendance_time": "2024-01-02 12:06:02"
    },
    "TP068713":{
        "name": "Suzanne Lai",
        "major": "AI",
        "starting_year": 2022,
        "total_attendance": 10,
        "standing": "A",
        "year": 2,
        "last_attendance_time": "2024-01-02 15:09:02"
    },
    "TP088888":{
        "name": "Karina",
        "major": "Slay",
        "starting_year": 2024,
        "total_attendance": 10,
        "standing": "A+",
        "year": 1,
        "last_attendance_time": "2024-01-09 06:06:06"
    },
    "TP054321":{
        "name": "Elon Musk",
        "major": "Ruining Lives",
        "starting_year": 1995,
        "total_attendance": 10,
        "standing": "A+",
        "year": 29,
        "last_attendance_time": "2024-01-08 13:10:30"
    },
}

# This is how to "unzip a dictionary in Python"
# writing the dictionary details into the realtime database
for key, value in data.items():
    # Storing the vaue in the dictionary "children" for the key in the ref you created ("Students")
    ref.child(key).set(value)
