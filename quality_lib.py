
def get_audio_url(streams, quality, unwanted_extension = ["webm"]):
    """ 
################################################################################
# DESCRIPTION: 
#    @param streams: list of stream of the audio
#    @param quality: wanted quality 
#    @param unwanted_extension: file extension not wanted as return 
# This function return the audio stream that correspond to the requested quality
# This function return a empty string if no stream correspond
################################################################################
    """
    stream = streams
    for i in unwanted_extension:
        stream = [s for s in stream if i not in s.extension]
    if len(stream) == 0:
        print("Extension restriction is too strong\n")
        return ""
    if quality == 'Best':
        highest_quality=max(stream, key=lambda c: int(c.bitrate[:-1]))  
        return highest_quality.url
    elif quality == 'Worst':
        lowest_quality=min(stream, key=lambda c: int(c.bitrate[:-1]))
        return lowest_quality.url
    elif quality == 'Medium':
        # I assum here that the stream quality are sorted (exeprimental)
        medium_quality=stream[int(len(stream)/2)]
        return medium_quality.url
    else :
        #TODO improve to find the closest quality
        for i in stream:
            if quality==i.bitrate:
                return i.url
        print ("No such quality in this stream\n")
        return ""

def get_video_url(streams, quality, unwanted_extension = ["webm","3gp"]):
    """ 
################################################################################
# DESCRIPTION: 
#    @param streams: list of stream of the video
#    @param quality: wanted quality 
#    @param unwanted_extension: file extension not wanted as return 
# This function return the video stream that correspond to the requested quality
# This function return a empty string if no stream correspond
################################################################################
    """
    stream = streams
    for i in unwanted_extension:
        stream = [s for s in stream if i not in s.extension]
    if len(stream) == 0:
        print("Extension restriction is too strong\n")
        return ""
    # I assum here that the stream quality are sorted (exeprimental)
    if quality == 'Best':
         highest_quality=stream[-1]
         return highest_quality.url
    elif quality == 'Worst':
        lowest_quality=stream[0]
        return lowest_quality.url
    elif quality == 'Medium':
        medium_quality=stream[int(len(stream)/2)]
        return medium_quality.url
    else :
        #TODO improve to find the closest quality
        for i in stream:
            if quality==i.resolution:
                return i.url
        print ("No such quality in this stream\n")
        return ""

def get_audio_extension(streams, quality, unwanted_extension = ["webm"]):
    """ 
################################################################################
# DESCRIPTION: 
#    @param streams: list of stream of the audio
#    @param quality: wanted quality 
#    @param unwanted_extension: file extension not wanted as return 
# This function return the extension of the returned stream by get_audio_url
# This function return a empty string if no stream correspond
################################################################################
    """
    stream = streams
    for i in unwanted_extension:
        stream = [s for s in stream if i not in s.extension]
    if len(stream) == 0:
        print("Extension restriction is too strong\n")
        return ""
    if quality == 'Best':
        highest_quality=max(stream, key=lambda c: int(c.bitrate[:-1]))  
        return highest_quality.extension
    elif quality == 'Worst':
        lowest_quality=min(stream, key=lambda c: int(c.bitrate[:-1]))
        return lowest_quality.extension
    elif quality == 'Medium':
        # I assum here that the stream quality are sorted (exeprimental)
        medium_quality=stream[int(len(stream)/2)]
        return medium_quality.extension
    else :
        #TODO improve to find the closest quality
        for i in stream:
            if quality==i.bitrate:
                return i.extension
        print ("No such quality in this stream\n")
        return ""

def get_video_extension(streams, quality, unwanted_extension = ["webm","3gp"]):
    """ 
################################################################################
# DESCRIPTION: 
#    @param streams: list of stream of the video
#    @param quality: wanted quality 
#    @param unwanted_extension: file extension not wanted as return 
# This function return the extension of the returned stream by get_video_url
# This function return a empty string if no stream correspond
################################################################################
    """
    stream = streams
    for i in unwanted_extension:
        stream = [s for s in stream if i not in s.extension]
    if len(stream) == 0:
        print("Extension restriction is too strong\n")
        return ""
    # I assum here that the stream quality are sorted (exeprimental)
    if quality == 'Best':
         highest_quality=stream[-1]
         return highest_quality.extension
    elif quality == 'Worst':
        lowest_quality=stream[0]
        return lowest_quality.extension
    elif quality == 'Medium':
        medium_quality=stream[len(stream)/2]
        return medium_quality.extension
    else :
        #TODO improve to find the closest quality
        for i in stream:
            if quality==i.resolution:
                return i.extension
        print ("No such quality in this stream\n")
        return ""

 
