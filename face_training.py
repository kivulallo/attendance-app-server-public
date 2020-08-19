''''
Training Multiple Faces stored on a DataBase:
	==> Each face should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model will be saved on trainer/ directory. (if it does not exist, pls create one)
	==> for using PIL, install pillow library with "pip install pillow"

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18   

'''

import cv2
import numpy as np
from PIL import Image
import os
import printlog as pr

class Trainer:

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("./cascades/haarcascade_frontalface_default.xml");

    # function to get the images and label data
    def getImagesAndLabels(self, path):

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = cv2.imread(imagePath)
            img_numpy = cv2.flip(img_numpy, -1)
            img_numpy = cv2.cvtColor(img_numpy,cv2.COLOR_BGR2GRAY)

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = self.detector.detectMultiScale(img_numpy,1.3,5)

            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

        return faceSamples,ids

    def train(self, faces, ids):
        pr.pl("Training faces. It will take a few seconds. Wait ...")
        self.recognizer.train(faces,np.array(ids))
        pr.pl ("{0} faces trained. Finished training.".format(len(np.unique(ids))))
        pr.pl ("Writing trainer.yml file. Please Wait ...")
        self.recognizer.write('./trainer.yml')
        pr.pl("Write completed.")

    if __name__ == "__main__":
        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
