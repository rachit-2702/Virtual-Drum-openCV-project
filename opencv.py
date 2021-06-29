from pygame import mixer
import pygame
import time
import numpy as np
import cv2
img1 = cv2.imread('C:\\Users\\rachi\\Desktop\\splash.jpg', -1)
img1 = cv2.resize(img1, (0, 0), fx=0.8, fy=0.8)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2BGRA)
img_h, img_w, img_c = img1.shape
i = 0
j = 0
k = (img_w)
l = (img_h)
img2 = cv2.imread('C:\\Users\\rachi\\Desktop\\tom.jpg', -1)
img2 = cv2.resize(img2, (k, l))
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2BGRA)
img3 = cv2.imread('C:\\Users\\rachi\\Desktop\\snare.jpg', -1)
img3 = cv2.resize(img3, (k, l))
img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2BGRA)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time_1 = 0
time_2 = 0
time_3 = 0
time_delay = .5
mixer.init()
while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    frame_h, frame_w, frame_c = frame.shape
    img_h, img_w, img_c = img1.shape
    i = 0
    j = 0
    k = (img_w)
    l = (img_h)
    frame = cv2.rectangle(frame, (i, j), (k, l), (0, 0, 255), 1)
    frame = cv2.rectangle(frame, (frame_w-k, j), (frame_w, l), (0, 0, 255), 1)
    frame = cv2.rectangle(frame, ((frame_w-k)//2, frame_h-l),
                          ((frame_w+k)//2, frame_h), (0, 0, 255), 1)
    check_blue1 = frame[j+1:l-1, i+1:k-1]
    check_blue2 = frame[j+1:l-1, frame_w-k+1:frame_w-1]
    check_blue3 = frame[frame_h-l+1:frame_h -
                        1, (frame_w-k)//2+1:(frame_w+k)//2-1]
    hsv1 = cv2.cvtColor(check_blue1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(check_blue2, cv2.COLOR_BGR2HSV)
    hsv3 = cv2.cvtColor(check_blue3, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    blue_mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    blue_mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    blue_mask3 = cv2.inRange(hsv3, lower_blue, upper_blue)
    blue_result1 = cv2.bitwise_and(check_blue1, check_blue1, mask=blue_mask1)
    blue_result2 = cv2.bitwise_and(check_blue2, check_blue2, mask=blue_mask2)
    blue_result3 = cv2.bitwise_and(check_blue3, check_blue3, mask=blue_mask3)
    blue_h1, blue_w1, blue_c1 = blue_result1.shape
    blue_h2, blue_w2, blue_c2 = blue_result2.shape
    blue_h3, blue_w3, blue_c3 = blue_result3.shape
    blue_con1 = 0
    blue_con2 = 0
    blue_con3 = 0
    for i in range(blue_h1):
        for j in range(blue_w1):
            if all(blue_result1[i][j][1] != [0, 0, 0]):
                blue_con1 += 1
            if all(blue_result2[i][j][1] != [0, 0, 0]):
                blue_con2 += 1
            if all(blue_result3[i][j][1] != [0, 0, 0]):
                blue_con3 += 1
    if blue_con1 > 200 and time.time()-time_1 > time_delay:
        mixer.music.load('C:\\Users\\rachi\\Desktop\\splash.ogg')
        mixer.music.play()
        time_1 = time.time()
    if blue_con2 > 200 and time.time()-time_1 > time_delay:
        mixer.music.load('C:\\Users\\rachi\\Desktop\\tom.ogg')
        mixer.music.play()
        time_1 = time.time()
    if blue_con3 > 200 and time.time()-time_1 > time_delay:
        mixer.music.load('C:\\Users\\rachi\\Desktop\\snare.ogg')
        mixer.music.play()
        time_1 = time.time()
    overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')

    for i in range(0, img_h):
        for j in range(0, img_w):
            if img1[i, j][3] != 0:
                overlay[(i), (j)] = img1[i, j]
            if img2[i, j][3] != 0:
                overlay[(i), (frame_w-img_w+j)] = img2[i, j]
            if img3[i, j][3] != 0:
                overlay[(frame_h-img_h+i), ((frame_w-img_w)//2+j)] = img3[i, j]
    cv2.addWeighted(overlay, 0.7, frame, 1.0, 1, frame)
    cv2.imshow('frame ', frame)
    cv2.imshow("1", blue_result1)
    cv2.imshow("2", blue_result2)
    cv2.imshow("3", blue_result3)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
