import cv2
from model import FacialExpressionModel
import numpy as np

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        # self.video = cv2.VideoCapture("/home/rhyme/Desktop/Project/videos/facial_exp.mkv")
        self.video = cv2.VideoCapture(0) # Sets the source as default video source for Webcam
        
    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read() # load the video and take it into frame
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY) #make sure it is in gray scale
        faces = facec.detectMultiScale(gray_fr, 1.3, 5) # Detects faces

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis]) # sends images to a neural network and gets the predictions back from CNN model

            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2) # Use models prediction and overlay text next to bounding boxes drawn by openCV
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2) # use openCV face detector to draw a rectangular bounding box around faces

        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes() # return image back to the script that calls camera script which is the main.py script
