from read_video import VideoPlayer
from interface import CommandLineInterface
content = []
try:
    with open(".config") as config:
        content = config.readlines()
except (IOError):
    print("No config file found")
    content.append('Best\n')
    content.append('Audio\n')
my_player = VideoPlayer(debug=False)
my_interface = CommandLineInterface(my_player)
my_player.start()
my_player.set_quality(content[0][:-1])
my_player.set_mode(content[1][:-1])
my_player.set_interface(my_interface)
my_interface.main()
my_player.join()
