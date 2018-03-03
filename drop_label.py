from PyQt5.QtWidgets import QLabel
from thread_lib import Threader
import pafy

def void(none):
    pass

def update_duration(param):
    # param = [[duration], url]
    video = pafy.new(param[1])
    param[0][0] = param[0][0] + video.length

class VideoDropLabel(QLabel):

    def __init__(self, title, parent, time_label):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.__video_list = []
        self.__event_function = void
        self.__duration = [0]
        self.__threader = Threader()
        self.__threader.start()
        self.__time_label = time_label
        self.updateTimeLabel(None)
    
    def updateTimeLabel(self, none):
        if self.__time_label != None:
            self.__time_label.setText(str(self.__duration[0]))

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())
        self.__event_function(None)
        self.__video_list.append([e.mimeData().text()])
        self.__threader.addInstruction([update_duration, void, self.updateTimeLabel, None, [self.__duration, self.__video_list[-1][0]], self.__duration])
        print("New list element: "+self.__video_list[-1][0])
        print("New durantion :"+str(self.__duration))

    def connect(self, function):
        self.__event_function = function

    def getList():
        return self.__video_list

    def resetDownloadList(new_list):
        self.__video_list = new_list
        self.__duration = self.getListDuration(new_list)
    
    def getListDuration(new_list):
        duration = 0
        for i in new_list :
            video = pafy.new(i[0])
            duration += video.length
        return duration
