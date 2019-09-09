import cv2
import os
import numpy as np

from ImageSpider import FruitList
"""
将下载的文件进行二值化获取轮廓
生成后应该手动删除“不具备典型特征”的图片
"""

def GetBinaryImage():
    count =0
    for item in FruitList:
        print(item)
        for dir_image in os.listdir("DownloadImage/"+item):
            if dir_image.endswith('.jpg') or dir_image.endswith('.jpeg'):
                dir_image="DownloadImage/"+item+"/"+dir_image
                # 读取图片
                img = cv2.imread(dir_image)
                # 二值化，canny检测
                binaryImg = cv2.Canny(img, 100, 200)
                # 寻找轮廓
                # 也可以这么写：
                # binary,contours, hierarchy = cv2.findContours(binaryImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                # 这样，可以直接用contours表示
                h = cv2.findContours(binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                # 提取轮廓
                contours = h[1]
                # 打印返回值，这是一个元组
               # print(type(h))
                # 打印轮廓类型，这是个列表
               # print(type(h[1]))
                # 查看轮廓数量
               # print(len(contours))
                # 创建白色幕布
                try:
                    temp = np.ones(binaryImg.shape, np.uint8) * 255
                    # 画出轮廓：temp是白色幕布，contours是轮廓，-1表示全画，然后是颜色，厚度
                    cv2.drawContours(temp, contours, -1, (0, 255, 0), 3)
                    cv2.imwrite("Binaryzation_Image/"+item+"/" + str(count) + '.png', temp)#保存图片
                    count=count+1
                    print("第",str(count),"张")
                except:
                    pass
        count=0
#调用方法
#GetBinaryImage()