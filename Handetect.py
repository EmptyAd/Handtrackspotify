import cv2
import os
import time
from cvzone.HandTrackingModule import HandDetector

# Constants
PLAY = """ osascript -e 'tell application "Spotify"' -e 'play' -e ' end tell'' '"""
PAUSE = """ osascript -e 'tell application "Spotify"' -e 'pause' -e ' end tell'' '"""
PREVIOUS_TRACK = """ osascript -e 'tell application "Spotify"' -e 'previous track' -e ' end tell'' '"""
NEXT_TRACK = """ osascript -e 'tell application "Spotify"' -e 'next track' -e ' end tell'' '"""

# Initialize variables
cx, cy, w, h = 800, 500, 400, 1300
colorR = (255, 0, 255)
hand_detector = HandDetector(detectionCon=0.8)
font = cv2.FONT_HERSHEY_SIMPLEX


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    hands, img = hand_detector.findHands(img, flipType=False)

    lmlist1 = []
    finger1 = []

    if hands:
        hand1 = hands[0]
        if hand1["type"] == 'Right':
            lmlist1 = hand1["lmList"]  # List of 21 landmarks points
            bbox1 = hand1["bbox"]  # bounding box info
            centerpoint1 = hand1["center"]  # center of hand
            handtype1 = hand1["type"]
            print(handtype1)
        else:
            finger2 = hand_detector.fingersUp(hand1)
            print(finger2)
            if finger2 == [0, 1, 1, 1, 1] or finger2 == [1, 1, 1, 1, 1]:
                os.system(PLAY)
                cv2.putText(gray, 'PLAY', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
            if finger2 == [1, 0, 0, 0, 0] or finger2 == [0, 0, 0, 0, 0]:
                os.system(PAUSE)
                cv2.putText(gray, 'PAUSE', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)

    if lmlist1:
        cursor = lmlist1[8]
        print(cursor)
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            colorR = (0, 255, 0)
            cx, cy = cursor[0], cursor[1]
        else:
            colorR = (255, 0, 255)

    cv2.rectangle(gray, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, thickness=1)

    if cx - w // 2 <= 450:
        print("PREVIOUS_TRACK")
        os.system(PREVIOUS_TRACK)
        time.sleep(1)
        cv2.putText(gray, 'PREVIOUS_TRACK', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
        time.sleep(0.5)


    if cx - w // 2 >= 750:
        print("NEXT_TRACK")
        os.system(NEXT_TRACK)
        time.sleep(1)
        cv2.putText(gray, 'NEXT_TRACK', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
        time.sleep(0.5)


    cv2.imshow("image", gray)

    cx, cy = 800, 500
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # Press Esc to stop the video
        break
