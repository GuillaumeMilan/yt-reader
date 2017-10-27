import sys

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
	print self.__urls
	if self.__urls != [] : 
	    self.__url = self.__urls[0]
	    self.__video_player.define_url(self.__urls[0])
	    del self.__urls[0]
	    return True
	else :
	    print "No new music to play! Add new music and start the player again!"
	    return False
    def get_current_music(self): 
	print self.__url

    def main(self): 
	sys.stdout.write(">>>")
	while self.__continue : 
	    command = raw_input()
	    commands = command.split(" ")
	    if commands[0] == "url":
		for i in commands [1:]: 
		    self.__urls.append(i)
	    elif commands[0] == "skip" :
		self.set_next_music()
	    elif commands[0] == "stop":
	        self.__continue = False
		self.__video_player.stop_stream()
		print "Stopping the player"
		return 
	    elif commands[0] == "set": 
		self.__video_player.set_time(int(float(commands[1])))
	    elif commands[0] == "help": 
		print "The commands available are: "
		print "    url [list of urls]"
		print "    stop"
		print "    play"
		print "    pause"
		print "    skip"
		print "    quality <quality> (only Best available)"
		print "    mode <Video,Audio>"
		print "    set <time in sec>"
	    elif commands[0] == "set":
		#need to parse time over a minute to the format hh:mm:ss
		self._video_player.set_time(int(float(commands[1]))*10)
	    elif commands[0] == "quality": 
		self._video_player.set_quality(commands[1])
	    elif commands[0] == "mode": 
		self._video_player.set_mode(commands[1])
	    elif commands[0] == "pause": 
		self.__video_player.pause_stream()
	    elif commands[0] == "play": 
		if self.__video_player.is_running():
		    if self.__video_player.is_paused(): 
			print "Unpausing the player"
			self.__video_player.resume_stream()

		    elif self.__video_player.is_playing(): 
			print "The player is already playing. Verify your sound level."
		    else: 
			self.__video_player.play_stream()
		else :
		    self.set_next_music()
		    self.__video_player.play_stream()

	    else :
		print "Command not found!"
	    sys.stdout.write(">>>")
