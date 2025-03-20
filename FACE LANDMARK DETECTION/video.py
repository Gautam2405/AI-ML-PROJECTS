import cv2
import mediapipe as mp
import time
from constant_messages import INPUT_VIDEO,FPS,RESIZED_WINDOW

data = str(input(INPUT_VIDEO))
cap = cv2.VideoCapture(data)
pTime = 0


mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 5)
drawSpec = mpDraw.DrawingSpec(thickness = 2,circle_radius = 2)



while True:
    success,img = cap.read()

    # Naming a window 
    cv2.namedWindow(RESIZED_WINDOW, cv2.WINDOW_NORMAL) 

    # Resize the image frames 
    cv2.resizeWindow(RESIZED_WINDOW, 1100,900)

    imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img,faceLms, mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec)

            for id,lm in enumerate(faceLms.landmark):
                ih,iw,ic = img.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                print(id,x,y)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'{FPS}: {int(fps)}',(150,200),cv2.FONT_HERSHEY_PLAIN,7,(0,0,0),7)
    cv2.imshow(RESIZED_WINDOW,img)
    cv2.waitKey(1)