from PyQt5.QtWidgets import QLabel
from thread_lib import Threader
import pafy

def void():
    pass
def update_duration(param):
    # param = [[duration], url]
    video = pafy.new(param[1])
    param[0][0] = param[0][0] + video.length

class DropLabel(QLabel):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.__download_list = []
        self.__event_function = void
        self.__duration = 0
        self.__threader = Threader()
        self.__threader.start()

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())
        self.__event_function()
        self.__download_list.append([e.mimeData().text()])
        video = pafy.new(self.__download_list[-1][0])
        self.__duration += video.length
        print("New list element: "+self.__download_list[-1][0])
        print("New durantion :"+str(self.__duration))

    def connect(self, function):
        self.__event_function = function

    def getDownloadList():
        return self.__download_list

    def resetDownloadList(new_list):
        self.__download_list = new_list
        self.__duration = self.getListDuration(new_list)
    
    def getListDuration(new_list):
        duration = 0
        for i in new_list :
            video = pafy.new(i[0])
            duration += video.length
        return duration
