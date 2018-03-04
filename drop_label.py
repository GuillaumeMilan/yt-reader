from PyQt5.QtWidgets import QLabel
from thread_lib import Threader
import pafy
from downloader import download_list

def void(none):
    """
################################################################################
#DESCRIPTION: 
#   This function is used initialize variable function to nothing
################################################################################
    """
    pass

def two_digit(value):
    if value<10 and value>=0:
        return "0"+str(value)
    else:
        return str(value)

def format_time(time):
    if time >= 3600:
        return str(int(time/3600))+":"+two_digit(int((time % 3600)/60))+":"+two_digit(time % 60)
    else :
        return str(int((time % 3600)/60))+":"+two_digit(time % 60)

def update_duration(param):
    # param = [[duration], url]
    print("Im getting executed")
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
            self.__time_label.setText("Playlist duration: "+format_time(self.__duration[0]))

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
        print("New duration :"+str(self.__duration))

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

    def download(self):
        """
################################################################################
# DESCRIPTION:
#   This function is used to download all the video in the list of the class
#   TODO
################################################################################
        """
        download_list(self.__video_list, ['Video', 'Best'])

    def save(self):
        """
################################################################################
# DESCRIPTION:
#   This function is used to save the playlist in a file for a future download
#   or for a future watch 
#   TODO
################################################################################
        """
        pass
 


