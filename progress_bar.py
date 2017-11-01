from __future__ import print_function
from threading  import Thread 
import urllib 
import os
import time

class DownloadProgress(Thread):
    """
        This class create a thread that mesure the download progress with a 
        download bar
        @params:
            filename   - Required : (Str) is the name of the file in download 
            url        - Required : (Str) url from which the file is downloaded
    """
    def __init__(self, filename, url):
        Thread.__init__(self)
        self.__url = url
        self.__filename = filename

    def run(self):
        while not os.path.exists(self.__filename):
            time.sleep(0.5)
            print("existe toujours pas")
        online_file = d = urllib.urlopen(self.__url)
        information = online_file.info()
        total_size = int(information.getheaders("Content-Length")[0])
        percent = 0
        while percent < 100:
            current_size = int(os.path.getsize(self.__filename))
            percent = (current_size * 100)/total_size
            printProgressBar(percent, prefix = 'Progress:', suffix = 'Complete', length = 50)

        printProgressBar(100, prefix = 'Progress:', suffix = 'Complete', length = 50)
        print()
# Print iterations progress

def printProgressBar (percent, prefix = '', suffix = '', decimals = 1, length = 100, fill = '='):
    """
    Call in a loop to create terminal progress bar
    @params:
        percent     - Required  : (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    filledLength = int(length * percent // 100)
    bar = fill * filledLength + ' ' * (length - filledLength)
    percent_str = str(percent)+"%"
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
#    # Print New Line on Complete
#    if percent == 100: 
#        print()
#
# 
# Sample Usage
# 

##from time import sleep
#
## A List of Items
#items = list(range(0, 57))
#l = len(items)
#
## Initial call to print 0% progress
#printProgressBar(0, prefix = 'Progress:', suffix = 'Complete', length = 50)
#for i in range(1,101):
#    printProgressBar(i, prefix = 'Progress:', suffix = 'Complete', length = 50)
#    sleep(0.1)
#