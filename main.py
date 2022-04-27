import cv2
import pickle
import cvzone
import numpy as np
import pyrebase

from datetime import datetime
firebaseConfig = {
     'apiKey': "TXp6PAw54VCdgLomVzEgmvyczT7BE9wg0S5k0pcn",
    'authDomain': "Parkinny-test.firebaseapp.com",
    'databaseURL': "https://parkinny-test-default-rtdb.firebaseio.com/",
    'storageBucket': "Parkinny-test.appspot.com",
    }
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

#video feed
cap = cv2.VideoCapture('carPark.mp4')
width, height = 107, 48
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)
m= []
max_pixel = 900


def checkParkingSpace(imgPro):

    spacecounter =0
    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y+height, x:x+width]
        #cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        m.append(count)


        if count < max_pixel:
            color = (0, 255, 0)
            tickness= 5
            spacecounter+=1
        else:

            color = (0,0,255)
            tickness = 2



        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height),color, tickness)
        cvzone.putTextRect(img, str(count), (x, y+height-10), scale = 1,
                           thickness=1, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free:{spacecounter}/{len(posList)}', (100, 50), scale = 3,
                           thickness=5, offset=20, colorR=(0,200,0))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()

    #img = cv2.imread('carParkImg.png')
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C
                                         ,cv2.THRESH_BINARY_INV,25,16)

    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernal = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernal, iterations=1)


    checkParkingSpace(imgDilate)
    cv2.imshow("image", img)
    cv2.waitKey(10)





    with open("count.py", "w") as w:
        for i in range(len(m)):
            w.write(str(m[i]) + '\n')






    for i in range(len(m)):
        m.pop()









    '''cv2.imshow("imageBlur",imgBlur)
    cv2.imshow("imgThreashold",imgThreshold)
    cv2.imshow("imgMedian",imgMedian)
    cv2.imshow("imgDilate",imgDilate)'''




