import pafy 
import time
from read_video import read_video

url ="https://www.youtube.com/watch?v=ls-LYas5j8U"
video = pafy.new(url)

read_video(video, 'Best', 'Video')

time.wait(0)
