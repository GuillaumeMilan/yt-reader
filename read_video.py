import vlc
import time
import pafy
from threading import Thread

class VideoPlayer(Thread): 
    """ This class will create a thread in which the sound and the video will
        be played
    """
    def __init__(self, video = None, quality = '', output = '', debug = False): 
        Thread.__init__(self)
#define the url of the current video
        self.__url = ""
#define the pafy video stream the player will use 
        self.__video = video
#define the instance of vlc
        self.__instance = vlc.Instance()
#define the player of the class 
        self.__player = self.__instance.media_player_new()
#define the quality of the stream to get 
        self.__quality = quality
#define if the stream shoud be played as video or audio
        self.__output = output
#define the livness constant of the thread 
        self.__is_alive = True
#define kill the player when the next video end
        self.__kill_at_end = False
#define if the player is used with an interface 
        self.__interface = None
#define if the player is runnning in debug mode 
        self.__debug = debug
#define the list of next content to watch 
        self.__following = []
#define the history off all content watched 
        self.__history = []
#define the video currently playing
        self.__current  = None

    def get_player(self):
        return self.__player

    def add_url(self, url):
        if "list=" in url:
            #this is an url of a playlist 
            playlist = pafy.get_playlist(url)
            for i in playlist['items']:
                self.__following.append(i['pafy'])
        elif "www.youtube.com/watch?v=" in url :
            video = pafy.new(url)
            self.__following.append(video)
        else :
            print("Error: url not recoginzed")
    
    def set_quality(self,quality): 
        self.__quality = quality

    def set_volume(self,value):
        if value < 0 or value > 200 :
            print("Cannot set the volume to: "+str(value))
            return 
        self.__player.audio_set_volume(value)

    def __two_digit(self,value):
        if value<10 and value>0:
            return "0"+str(value)
        else:
            return str(value)

    def __hour(self,in_second):
        if in_second/3600 != 0:
            return str(in_second/3600)+":"+self.__two_digit((in_second % 3600)/60)+":"+self.__two_digit(in_second % 60)
        else:
            return str((in_second % 3600)/60)+":"+self.__two_digit(in_second % 60)
    
    def get_time(self): 
        if self.__video == None:
            print("No video playing at the moment")
            return 
        current_time = self.__player.get_time()/1000
        print(self.__hour(current_time)+"/"+self.__hour(self.__video.length))

    def set_mode(self,output):
        self.__output = output
    
    def get_mode(self):
        return self.__output

    def kill_player(self):
        self.__is_alive = False
    
    def kill_at_end(self):
        self.__kill_at_end = True

    def define_url(self, url): 
        """ 
            called to define the youtube url to use to play the next video
        """
        self.__url = url
        self.__video = pafy.new(self.__url)
        self.__parse_video()
        self.__start_stream()

    def is_paused(self): 
        return self.__player.get_state()== vlc.State.Paused

    def is_running(self):
        return not (self.__player.get_state() == vlc.State.NothingSpecial or self.__player.get_state() == vlc.State.Stopped)

    def pause_stream(self):
        self.__player.pause()

    def resume_stream(self): 
        self.__player.play()
    def set_time(self, time):
        self.__player.set_time(time)

    def stop_stream(self): 
        self.__is_alive = False
        self.__player.stop()
    
    def play_stream(self): 
        self.__parse_video()
        self.__start_stream()

    def set_interface(self,interface):
        """ 
            interface must only have a method called set_next_music(self)
        """
        self.__interface = interface
    
    def __to_string(self,value, max_val):
        nb_blank = len(str(max_val))-len(str(value))
        return str(value)+" "*nb_blank

    def to_play(self):
        print("----------")
        for i in range(0,len(self.__following)):
            print(self.__to_string(i,len(self.__following))+" -- "+self.__following[i].title)
        print("----------")

    def history(self):
        print("----------")
        for i in range(0,len(self.__history)):
            print(self.__to_string(i,len(self.__history))+" -- "+self.__history[i].title)
        print("----------")
    
    def is_playing(self):
        if self.__video is not None:
            print("----------")
            print(self.__video.title)
            print("----------")

    def get_current(self):
        return self.__video
    
    def get_playlist(self):
        return self.__following

    def skip(self):
        self.__history.append(self.__video)
        self.__video = None
        self.play_stream()

    def __parse_video(self): 
        url = ""
        if self.__video == None :
            if len(self.__following) == 0:
                print("No video to play!")
                return
            self.__video = self.__following.pop(0)
        if self.__output == 'Audio': 
            if self.__quality=='Best':
                #Play audio 
                stream = self.__video.audiostreams
                stream = [s for s in stream if "webm" not in s.extension]
                highest_quality=max(stream, key=lambda c: int(c.bitrate[:-1]))
                url = highest_quality.url
            else :
                print("Not Yet implemented!")
                return 
        elif self.__output == 'Video':
            if self.__quality == 'Best' : 
                stream = self.__video.getbest()
                url = stream.url
                #Need to be ajusted to make the user able to pause the music
            else:
                print("Not implemented yet!")
                return  
        self.__player.set_mrl(url)

    def __start_stream(self):
        self.__player.play()
    
    def run(self):
        while self.__is_alive:
            if self.__debug: 
                print("----------")
                print("STATE : ")
                print(self.__player.get_state())
                print("----------")
            if self.__player.get_state() == vlc.State.Ended:
                if not self.__kill_at_end and self.__interface != None: 
                    if len(self.__following)==0:
                        self.__player.stop()    
                        self.__history.append(self.__video)
                        self.__video = None
                        if self.__debug: 
                            print("----------")
                            print("STATE : ")
                            print(self.__player.get_state())
                            print("----------")
                    else: 
                        self.__history.append(self.__video)
                        self.__video = None
                        self.__parse_video()
                        self.__start_stream()
                else :
                    self.__is_alive = False
            else:
                time.sleep(0.5)

