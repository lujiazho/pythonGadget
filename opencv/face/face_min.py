import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection()

cap = cv2.VideoCapture('1.mp4')
# cap = cv2.VideoCapture(0)
pTime = 0

while True:
    success, img = cap.read()
    # if not success:
    #     cap = cv2.VideoCapture('1.mp4')
    #     success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    if results.detections:
        for idx, detection in enumerate(results.detections):
            mpDraw.draw_detection(img, detection)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(20)