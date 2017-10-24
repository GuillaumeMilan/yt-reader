import time
from read_video import VideoPlayer

url ="https://www.youtube.com/watch?v=ls-LYas5j8U"
url ="https://www.youtube.com/watch?v=lvs68OKOquM" #talking to my self
url ="https://www.youtube.com/watch?v=QjxScn7cKo8" #10s video

my_player = VideoPlayer()
my_player.start()
my_player.kill_at_end()
my_player.set_quality('Best')
my_player.set_mode('Video')
my_player.define_url(url)

my_player.play_stream()
time.sleep(4)
my_player.pause_stream()
time.sleep(3)
my_player.resume_stream()
my_player.join()
