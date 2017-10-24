import vlc
import time

paused = False
remaining_time = 0.0
end_date = 0.0

def pause_stream():
    global paused, remaining_time, end_date
    remaining_time = end_date - time.time()
    paused = True

def resume_stream(): 
    global paused, remaining_time, end_date
    end_date = time.time() + remaining_time
    paused = False
    
def read_video(video, quality, output): 
    """
        DESCRIPTION: 
        This function start displaying the video. 
        video = pafy.new(url)
        quality can be Best Lowest Medium 
        output can be 'Audio'(sounds the audio of the video) or 'Video'
        REQUIRE : 
        This function need to be call in a seprated thread. 
        This thread need to be killed when we want to change the music.     
    """
    global remaining_time,end_date
    url=""
    #if paused then don't check if the music is finished
    
    if output == 'Audio': 
        if quality=='Best':
            #Play audio 
            stream = video.audiostreams
            stream = [s for s in stream if "webm" not in s.extension]
            highest_quality=max(stream, key=lambda c: int(c.bitrate[:-1]))
            url = highest_quality.url
        else :
            print "Not Yet implemented Bruh!!!"
            return 
    elif output == 'Video':
        if quality == 'Best' : 
            stream = video.getbest()
            url = stream.url
            #Need to be ajusted to make the user able to pause the music
    else:
        print "Not implemented yet!"
        return 

    instance = vlc.Instance()
    player = instance.media_player_new()
    player.set_mrl(url)
    player.play()
    #for debug 
    start_time = time.time()
    end_date = time.time() + video.length
    
    while end_date > time.time() or paused:
        time.sleep(0.5)
    print ("Date debut",start_time,"Date fin",end_date)
    print ("heure actuel",time.time())
