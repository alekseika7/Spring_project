#!/usr/bin/python3.7

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon
import sys
import cv2
import qimage2ndarray
import car


class Window(QWidget):
    
    def __init__(self):
        
        super().__init__()
        
        self.stream_res = [480,320]
         
        self.initWindow()
        self.initCamera()
          
       
    def initWindow(self):
        
        
        self.setGeometry(100, 100, 490, 490)
        self.setWindowTitle('Car')
        self.setWindowIcon(QIcon('r.png'))
        
        grid = QGridLayout()
        grid.setSpacing(5)
        
        b_front = QPushButton('(W)', self)
        b_front.setIcon(QIcon('up.png'))
        b_front.setIconSize(QSize(30,30))
        grid.addWidget(b_front, 3, 1)
        
        b_back = QPushButton('(S)', self)
        b_back.setIcon(QIcon('down.png'))
        b_back.setIconSize(QSize(30,30))
        grid.addWidget(b_back, 4, 1)
        
        b_right = QPushButton('(D)', self)
        b_right.setIcon(QIcon('right.png'))
        b_right.setIconSize(QSize(30,30))
        grid.addWidget(b_right, 4, 2)
        
        b_left = QPushButton('(A)', self)
        b_left.setIcon(QIcon('left.png'))
        b_left.setIconSize(QSize(30,30))
        grid.addWidget(b_left, 4, 0)
        
        b_exit = QPushButton('', self)
        b_exit.setIcon(QIcon('exit.png'))
        b_exit.setIconSize(QSize(30,30))
        b_exit.clicked.connect(QCoreApplication.instance().quit)
        grid.addWidget(b_exit, 4, 5)
        
        self.label = QLabel('No Camera Found')
        grid.addWidget(self.label, 0, 0, 2, 5)
        
        self.setLayout(grid)
        
        self.show()
        
        
    def initCamera(self):
            
        self.vs = cv2.VideoCapture(0)
        self.vs.set(cv2.CAP_PROP_FRAME_WIDTH, self.stream_res[0])
        self.vs.set(cv2.CAP_PROP_FRAME_HEIGHT, self.stream_res[1])
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.stream)
        self.timer.start(60)
        
        
    def stream(self):
        
        _, frame = self.vs.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(frame)
        self.label.setPixmap(QPixmap.fromImage(image))

    
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_A and not event.isAutoRepeat():
            car.turn('left')
            print('left')
        elif key == Qt.Key_D and not event.isAutoRepeat():
            car.turn('right')
            print('right')
        elif key == Qt.Key_S and not event.isAutoRepeat():
            car.move('back')
            print('back')
        elif key == Qt.Key_W and not event.isAutoRepeat():
            car.move('front')
            print('front')
            
            
    def keyReleaseEvent(self, event):
        key = event.key()
        if key in (Qt.Key_A, Qt.Key_D, Qt.Key_S, Qt.Key_W) and not event.isAutoRepeat():
            car.motors_off()
        
     

if __name__ == '__main__':
    car.init()
    app = QApplication(sys.argv)
    W = Window()
    sys.exit(app.exec_())
    car.off_n_reset()
    