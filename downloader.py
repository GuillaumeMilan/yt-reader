import pafy 
import urllib
import os
import os.path
import sys
from pydub import AudioSegment
import string
from progress_bar import DownloadProgress

valids_chars_in_file = "-_.() %s%s" % (string.ascii_letters, string.digits)

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
            print "----------"
            print "Downloading "+video.title
            try:
                target_file = video.title+"."+stream.extension
                target_file = ''.join(c for c in target_file if c in valids_chars_in_file)
                progress_bar = DownloadProgress("downloads/"+target_file, stream.url)
                progress_bar.start()
                urllib.urlretrieve(stream.url,"downloads/"+target_file)
                progress_bar.join()
                print "----------"
                del progress_bar
                if mode == 'Audio':
                    convert(target_file)
            except (IOError):
                print "Unable to open the file: "+target_file
    except (IOError):
        print "No such file: "+fname
        return 

def convert(filename):
    path = os.getcwd()
    path = os.path.join(path,"downloads")
    OUTPUT_DIR = path
    print os.path.join(OUTPUT_DIR, '%s.mp3' % filename[:-4])
    m4a_audio = AudioSegment.from_file(os.path.join(path, filename), "m4a")
    m4a_audio.export(os.path.join(OUTPUT_DIR, '%s.mp3' % filename[:-4]), "mp3")

def convert_all():
    path = os.getcwd()
    path = os.path.join(path, "downloads")
    OUTPUT_DIR = path
    filenames = [
        filename
        for filename
        in os.listdir(path)
        if filename.endswith('.m4a')
        ]
    print filenames
    for filename in filenames:
        print os.path.join(OUTPUT_DIR, '%s.mp3' % filename[:-4])
        m4a_audio = AudioSegment.from_file(os.path.join(path, filename), "m4a")
        m4a_audio.export(os.path.join(OUTPUT_DIR, '%s.mp3' % filename[:-4]), "mp3")
