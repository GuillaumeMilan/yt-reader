from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import urllib.request

class ThumbLabel(QLabel):

    def __init__(self, parent):
        super().__init__(parent)
        self.__thumb = None
        
    def setUrl(self, url):
        data = urllib.request.urlopen(url).read()
        tmp_image = QImage()
        tmp_image.loadFromData(data)
        self.__thumb = QPixmap(tmp_image)

    def resize(self, w, h):
        super().resize(w, h)
        self.setPixmap(self.__thumb.scaled(w, h, Qt.KeepAspectRatio))
        
