import sys,os
from downloader import download
from downloader import download_pafy
from combo_box import ComboMode
from drop_label import VideoDropLabel
from translucid_button import TranslucidButton
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit
from PyQt5.QtWidgets import QPushButton, QLabel, QFrame
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor
from graphical_object import GraphicalObject
import pafy
import random 
import string

def read_css(fname):
    with open(fname) as f:
        content = f.read()
    return content

class Interface:
    def end_of_play_list(self):
        pass 

    def update_title(self,title):
        print("----------")
        print(title)
        print("----------")

class GraphicalInterface(QMainWindow,Interface):
    def __init__(self, video_player, debug = False):
        self.__app = QApplication(sys.argv)
        super().__init__()
        self.__video_player = video_player
#TODO get in .config the value of the volume by default 
        self.__video_player.set_volume(100)
# Property of the main window
        self.__width = 0
        self.__height = 0
# List of all derivated object from the following QWidgets 
        self.__palette = None
        self.__drop_color = None
        self.__logo_image = None
        self.__previousbtn_image = None
        self.__skipbtn_image = None
        self.__playbtn_image = None
        self.__pausebtn_image = None
# List of all the QWidget present in the main window 
        self.__videotitle = None
        self.__searchbtn = None
        self.__searchbar = None
        self.__mainbox = None
        self.__modebox = None
        self.__logo = None
        self.__video_reader = None
        self.__previousbtn_audio = None
        self.__playbtn_audio = None
        self.__skipbtn_audio = None
        self.__previousbtn_video = None
        self.__playbtn_video = None
        self.__skipbtn_video = None
        self.__buttonbar_video = None
        self.__drop_area = None
        self.__playlist_time = None
# List of all the GraphicalObject in the main window 
        self.__header = None
        self.__footer = None
        self.__body = None
        self.__gr_videotitle = None
        self.__gr_searchbar = None
        self.__gr_searchbtn = None
        self.__gr_modebox = None
        self.__gr_logo = None
        self.__gr_video_reader = None
        self.__gr_buttonbar_video = None
        
        self.__gr_previousbtn_audio = None
        self.__gr_playbtn_audio = None
        self.__gr_skipbtn_audio = None
        self.__gr_previousbtn_video = None
        self.__gr_playbtn_video = None
        self.__gr_skipbtn_video = None
        self.__gr_drop_area = None
        self.__gr_playlist_time = None

        self.__object_list = []

        self.__debug = debug
        
    def main(self):
        """ 
        Main loop of the graphic interface
        """
        self.resize(640, 480)
        self.move(0, 0)
        self.setWindowTitle('Youtube Reader')
        self.setWindowIcon(QIcon('resources/icon.svg'))
        content = read_css("./css/main.css")
        self.setStyleSheet(content)
        self.__mainbox = GraphicalObject(self, width = 640, height = 480, pos_x = 0, pos_y = 0)

        self.__header = GraphicalObject(None, width = 100, height = 10, pos_x = 0, pos_y = 0, parent = self.__mainbox)

        self.__searchbar = QLineEdit(self)
        self.__searchbar.returnPressed.connect(self.handle_research)
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
        

        self.create_reader()
        self.set_player_mode(self.__video_player.get_mode())
        
        self.__footer = GraphicalObject(None, width = 100, height = 10, pos_x = 0, pos_y = 90, parent = self.__mainbox)

        self.__modebox = ComboMode(self, self)
        self.__modebox.init_combo_box(self.__video_player.get_mode())
        modebox_css = read_css("./css/combo_box.css")
        self.__modebox.setStyleSheet(modebox_css)
        self.__gr_modebox = GraphicalObject(self.__modebox, width = 20, height = 100, pos_x = 80, pos_y = 20, parent = self.__footer)

        self.show()
        self.__app.exec_()
        self.__video_player.stop_stream()

    def handle_research(self):
        my_string = self.__searchbar.text()
        self.__searchbar.clear()
        if "www.youtube.com/" in my_string:
            self.__video_player.add_url(my_string)
        else:
            print("Search functionnality not implemented yet. Put url please!")
        
    def create_reader(self):
        # code from github.com/devos50/vlc-pyqt5-example.git
        # Video UI
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

        self.__videotitle = QLabel("No Video!", self)
        self.__videotitle.setWordWrap(True)
        self.__gr_videotitle = GraphicalObject(self.__videotitle, width = 80, height = 10, pos_x = 10, pos_y = 90, parent = self.__body)
        

        number_of_button = 3
        btn_height = 7
        btn_width = 7
        ui_origin_x = 0
        ui_origin_y = 100 - btn_height
        self.__buttonbar_video = QLabel(self)
        self.__buttonbar_video.setStyleSheet("QLabel { background-color : white; color : blue; }");
        self.__gr_buttonbar_video = GraphicalObject(self.__buttonbar_video, width = 100, height = btn_height, pos_x = 0, pos_y = ui_origin_y, parent = self.__gr_video_reader)

        self.__previousbtn_video = TranslucidButton(self)
        self.__previousbtn_image = QPixmap('resources/back.svg')
        self.__previousbtn_video.setScaledContents(True)
        self.__previousbtn_video.setPixmap(self.__previousbtn_image)
        self.__gr_previousbtn_video = GraphicalObject(self.__previousbtn_video, width = btn_width, height = btn_height, pos_x = ui_origin_x+0*btn_width, pos_y = ui_origin_y, parent = self.__gr_video_reader)

        self.__skipbtn_video = TranslucidButton(self)
        self.__skipbtn_image = QPixmap('resources/skip.svg')
        self.__skipbtn_video.setScaledContents(True)
        self.__skipbtn_video.setPixmap(self.__skipbtn_image)
        self.__gr_skipbtn_video = GraphicalObject(self.__skipbtn_video, width = btn_width, height = btn_height, pos_x = ui_origin_x+2*btn_width, pos_y = ui_origin_y, parent = self.__gr_video_reader)

        self.__playbtn_video = TranslucidButton(self)
        self.__playbtn_video.clicked.connect(self.video_play_pause)
        self.__playbtn_image = QPixmap('resources/play.svg')
        self.__playbtn_video.setScaledContents(True)
        self.__playbtn_video.setPixmap(self.__playbtn_image)
        self.__gr_playbtn_video = GraphicalObject(self.__playbtn_video, width = btn_width, height = btn_height, pos_x = ui_origin_x+1*btn_width, pos_y = ui_origin_y, parent = self.__gr_video_reader)

        # Audio UI 
        number_of_button = 3
        btn_height = 5
        btn_width = 10
        ui_origin_x = 30
        ui_origin_y = 50 - (btn_height/2)

        self.__previousbtn_audio = QPushButton('Previous', self)
        #clicked.connect(self.handle_research)
        self.__gr_previousbtn_audio = GraphicalObject(self.__previousbtn_audio, width = btn_width, height = btn_height, pos_x = ui_origin_x+(0*(100-2*ui_origin_x))/number_of_button, pos_y = ui_origin_y, parent = self.__body)

        self.__playbtn_audio = QPushButton('Play', self)
        self.__playbtn_audio.clicked.connect(self.audio_play_pause)
        self.__gr_playbtn_audio = GraphicalObject(self.__playbtn_audio, width = btn_width, height = btn_height, pos_x = ui_origin_x+(1*(100-2*ui_origin_x))/number_of_button, pos_y = ui_origin_y, parent = self.__body)

        self.__skipbtn_audio = QPushButton('Skip', self)
        self.__skipbtn_audio.clicked.connect(self.__video_player.skip)
        self.__gr_skipbtn_audio = GraphicalObject(self.__skipbtn_audio, width = btn_width, height = btn_height, pos_x = ui_origin_x+(2*(100-2*ui_origin_x))/number_of_button, pos_y = ui_origin_y, parent = self.__body)

# Need to be put before drop area to link it 
        self.__playlist_time = QLabel("0", self)

        self.__drop_area = VideoDropLabel('Drop Here!', self, self.__playlist_time)

        drop_area_css = read_css("./css/drop_area.css")
        self.__drop_area.setStyleSheet(drop_area_css)
        self.__gr_drop_area = GraphicalObject(self.__drop_area, width = 80, height = 30, pos_x = 10, pos_y = 25, parent = self.__body)

# End of the playlist time label definition
        self.__playlist_time.setWordWrap(True)
        playlist_time_css = read_css("./css/drop_area.css")
        self.__playlist_time.setStyleSheet(playlist_time_css)
        self.__gr_playlist_time = GraphicalObject(self.__playlist_time, width = 60, height = 40, pos_x = 40, pos_y = 0, parent = self.__gr_drop_area)
        self.__playlist_time.raise_()


    def set_player_mode(self, value):
        if value == 'Video':
            self.__video_player.set_mode(value)
            self.__video_reader.show()
            self.__skipbtn_video.show()
            self.__previousbtn_video.show()
            self.__playbtn_video.show()
            self.__videotitle.show()
            

            self.__previousbtn_audio.hide()
            self.__playbtn_audio.hide()
            self.__skipbtn_audio.hide()

            self.__drop_area.hide()
            self.__playlist_time.hide()

        elif value == 'Audio':
            self.__video_player.set_mode(value)
            self.__video_reader.hide()
            self.__skipbtn_video.hide()
            self.__previousbtn_video.hide()
            self.__playbtn_video.hide()
            self.__videotitle.show()

            self.__previousbtn_audio.show()
            self.__playbtn_audio.show()
            self.__skipbtn_audio.show()

            self.__drop_area.hide()
            self.__playlist_time.hide()

        elif value == 'Download':
            self.__video_reader.hide()
            self.__video_reader.hide()
            self.__skipbtn_video.hide()
            self.__previousbtn_video.hide()
            self.__playbtn_video.hide()
            self.__videotitle.hide()

            self.__previousbtn_audio.hide()
            self.__playbtn_audio.hide()
            self.__skipbtn_audio.hide()

            self.__playlist_time.show()
            self.__drop_area.show()


    def end_of_play_list(self):
        print("End of stream")
        self.__palette.setColor (QPalette.Window,
                               QColor(0,0,0))
        self.__video_reader.setPalette(self.__palette)

    def update_title(self, title):
        self.__videotitle.setText(title)

    def audio_play_pause(self):
        if self.__video_player.is_running():
            self.pause_start()
        else:
            self.__playbtn_audio.setText('Pause')
            self.__video_player.play_stream()

    def video_play_pause(self):
        print("Play pause")
        if self.__video_player.is_running():
            self.pause_start()
        else :
            print("Launching the stream")
            if sys.platform.startswith('linux'): # for Linux using the X Server
                self.__video_player.get_player().set_xwindow(self.__video_reader.winId())
            elif sys.platform == "win32": # for Windows
                self.__video_player.get_player().set_hwnd(self.__video_reader.winId())
            elif sys.platform == "darwin": # for MacOS
                self.__video_player.get_player().set_nsobject(int(self.__video_reader.winId()))
#TODO LAPALETTE
            self.__video_player.play_stream()
            if self.__video_player.is_playing():
                self.__palette.setColor (QPalette.Window,
                           QColor(255,255,255))
                self.__video_reader.setPalette(self.__palette)
                self.__video_reader.setAutoFillBackground(True)



    def pause_start(self):
        if self.__video_player.is_paused(): 
            print("Unpausing the player")
            self.__playbtn_audio.setText('Pause')
            self.__video_player.resume_stream()
        elif self.__video_player.is_playing(): 
            print("Pausing the player")
            self.__playbtn_audio.setText('Play')
            self.__video_player.pause_stream()
        else: 
            print("Restarting the stream")
            self.__playbtn_audio.setText('Pause')
            self.__video_player.play_stream()

# Redefinition of the QMainWindow built-in methods

    def mousePressEvent(self, event):
        # Left click 
        if event.button() == 1:
            if ((event.x() <= (self.__gr_video_reader.getRealWidth()+self.__gr_video_reader.getRealPosX())) and 
                (event.x() >= self.__gr_video_reader.getRealPosX()) and 
                (event.y() <= (self.__gr_video_reader.getRealHeight()+self.__gr_video_reader.getRealPosY())) and 
                (event.y() >= self.__gr_video_reader.getRealPosY()) and 
                self.__video_player.get_mode()=='Video'):
                
                print("True")
                if self.__video_player.is_running():
                    self.pause_start()
                else :
                    print("Launching the stream")
                    if sys.platform.startswith('linux'): # for Linux using the X Server
                        self.__video_player.get_player().set_xwindow(self.__video_reader.winId())
                    elif sys.platform == "win32": # for Windows
                        self.__video_player.get_player().set_hwnd(self.__video_reader.winId())
                    elif sys.platform == "darwin": # for MacOS
                        self.__video_player.get_player().set_nsobject(int(self.__video_reader.winId()))
#TODO LAPALETTE
                    self.__video_player.play_stream()
                    if self.__video_player.is_playing():
                        self.__palette.setColor (QPalette.Window,
                                   QColor(255,255,255))
                        self.__video_reader.setPalette(self.__palette)
                        self.__video_reader.setAutoFillBackground(True)


        print("Plop X "+str(event.x())+" Plop Y "+str(event.y()))
        print("Glob X "+str(event.globalX())+" Glob Y "+str(event.globalY()))
        
    def resizeEvent (self, event):
        print("OLD height: " + str(event.oldSize().height())+ " width: " + str(event.oldSize().width()))
        print("NEW height: " + str(event.size().height())+ " width: " + str(event.oldSize().width()))
        self.__width = event.size().width()
        self.__height = event.size().height()
        self.__mainbox.resize(event.size().width(), event.size().height())


class CommandLineInterface(Interface):
    """ 
        This class provide a command line interface for the music player
    """
    def __init__(self, video_player, debug=False): 
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
                print("    vol <volume>")
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
