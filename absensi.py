##############################
## Code by: Ridho Alamsyah ###
##############################

import cv2
import numpy as np
import os
import openpyxl
from datetime import datetime

# Load existing Excel file or create a new one
wb_path = 'absensi.xlsx'
if os.path.exists(wb_path):
    wb = openpyxl.load_workbook(wb_path)
else:
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = 'Nama'
    sheet['B1'] = 'Waktu'
    wb.save(wb_path)

sheet = wb.active

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

# initiate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1, etc
names = ['none', 'Ridho', 'Septian', 'Unsa', 'Pradana', 'Hardi']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video width
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

detected_ids = set()

while True:
    ret, img = cam.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        # Check if confidence is less than 100 ==> "0" is perfect match
        if confidence < 100:
            name = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            if id not in detected_ids:
                # Write to Excel
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet.append([name, current_time])
                detected_ids.add(id)
        else:
            name = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(name), (x+5, y-5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x+5, y+h-5),
                    font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

# Save Excel file
wb.save(wb_path)

# Do a bit of cleanup
print("[ Face Recognition ] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
