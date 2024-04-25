# coding:utf-8
import sys

from PyQt5.QtCore import QEasingCurve, Qt 
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout , QHBoxLayout , QSizePolicy

from qfluentwidgets import (SmoothScrollArea, TextEdit , 
                            VBoxLayout ,SubtitleLabel , 
                            ComboBox , TitleLabel , TransparentPushButton )
from qfluentwidgets import FluentIcon as FIF


from App.moduls import Translator 

from json import load

class HomeWidget(SmoothScrollArea):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        self.Frame = QFrame(self)
        self.HBOX = QHBoxLayout(self)
        self.HBOX.addWidget(self.Frame)

        with open("resources/home.qss" , encoding='utf-8') as f : 
            self.setStyleSheet( f.read() )
        
        self.setObjectName(text.replace(' ', '-'))
    
        self.initHomeInterface()

    def updateComboBox(self , packages:list) :
        if packages : 
            self.combo.clear()
            self.combo.addItems( sorted(packages ) )
            self.combo.setPlaceholderText("Choose packages")
            
            self.translate_buton.setEnabled(True)

        else : 
            self.combo.setPlaceholderText("No packages ❗❗")


    def updateLabel(self) : 
        current = self.combo.currentText()
        from_text = current.split(" → ")[0]
        to_text = current.split(" → ")[1]

        self.from_label.setText(from_text)
        self.to_label.setText(to_text)

    def initHomeInterface(self) : 
        self.frame1 = QFrame(self.Frame)
        self.frame2 = QFrame(self.Frame)

        self.Title = SubtitleLabel(self.frame1)
        self.Title.setText("Translate text from an languageto \nan other using your available Packages : ")

        self.combo = ComboBox(self.frame1)
        self.combo.currentTextChanged.connect(self.updateLabel)

        self.from_editor = TextEdit(self.frame2)
        self.from_editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.to_editor = TextEdit(self.frame2)
        self.to_editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            

        self.from_label = SubtitleLabel(self.frame2)
        self.to_label = SubtitleLabel(self.frame2)
        self.translate_buton = TransparentPushButton( FIF.PLAY_SOLID ,"Translate" ,self.frame2 )
        self.translate_buton.setEnabled(False)

        self.hbox_frame1 = QHBoxLayout(self.frame1)
        self.vbox_frame2 = QVBoxLayout(self.frame2)

        self.hbox_frame2 = QHBoxLayout(self.frame2)
        self.hbox_frame2.addWidget(self.from_label,0 , Qt.AlignmentFlag.AlignLeft)
        self.hbox_frame2.addWidget(self.translate_buton,0 , Qt.AlignmentFlag.AlignCenter)

        self.Vbox = QVBoxLayout(self.Frame)
        self.Vbox.addWidget(self.frame1, 0, Qt.AlignmentFlag.AlignTop)
        self.Vbox.addWidget(self.frame2, 1 , Qt.AlignmentFlag.AlignTop)

        self.hbox_frame1.addWidget(self.Title , 0 , Qt.AlignmentFlag.AlignLeft)
        self.hbox_frame1.addWidget(self.combo, 0 , Qt.AlignmentFlag.AlignLeft)

        self.vbox_frame2.addLayout(self.hbox_frame2)
        self.vbox_frame2.addWidget(self.from_editor , 1 , Qt.AlignmentFlag.AlignTop)
        self.vbox_frame2.addWidget(self.to_label , 0 , Qt.AlignmentFlag.AlignLeft)
        self.vbox_frame2.addWidget(self.to_editor, 1 , Qt.AlignmentFlag.AlignTop)



    def translation(self , tranlator:Translator ) :
        from_language = self.from_label.text()
        to_language = self.to_label.text()
        
        if tranlator.isLangInit == False : 
            tranlator.initLang( from_language=from_language , 
                           to_language=to_language )
            from_text = f"""{self.from_editor.toPlainText()}"""
            translated = tranlator.translate(text=from_text)

            self.to_editor.clear()
            self.to_editor.setPlainText(translated)
        else : 
            from_text = f"""{self.from_editor.toPlainText()}"""
            translated = tranlator.translate(text=from_text)

            self.to_editor.clear()
            self.to_editor.setPlainText(translated)
        