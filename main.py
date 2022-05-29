
#importing packages....

import cv2
import numpy as np
import face_recognition
import sys
import os
from datetime import datetime

#providing path
path = 'images'
# variable for list
images = []
# variable for person name list
personName = []
# storing images in path to mylist
myList = os.listdir(path)
print(myList)

# in the name of person just use first name depricate .jpg extension, this is the reason
# we saved the name of the file with the person name itself
for cu_img in myList:
    current_img = cv2.imread(f'{path}/{cu_img}')
    images.append(current_img)
    personName.append(os.path.splitext(cu_img)[0])

# for debugging purpose we checked if the above for loop working properly or not
print(personName)

# defining a function for storing the encodings of the image:


def face_ncodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        encodelist.append(encode)
    return encodelist


encodeListKnown = face_ncodings(images)
print("All encodings are completed!!!!")


def attendance(name):
    with open('Attemdance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.now()
            tstr = time_now.strftime('%H:%M:%S')
            dstr = time_now.strftime('%d/%m/%Y')
            f.writelines(f'{name},{tstr},{dstr}')

# here we use the web cam of our laptop to capture the person photo
cap = cv2.VideoCapture(0)

# infinite loop is running here
while True:
    ret, frame = cap.read()
    faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

    # This will search the frame where face is......
    facesCurrentFrame = face_recognition.face_locations(faces)
    # This will search for the face encodings of the frame
    encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
        # Here we will get the face matches
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        # If the distance btw faces is large enough faces dont match, otherwise they match
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = personName[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1, y2), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1,y2-35),(x2, y2), (0,255,0), cv2.FILLED)
            cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        #     attendance(name)

        cv2.imshow("Camera", frame)
        if cv2.waitKey(10) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()