import sys,os
from downloader import download
from downloader import download_pafy
from combo_box import ComboMode
from drop_label import VideoDropLabel
from thumb_label import ThumbLabel
from translucid_button import TranslucidButton
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit
from PyQt5.QtWidgets import QPushButton, QLabel, QFrame
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor, QImage
from PyQt5.QtCore import Qt
from graphical_object import GraphicalObject
import pafy
import random 
import string

def read_css(fname):
    """
################################################################################
# DESCRIPTION:
#    @param fname: name of the file containing the css  
#    @return string containing the content of the file
# This function goal is to return the css content of a file to edit the style
# of your PyQt object
################################################################################
    """
    with open(fname) as f:
        content = f.read()
    return content

class Interface:
    """
################################################################################
# DESCRIPTION: 
#    @class reference to construct an interface for the yt_reader app
################################################################################
    """
    def end_of_play_list(self):
        """
################################################################################
# DESCRIPTION:
#    This method notify to the interface that the playlist just finished
#    This method is call by the VideoPlayer
################################################################################
        """
        pass 

    def update_title(self,title):
        """
################################################################################
# DESCRIPTION: 
#    This method notify to the interface the title of the new video playing
#    This method is to be used to update the interface video title
################################################################################
        """
        print("----------")
        print(title)
        print("----------")

class GraphicalInterface(QMainWindow,Interface):
    """
################################################################################
# DESCRIPTION: 
#    @class which will create a GUI for the VideoReader and the download
################################################################################
    """
    def __init__(self, video_player, debug = False):
        """
################################################################################
# DESCRIPTION: 
#    @class GraphicalInterface initialisation need:
#       @depends Interface
        @depends QMainWindow
#       @param VideoPlayer that will communicate with the interface
#       @param debug ... No explaination
################################################################################
        """
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
# List containing all the Widget of an interface
        self.__videowidgets = []
        self.__audiowidgets = []
        self.__downloadwidgets = []
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
        self.__start_download = None
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
        self.__gr_start_download = None

        self.__object_list = []

        self.__debug = debug
        
    def main(self):
        """
################################################################################
# DESCRIPTION: 
#       Main loop of the graphic interface
#       @use self.create_reader to create the body 
################################################################################
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
        """
################################################################################
# DESCRIPTION: 
#    This function is an intern function of the class to search for the video 
#    TODO: Change it to private 
################################################################################
        """
        my_string = self.__searchbar.text()
        self.__searchbar.clear()
        self.__add_to_player(my_string)

    def __add_to_player(self,url):
        if "www.youtube.com/" in url:
            self.__video_player.add_url(url)
        else:
            print("Search functionnality not implemented yet. Put url please!")
        
    def create_reader(self):
        """
################################################################################
# DESCRIPTION: 
#    This function create the body of the interface
#    TODO put it in private 
################################################################################
        """
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
        self.__videowidgets.append(self.__video_reader)
        self.__gr_video_reader = GraphicalObject(self.__video_reader, width = 80, height = 80, pos_x = 10, pos_y = 10, parent = self.__body)

        self.__videotitle = QLabel("No Video!", self)
        self.__videotitle.setWordWrap(True)
        self.__videowidgets.append(self.__videotitle)
        self.__audiowidgets.append(self.__videotitle)
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
        self.__videowidgets.append(self.__previousbtn_video)
        self.__gr_previousbtn_video = GraphicalObject(self.__previousbtn_video, width = btn_width, height = btn_height, pos_x = ui_origin_x+0*btn_width, pos_y = ui_origin_y, parent = self.__gr_video_reader)

        self.__skipbtn_video = TranslucidButton(self)
        self.__skipbtn_image = QPixmap('resources/skip.svg')
        self.__skipbtn_video.setScaledContents(True)
        self.__skipbtn_video.setPixmap(self.__skipbtn_image)
        self.__videowidgets.append(self.__skipbtn_video)
        self.__gr_skipbtn_video = GraphicalObject(self.__skipbtn_video, width = btn_width, height = btn_height, pos_x = ui_origin_x+2*btn_width, pos_y = ui_origin_y, parent = self.__gr_video_reader)

        self.__playbtn_video = TranslucidButton(self)
        self.__playbtn_video.clicked.connect(self.video_play_pause)
        self.__playbtn_image = QPixmap('resources/play.svg')
        self.__playbtn_video.setScaledContents(True)
        self.__playbtn_video.setPixmap(self.__playbtn_image)
        self.__videowidgets.append(self.__playbtn_video)
        self.__gr_playbtn_video = GraphicalObject(self.__playbtn_video, width = btn_width, height = btn_height, pos_x = ui_origin_x+1*btn_width, pos_y = ui_origin_y, parent = self.__gr_video_reader)

        # Audio UI 
        number_of_button = 3
        btn_height = 5
        btn_width = 10
        ui_origin_x = 30
        ui_origin_y = 50 - (btn_height/2)

        self.__previousbtn_audio = QPushButton('Previous', self)
        self.__audiowidgets.append(self.__previousbtn_audio)
        #clicked.connect(self.handle_research)
        self.__gr_previousbtn_audio = GraphicalObject(self.__previousbtn_audio, width = btn_width, height = btn_height, pos_x = ui_origin_x+(0*(100-2*ui_origin_x))/number_of_button, pos_y = ui_origin_y, parent = self.__body)

        self.__playbtn_audio = QPushButton('Play', self)
        self.__playbtn_audio.clicked.connect(self.audio_play_pause)
        self.__audiowidgets.append(self.__playbtn_audio)
        self.__gr_playbtn_audio = GraphicalObject(self.__playbtn_audio, width = btn_width, height = btn_height, pos_x = ui_origin_x+(1*(100-2*ui_origin_x))/number_of_button, pos_y = ui_origin_y, parent = self.__body)

        self.__skipbtn_audio = QPushButton('Skip', self)
        self.__skipbtn_audio.clicked.connect(self.__video_player.skip)
        self.__audiowidgets.append(self.__skipbtn_audio)
        self.__gr_skipbtn_audio = GraphicalObject(self.__skipbtn_audio, width = btn_width, height = btn_height, pos_x = ui_origin_x+(2*(100-2*ui_origin_x))/number_of_button, pos_y = ui_origin_y, parent = self.__body)

# Need to be put before drop area to link it 
        self.__playlist_time = QLabel("0", self)
        self.__downloadwidgets.append(self.__playlist_time)

        self.__drop_area = VideoDropLabel('Drop Here!', self, self.__playlist_time)

        drop_area_css = read_css("./css/drop_area.css")
        self.__drop_area.setStyleSheet(drop_area_css)
        self.__downloadwidgets.append(self.__drop_area)
        self.__gr_drop_area = GraphicalObject(self.__drop_area, width = 80, height = 30, pos_x = 10, pos_y = 25, parent = self.__body)

# End of the playlist time label definition
        self.__playlist_time.setWordWrap(True)
        playlist_time_css = read_css("./css/drop_area.css")
        self.__playlist_time.setStyleSheet(playlist_time_css)
        self.__gr_playlist_time = GraphicalObject(self.__playlist_time, width = 60, height = 40, pos_x = 40, pos_y = 0, parent = self.__gr_drop_area)
        self.__playlist_time.raise_()

        self.__start_download = QPushButton('Download', self)
        self.__start_download.clicked.connect(self.__drop_area.download)
        self.__downloadwidgets.append(self.__start_download)
        self.__gr_start_download = GraphicalObject(self.__start_download, width = 20, height = 10, pos_x = 55, pos_y = 90, parent = self.__body)
        
        self.__save_download = QPushButton('Save', self)
        self.__save_download.clicked.connect(self.__drop_area.save)
        self.__downloadwidgets.append(self.__save_download)
        self.__gr_save_download = GraphicalObject(self.__save_download, width = 20, height = 10, pos_x = 25, pos_y = 90, parent = self.__body)

# --TODO-- put all the thumb in a list
        url = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACoCAMAAABt9SM9AAAAP1BMVEX8/Pz9/f38/Pr8/P75+fn29vbv7+/y8vL9/f/y8vT8+v39//+LjZn6/f/u8Prr7va9v8vi4uLT09Pp6ene3uCVnvR7AAACrElEQVR4nO3djXLiIBSGYU5zEm3cn3bt/V/rBki0zu42h8gKkfeZTtOZaorfwBHQGucsZHjvxYmYbny5062k++6ZqE4PNvHxthpW6FSqpVuxF75rEZaJxEFVuhk7of6LsGwI6wajLEVIixpuRN9KQFZmsV8xDC3iNIpJug09Kwk1K48pRwnLQ6yTuJlFWEYSehdsmLMmmMLiudJq6lh96Tbsgx+BoofSzSjNVIjmcqXhKVFce69BzGyFKGajgwqFflUISw+/hiY71JVtTRjGX3/u285K42TTEMFSqRrejO910q9MCuZy7utb0z3Lr5D783k1rXDDeGw3r7DnNwyrRUun8apzz2p26hA09Lg7z//wEpRuTt0IK8GSlYtxFW1L9S5REda6T2H5uIq1Y38Iq6C6plOhLZrjpZN4psx7v9VNPmNz7t0qEkl+9/XuhJ4Qtm23ZjWXqbgQOXYrt05SWfZ+2KjqPSvUzzX9/4RVU2bXnY9NrZonV6FndpI7LNV6Brdfy1+qzbZWXWaiosMwPnNY8V89Dr0fiBv3IK9LwtePj9fsYeU83738Nm1/Puj2p8IlLAlhZekFFdYqdy3qOZrlN4gz9YRaw8p4qu1l749z3RyeUM7N3qcPK6eqw8rUqmzvN6s5rEyVK9+it+Kwcj3G6nYIAAAAAAAAUJWcLxE8PeHDblL4l5F70rKhZ6Vh39smvmGPsMxIyii+CY2aBQAAAAAAAAAAAAAAAAAAAAAAAAAPJ/PnZ5duxz5o+IDw0q3YDXFrl/nDTMO1EfhHSxtxmvsyLM9quSwkLEgKAAAAAAAAAAAAAAAAAAAAwEYi8qDLesnj/lS6cQwHGcdOtDv941aEFcSwXnxY7nT6sTT2r9yXv23AOC7Hozt9fyOsr/iwjlMO4/RNfn77DUdfCIhnVMkqAAAAAElFTkSuQmCC'
        self.__current_thumb = ThumbLabel(self)
        self.__current_thumb.setUrl(url)
        self.__drop_area.setThumbWidget(self.__current_thumb)

        self.__gr_current_thumb = GraphicalObject(self.__current_thumb, width = 30, height = 30, pos_x = 35, pos_y = 58, parent = self.__body)
        self.__downloadwidgets.append(self.__current_thumb)

    def set_player_mode(self, value):
        """
################################################################################
# DESCRIPTION: 
#    This function is used to change the mode of the VideoReader @class 
#    This funtion is private and called on interface changing mode
#    TODO privatize + use it when in download mode 
################################################################################
        """
        if value == 'Video':
            self.__video_player.set_mode(value)
            for i in self.__audiowidgets:
                i.hide()
            for i in self.__downloadwidgets:
                i.hide()
            for i in self.__videowidgets:
                i.show()
            
        elif value == 'Audio':
            self.__video_player.set_mode(value)
            for i in self.__downloadwidgets:
                i.hide()
            for i in self.__videowidgets:
                i.hide()
            for i in self.__audiowidgets:
                i.show()

        elif value == 'Download':
# This is a quick fix TODO rewrite mouse press event Plop Glob
            self.__video_player.set_mode('Audio')
            for i in self.__videowidgets:
                i.hide()
            for i in self.__audiowidgets:
                i.hide()
            for i in self.__downloadwidgets:
                i.show()

            
    def end_of_play_list(self):
        """
################################################################################
# DESCRIPTION: 
#    @Override This class handle the end playlist event raise by the 
#    VideoReader @class
################################################################################
"""
        print("End of stream")
        self.__palette.setColor (QPalette.Window,
                               QColor(0,0,0))
        self.__video_reader.setPalette(self.__palette)

    def update_title(self, title):
        """
################################################################################
# DESCRIPTION: 
#    @param title: change the video title of the interface with the param
#    TODO privatize 
################################################################################
        """
        self.__videotitle.setText(title)

    def audio_play_pause(self):
        """
################################################################################
# DESCRIPTION: 
#    This function objective is to swap pause and play for the VideoReader
#    TODO privatize + put in template
################################################################################
        """
        if self.__video_player.is_running():
            self.pause_start()
        else:
            self.__playbtn_audio.setText('Pause')
            self.__video_player.play_stream()

    def video_play_pause(self):
        """
################################################################################
# DESCRIPTION: 
#    This function is used to swap play pause of the VideoReader and modify the
#    interface in consequence
#    TODO privatize ?
################################################################################
        """
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
        """
################################################################################
# DESCRIPTION: 
#    Function to be called to update the VideoReader status 
#    TODO privatize?
################################################################################
        """
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
        """
################################################################################
# DESCRIPTION: 
#    @Override from QMainWindow 
#       Handle the click event and verify if it is on the player 
#    TODO Clarifiy the code and scalable
################################################################################
        """
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
        """
################################################################################
# DESCRIPTION: 
#    @Override from QMainWindow 
#    This method is called to scale all the content of the window
################################################################################
        """
        print("OLD height: " + str(event.oldSize().height())+ " width: " + str(event.oldSize().width()))
        print("NEW height: " + str(event.size().height())+ " width: " + str(event.oldSize().width()))
        self.__width = event.size().width()
        self.__height = event.size().height()
        self.__mainbox.resize(event.size().width(), event.size().height())


class CommandLineInterface(Interface):
    """
################################################################################
# DESCRIPTION: 
#    This @class provide a command line interface for the music player
################################################################################
    """
    def __init__(self, video_player, debug=False): 
        """
################################################################################
# DESCRIPTION: 
#    @class CommandLineInterface initialisation need:
#       @depends Interface
#       @param VideoPlayer that will communicate with the interface
#       @param debug ... No explaination
################################################################################
        """
#define the currently playing video url 
        self.__url = "" 
#define the player to use for this interface 
        self.__video_player = video_player
#define the list of url to display for the next videos
        self.__urls = []
#define if the user ask to quit the command line 
        self.__continue = True

    def set_next_music(self): 
        """
################################################################################
# DESCRIPTION: 
#    TODO verify the use 
################################################################################
        """
        self.__video_player.skip()

    def get_current_music(self): 
        """
################################################################################
# DESCRIPTION: 
#    print the url of the current playing music 
################################################################################
        """
        print(self.__url)

    def __crypt(self):
        """
################################################################################
# DESCRIPTION: 
#    Clear your terminal with random char (fun.exe)
################################################################################
        """
        rand_str = lambda n: ''.join([random.choice(string.ascii_letters+string.punctuation+string.digits) for i in range(n)])
        rows, columns = os.popen('stty size', 'r').read().split()
        print("")
# Now to generate a random string of length 10
        for i in range(0,int(rows)):
            s = rand_str(int(columns))  
            print(s)

    def main(self): 
        """
################################################################################
# DESCRIPTION: 
#    This is the main loop of the interface (can be called in a Thread)
#    This function provide the command ask loop of the interface to provide the
#    more terminal like behave
################################################################################
        """
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
