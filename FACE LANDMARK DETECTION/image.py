import cv2
import mediapipe as mp
import time
from constant_messages import INPUT_IMAGE,RESIZED_WINDOW

# Face Mesh
mpFaceMesh = mp.solutions.faceMesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 5)
mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness = 7,circle_radius = 1)

#Image
data = input(INPUT_IMAGE)
image = cv2.imread(data)


while True : 
      
    height,width,channel = image.shape

    # Naming a window 
    cv2.namedWindow(RESIZED_WINDOW, cv2.WINDOW_NORMAL) 

    # Resize the image frames 
    cv2.resizeWindow(RESIZED_WINDOW, 1100,900)
    rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)


    #Facial Landmarks
    result = faceMesh.process(rgb_image)

    if result.multi_face_landmarks:
            for faceLms in result.multi_face_landmarks:
                mpDraw.draw_landmarks(image,faceLms, mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec)


    cv2.imshow("Resized_Window",image)
    cv2.waitKey(0)
