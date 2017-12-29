import sys,os
from downloader import download
from downloader import download_pafy
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
import pafy
import random 
import string

def verify(value):
    """ Verify that value is between 0 and 100 """ 
    if value >= 0 and value <= 100:
        return True 
    else :
        return False

class GraphicalObject():
    def __init__(self, obj, width = -1, height = -1, pos_x = 0, pos_y = 0, parent=None, children=[]):
        """
            height and width are in procent of the parent window.
            if there is no parent, this is in pixel.
            object @type is QObject can be None 
            parent @type is GraphicalObject
            children @type is GraphicalObject
            width height @type are int (can be percent or real size depending if parent is None or not )
        """
        self.__object = obj
        self.__parent = parent
        self.__percent_pos_x = 0
        self.__percent_pos_y = 0
        self.__pos_x = 0
        self.__pos_y = 0
        self.__percent_height = -1
        self.__percent_width = -1
        self.__width = -1
        self.__height = -1
        if parent == None:
            self.__height = height
            self.__width = width
            self.__percent_height = -1
            self.__percent_width = -1
            self.__pos_x = pos_x
            self.__pos_y = pos_y
        else: 
            # Verify percent size is correct (0-100)
            if (not verify(height)) or (not verify(width)):
                raise ValueError("The size given is not a percent size")
            self.__percent_height = height
            self.__percent_width = width
            self.__percent_pos_x = pos_x
            self.__percent_pos_y = pos_y
            self.__height = (parent.getRealHeight()*height) /100
            self.__width = (parent.getRealWidth()*width)    /100
            self.__pos_y = (parent.getRealHeight()*pos_y)   /100
            self.__pos_x = (parent.getRealWidth()*pos_x)    /100

    def getSize(self):
        if parent == None: 
            return (self.__width, self.__height)
        else :
            return parent.getSize()
    
    def getRealHeight(self):
        return self.__height
    
    def getRealWidth(self):
        return self.__width

    def getPercentHeight(self):
        return slef.__percent_height

    def getPercentWidth(self):
        return self.__percent_width

    def resize(self, width, height):
        if parent == None:
            self.__height = height
            self.__width = width
            self.__percent_height = -1
            self.__percent_width = -1
        else: 
            # Verify percent size is correct (0-100)
            if (not verify(height)) or (not verify(width)):
                raise ValueError("The size given is not a percent size")
            self.__percent_height = height
            self.__percent_width = width
            self.__height = (parent.getRealHeight()*height) /100
            slef.__width = (parent.getRealWidth()*width)    /100
        if slef.__object != None:
            self.__object.resize(self.__width, self.__height)

    def move(self, pos_x, pos_y):
        if parent == None:
            self.__pos_x = pos_x
            self.__pos_y = pos_y
            self.__percent_pos_x = 0
            self.__percent_pos_y = 0
        else:
            # Verify percent size is correct (0-100)
            if (not verify(pos_x)) or (not verify(pos_y)):
                raise ValueError("The position given is not a percent size")
            self.__percent_pos_x = pos_x
            self.__percent_pos_y = pos_y 
            self.__pos_x = (parent.getRealWidth()*pos_x)    /100
            self.__pos_y = (parent.getRealHeight()*pos_y)   /100
        if self.__object != None:
            self.__object.move(slef.__pos_x, slef.__pos_y)

class GraphicalInterface(QMainWindow):
    def __init__(self, video_player):
        self.__app = QApplication(sys.argv)
        super().__init__()
        self.__video_player = video_player
        self.__search_btn = None
        self.__textbox = None
        self.__object_list = []
    def main(self):
        """ 
        Main loop of the graphic interface
        """
        self.resize(640, 480)
        self.move(0, 0)
        self.setWindowTitle('Youtube Reader')
        self.setWindowIcon(QIcon('resources/icon.svg'))
        
        self.__textbox=QLineEdit(self)
        self.__textbox.move(20,20)
        self.__textbox.resize(280,40)

        self.__search_btn = QPushButton('Search', self)
        self.__search_btn.clicked.connect(self.handle_research)
        self.__search_btn.move(300,20)
        self.__search_btn.resize(40,40)

        self.show()
        self.__app.exec_()
        self.__video_player.stop_stream()

    def handle_research(self):
        print(self.__textbox.text())
        self.__textbox.clear()
    
    def resizeEvent (self, event):
        print("OLD height: " + str(event.oldSize().height())+ " width: " + str(event.oldSize().width()))
        print("NEW height: " + str(event.size().height())+ " width: " + str(event.oldSize().width()))

class CommandLineInterface:
    """ 
        This class provide a command line interface for the music player
    """
    def __init__(self, video_player): 
#define the currently playing video url 
        self.__url = "" 
#define the player to use for this interface 
        self.__video_player = video_player
#define the list of url to display for the next videos
        self.__urls = []
#define if the user ask to quit the command line 
        self.__continue = True
    def set_next_music(self): 
        self.__video_player.skip()

    def get_current_music(self): 
        print(self.__url)

    def __crypt(self):
        rand_str = lambda n: ''.join([random.choice(string.ascii_letters+string.punctuation+string.digits) for i in range(n)])
        rows, columns = os.popen('stty size', 'r').read().split()
        print("")
# Now to generate a random string of length 10
        for i in range(0,int(rows)):
            s = rand_str(int(columns))  
            print(s)

    def main(self): 
        sys.stdout.write(">>>")
        while self.__continue : 
            command = input()
            commands = command.split(" ")
            if commands[0] == "url":
                for i in commands [1:]: 
                    self.__video_player.add_url(i)
            elif commands[0] == "skip" :
                self.set_next_music()
            elif commands[0] == "stop" or commands[0] == "quit" or commands[0] == "exit":
                self.__continue = False
                self.__video_player.stop_stream()
                print("Stopping the player")
                return 
            elif commands[0] == "set": 
                self.__video_player.set_time(int(float(commands[1])))
            elif commands[0] == "help": 
                print("The commands available are: ")
                print("    url [list of urls]")
                print("    stop")
                print("    play")
                print("    pause")
                print("    skip")
                print("    quality <quality> (only Best available)")
                print("    mode <Video,Audio>")
                print("    set <time in sec>")
                print("    dl <file_name>")
            elif commands[0] == "dl":
                if commands[1] == "current":
                    download_pafy(self.__video_player.get_current(),self.__video_player.get_mode())
                elif commands[1] == "playlist":
                    playlist = self.__video_player.get_playlist()
                    for i in playlist:
                        download_pafy(i, self.__video_player.get_mode())
                else :
                    download(commands[1],self.__video_player.get_mode())
            elif commands[0] == "set":
                #need to parse time over a minute to the format hh:mm:ss
                self.__video_player.set_time(int(float(commands[1]))*10)
            elif commands[0] == "quality": 
                self.__video_player.set_quality(commands[1])
            elif commands[0] == "mode": 
                self.__video_player.set_mode(commands[1])
            elif commands[0] == "pause": 
                self.__video_player.pause_stream()
            elif commands[0] == "playlist":
                self.__video_player.to_play()
            elif commands[0] == "history": 
                self.__video_player.history()
            elif commands[0] == "current":
                self.__video_player.is_playing()
            elif commands[0] == "time":
                self.__video_player.get_time()
            elif commands[0] == "play": 
                if self.__video_player.is_running():
                    if self.__video_player.is_paused(): 
                        print("Unpausing the player")
                        self.__video_player.resume_stream()

                    elif self.__video_player.is_playing(): 
                        print("The player is already playing. Verify your sound level.")
                    else: 
                        self.__video_player.play_stream()
                else :
                    self.__video_player.play_stream()
            elif commands[0] == "vol":
                self.__video_player.set_volume(int(commands[1]))
            elif commands[0] == "crypt":
                self.__crypt()
            elif commands[0] == "":
                pass
            else :
                print(commands[0])
                print("Command not found!")
            sys.stdout.write(">>>")
