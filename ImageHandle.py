"""
ROI（Region Of Interest），感兴趣区域。
机器视觉、图像处理中，从被处理的图像以方框、圆、椭圆、不规则多边形等方式勾勒出需要处理的区域，称为感兴趣区域ROI。
"""
import cv2
import os
from FruitTrain import Model
from LoadDataset import get_file_name
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('C:\\Users\\hasee\\Downloads\\recognition_gender-master\\recognition_gender-master\\haarcascade_frontalface_alt.xml')
model = Model()
model.load()
IMAGE_SIZE = 128
name_list=['0','1']
def draw(frame,gray):
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        ROI = gray[x:x + w, y:y + h]
        ROI = cv2.resize(ROI, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_LINEAR)
        label, prob = model.predict(ROI)
        print(prob)
        if prob > 0.5:
            show_name = name_list[label]
            if (show_name == '0'):
                show_name = "women"
            else:
                show_name = "man"
            print(name_list[label])
        else:
            show_name = 'unknow'
        cv2.putText(frame, show_name, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)  # 显示名字
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # 在人脸区域画一个正方形出来
    cv2.imshow("frame", frame)
if __name__ == '__main__':
    while True:
        # get a frame
        ret, frame = cap.read()
        # show a frame
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        draw(frame,gray)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()