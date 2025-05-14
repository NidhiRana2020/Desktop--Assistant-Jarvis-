import sys
import os
import typing
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui
import faceRecognition
import cv2
import numpy
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QTimer


from faceRecognition import Ui_MainWindow

def nameList(nameofImg):
    if nameofImg.startswith('Ni',0):
        return "Nidhi Rana"
    elif nameofImg.startswith('ka',0):
        return "Karishma"
class faceRecog(QWidget):
    def __init__(self):
        super(faceRecog, self).__init__()

        self.faceUi=Ui_MainWindow()
        self.faceUi.setupUi(self)
        self.faceUi.exitButton.clicked.connect(self.close)
        self.runProgram()

    def runProgram(self):
        videoPath="C:\\Users\\admin\\Desktop\\Desktop -Assistant"
        self.encodeImages(videoPath)

    def encodeImages(self,cameraName):
        print("encoding started")
        if len(cameraName)==1:
            self.capture=cv2.VideoCapture(int(cameraName))
        else:
            self.capture=cv2.VideoCapture(cameraName)
        self.timer=QTimer(self)
        path='images'
        if not os.path.exist(path):
            os.mkdir(path)

        images=[]
        self.classNames=[] #names of images
        self.encodeList=[] #encodin of images

        photoList=os.listdir(path)

        for cl in photoList:
            currentImage=cv2.imread(f'{path}/{cl}') 
            images.append(currentImage)
            self.classNames.append(os.path.splitext(cl)[0])

        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)   
            box=faceRecognition.face_Locations(img)
            encodeCurFrame=faceRecognition.face_encodings(img,box)[0]
            self.encodeList.append(encodeCurFrame)   

        print("Images encode successfully")
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(10)

    def updateFrame(self):
        ret,self.image=self.capture.read()
        self.displayImages(self.image,self.encodeList,self.classNames,1)


    def displayImage(self,image,encodeList,classNames,window=1):
        image=cv2.resize(image,( 431, 281)) 
        try:
            self.faceRecognition(image,encodeList,classNames)
        except Exception as e:
            print(e) 


        qformat=QImage.Format_Indexed8
        if len(image.shape)==3:
            if image.shape[2]==4:
                qformat=QImage.Format_RGBA888
            else:
                qformat=QImage.format_RGB888
        outImage=QImage(image,image.shape[1],image.shape[0],image.strides[0],qformat)
        outImage=outImage.rgbSwapped()

        if window==1:
            self.faceUi.videolable.setPixmap(QPixmap.fromImage(outImage))
            self.faceUi.videolable.setScaledContents(True)
            if self.name=="Nidhi Rana":
                self.connectToMainFile()
                self.timer.stop()


    def faceRecognition(self,image,encodeList,className):  
        facesOfCurrentFrame=faceRecognition.face_Locations(image) 
        encodeCurrentFrame=faceRecognition.face_encodings(image,facesOfCurrentFrame)  

        for encodeFace,faceLocation in zip(encodeList,facesOfCurrentFrame):
            match=faceRecognition.compare_faces(encodeList,encodeFace,tolerance=0.5)
            faceDistance=faceRecognition.face_distance(encodeList,encodeFace)
            self.name="Unknown"
            bestMatchIndex=numpy.argmin(faceDistance)

            if match[bestMatchIndex]:
                self.name=className[bestMatchIndex]
                self.name=nameList(self.name)
                y1,x2,y2,x1=faceLocation
                cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(image,self.name,(x1-6,y2+20),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255) ,1)
        return image   
    
    def connectToMainFile(self):
        from subprocess import call
        self.close()
        call(["python","loginWindow.py"])

if __name__=='__main__' :
    app= QApplication(sys.argv)
    ui=faceRecog()
    ui.show()
    sys.exit(app.exec_())   
