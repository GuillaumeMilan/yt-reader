import pafy 
import urllib
import os
import os.path
import sys
import subprocess

def download(fname,mode='Video'):
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
        print "----------"
        urllib.urlretrieve(stream.url,"downloads/"+video.title+"."+stream.extension)

def convert():
    OUTPUT_DIR = 'downloads/'
    path = os.getcwd()
    filenames = [
        filename
        for filename
        in os.listdir(path)
        if filename.endswith('.m4a')
        ]

    for filename in filenames:
        subprocess.call([
            "ffmpeg", "-i",
            os.path.join(path, filename),
            "-acodec", "libmp3lame", "-ab", "256k",
            os.path.join(OUTPUT_DIR, '%s.mp3' % filename[:-4])
            ])
