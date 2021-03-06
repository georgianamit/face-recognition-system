import cv2
import numpy as np
import pickle
import os

def recognize_face():
    cap = cv2.VideoCapture(0)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, 'images')

    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(os.path.join(os.path.join(os.path.join(BASE_DIR, 'assests'),'trainner'),'trainner.yml'))

    labels = {}

    with open(os.path.join(os.path.join(os.path.join(BASE_DIR, 'assests'),'serializer'),'label.pickle'), 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}

    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            id_, conf = recognizer.predict(roi_gray)
            if conf>=45 and conf<=85:
                print(id_)
                print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y-10), font, 1, color, stroke, cv2.LINE_AA)


            # img_item = 'my-image.png'
            # cv2.imwrite(os.path.join(image_dir,img_item), roi_gray)

            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)

        cv2.imshow('frame',frame)

        if(cv2.waitKey(20) & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    recognize_face()