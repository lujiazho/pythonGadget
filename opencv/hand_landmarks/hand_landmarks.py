import cv2
import mediapipe as mp 
import time 
import hand_landmarks_module as hlm

def main():
    cap = cv2.VideoCapture(0)

    pTime = 0
    cTime = 0

    detector = hlm.handDetector()

    while True:
        success, img = cap.read()
        img1 = detector.findHands(img)
        # lmList = detector.findPosition(img)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        # cv2.imshow("Image", img)
        cv2.imshow("Image1", img1)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()