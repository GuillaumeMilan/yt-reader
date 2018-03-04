#!/usr/bin/python3
from read_video import VideoPlayer
from interface import CommandLineInterface
from interface import GraphicalInterface
import sys
import settings

settings.init()

content = []
try:
    with open(".config") as config:
        content = config.readlines()
except (IOError):
    print("No config file found")
    content.append('Best\n')
    content.append('Audio\n')
interface_class = CommandLineInterface
for i in sys.argv[1:]:
    if i == "-X":
        interface_class = GraphicalInterface

my_player = VideoPlayer(debug=False)
#my_interface = CommandLineInterface(my_player)
my_interface = interface_class(my_player,debug = False)
my_player.start()
my_player.set_quality(content[0][:-1])
my_player.set_mode(content[1][:-1])
my_player.set_interface(my_interface)
my_interface.main()
my_player.join()
# Quit all the function currently threaded 
for i in settings.thread_list:
    i.quit()
