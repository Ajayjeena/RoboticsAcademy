

__author__ = 'frivas'


import resources_rc
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from gui.form import Ui_MainWindow
from gui.widgets.cameraWidget import CameraWidget
from gui.widgets.logoWidget import LogoWidget
from gui.widgets.graphicWidget import GLWidget


class MainWindow(QMainWindow, Ui_MainWindow):

    updGUI=pyqtSignal()
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.graphic=GLWidget(self)
        self.graphicLayout.addWidget(self.graphic)
        self.graphic.setVisible(True)
        self.logo = LogoWidget(self)
        self.logoLayout.addWidget(self.logo)
        self.logo.setVisible(True)

        self.pushButton.clicked.connect(self.playClicked)
        self.pushButton.setCheckable(True)
	self.resetButton.clicked.connect(self.resetClicked)

        self.updGUI.connect(self.updateGUI)
        self.camera1=CameraWidget(self)

        #self.stopButton.clicked.connect(self.stopClicked)

    def updateGUI(self):
        #print 'update gui'
        self.camera1.updateImage()
        self.graphic.updateGL()

    
    def plot(self):
    	self.graphic.render_point(point[:3], point[3:], radius)
    
    def getCamera(self, lr):
        if(lr == 'left'):
        	return self.cameraL
        elif(lr == 'right'):
        	return self.cameraR
        else:
        	print("Invalid Camera")
        	exit()

    def setCamera(self,camera, lr):
        if(lr == 'left'):
        	self.cameraL=camera
        elif(lr == 'right'):
        	self.cameraR = camera
        else:
        	print("Invalid Camera")
        	exit()

    def setPlot(self, listener):
    	self.point = listener
    	
    def getPlot(self):
    	return self.point
    
    def playClicked(self):
        if self.pushButton.isChecked():
            self.pushButton.setText('Stop Code')
            self.pushButton.setStyleSheet("background-color: #7dcea0")
            self.algorithm.play()
        else:
            self.pushButton.setText('Play Code')
            self.pushButton.setStyleSheet("background-color: #ec7063")
            self.algorithm.stop()

    def resetClicked(self):
    	self.graphic.reset_view()
    
    def setAlgorithm(self, algorithm ):
        self.algorithm=algorithm

    def getAlgorithm(self):
        return self.algorithm

    def setXYValues(self,newX,newY):
        #print ("newX: %f, newY: %f" % (newX, newY) )
        myW=-newX*self.motors.getMaxW()
        myV=-newY*self.motors.getMaxV()
        self.motors.sendV(myV)
        self.motors.sendW(myW)
        None

    def stopClicked(self):
        self.motors.sendV(0)
        self.motors.sendW(0)
        self.teleop.returnToOrigin()

    def closeEvent(self, event):
        self.algorithm.kill()
        self.cameraL.stop()
        self.cameraR.stop()
        event.accept()
