# yt-reader

The youtube reader is a tool that will allow you to navigate on youtube without 
using your navigator. It will use VLC instead to display your video. This tool 
is designed for low performance tools. 

**YT-READER** can display videos as videos or as music and download them as m4a or mp4.

# How to install

For the moment there is no setup.py file so you need to install the software manually 

**Linux** 

First you need to install python2 with the package manager pip

`sudo apt-get install python`

Then you need to install all the dependencies for the program 

`sudo apt-get install vlc`

`pip intall --user youtube-dl`

`pip intall --user pafy`

`pip intall --user pyhton-vlc`

`pip intall --user urllib`


**Windows**

First you need to install python2. It is recommended to install annaconda from the website too. And use the option `add python to PATH`

Then you need to install VLC. Be sure to install the x64 version if you installed python x64. 

Then add to Path VLC by adding to Path the folder of VLC (C:\Program Files\VideoLAN\VLC). 

To add a folder to Path follow the instruction on this website: https://www.computerhope.com/issues/ch000549.htm

Last but not least you need to install all the python dependencies for the App. Open cmd and type the following commands. 

`pip intall --user youtube-dl`

`pip intall --user pafy`

`pip intall --user pyhton-vlc`

`pip intall --user urllib`


# Version and Features
__Current version of the project: Alpha 1.1__ 
In the current version the player is available in command line. And you can download videos. 
Playlist will be added in the next patch.

Version | Expected content | Expected Date
--- | --- | --- 
Pre Alpha | Manually write link in the code | Oct. 25 2017
Alpha | Player available | Nov. 1 2017
Pre Beta | Youtube navigator available | Nov. 15 2017
Beta | Introdution of playlist  | Nov. 25 2017
Realease | Audio player and navigator fully available | Dec. 24 2017


# Known bug 

## Player unable to display video and open it

**Symptoms:** Some times, you may be unable to watch the video. All seems to go well, but if you start the video, the screen stays white. This error, might be due of the python-vlc lib. 
**Correction:**For the moment the best way is to open the video in VLC and accept the certificate for ever. I am working on an automatic fix.
