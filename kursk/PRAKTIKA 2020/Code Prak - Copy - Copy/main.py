from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen, QImage, QPixmap, QColor
from PyQt5.QtCore import Qt
from math import *
import numpy as np

from Color import *
from Point3D import *
from Polygon import *
from Vector3D import *
from Model import *
from ZBuffer import *
from Scene import *
from Static_Func import *
from Light import *


red = Qt.red
blue = Qt.blue
black = Qt.black
white = Qt.white
skyBlue = QColor(0, 127, 255)
size = {'width': 600, 'height':600 }
centerSun = Point3D(size['width'] // 2, 0, size['height'] // 2)
center = Point3D(size['width'] // 2, 0, size['height'])

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = QGraphicsScene(0, 0, size['width'], size['height'])
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(size['width'], size['height'], QImage.Format_RGB32)
        self.image.fill(skyBlue)
        self.MyScene = MyScene()
        self.MyScene.default()
        self.carDirecBtn.clicked.connect(lambda: carDirecBtnClicked(self))
        self.sceneDownBtn.clicked.connect(lambda: sceneDownBtnClicked(self))
        self.sceneUpBtn.clicked.connect(lambda: sceneUpBtnClicked(self))
        self.sceneLeftBtn.clicked.connect(lambda: sceneLeftBtnClicked(self))
        self.sceneRightBtn.clicked.connect(lambda: sceneRightBtnClicked(self))
        self.speedBtn.clicked.connect(lambda: speedBtnClicked(self))
        self.carRunBtn.clicked.connect(lambda: carRunBtnClicked(self))
        self.carStopBtn.clicked.connect(lambda: carStopBtnClicked(self))
        self.dialLight.valueChanged.connect(lambda: lightChange(self))
        self.shadowCheckBox.stateChanged.connect(lambda: shadowCheckBoxChanged(self))


    def addImage(self, image):
        pix = QPixmap()
        pix.convertFromImage(image)
        self.scene.addPixmap(pix)

def speedBtnClicked(win):
    print("Speed Btn Click")
    scene = win.MyScene
    scene.carSpeed = win.speedBox.value()

def carDirecBtnClicked(win):
    print("direc")
    scene = win.MyScene
    scene.carDirec *= -1
    print("car direc ", scene.carDirec)

def carRunBtnClicked(win):
    print("carRunBtnClicked")
    scene = win.MyScene
    c = 0
    scene.updateDinamic = True
    while (scene.updateDinamic):
        print(c, scene.carPositionZ)
        c += 1
        if (scene.carPositionZ >= 600):
            scene.carSpeed = -600
            scene.carPositionZ -= 600
        elif (scene.carPositionZ <= 0):
            scene.carSpeed = -600
            scene.carPositionZ += 600
        else:
            scene.carSpeed = win.speedBox.value()
            scene.carPositionZ += scene.carSpeed * scene.carDirec
        image = scene.show()
        win.addImage(image)
        QtWidgets.QApplication.processEvents()

def carStopBtnClicked(win):
    scene = win.MyScene
    scene.updateDinamic = False


def sceneDownBtnClicked(win):
    print("Down Btn Clecked")
    scene = win.MyScene
    teta = -pi / 10
    scene.goc_quay += teta
    print(scene.goc_quay)
    if (scene.goc_quay) < 0:
        return
    tranf = getMatrixRotateX(teta, center)
    scene.matrixTranform = scene.matrixTranform @ tranf
    scene.updateStatic = True
    image = scene.show()
    win.addImage(image)

def sceneUpBtnClicked(win):
    print("Up Btn Clecked")
    scene = win.MyScene
    teta = pi / 10
    scene.goc_quay += teta
    if (scene.goc_quay) > pi / 2:
        return
    tranf = getMatrixRotateX(teta, center)
    scene.matrixTranform = scene.matrixTranform @ tranf
    scene.updateStatic = True
    image = scene.show()
    win.addImage(image)

def sceneLeftBtnClicked(win):
    print("Left Btn Clecked")
    scene = win.MyScene
    teta = - pi / 2
    tranf = getMatrixRotateY(teta, centerSun)
    scene.matrixTranform = tranf @ scene.matrixTranform
    scene.sunTranform = scene.sunTranform @ tranf
    scene.updateStatic = True
    image = scene.show()
    win.addImage(image)

def sceneRightBtnClicked(win):
    print("Right Btn Clecked")
    scene = win.MyScene
    teta =  pi / 2
    tranf = getMatrixRotateY(teta, centerSun)
    scene.matrixTranform = tranf @ scene.matrixTranform
    scene.sunTranform = scene.sunTranform @ tranf
    scene.updateStatic = True
    image = scene.show()
    win.addImage(image)
    
def lightChange(win):
    print("Light Change: ...")
    scene = win.MyScene
    value = win.dialLight.value()
    value = value * -1 + 90
    print("\t\t\tvalue = ", value) 
    angle = (value / 180 * pi)
    pos = Vector3D(x = -cos(angle), y = -1, z = sin(angle))
    scene.sun = Light(pos)
    scene.updateSun = True
    image = scene.show()
    win.addImage(image)
    print('beta = ', scene.sun.beta)
    print('end')

def shadowCheckBoxChanged(win):
    scene = win.MyScene
    if win.shadowCheckBox.isChecked():
        print("Box Checked")
        if scene.withSadow == False:
            print('add shadow...')
            scene.withSadow = True
            image = scene.show()
            win.addImage(image)
            print('added end')
        
    else:
        print("Box UNcheck")
        if (scene.withSadow == True):
            scene.withSadow = False
            image = scene.show()
            win.addImage(image)
    
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = Window()

    win.image = win.MyScene.show()
    pix = QPixmap()
    pix.convertFromImage(win.image)
    win.scene.addPixmap(pix)
    win.show() 



    sys.exit(app.exec_())


import numpy as np

mat1 = np.matrix(getMatrixRotateX(pi / 6))
mat2 = np.linalg.inv(mat1)
mat3 =  mat2 @ mat1 @ mat2 @ mat1
b = mat3.tolist()[0]


