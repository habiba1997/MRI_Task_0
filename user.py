from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QFileDialog
import cv2
import numpy as np
import sys
import math
import qimage2ndarray
import threading
from output import Ui_MainWindow


class Window(QtWidgets.QMainWindow):
    

    changedValue = pyqtSignal()

    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.get_image)
        
        # Making the connection
        self.changedValue.connect(self.changeProgressBarValue)

        self.error_dialog = None

        self.img = None
        self.fimg_const = None
        self.fimg_original = None
        self.fimg_copy = None

        self.afra7_flag = False
        self.outer_loop_saved = None
        self.Lower_loop_saved = None
        
        
        self.step = 1
        self.ui.progressBar.setRange (0, 520)

        self.pauseFlag = False
        
        self.borderLoops = 4

        self.ui.pushButton_2.clicked.connect(self.pauseAndResume)

        self.InitWindow(self)

        

    @pyqtSlot()
    def changeProgressBarValue(self):
        if self.step >= 520:
            self.step = 0
        self.step = self.step + 1
        self.ui.progressBar.setValue(self.step)

  
        
    def InitWindow(self, Window):
    
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.show()
        

    def pauseAndResume(self):
        if self.pauseFlag == False:
            self.pauseFlag = True
            self.ui.pushButton_2.setText("Start")
        else:
            self.pauseFlag = False
            self.ui.pushButton_2.setText("Start")


        print("pause")

    def get_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.jpg *.gif)")
        self.img = cv2.imread(fname[0], 0)
        if self.img is None:
            return self.show_error()

        self.afra7_flag = False

        self.fimg_original = np.fft.fft2(self.img)
        self.fimg_copy = self.fimg_original.copy()
        self.fimg_const = self.fimg_original.copy()

        self.show_images()
        self.step =0
        
        self.thread= threading.Thread(target=self.sho8l_afra7)
        self.thread.start()


    


    def sho8l_afra7(self):
        self.afra7_flag = True
        size = self.fimg_original.shape[0]
        size = size / 2
        size = math.floor(size)
        self.pauseFlag = False

        while True:
            
            self.borderLoops= (int) (self.ui.lineEdit.text())

            if self.pauseFlag:
                break
           
            i = 0
            while i < size:
                if self.pauseFlag:
                 break

                if not self.afra7_flag:
                    return

                endlimit = i + self.borderLoops
                self.fimg_original[i:endlimit, :] = 0
                self.fimg_original[:, i:endlimit] = 0
                j = -1 * (i + 1)
                endlimit = j - self.borderLoops
                self.fimg_original[endlimit:j, :] = 0
                self.fimg_original[:, endlimit:j] = 0
                i = i + self.borderLoops
                self.img = np.fft.ifft2(self.fimg_original).real
                self.fimg_copy = self.fimg_original.copy()
                self.show_images()
                for loop in range(self.borderLoops):
                    self.changedValue.emit()


            if self.pauseFlag:
                break
            self.fimg_original = self.fimg_const.copy()
            self.show_images()

            j = size - 1
            for i in range(0, size).__reversed__():
                if self.pauseFlag:
                    break
                if not self.afra7_flag:
                    return
                j = j + 1
                for r in range(i, j + 1):
                    for c in range(i, j + 1):
                        self.fimg_original[r, c] = 0
                
                self.changedValue.emit()


                self.img = np.fft.ifft2(self.fimg_original).real
                self.fimg_copy = self.fimg_original.copy()
                self.show_images()
               


            self.fimg_original = self.fimg_const.copy()
            self.show()
            
          
    def show_images(self):

        # height, width = img.shape
        # bytesPerLine = 1 * width
        q_img = qimage2ndarray.array2qimage(self.img)
        self.ui.label.setPixmap(QPixmap(q_img))
        # height, width = fimg.shape
        # bytesPerLine = 1 * width
        q_img = qimage2ndarray.array2qimage(self.fimg_copy)
        self.ui.label_2.setPixmap(QPixmap(q_img))
        self.ui.label.show()
        self.ui.label_2.show()

    def show_error(self):
        self.error_dialog = QtWidgets.QErrorMessage()
        self.error_dialog.showMessage("الصورة دي مش نافعة يا زميلي")


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
