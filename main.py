""" coding:utf-8

# By Stephene WANTCHEKON 

### GITHUB : 
https://github.com/stephene369


### LINKEDIN : 
https://www.linkedin.com/in/stephene-wantchekon-b13322252/


### FACEBOOK : 
https://www.facebook.com/stephene.wantchekon/


### INSTAGRAM : 
https://www.instagram.com/stephene.nk/

### coding:utf-8"""


from Ui.window import * 


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()

    
