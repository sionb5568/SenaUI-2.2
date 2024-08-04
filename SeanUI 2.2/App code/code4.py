import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Web')


        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))  

   
        self.setCentralWidget(self.browser)


        self.showFullScreen()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebBrowser()
    sys.exit(app.exec_())
