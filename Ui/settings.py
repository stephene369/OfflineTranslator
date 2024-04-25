# coding:utf-8
import sys
from PyQt5.QtCore import QEasingCurve, Qt 
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import SmoothScrollArea, PixmapLabel, widgets


class SettingWidget(SmoothScrollArea):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        self.Frame = QFrame(self)
        self.setWidget(self.Frame)

        with open("resources/settings.qss" , encoding='utf-8') as f : 
            self.setStyleSheet( f.read() )
        
        self.setObjectName(text.replace(' ', '-'))
