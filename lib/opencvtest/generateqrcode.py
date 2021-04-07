from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
from PyQt5.uic import loadUiType

import os
from os import path
import pyqrcode
ui,_ = loadUiType('generate.ui')
class MainApp(QMainWindow , ui):
    def __init__(self , parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handel_generate)

    def handel_generate(self):
        code=self.lineEdit.text()
        name=self.lineEdit_2.text()
        if len(code)!=10:
            warning = QMessageBox.warning(self , 'Error ' , "card code must be 10 digits . " )
        else:
            qr=pyqrcode.create(code) 
            qr.png(name+'.png',scale=8)
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()