import vlc
import time
import pafy
from threading import Thread

class VideoPlayer(Thread): 
    """ This class will create a thread in which the sound and the video will
        be played
    """
    def __init__(self,video = None, quality = '', output = '', paused = False): 
        Thread.__init__(self)
#define the url of the current video
        self.__url = ""
#define the pafy video stream the player will use 
        self.__video = video
#define if the player status is paused 
        self.__paused = paused
#define the time remaining to play (to set the date correctly after pause)
        self.__remaining_time = 0.0
#define the date at which the stream will end for this video
        self.__end_date = 0.0
#define if the player has currently a video in memory
        self.__is_reading = False
#define if the player is asked to stop the current stream
        self.__exited_stream = False
#define the instance of vlc
        self.__instance = vlc.Instance()
#define the player of the class 
        self.__player = self.__instance.media_player_new()
#define the pafy getted stream
        self.__video = video
#define the quality of the stream to get 
        self.__quality = quality
#define if the stream shoud be played as video or audio
        self.__output = output
#define the livness constant of the thread 
        self.__is_alive = True
#define kill the player when the next video end
        self.__kill_at_end = False
        
    def set_quality(self,quality): 
        self.__quality = quality
    
    def set_mode(self,output):
        self.__output = output

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

    def pause_stream(self):
        self.__remaining_time = self.__end_date - time.time()
        self.__paused = True
        self.__player.pause()

    def resume_stream(self): 
        self.__end_date = time.time() + self.__remaining_time
        self.__paused = False
        self.__player.play()
        
    def is_playing(self): 
        return self.__is_reading

    def stop_stream(self): 
        self.__exited_stream = True
    
    def play_stream(self): 
        self.__parse_video()
        self.__start_stream()

    def __parse_video(self): 
        url = ""
        if self.__video == None :
            print "Cannot read a none video. Use video_player.define_url(url)!"
            return 
        if self.__output == 'Audio': 
            if self.__quality=='Best':
                #Play audio 
                stream = self.__video.audiostreams
                stream = [s for s in stream if "webm" not in s.extension]
                highest_quality=max(stream, key=lambda c: int(c.bitrate[:-1]))
                url = highest_quality.url
            else :
                print "Not Yet implemented!"
                return 
        elif self.__output == 'Video':
            if self.__quality == 'Best' : 
                stream = self.__video.getbest()
                url = stream.url
                #Need to be ajusted to make the user able to pause the music
        else:
            print "Not implemented yet!"
            return  
        self.__player.set_mrl(url)

    def __start_stream(self):
        self.__is_reading = True
        self.__player.play()
        self.__end_date = time.time() + self.__video.length
    
    def run(self):
        while self.__is_alive:
            if self.__is_reading: 
                if self.__end_date < time.time() and not self.__paused: 
                    self.__is_reading = False
                    if self.__kill_at_end: 
                        #self.__instance
                        return
            time.sleep(0.5)

