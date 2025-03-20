import cv2
import mediapipe as mp
# import streamlit as st
import time
from constant_messages import INPUT_IMAGE,RESIZED_WINDOW,INPUT_VIDEO,MY_VIDEO_CAPTURE,FPS,Q,CHOICE,INVALID_CHOICE,INVALID_INPUT



class Face_landmark_detection: 

    def __init__(self,staticMode = False,maxFaces = 5,minDetectionCon = 0.3,minTrackCon = 0.3):
        """
        These are esential and common inbuilt methods of mediapipe and opncv are passed here which will use further in methods.
        
        maxFaces : indicates maximum number of face model have to detect.
        minDetectionCon & minTrackCon are used for pre-check accuricy of content.
        Static mode is selected when the -d n option is used, and enables you to create relocatable objects and static executables

        mp.solutions.drawing_utils is a class that helps visualize the results.
        mp.solutions.face_mesh provides a solution that estimates 468 3D face landmarks in real-time.
        .DrawingSpec contains values on base of that we will define the style of markings.
        """

        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=self.staticMode, max_num_faces=self.maxFaces, min_detection_confidence=self.minDetectionCon, min_tracking_confidence=self.minTrackCon)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness = 2,circle_radius = 1)
        

    def image(self):

        """
        As per name This methods holds authority to perform task on image data.

        It will take image data as an input,
        read it,
        finds the shape of image,
        holds control of output window and it will show output along-side the labels of landmark placements.
        """
        #Image
        data = input(INPUT_IMAGE)
        image = cv2.imread(data)

        while True : 
            height,width,channel = image.shape

            #Naming window
            cv2.namedWindow(RESIZED_WINDOW, cv2.WINDOW_NORMAL) 

            # Redsize the image frames
            cv2.resizeWindow(RESIZED_WINDOW, 600,400)

            rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

            #Facial Landmarks
            result = self.faceMesh.process(rgb_image)

            if result.multi_face_landmarks:
                for faceLms in result.multi_face_landmarks:
                    self.mpDraw.draw_landmarks(image,faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,self.drawSpec,self.drawSpec)

                    for id,lm in enumerate(faceLms.landmark):
                        x,y = int(lm.x*width), int(lm.y*height)
                        print([id,x,y])


            cv2.imshow(RESIZED_WINDOW,image)
            cv2.waitKey(0)


    def video(self):

        """
        As per name This method holds authority to perform task on video data.

        It will take video data as an input,
        read it,
        finds the shape of video frames,
        holds control of output window and it will show output along-side the labels of landmark placements.
        it will show output along side Fps.
        """

        data = input(INPUT_VIDEO)
        cap = cv2.VideoCapture(data)
        pTime = 0


        while True:
            success, img = cap.read()
            height,width,channel = img.shape

            # Naming a window 
            cv2.namedWindow(RESIZED_WINDOW, cv2.WINDOW_NORMAL) 

            # Resize the image frames 
            cv2.resizeWindow(RESIZED_WINDOW, 600,400)

            imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            results = self.faceMesh.process(imgRGB)

            if results.multi_face_landmarks:
                for faceLms in results.multi_face_landmarks:
                    self.mpDraw.draw_landmarks(img,faceLms,self.mpFaceMesh.FACEMESH_CONTOURS,self.drawSpec,self.drawSpec)

                    for id,lm in enumerate(faceLms.landmark):
                        x,y = int(lm.x*width), int(lm.y*height)
                        print([id,x,y])

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(img,f'{FPS}: {int(fps)}',(150,200),cv2.FONT_HERSHEY_PLAIN,7,(200,200,0),7)
            cv2.imshow(RESIZED_WINDOW,img)
            cv2.waitKey(1)

    def webcam(self):

        """
        As per name This method holds authority to perform task on webcam.

        It will take web came live video data as an input,
        read it,
        finds the shape of video frames,
        holds control of output window and it will show output along-side the labels of landmark placements.
        if clearity is bad or model is unable to read data or place lan dmark then it will automatically stop.
        """

        cap = cv2.VideoCapture(0)

        while cap.isOpened():

            success, image = cap.read()
            height,width,channel = image.shape

            if not success:
                break

            results = self.faceMesh.process(image)

            for face_landmarks in results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(image,face_landmarks, self.mpFaceMesh.FACEMESH_CONTOURS,self.drawSpec,self.drawSpec)

                for id,lm in enumerate(face_landmarks.landmark):
                        x,y = int(lm.x*width), int(lm.y*height)
                        print([id,x,y])


            cv2.imshow(MY_VIDEO_CAPTURE, cv2.flip(image,1))

            if cv2.waitKey(1) & 0xFF == ord(Q):
                break
        cap.release()
        cv2.destroyAllWindows()


    def choice(self):

        """
        This method will be the target method 
        which holds all the authority and 
        it will used to ask human input to process upon
        """
        while True:
            try : 
                choice = int(input(CHOICE))
                if choice == 1:
                    self.video()
                elif choice == 2:
                    self.image()
                elif choice == 3:
                    self.webcam()
                else:
                    print(INVALID_CHOICE)
                    break
            except ValueError:
                print(INVALID_INPUT)
                break



if __name__ == "__main__":
    obj = Face_landmark_detection()
    obj.choice()

