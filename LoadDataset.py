import os
import numpy as np
from cv2 import *
# 循环读取图片，添加到一个列表，128 *128
def get_file(path):
    IMAGE_SIZE = 128
    images_list = []
    labels_list = []
    counter = 0
    for child_dir in os.listdir(path):
        child_path = os.path.join(path, child_dir)
        print(child_path)
        #根据child_path的名称确认 ReadModel里的FruitDictionary键值，由0开始
        for dir_image in os.listdir(child_path):
            # print(dir_image)
            if dir_image.endswith('.png'):
                #print(dir_image)
                img = cv2.imread(os.path.join(child_path, dir_image))#图片读取
                resized_img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))#缩小为128*128尺寸
                colored_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY) #转为灰度图
                images_list.append(colored_img)
                labels_list.append(counter)
        counter += 1
        #种类数，每执行一个文件夹加1，一个文件里包含一类
    images_list = np.array(images_list)
    return images_list,labels_list,counter

def get_file_name(path):
    name_list = []
    for child_dir in os.listdir(path):
        name_list.append(child_dir)
    return name_list
