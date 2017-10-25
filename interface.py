
class CommandLineInterface:
    """ 
	This class provide a command line interface for the music player
    """
    def __init__(self, video_player): 
#define the player to use for this interface 
	self.__video_player = video_player
#define the list of url to display for the next videos
	self.__urls = []
#define if the user ask to quit the command line 
	self.__continue = True
    
    def main(self): 
	while self.__continue : 
	    command = raw_input()
	    commands = command.split(" ")
	    if commands[0] == "url":
		for i in commands [1:]: 
		    urls.append(i)
	    elif commands[0] == "skip" :
		slef.__video_player.define_url(urls[0])
		del urls[0]
	    elif commands[0] == "stop":
	        self.__continue = False
		self.__video_player.stop_stream()
		print "Stopping the player"
	    elif commands[0] == "help": 
		print "The commands available are: "
		print "    url [list of urls]"
		print "    stop"
		print "    play"
		print "    skip"
		print "    quality <quality> (only Best available)"
		print "    mode <Video,Audio>"
	    elif commands[0] == "play": 
		if self.__video_player.is_paused(): 
		    print "Unpausing the player"
		    self.__video_player.resume_stream()

		elif self.__video_player.is_playing(): 
		    print "The player is already playing. Verify your sound level."
		else 
	    else 
		print "Command not found!"

