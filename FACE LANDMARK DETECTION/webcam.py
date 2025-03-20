import cv2
import mediapipe as mp
from constant_messages import Q,MY_VIDEO_CAPTURE

mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness = 1,circle_radius = 1)
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 5)

cap = cv2.VideoCapture(1)


while cap.isOpened():
    success, image = cap.read()
    breakpoint()

    if not success:
        break

    results = faceMesh.process(image)

    for face_landmarks in results.multi_face_landmarks:
        mpDraw.draw_landmarks(image,face_landmarks, mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec)


    cv2.imshow(MY_VIDEO_CAPTURE, cv2.flip(image,1))

    if cv2.waitKey(100) & 0xFF == ord(Q):
        break

cap.release()
cv2.destroyAllWindows()




# import cv2

# # Open the default camera
# cam = cv2.VideoCapture(0)

# # Get the default frame width and height
# frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# # Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

# while True:
#     ret, frame = cam.read()

#     # Write the frame to the output file
#     out.write(frame)

#     # Display the captured frame
#     cv2.imshow('Camera', frame)

#     # Press 'q' to exit the loop
#     if cv2.waitKey(100) == ord('q'):
#         break

# # Release the capture and writer objects
# cam.release()
# out.release()
# cv2.destroyAllWindows()
