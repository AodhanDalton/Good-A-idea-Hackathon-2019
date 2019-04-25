import cv2
import sys
from scratch import VectorPredictor
# Get user supplied values
cascPath = "haarcascade_frontalface_default.xml"
# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)
# Read the image
cap = cv2.VideoCapture('sample2.mp4')

vecP= VectorPredictor()

while (cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(20, 20),
            maxSize=(100, 100)
        )

        # Draw a rectangle around the faces
        newbb = []
        for (x, y, w, h) in faces:
            x2 = x+w
            y2 = y+h
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)
            newbb.append(((x,y),(x2,y2)))

        newvecs = vecP.add_frame(newBB)
        for name,a,b in newvecs:
            cv2.rectangle(frame, a, b, (0, 255, 0), 2)

        cv2.imshow('BUM', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cv2.waitKey(0)