from PyQt5.QtWidgets import QLabel
import pafy

def void():
    pass

class DropLabel(QLabel):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.__download_list = []
        self.__event_function = void()

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())
        self.__download_list.append([e.mimeData().text()])
        print("New list element: "+self.__download_list[-1][0])
        self.__event_function()

    def connect(self, function):
        self.__event_function = function

    def getDownloadList():
        return self.__download_list

    def resetDownloadList(new_list):
        self.__download_list = new_list
    
    def getPlaylistDuration():
        duration = 0
        for i in self.__download_list :
            video = pafy.new(i[0])
            duration += video.length
        return duration
