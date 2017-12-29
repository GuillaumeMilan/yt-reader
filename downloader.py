import pafy 
import urllib
import wget
import os
import os.path
import sys
import string
from progress_bar import DownloadProgress

valids_chars_in_file = "-_.() %s%s" % (string.ascii_letters, string.digits)

def download_pafy(video=None,mode='Video'):
    stream = None
    if mode == 'Video':
        stream = video.getbest()
    elif mode == 'Audio':
        stream = video.audiostreams
        stream = [s for s in stream if "webm" not in s.extension]
        stream=max(stream, key=lambda c: int(c.bitrate[:-1]))
    print("----------")
    print("Downloading "+video.title)
    try:
        target_file = video.title+"."+stream.extension
        target_file = ''.join(c for c in target_file if c in valids_chars_in_file)
        output = wget.download(stream.url, out="downloads/"+target_file, bar=None)
        #progress_bar = DownloadProgress("downloads/"+target_file, stream.url)
        #progress_bar.start()
        #print(stream.url)
        #urllib.request.urlretrieve(stream.url,"downloads/"+target_file)
        #progress_bar.join()
        print("----------")
        del progress_bar
    except (IOError):
        print("Unable to open the file: "+target_file)

def download(fname,mode='Video'):
    try:
        with open(fname) as f:
            content = f.readlines()
        content = [x.strip("\n") for x in content]
        for url in content: 
            video = pafy.new(url)
            if mode == 'Video':
                stream = video.getbest()
            elif mode == 'Audio':
                stream = video.audiostreams
                stream = [s for s in stream if "webm" not in s.extension]
                stream=max(stream, key=lambda c: int(c.bitrate[:-1]))
            print("----------")
            print("Downloading "+video.title)
            try:
                print(stream)
                target_file = video.title+"."+stream.extension
                target_file = ''.join(c for c in target_file if c in valids_chars_in_file)
                output = wget.download(stream.url, out="downloads/"+target_file, bar=None)
                #progress_bar = DownloadProgress("downloads/"+target_file, stream.url)
                #progress_bar.start()
                #urllib.request.urlretrieve(stream.url,"downloads/"+target_file)
                #progress_bar.join()
                print("----------")
                #del progress_bar
            except (IOError):
                print("Unable to open the file: "+target_file)
    except (IOError):
        print("No such file: "+fname)
        return 

