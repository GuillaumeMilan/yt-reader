import pafy 
import urllib
import wget
import os
import os.path
import sys
import string
from progress_bar import DownloadProgress
from quality_lib import get_audio_url, get_audio_extension, get_video_url, get_video_extension
from thread_lib import Threader 

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

def parse_param(param, cur_mode = 'Video', cur_qual = 'Best'):
    return {
            'Video' :    ( 'Video', cur_qual),
            'Audio' :    ( 'Audio', cur_qual),
            'Worst' :    (cur_mode, 'Worst'),
            'Best'  :    (cur_mode, 'Best'),
            'Medium':    (cur_mode, 'Medium'),
            ''      :    (cur_mode, cur_qual),
            }.get(param, (cur_mode, param))

def print_video_info(video):
    print("Video streams:")
    stream_list = [i.quality+" "+i.extension for i in video.streams]
    print(stream_list)
    print("Audio streams:")
    stream_list = [i.quality+" "+i.extension for i in video.audiostreams]
    print(stream_list)

def download_video(url, mode, qual, unwanted_type):
    """ 
################################################################################
#DESCRIPTION:
#    @param url: url of the video "youtube.com/..."
#    @param mode: Video or Audio
#    @param qual: Quality of the video 
#    @param unwanted_type: list of all type that we shouldn't download
################################################################################
    """

    video = pafy.new(url)
    passed = False
    while not passed:
        if mode == 'Video':
            file_link = get_video_url(video.streams, qual, unwanted_type)
            file_extension = get_video_extension(video.streams, local_qual, unwanted_type)
        elif local_mode == 'Audio':
            file_link = get_audio_url(video.audiostreams, qual, unwanted_type)
            file_extension = get_audio_extension(video.audiostreams, qual, unwanted_type)
        passed = file_link != "" and file_extension != ""
        failed = False
        if not passed : 
            print("We didn't found a video corresponding to your requirement!")
            print("Do you want to skip?(y/n)")
            command = input()
            if command == "y" :
                passed = True
                failed = True
            else :
                print("Current parameters: "+local_mode+", "+local_qual)
                print_video_info(video)
                print("Set your new parameter: ")
                command = input()
                command = command.split(" ")
                print(command)
                for i in command:
                    (local_mode, local_qual) = parse_param(i, local_mode, local_qual)

    print("----------")
    print("Downloading "+video.title)
    if not failed:
        try:
            target_file = video.title+"."+file_extension
            target_file = ''.join(c for c in target_file if c in valids_chars_in_file)
            output = wget.download(file_link, out=destination_folder+target_file, bar=None)
            print("----------")
        except (IOError):
            print("Unable to open the file: "+target_file)
    else :
        print("Aborted!")
        print(video.watchv_url)
        print("----------")


def dowload_list(video_list, options):
    """ 
################################################################################
#DESCRIPTION:
#    @param video_list: list of the videos (+ qual + mode)
#    @param options: contain all the unwanted extension + default qual and mode
#    This function objective is to download all the videos in the video_list 
#    This function will replace all the other dowload function in the next 
#    version of the software
################################################################################
    """
    default_mode = 'Video'
    default_qual = 'Best'
    unwanted_type = []
    if 'Audio' in options:
        default_mode = 'Audio'
    if "--nowebm" in options:
        unwanted_type.append("webm")
    if "--no3gp" in options:
        unwanted_type.append("3gp")
    if "--nom4a" in options:
        unwanted_type.append("m4a")
    if "--nomp4" in options:
        unwanted_type.append("mp4")

    for video in video_list: 
        local_mode = default_mode
        local_qual = default_qual
        for i in video[1:]:
            if i == 'Audio':
                local_mode = 'Audio'
            elif i == 'Video':
                local_mode = 'Video'
            else:
                local_qual = i
        download_video(video[0], local_mode, local_qual, unwanted_type)

def download(fname,mode='Video'):
    try:
        with open(fname) as f:
            content = f.readlines()
        content = [x.strip("\n") for x in content]
        unwanted_type = []
        default_mode = mode
        default_qual = 'Best'
        destination_folder = "downloads/"

        #Parse options
        splited_line = content[0].split(" ")
        if splited_line[0] == "options:":
            content = content[1:]
            for i in splited_line[1:] :
                if i == "--nowebm":
                    unwanted_type.append("webm")
                elif i == "--no3gp":
                    unwanted_type.append("3gp")
                elif i == "--nom4a":
                    unwanted_type.append("m4a")
                elif i == "--nomp4":
                    unwanted_type.append("mp4")
                elif i[:10] == "--quality[" and i[-1]==']':
                    default_qual = i[10:-1]
                elif i[:7] == "--mode[" and i[-1]==']':
                    default_mode = i[7:-1]
                elif i[:14] == "--destination[" and i[-1]==']':
                    destination_folder = i[14:-1]
                    if not destination_folder[-1]=='/':
                        destination_folder+='/'

        for line in content: 
            #Variable definition
            local_mode = default_mode
            local_qual = default_qual
            file_link = ""
            file_extension=""
            
            splited_line = line.split(" ")
            url = splited_line[0]
            if ("www.youtube.com/watch?v=" in url):
                #get the url and parameters
                for param in splited_line[1:]:
                    (local_mode, local_qual) = parse_param(param, local_mode, local_qual)

                video = pafy.new(url)
                passed = False
                while not passed:
                    if local_mode == 'Video':
                        file_link = get_video_url(video.streams, local_qual, unwanted_type)
                        file_extension = get_video_extension(video.streams, local_qual, unwanted_type)
                    elif local_mode == 'Audio':
                        file_link = get_audio_url(video.audiostreams, local_qual, unwanted_type)
                        file_extension = get_audio_extension(video.audiostreams, local_qual, unwanted_type)
                    passed = file_link != "" and file_extension != ""
                    failed = False
                    if not passed : 
                        print("We didn't found a video corresponding to your requirement!")
                        print("Do you want to skip?(y/n)")
                        command = input()
                        if command == "y" :
                            passed = True
                            failed = True
                        else :
                            print("Current parameters: "+local_mode+", "+local_qual)
                            print_video_info(video)
                            print("Set your new parameter: ")
                            command = input()
                            command = command.split(" ")
                            print(command)
                            for i in command:
                                (local_mode, local_qual) = parse_param(i, local_mode, local_qual)

                print("----------")
                print("Downloading "+video.title)
                if not failed:
                    try:
                        target_file = video.title+"."+file_extension
                        target_file = ''.join(c for c in target_file if c in valids_chars_in_file)
                        output = wget.download(file_link, out=destination_folder+target_file, bar=None)
                        #progress_bar = DownloadProgress("downloads/"+target_file, stream.url)
                        #progress_bar.start()
                        #urllib.request.urlretrieve(stream.url,"downloads/"+target_file)
                        #progress_bar.join()
                        print("----------")
                        #del progress_bar
                    except (IOError):
                        print("Unable to open the file: "+target_file)
                else :
                    print("Aborted!")
                    print(video.watchv_url)
                    print("----------")
    except (IOError):
        print("No such file: "+fname)
        return 

