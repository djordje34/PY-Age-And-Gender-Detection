import cv2
import dlib
import numpy as np


def doStuff(img):
  
    #img = cv2.imread('data/people3.jpg')
    img=cv2.imread(img)
    img = cv2.resize(img, (720, 640))
    frame = img.copy()
    
    # Detekcija god
    age_weights = "data/age_deploy.prototxt"
    age_config = "data/age_net.caffemodel"
    age_Net = cv2.dnn.readNet(age_config, age_weights)
    gender_weights="data/gender_deploy.prototxt" 
    gender_config="data/gender_net.caffemodel" 
    gender_Net=cv2.dnn.readNet(gender_config,gender_weights)
    
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
            '(25-32)', '(38-43)', '(48-53)', '(60-100)']

    genderList=["Muski","Zenski"]
    model_mean = (78.4263377603, 87.7689143744, 114.895847746)
    
    
    fH = img.shape[0]
    fW = img.shape[1]
    
    Boxes = []  
    mssg = ''  
    
    # detekcija lica
    face_detector = dlib.get_frontal_face_detector()
    # grayscale
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    faces = face_detector(img_gray)
    

    if not faces:
        mssg = 'Nema prepoznatog lica'
        cv2.putText(img, f'{mssg}', (40, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (200), 2)
        cv2.imshow('Greška', img)
        cv2.waitKey(0)
        return [0]
    
    else:

        for face in faces:
            x = face.left()  # koordinate lica
            y = face.top()
            x2 = face.right()
            y2 = face.bottom()
    
            # kutija
            box = [x, y, x2, y2]
            Boxes.append(box)
            cv2.rectangle(frame, (x, y), (x2, y2), 
                        (00, 200, 200), 2)
    
        for box in Boxes:
            face = frame[box[1]:box[3], box[0]:box[2]]
    
            # ocitavanje lica
            blob = cv2.dnn.blobFromImage(
                face, 1.0, (227, 227), model_mean, swapRB=False)
    

            age_Net.setInput(blob)
            age_preds = age_Net.forward()
            age = ageList[age_preds[0].argmax()]
            print(age_preds[0]*100)
            gender_Net.setInput(blob)
            gender_preds=gender_Net.forward()
            val=gender_preds[0].argmax()
            gender=genderList[val]
            gender_confidence_score=gender_preds[0][val]
            
            cv2.putText(frame, f'{mssg}{age}', (box[0],
                                                box[1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame,f'Pol:{gender}', (box[2]-130,
                                                box[3] + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 255), 2, cv2.LINE_AA)
        print(type(frame))
        return frame