import cv2
import numpy as np


# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


def detect_faces(img):
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    if len(eye_cascade.detectMultiScale(gray, 1.1, 4)):
        return True
    elif len(face_cascade.detectMultiScale(gray, 1.1, 4)):
        return True
    else:
        return False


def detect_people(img):

    # resizing for faster detection
    frame = cv2.resize(img, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

    return len(np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes]) > 0)
