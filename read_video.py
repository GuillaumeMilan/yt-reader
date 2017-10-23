import vlc

import time

def read_video(video, quality, output): 
    """
        DESCRIPTION: 
        This function start displaying the video. 
        video = pafy.new(url)
        quality can be Best Lowest Medium 
        output can be Audio(sounds the audio of the video) or Video 
        REQUIRE : 
        This function need to be call in a seprated thread. 
        This thread need to be killed when we want to change the music.     
    """
    if quality == 'Best' : 
        stream = video.getbest()
        print(stream.url)
        #instance = vlc.Instance()
        #player = instance.media_player_new()
        #player.set_mrl(stream.url)
        #player.play()

        #Need to be ajusted to make the user able to pause the music

        time.sleep(video.length)
    else :
        print ("Not implemented yet!")
