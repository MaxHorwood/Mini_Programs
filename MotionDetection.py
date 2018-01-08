import numpy as np
import cv2
import os
import time
from datetime import datetime, timedelta

# Work around for a fault in OpenCL with fgbg.apply()
cv2.ocl.setUseOpenCL(False) 

# Motion Class
class Motion_Detection():
    # On declaration
    def __init__(self, camera, resolution, debug):
        self.resolution = resolution
        self.camera = camera
        self.debug = debug
        self.codec = cv2.VideoWriter_fourcc(*'MJPG')
        self.isMotion = False
        self.bufferWaitTime = timedelta(seconds=2)
        self.stopMotionTime = datetime.now()
        self.fileName = ""
        self.writer = None
    
    # Start the video stream
    def begin(self):
        
        img_fgbg = cv2.createBackgroundSubtractorMOG2(1000, 16, detectShadows=True)
        kernel = np.ones((5,5),np.uint8)
        # Get the video capture can be a stream or file
        cam = cv2.VideoCapture(self.camera)
        while(1):
            cap, img_original = cam.read()
            img = img_original
            temp = img_original
            if not cap:
                print ("No Capture")
                break

            # If a resolution was given then resize the image
            if self.resolution is not None:
                img = cv2.resize(img, self.resolution, interpolation=cv2.INTER_CUBIC)

            # Convert image to grey
            img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Apply img_grey (Quicker to process in grey scale)
            img_applied = img_fgbg.apply(img_grey, None, 0.2)
            # Dilate the image (Makes movement easier to detect)
            img_dilate = cv2.dilate(img_applied, kernel, iterations=1)
            # Detects the motion
            img_morph = cv2.morphologyEx(img_dilate, cv2.MORPH_OPEN, kernel)

            # Find the contours of the motion
            _, contours, __ = cv2.findContours(img_morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            for c in contours:
                # Rectangle 
                rectangle = cv2.boundingRect(c)
                # If the rectangle is < then val
                # the 40 and 30 need to be tuned based
                # on lighting and image noise etc
                if rectangle[2] > 40 or rectangle[3] > 40:
                    
                    # Draw a rectangle around the movement detected
                    x,y,w,h = rectangle
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                    cv2.putText(img, 'Motion Detected', (50,50), 0, 0.7, (0, 0, 255))
                    
                    # rectangle[2] or [3] == true so motion is true
                    self.isMotion = True
                    
                    # If no file name then new file name is needed
                    # (as no file name is set when finished writing)
                    if self.fileName == "":
                        self.fileName = str(datetime.now()).split('.', 1)[0] + ".avi"
                        self.fileName = self.fileName.replace(":", "-")
                        print ("Writing to: " + self.fileName)
                        self.writer = cv2.VideoWriter(self.fileName, self.codec, 15, (1280, 720))
                    
                    # The time (5 seconds ahead of currect time) to stop
                    self.stopMotionTime = datetime.now() + self.bufferWaitTime
                    break
                
            # self.isMotion == True
            if self.isMotion:
                # Only on frames that isMotion==True
                cv2.putText(img, "RECORDING", (50,100), 0, 0.7, (0, 0, 255))
                # check stopMotionTime with currect time
                # if currect time is < then write
                # otherwise no motion for 5 seconds so motion=Flase
                # Basicly creates the 5 window for additional motion
                if self.stopMotionTime > datetime.now():
                    self.writer.write(img_original)
                else:
                    self.isMotion = False
                    print ("Stopped Writing")
                    self.fileName = "" # Set back to nothing
                    self.writer.release()
            # Frame count
            frameNumber = cam.get(cv2.CAP_PROP_POS_FRAMES)
            cv2.putText(img, "Frames: " + str(frameNumber), (50,150), 0, 0.7, (0, 0, 255))

            if self.debug:
                cv2.imshow("Original", img)
                cv2.imshow("Appiled", img_applied)
                cv2.imshow("Dilate", img_morph)

            key = cv2.waitKey(30) & 0xff

            if key == 27:
                break
        # Loop was broken so release cam and destroy if needed
        cam.release()
        if self.debug is not None or self.debug is not False:
            cv2.destroyAllWindows()

# Motion_Detection(source, (resolution), debug)
# Input with a video file or can be a video stream (from a web cam)
videoInput = Motion_Detection("Untitled.mxf", None, True)
# videoInput = Motion_Detection(0, None, True)
videoInput.begin()
videoInput.writer.release()


