# my_music_player
Python project SS2022

## 1. Goal, Motivation and Structure
The goal with this project was to create a nice music player application for my python coding classes. I always have a music playing device with me at all times. I grew up with the good old windows media player and listend to my favourite music all day. When I got my first MP3 player I was the happiest girl alive. All over the year I lived through 5 generations of MP3 players and I still have one on me everytime I go out. So my passion for listening to music hasn't waned a bit. But every device I owned had a little flaw and I kept thinking about how I would improve it if I were the one designing it. So with this project I got the perfect opportunity to actually design and programm a music player that workes in a way I always hoped it would be. The thing that always bothered me the most was the structuring of the songs. They all provide a stucture where you can choose among the artists, then the artists albums and their songs. But everything is ordered alphabetically. In my opinion albums should be sorted by release year. And finally I managed to do that.

I obviously had to create an interface to work with first, so at the beginning of my code I do exactly that. Afterwards I began to add functionality. To getting started I had to upload some songs and give them the proper structure and display everthing nicely in my player. Only then I could begin with adding and testing the commands for navigating the music, like play/pause, stop, previous song and next song. Now that music was playing I could add the timebar that shows how long a song is playing right now and how long the entire song is. The cherry on top is the option to show lyrics for every playing song.


## 2. System Requirements and Download links
To run the program you should have installed a working Python version (3.7 or higher). As well as the following libraries tkinter, gygame.mixer, mutagen.id3 and mutagen.mp3, lyricsgenius and time. 

If you're using anaconda you can get the music players environment with all libraries from the environment file musicplayer.yaml.
Else you can install the libraries given in the requirements.txt file.


## 3. Instruction for usage
Start the musicplayer by running the main.py file. You will now see the following screen:

![Image of started musicplayer](just_started_musicplayer.png)

Now you can upload your desired songs by clicking on the "Menu" button on the top left and select "Load Songs". You can only upload song files not entire folders with music, so keep that in mind. Also every song has to inherit the information about the artists and albums name, as well as the release year of the album. 

