import sys,os
from downloader import download
from downloader import download_pafy
from combo_box import ComboDemo
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit
from PyQt5.QtWidgets import QPushButton, QLabel, QFrame
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor
from graphical_object import GraphicalObject
import pafy
import random 
import string

class GraphicalInterface(QMainWindow):
    def __init__(self, video_player):
        self.__app = QApplication(sys.argv)
        super().__init__()
        self.__video_player = video_player
# List of all derivated object from the following QWidgets 
        self.__palette = None
        self.__logo_image = None
# List of all the QWidget present in the main window 
        self.__searchbtn = None
        self.__searchbar = None
        self.__mainbox = None
        self.__modebox = None
        self.__logo = None
        self.__video_reader = None
# List of all the GraphicalObject in the main window 
        self.__header = None
        self.__footer = None
        self.__body = None
        self.__gr_searchbar = None
        self.__gr_searchbtn = None
        self.__gr_modebox = None
        self.__gr_logo = None
        self.__gr_video_reader = None
        self.__object_list = []
        
    def main(self):
        """ 
        Main loop of the graphic interface
        """
        self.resize(640, 480)
        self.move(0, 0)
        self.setWindowTitle('Youtube Reader')
        self.setWindowIcon(QIcon('resources/icon.svg'))
        self.setStyleSheet("QMainWindow {background: 'white';}");
        self.__mainbox = GraphicalObject(self, width = 640, height = 480, pos_x = 0, pos_y = 0)

        self.__header = GraphicalObject(None, width = 100, height = 10, pos_x = 0, pos_y = 0, parent = self.__mainbox)

        self.__searchbar=QLineEdit(self)
        self.__gr_searchbar = GraphicalObject(self.__searchbar, width = 70, height = 60, pos_x = 15, pos_y = 20, parent = self.__header)

        self.__searchbtn = QPushButton('Search', self)
        self.__searchbtn.clicked.connect(self.handle_research)
        self.__gr_searchbtn = GraphicalObject(self.__searchbtn, width = 10, height = 60, pos_x = 87, pos_y = 20, parent = self.__header)

        self.__logo_image = QPixmap('resources/logo.png')
        self.__logo = QLabel(self)
        self.__logo.setScaledContents(True)
        self.__logo.setPixmap(self.__logo_image)
        self.__gr_logo = GraphicalObject(self.__logo, width = 15, height = 60, pos_x = 0, pos_y = 20, parent = self.__header)

        self.__body = GraphicalObject(None, width = 100, height = 80, pos_x = 0, pos_y = 10, parent = self.__mainbox)
        if self.__video_player.get_mode() == 'Video':
            self.create_reader()
        self.__footer = GraphicalObject(None, width = 100, height = 10, pos_x = 0, pos_y = 90, parent = self.__mainbox)

        self.__modebox = ComboDemo(self, self)
        self.__modebox.init_combo_box(self.__video_player.get_mode())
        self.__gr_modebox = GraphicalObject(self.__modebox, width = 20, height = 100, pos_x = 80, pos_y = 20, parent = self.__footer)

        self.show()
        self.__app.exec_()
        self.__video_player.stop_stream()

    def handle_research(self):
        my_string = self.__searchbar.text()
        self.__searchbar.clear()
        print(my_string)
        if "www.youtube.com/" in my_string:
            self.__video_player.add_url(my_string)
        else:
            print("Search functionnality not implemented yet. Put url please!")
    
    def resizeEvent (self, event):
        print("OLD height: " + str(event.oldSize().height())+ " width: " + str(event.oldSize().width()))
        print("NEW height: " + str(event.size().height())+ " width: " + str(event.oldSize().width()))
        self.__mainbox.resize(event.size().width(), event.size().height())
    
    def create_reader(self):
        # code from github.com/devos50/vlc-pyqt5-example.git
        if sys.platform == "darwin" :
            from PyQt5.QtWidgets import QMacCocoaViewContainer
            self.__video_reader = QMacCocoaViewContainer(0)
        else:
            self.__video_reader = QFrame(self)
        self.__palette = self.__video_reader.palette()
        self.__palette.setColor (QPalette.Window,
                               QColor(0,0,0))
        self.__video_reader.setPalette(self.__palette)
        self.__video_reader.setAutoFillBackground(True)

        self.__gr_video_reader = GraphicalObject(self.__video_reader, width = 80, height = 80, pos_x = 10, pos_y = 10, parent = self.__body)

    def set_player_mode(self, value):
        self.__video_player.set_mode(value)
        if value == 'Video':
            self.__video_reader.show()
        else:
            if self.__video_reader != None and self.__gr_video_reader != None:
                self.__video_reader.hide()

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
