import cv2
import mediapipe as mp
import streamlit as st
import numpy as np
import time 
import tempfile
from constant_messages import STREAMLIT_TITLE,SELECT_OPTION,WEBCAM,IMAGE,VIDEO,WEB_TITLE,WEB_CAPTION,STOP,CHOOSE_IMAGE_FILE,JPG,UPLOAD_VIDEO,MY_VIDEO_CAPTURE,RESIZED_WINDOW,Q,FPS,MAIN



#mp.solutions.drawing_utils is a class that helps visualize the results.
#mp.solutions.face_mesh provides a solution that estimates 468 3D face landmarks in real-time.
#.DrawingSpec contains values on base of that we will define the style of markings.

mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness = 5,circle_radius = 3)
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 5)


#utilizing streamlit for user interface
#for giving options we're using radio button

st.set_page_config(page_title=STREAMLIT_TITLE)

options = st.radio(
    SELECT_OPTION,
    [WEBCAM, IMAGE, VIDEO],
    index=None,
)



if options==WEBCAM:
    def webcam():
        """
        As per name This method holds authority to perform task on webcam.

        It will take web came live video data as an input,
        read it,
        finds the shape of video frames,
        holds control of output window and it will show output along-side the labels of landmark placements.
        if clearity is bad or model is unable to read data or place lan dmark then it will automatically stop.

        """
        st.title(WEB_TITLE)
        st.caption(WEB_CAPTION)
        cap = cv2.VideoCapture(0)
        stop_button_pressed = st.button(STOP)


        while cap.isOpened() and not stop_button_pressed:
            success, image = cap.read()

            height,width,channel = image.shape

            if not success or stop_button_pressed:
                break

            results = faceMesh.process(image)

            for face_landmarks in results.multi_face_landmarks:
                mpDraw.draw_landmarks(image,face_landmarks, mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec)

                # Showing id and x,y axes of facial landmaks
                for id,lm in enumerate(face_landmarks.landmark):
                    x,y = int(lm.x*width), int(lm.y*height)
                    print([id,x,y])


            img = cv2.imshow(MY_VIDEO_CAPTURE, cv2.flip(image,1))
            st.image(image=img)

            if cv2.waitKey(100) & 0xFF == ord(Q):
                break

        cap.release()
        cv2.destroyAllWindows()

    if __name__ == MAIN:
        webcam()




if options==IMAGE:
    def image():
        """
        As per name This methods holds authority to perform task on image data.

        It will take image data through streamlit dropbox,
        read it,
        finds the shape of image,
        holds control of output window and it will show output along-side the labels of landmark placements.

        other than that stramlit is implemented for ui,labeling and select content box.
        """
        uploaded_file = st.file_uploader(CHOOSE_IMAGE_FILE, type=JPG)

        if uploaded_file is not None : 
            
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)
            height,width,channel = image.shape

            # Naming a window 
            cv2.namedWindow(RESIZED_WINDOW, cv2.WINDOW_NORMAL) 

            # Resize the image frames 
            cv2.resizeWindow(RESIZED_WINDOW, 1100,900)
            rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

            #Facial Landmarks
            result = faceMesh.process(rgb_image)

            if result.multi_face_landmarks:
                    for face_landmarks in result.multi_face_landmarks:
                        mpDraw.draw_landmarks(image,face_landmarks, mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec)

                        # Showing id and x,y axes of facial landmaks
                        for id,lm in enumerate(face_landmarks.landmark):
                            x,y = int(lm.x*width), int(lm.y*height)
                            print([id,x,y])


            img = cv2.imshow(RESIZED_WINDOW,image)
            cv2.waitKey(0)

    if __name__ == MAIN:
        image()




if options==VIDEO:
    def video():
        """
        As per name This method holds authority to perform task on video data.

        It will take video data as an input by streamlit dropbox,
        read it,
        finds the shape of video frames,
        holds control of output window and it will show output along-side the labels of landmark placements.
        it will show output along side Fps.

        other than that stramlit is implemented for ui,labeling and select content box.
        """
        video = st.file_uploader(UPLOAD_VIDEO)
        if video:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(video.read())

        cap = cv2.VideoCapture(tfile.name)
        pTime = 0

        while True:
            sucess,image = cap.read()

            height,width,channel = image.shape

            # Naming a window 
            cv2.namedWindow(RESIZED_WINDOW, cv2.WINDOW_NORMAL) 

            # Resize the image frames 
            cv2.resizeWindow(RESIZED_WINDOW, 1100,900)

            imgRGB= cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            results = faceMesh.process(imgRGB)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mpDraw.draw_landmarks(image,face_landmarks, mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec)

                    # Showing id and x,y axes of facial landmaks
                    for id,lm in enumerate(face_landmarks.landmark):
                        x,y = int(lm.x*width), int(lm.y*height)
                        print([id,x,y])

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(image,f'{FPS}: {int(fps)}',(150,200),cv2.FONT_HERSHEY_PLAIN,7,(0,0,0),7)
            cv2.imshow(RESIZED_WINDOW,image)
            cv2.waitKey(1)


    if __name__ == MAIN:
        video()