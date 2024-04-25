# coding:utf-8
import sys
from PyQt5.QtCore import QEasingCurve, Qt , QThread , pyqtSignal
from PyQt5.QtGui import QPixmap , QFont 
from PyQt5.QtWidgets import QFrame 
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (SmoothScrollArea, PixmapLabel, widgets , 
                            TitleLabel , SubtitleLabel, ComboBox , 
                            TransparentPushButton,BodyLabel, CaptionLabel,
                            StateToolTip, InfoBarPosition , InfoBar)

from qfluentwidgets import FluentIcon as FIF

from .home import HomeWidget
from PyQt5.QtWidgets import QVBoxLayout , QHBoxLayout

from App.moduls import Translator

class Frame(QFrame) : 
    def __init__(self,title, subtitle,butonText,icon , parent=None) -> None:
        super().__init__(parent )

        self.frame1 = QFrame(self)
        self.frame2 = QFrame(self)

        self.Hbox = QHBoxLayout(self)       
        self.Hbox.addWidget(self.frame1,0,Qt.AlignmentFlag.AlignLeft)
        self.Hbox.addWidget(self.frame2,0,Qt.AlignmentFlag.AlignRight)

        self.title = SubtitleLabel(title , self.frame1)
        self.subTitle = CaptionLabel(subtitle , self.frame1)
        self.subTitle.setObjectName("Subtitle")
        font = QFont() ; font.setPointSize(15) ; self.subTitle.setFont( font )

        self.vbox1 = QVBoxLayout(self.frame1)
        self.vbox1.addWidget(self.title, 0 , Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)        
        self.vbox1.addWidget(self.subTitle, 0 , Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)

        self.button = TransparentPushButton( icon , butonText , self.frame2)
        self.combo = ComboBox(self.frame2)

        self.vbox2 = QVBoxLayout(self.frame2)
        self.vbox2.addWidget(self.button, 0 , Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)
        self.vbox2.addWidget(self.combo, 0 , Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)

        

class PackWidget(SmoothScrollArea):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        self.Frame = QFrame(self)

        with open("resources/packages.qss" , encoding='utf-8') as f : 
            self.setStyleSheet( f.read() )
        
        self.setObjectName(text.replace(' ', '-'))

        self.initFrame()

    def initFrame(self) : 
        self.frame1 = Frame( 
            title="Install" , 
            subtitle="You can install new packages, \nor update existing" , 
            butonText="Install" , 
            parent=self.Frame , 
            icon=FIF.DOWNLOAD
         )
        
        self.frame2 = Frame(
            title="Delete" , 
            subtitle="Remove installed packages.\nYou will not be able to translate text with deleted packages." , 
            butonText="Delete" , 
            parent=self.Frame , 
            icon=FIF.REMOVE )

        self.Vbox = QVBoxLayout(self.Frame )
        self.Vbox.addWidget(self.frame1)
        self.Vbox.addWidget(self.frame2)
    
    def updateCombo(self , translator:Translator , homeWidget:HomeWidget) : 
        self.frame1.combo.clear()
        self.frame1.combo.addItems( translator.available_packages_list )

        self.frame2.combo.clear()
        self.frame2.combo.addItems( [ str(i) for i in translator.installedPackages() ] )

        print("Installing")
        self.frame1.button.clicked.connect( lambda : self.installLanguagesPackages(translator=translator , homeWidget=homeWidget) )
        #self.frame2.button.clicked.connect( lambda : self.deleteLanguagesPackages(translator=translator) )
        self.frame2.button.setEnabled(False)

    def installLanguagesPackages(self,translator:Translator , homeWidget:HomeWidget) :
        self.frame1.button.setEnabled(False) 
        self.stateToolTip = None

        splited = self.frame1.combo.currentText().split(" -> ")
        from_language = splited[0]
        to_language = splited[1]

        self.worker = Worker(translator=translator , from_language=from_language , to_language=to_language )
        self.worker.finished.connect(self.finishedInstallation)
        self.worker.finished.connect( lambda : self.updateHomeCombo(homeWidget=homeWidget , translator=translator) )
        self.worker.start()

        self.stateToolTip = StateToolTip('Installation', f'Installing Packges {from_language} -> {to_language} ....', 
                                        self)
        self.stateToolTip.move(510, 80)
        self.stateToolTip.show()

    def updateHomeCombo(self , homeWidget:HomeWidget , translator:Translator) :
        packages = [str(i) for i in translator.installedPackages()]
        homeWidget.updateComboBox(packages = packages)


    def finishedInstallation(self , message): 
        
        self.frame1.button.setEnabled(True)
        self.stateToolTip.setContent( "Intallation finished" )
        self.stateToolTip.setState(True)
        self.stateToolTip = None

        if message == True :
            self.createSuccessInfoBar()
        else : 
            self.createErrorInfoBar()


    def createSuccessInfoBar(self):
        # convenient class mothod
        InfoBar.success(
            title='Success',
            content="The package is successfull install.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=-1,
            parent=self.Frame
        )

    def createErrorInfoBar(self):
        InfoBar.error(
            title='Error',
            content="The packages is not installed, check you internet connection",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,    # won't disappear automatically
            parent=self.Frame
        )



    def deleteLanguagesPackages(self , translator:Translator) : 
        splited = self.frame1.combo.currentText().split(" -> ")
        from_language = splited[0]
        to_language = splited[1]

        translator.uninstallPackage(from_language=from_language, to_language=to_language)


class Worker(QThread):
    finished = pyqtSignal(bool)

    def __init__(self, translator: Translator, from_language, to_language):
        super().__init__()
        self.translator = translator
        self.from_language = from_language
        self.to_language = to_language

    def run(self) :
        try :
            self.translator.installLanguagesPackages(from_language=self.from_language, to_language=self.to_language)
            success = True
            self.finished.emit(success)
        except Exception as e :
            success = False 
            self.finished.emit( success )


