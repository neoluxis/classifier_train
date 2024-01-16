import cv2 as cv
from time import time

# cascadePath = "haarcascade_frontalface_default.xml"
cascadePath = "data/dt/cascade.xml"
faceCascade = cv.CascadeClassifier(cascadePath)
font = cv.FONT_HERSHEY_SIMPLEX

time1 = 0
time2 = 0

cam = cv.VideoCapture(0)
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()
    faces = faceCascade.detectMultiScale(
        cv.cvtColor(img, cv.COLOR_BGR2GRAY),
        scaleFactor=1.2,
        minNeighbors=5
    )
    for face in faces:
        (x, y, w, h) = face
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    time2 = time()
    fps = 1 / (time2 - time1)
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    time1 = time2
    cv.imshow('camera', img)
    k = cv.waitKey(10)
    if k == 27:
        break

cam.release()
cv.destroyAllWindows()
