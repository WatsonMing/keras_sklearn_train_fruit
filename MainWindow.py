import wx
import cv2
import numpy as np
from FruitTrain import *


#创建类
class ChangeFrame(wx.Frame):
    #初始化
    def __init__(self):
        #继承父类的__init__()函数
        self.model = Model()
        self.model.load()
        wx.Frame.__init__(self, None, -1, '水果识别工具',size=(1000, 900))
        self.InitUI()
        self.Centre()
        self.Show()
    def getBinary(self,path):
        img = cv2.imread(path)
        # 二值化，canny检测
        binaryImg = cv2.Canny(img, 100, 200)
        # 寻找轮廓
        # 也可以这么写：
        # binary,contours, hierarchy = cv2.findContours(binaryImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # 这样，可以直接用contours表示
        h = cv2.findContours(binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = h[1]
        self.ROI=contours
        # 创建白色幕布
        try:
            temp = np.ones(binaryImg.shape, np.uint8) * 255
            # 画出轮廓：temp是白色幕布，contours是轮廓，-1表示全画，然后是颜色，厚度
            cv2.drawContours(temp, contours, -1, (0, 255, 0), 3)
            cv2.imwrite("TestImage/getBinaryImage.jpg", temp)  # 保存图片
        except:
            return None

    def getGray(self,path):
        img = cv2.imread(path)
        colored_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转为灰度图
        cv2.imwrite("TestImage/getGrayImage.jpg", colored_img)  # 保存图片
        return colored_img

    def InitUI(self):
        #创建面板
        panel = wx.Panel(self, -1)
        #利用wxpython的GridBagSizer()进行页面布局
        sizer = wx.GridBagSizer(10, 20) #列间隔为10，行间隔为20
        #添加字段，并加入页面布局，为第一行，第一列
        text1 = wx.StaticText(panel, label="1.原图")
        sizer.Add(text1, pos = (0, 0), flag=wx.ALL, border=5)

        #获取shanghai.png图片，转化为Bitmap形式，添加到第一行，第二列
        srcImage = wx.Image('UI/InitImage.jpg', wx.BITMAP_TYPE_JPEG).Rescale(350, 350).ConvertToBitmap()
        self.srcBmp = wx.StaticBitmap(panel, -1,srcImage) #转化为wx.StaticBitmap()形式
        sizer.Add(self.srcBmp, pos=(0,1), flag=wx.ALL, border=5)

        text2 = wx.StaticText(panel,label="2.灰度")
        sizer.Add(text2, pos=(0, 2), flag=wx.ALL, border=5)
        grayImag = wx.Image('UI/InitGrayImage.jpg', wx.BITMAP_TYPE_JPEG).Rescale(350, 350).ConvertToBitmap()
        self.grayBmp = wx.StaticBitmap(panel, -1,grayImag)  # 转化为wx.StaticBitmap()形式
        sizer.Add(self.grayBmp, pos=(0,3), flag=wx.ALL, border=5)

        #添加二值化字段，并加入页面布局，为第二行，第一列
        text3 = wx.StaticText(panel, label="3.二值化")
        sizer.Add(text3, pos=(1,0), flag=wx.ALL, border=10)
        #获取图片，转化为Bitmap形式，添加到第二行，第二列
        binaryImage = wx.Image('UI/InitBinaryImage.jpg', wx.BITMAP_TYPE_JPEG).Rescale(350, 350).ConvertToBitmap()
        self.binaryBmp = wx.StaticBitmap(panel, -1, binaryImage) #转化为wx.StaticBitmap()形式
        sizer.Add(self.binaryBmp, pos=(1,1), flag=wx.ALL, border=5)

        text4 = wx.StaticText(panel, label="4.预测结果")
        sizer.Add(text4, pos=(1,2), flag=wx.ALL, border=5)

        knowImage=wx.Image('UI/NotKnow.jpg', wx.BITMAP_TYPE_JPEG).Rescale(350, 350).ConvertToBitmap()
        self.getFruitBmp = wx.StaticBitmap(panel,  -1, knowImage)  # 转化为wx.StaticBitmap()形式
        sizer.Add(self.getFruitBmp, pos=(1, 3), flag=wx.ALL, border=5)
        text5 = wx.StaticText(panel, label="输入图片名称")
        sizer.Add(text5, pos=(2,0), flag=wx.ALL, border=10)
        self.path_text = wx.TextCtrl(panel,size = (350,25))
        sizer.Add(self.path_text, pos=(2, 1),flag=wx.ALL, border=5)
        #添加按钮，并加入页面布局，为第四行，第2列
        btn = wx.Button(panel, -1, "读取")
        sizer.Add(btn, pos=(2,2), flag=wx.ALL, border=5)
        #为登录按钮绑定change_picture事件
        self.Bind(wx.EVT_BUTTON, self.change_picture, btn)

        # 添加按钮，并加入页面布局，为第四行，第2列
        btn = wx.Button(panel, -1, "百度图片爬虫")
        sizer.Add(btn, pos=(3, 1), flag=wx.ALL, border=5)
        # 为登录按钮绑定change_picture事件
        self.Bind(wx.EVT_BUTTON, self.goDownload, btn)

        # 添加按钮，并加入页面布局，为第四行，第2列
        btn = wx.Button(panel, -1, "机器训练")
        sizer.Add(btn, pos=(3, 2), flag=wx.ALL, border=5)
        # 为登录按钮绑定change_picture事件
        self.Bind(wx.EVT_BUTTON, self.goTrain, btn)
        #将Panmel适应GridBagSizer()放置
        panel.SetSizerAndFit(sizer)

    def goTrain(self,event):
        #from FruitTrain import *
        train()

    def goDownload(self,event):
        from ImageSpider import DownLoad
        DownLoad()

    def FruitJudge(self):
        IMAGE_SIZE=128
        srcImage=cv2.imread("TestImage/getBinaryImage.jpg")
        gray = cv2.cvtColor(srcImage, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(gray, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_LINEAR)
        if self.model.predict(image)!=None:
            label, prob = self.model.predict(image)
            print(prob)
            fruitName="未知"
            if int(label)==1:
                BinaryPath = "Model/fruit/Apple.jpg"
                fruitName="苹果"
            elif int(label)==3:
                BinaryPath = "Model/fruit/Banana.jpg"
                fruitName = "香蕉"
            elif int(label) == 2:
                BinaryPath = "Model/fruit/Grape.jpg"
                fruitName = "葡萄"
            elif int(label) == 0:
                BinaryPath = "Model/fruit/Orange.jpg"
                fruitName = "桔子"
            elif int(label) == 4:
                BinaryPath = "Model/fruit/PineApple.jpg"
                fruitName = "菠萝"
            self.image = wx.Image(BinaryPath, wx.BITMAP_TYPE_JPEG).Rescale(350, 350).ConvertToBitmap()
            self.getFruitBmp.SetBitmap(wx.BitmapFromImage(self.image))
            dlg = wx.MessageDialog(None, u"该水果为: "+fruitName, u"预测结果", wx.OK | wx.CANCEL)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
        else:
            print("预测异常！")

    #定义文字及图片转换函数
    def change_picture(self, event):
        #获取二值化的图片
        if self.path_text.GetValue()!="":
            path = self.path_text.GetValue()
            srcPath="TestImage/"+path+".jpg"
            #更新GridBagSizer()
            self.image = wx.Image(srcPath, wx.BITMAP_TYPE_JPEG).Rescale(350, 350).ConvertToBitmap()
            self.srcBmp.SetBitmap(wx.BitmapFromImage(self.image))
            self.getGray(srcPath)
            grayPath = "TestImage/getGrayImage.jpg"
            self.image = wx.Image(grayPath, wx.BITMAP_TYPE_JPEG).Rescale(350, 350).ConvertToBitmap()
            self.grayBmp.SetBitmap(wx.BitmapFromImage(self.image))
            self.getBinary(grayPath)
            BinaryPath="TestImage/getBinaryImage.jpg"
            self.image = wx.Image(BinaryPath, wx.BITMAP_TYPE_JPEG).Rescale(350, 350).ConvertToBitmap()
            self.binaryBmp.SetBitmap(wx.BitmapFromImage(self.image))
            #水果判断
            self.FruitJudge()
        else:
            dlg = wx.MessageDialog(None, u"未填写正确文件", u"读取错误", wx.OK | wx.CANCEL)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
#主函数
if __name__ == '__main__':
    app = wx.App()
    frame = ChangeFrame()
    app.MainLoop()