# This is a sample Python script.
import cv2
import mediapipe as mp



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose


    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            # describe the type of font
            # to be used.

            font = cv2.FONT_HERSHEY_SIMPLEX
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            if(results.pose_landmarks):
                thl_x= results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_THUMB].x
                thl_y= results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_THUMB].y
                thr_x= results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_THUMB].x
                thr_y= results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_THUMB].y
                # Hata tolerans
                er=0.09
                if ((thl_y >= thr_y - er) and (thl_y <= thr_y + er) ) or((thr_y <= thl_y - er) and (thr_y >= thl_y + er)) :
                    cv2.putText(image,
                                'the deep yoga breathing done properly',
                                (50, 50),
                                font, 1,
                                (0, 255, 0),
                                2,
                                50)
                else:
                    cv2.putText(image,
                                'the deep yoga breathing not done properly',
                                (50, 50),
                                font, 1,
                                (255, 0, 0),
                                2,
                                50)


            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()

