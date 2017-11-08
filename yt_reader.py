from read_video import VideoPlayer
from interface import CommandLineInterface

url ="https://www.youtube.com/watch?v=ls-LYas5j8U"
url ="https://www.youtube.com/watch?v=lvs68OKOquM" #talking to my self
url ="https://www.youtube.com/watch?v=QjxScn7cKo8" #10s video
url ="https://www.youtube.com/watch?v=KorwwAjKpaY"
my_player = VideoPlayer(debug=False)
my_interface = CommandLineInterface(my_player)
my_player.start()
my_player.set_quality('Best')
my_player.set_mode('Video')
my_player.set_interface(my_interface)
my_interface.main()
my_player.join()
