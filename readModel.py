import cv2
from FruitTrain import Model
from LoadDataset import get_file
#目前采集了四种水果
#如果一张图中有多种水果，那将以最"像"的为准
#字典FruitDictionary

if __name__ == '__main__':
    get_file("DownloadImage/")
    model = Model()
    model.load()
    IMAGE_SIZE = 128
    img = cv2.imread("DownloadImage/Apple/9.jpg")
    resized_img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE)) #缩小图片
    gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)  # 转为灰度图
    FruitDictionary = {"Apple": 0, "Banana": 1, "Orange": 2, "PineApple": 3}
    label, prob = model.predict(gray)
    for key, val in FruitDictionary.items():
        if val == label:
            label = key
    print("该图中最大概率含有的水果为:", label, "概率为:", prob)
    print("end")
