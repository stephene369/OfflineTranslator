# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl 
from PyQt5.QtGui import QIcon, QDesktopServices 
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, FluentBackgroundTheme)
from qfluentwidgets import FluentIcon as FIF

from .home import HomeWidget
from .packages import PackWidget 
from .settings import SettingWidget

from App.moduls import Translator

class Window(FluentWindow):

    def __init__(self):
        super().__init__()
        self.Translator = Translator()
        

        # create sub interface
        self.homeInterface = HomeWidget('Search Interface', self)
        self.packInterface = PackWidget("Packages" , self)
        self.settingInterface = SettingWidget('Setting', self)


        self.initNavigation()
        self.initWindow()
        self.updateItem()
        
        packages = [ str(i) for i in self.Translator.installedPackages() ]
        self.homeInterface.updateComboBox( packages=packages ) 
        self.packInterface.updateCombo(translator=self.Translator , homeWidget=self.homeInterface)

        self.homeInterface.combo.currentTextChanged.connect( self.initLang)
        self.homeInterface.translate_buton.clicked.connect( lambda : self.homeInterface.translation( tranlator=self.Translator ) )
        
        self.homeInterface.combo.currentTextChanged.connect(self.updateItem)

    def initLang(self): 
        self.Translator.isLangInit =False


    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')
        self.addSubInterface(self.packInterface, FIF.LIBRARY, 'Packges')

        self.navigationInterface.addSeparator()

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('stephene369', 'resources/images/logo.png'),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # add badge to navigation item


    def updateItem(self) :

        l = len(self.Translator.installedPackages())
        if l == 0 : text = "❗" 
        else : text = str(l)
        

        item = self.navigationInterface.widget(self.packInterface.objectName())        
        InfoBadge.attension(
            text= text ,
            parent=item.parent(),
            target=item,
            position=InfoBadgePosition.NAVIGATION_ITEM
        )

        # NOTE: enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resources/images/logo1.png'))
        self.setWindowTitle('Offline Translator')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        # use custom background color theme (only available when the mica effect is disabled)
        self.setCustomBackgroundColor(*FluentBackgroundTheme.DEFAULT_BLUE)
        # self.setMicaEffectEnabled(False)

        # set the minimum window width that allows the navigation panel to be expanded
        # self.navigationInterface.setMinimumExpandWidth(900)
        # self.navigationInterface.expand(useAni=False)

    def showMessageBox(self):
        w = MessageBox(
            'stephenew36@gmail.com',
            'Thank you for reaching out to us with your contributions and questions. We look forward to hearing from you!' , 
            self
        )
        w.yesButton.setText('github')
        w.cancelButton.setText('cancel')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/stephene369/"))


