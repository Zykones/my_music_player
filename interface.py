from tkinter import *
from tkinter import filedialog
from pygame import mixer
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import lyricsgenius as lg
from time import gmtime, strftime


"""
Set up the interface of the music players using tkinter and pygame.
"""

def build_interface():
    #Setting up the main frame
    global window
    window = Tk()
    window.geometry("500x350")
    window.title("My Music Player :D")
    #restrict user to change the windows size
    window.resizable(0, 0)


    #Setting up the buttons
    def button_frame(window):
        #initialize the mixer module
        mixer.init()

        #frame for placing buttons
        frame_left = Frame(window)
        frame_left.pack(side=LEFT)

        #create buttons
        play_button = Button(frame_left, text=u"\u23EF", width=7)
        play_button.grid(row=1, columnspan=3, sticky='ew')

        stop_button = Button(frame_left, text=u"\u23F9", width=7, command=stop)
        stop_button.grid(row=2, column=1)

        previous_button = Button(frame_left, text=u"\u23EE", width=7, command=previous)
        previous_button.grid(row=2, column=0)

        next_button = Button(frame_left, text=u"\u23ED", width=7, command=next)
        next_button.grid(row=2, column=2)

        #give play button the proper function
        play_button.focus()
        play_button.bind('<Button-1>', intermediate_play)

        #create frame for current playing song information
        global song_frame
        song_frame = LabelFrame(frame_left, text='Currently Playing', width= 180, height= 180)
        song_frame.grid(row= 0, columnspan=3, pady=20)

        Label(song_frame, text='Song:').place(x=3, y=10)
        Label(song_frame, text='Artist:').place(x=3, y=70)
        Label(song_frame, text='Album:').place(x=3, y=110)

        global song_time_bar
        song_time_bar = Label(frame_left, text="Songtime:", width=40)
        song_time_bar.place(x=-55, y=200) 

        #place buttons und songframe nicely
        frame_left.place(x=75, y=20)


    #Set up menubar for loading and selecting songs
    def menu():
        #create menubar
        menubar = Menu(window)
        window.config(menu=menubar)

        #create menu items
        filemenu = Menu(menubar, tearoff=0)
        
        filemenu.add_command(label="Load Songs", command=load)
        filemenu.add_separator()
        filemenu.add_command(label="Show Lyrics", command=show_lyrics)
        menubar.add_cascade(label="Menu", menu=filemenu)
        

    #build listbox for songs and structure
    def listbox_frame(window):
        frame_right = Frame(window)
        #frame_right.grid(column=1, row=0, padx=15, pady=15)
        frame_right.pack(side=RIGHT)

        #elements in listbox
        items = ("All Songs", "Artists")
        #listbox.insert(END, "All Songs") ?
        menu_items = StringVar(value=items)
        
        #create scrollbar for listbox
        global scrollbar_vertical
        global scrollbar_horizontal
        scrollbar_vertical = Scrollbar(frame_right, orient=VERTICAL)
        scrollbar_horizontal = Scrollbar(frame_right, orient=HORIZONTAL)

        scrollbar_vertical.pack(side=RIGHT, fill=Y)
        scrollbar_horizontal.pack(side=BOTTOM, fill=X)
        
        #create listbox
        global listbox
        listbox = Listbox(frame_right, listvariable=menu_items, height=21, width= 25, selectmode='browse', xscrollcommand = scrollbar_horizontal.set, yscrollcommand = scrollbar_vertical.set)
        listbox.pack(side=RIGHT)
        scrollbar_vertical.config(command = listbox.yview)
        scrollbar_horizontal.config(command = listbox.xview)

        listbox.bind("<Double-1>", get_action)
        listbox.pack()

     
    #run functions to create window
    menu()
    button_frame(window)
    listbox_frame(window)
   
    #continiously update the window until it is manually closed
    window.update()
    window.mainloop()



"""
Setting up the functions and commands for the interface.
"""

#variable for navigating through listbox menu
global status
global current_artist 

status = 0          #0 = main menu in listbox
current_artist = ""

#variables for keeping track of current song and tracklist
global tracklist
global current_track
global is_playing
global is_paused
global song_lbl
global album_lbl
global artist_lbl

tracklist = []
current_track = ""
is_playing = False      #change status between play() and stop()
is_paused = False       #change status between pause() and resume()
song_lbl = None         #update song label in currently playing
album_lbl = None        #update album label in currently playing
artist_lbl = None       #update artist label in currently playing



"""
Functions for the menu bar
"""

def load():
    global filepath
    global artists
    global albums
    global tracks
    global year
    global tracknumber

    artists = {}        #key: artist, value: albums
    albums = {}         #key: albums, value: tracks
    tracks = {}         #key: song titles, value: filepath
    year = {}           #key: album, value: release year
    tracknumber = {}    #key: song titles, value: title number

    filepath = filedialog.askopenfilenames(initialdir = "/", 
                                            title = "Select a File",
                                            filetypes = (("MP3-Files", "*.mp3*"), ("all files", "*.*")))
    
    store_id3()
   

def store_id3():
    #get id3 info and save them
    for item in filepath:
        tag = ID3(item)
        my_track = str(tag["TIT2"])
        my_artist = str(tag["TPE1"])
        my_album = str(tag["TALB"])
        my_year = str(tag["TDRC"])
        my_tracknumber = str(tag["TRCK"])

        #convert 1/11 style number to 1 as number not string
        my_tracknumber = int(my_tracknumber[:my_tracknumber.rfind("/")])
        
        #store track with respective filepath
        tracks[my_track] = item

        #store artist with respective albums
        if not my_artist in artists:
            artists[my_artist] = [my_album]

        elif not my_album in artists[my_artist]:
            artists[my_artist].append(my_album)

        #store albums with respective tracks
        if not my_album in albums:
            albums[my_album] = [my_track]

        elif not my_track in albums[my_album]:
            albums[my_album].append(my_track)
        
        #store album with respective release year
        if not my_album in year:
            year[my_album] = my_year

        #store track with respective tracknumber
        tracknumber[my_track] = my_tracknumber

def show_lyrics():
    api_key = "RkAaak3o5ILyWROqIVslYQxV7grjAk6LEEg_9lfP6IqC63OJZRms6vFmaO9O-ZFV"
    genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])
    
    #create text window for the lyrics
    new_window = Toplevel(window)
    new_window.geometry("600x600")
    new_window.title("Song Lyrics")
    
    #create a scrollbar for the text window
    scrollbar = Scrollbar(new_window)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_widget = Text(new_window, yscrollcommand=scrollbar.set)
    text_widget.pack(expand=True, fill=BOTH)
    scrollbar.config(command = text_widget.yview)
    
    #search song lyrics on Genius Lyrics and display them
    song = genius.search_song(title=current_track, artist=current_artist, get_full_info=TRUE)
    
    text_widget.insert("1.0", song.lyrics)
    


"""
Function to define double click actins in listbox menu
"""

def get_action(event):
    index = listbox.nearest(event.y)
    global status
    global is_playing

    if status == 0:
        if index == 0:
            all_songs(event)
            status = 4
        elif index == 1:
            show_artists(event)
            status = 1
    
    elif status == 1:
        if index == 0:
            main_menu(event)
            status -= 1
        else:
            show_albums(event)
            status = 2

    elif status == 2:
        if index == 0:
            show_artists(event)
            status -= 1
        else:
            show_tracks(event)
            status = 3

    elif status == 3:
        if index == 0:
            show_albums(event)
            status -= 1
        else:
            is_playing = False
            play_on_click(event)
            pass
    
    elif status == 4:
        if index == 0:
            main_menu(event)
            status = 0
        else:
            is_playing = False
            play_on_click(event)
            pass



"""
Functions for creating the listbox menu
"""

def main_menu(event):
    listbox.delete(0, END)

    listbox.insert(0, "All Songs")
    listbox.insert(1, "Artists")

def all_songs(event):
    #delete all listbox items and show all songs
    listbox.delete(0, END)
    global tracklist
    
    #empty existing tracklist
    tracklist = []
    
    #get song names
    names = tracks.keys()
    names = sorted(names)

    for index, title in enumerate(names):
        listbox.insert(index, title)
        tracklist.append(title)
    
    listbox.insert(0, "BACK")
    scrollbar_vertical.config(command = listbox.yview)
    scrollbar_horizontal.config(command = listbox.xview)
        
def show_artists(event):
    listbox.delete(0, END)
    
    #get artists
    names = artists.keys()
    names = sorted(names)

    for index, title in enumerate(names):
        listbox.insert(index, title)

    listbox.insert(0, "BACK")
    scrollbar_vertical.config(command = listbox.yview)
    scrollbar_horizontal.config(command = listbox.xview)

def show_albums(event):
    index = listbox.nearest(event.y)
    global current_artist

    #get artist
    artist_names = artists.keys()
    artist_names = sorted(artist_names)
    #check if Back Button was clicked
    if index > 0:
        current_artist = artist_names[index-1]
    
    listbox.delete(0, END)
    
    #get albums
    album_names = artists.get(current_artist)
    sorted_albums = sort_albums(album_names)

    for index, title in enumerate(sorted_albums):
        listbox.insert(index, title)

    listbox.insert(0, "BACK")
    scrollbar_vertical.config(command = listbox.yview)
    scrollbar_horizontal.config(command = listbox.xview)

def show_tracks(event):
    index = listbox.nearest(event.y)
    global current_artist
    global tracklist

    #empty existing tracklist
    tracklist = []

    #get album
    album_names = artists.get(current_artist)
    album_names = sort_albums(album_names)
    album_names = list(album_names.keys())
    current_album = album_names[index-1]

    listbox.delete(0, END)

    #get tracks
    track_names = albums.get(current_album)
    sorted_tracks = sort_tracks(track_names)
    
    for index, title in enumerate(sorted_tracks):
        listbox.insert(index, title)
        tracklist.append(title)

    listbox.insert(0, "BACK")
    scrollbar_vertical.config(command = listbox.yview)
    scrollbar_horizontal.config(command = listbox.xview)

def sort_albums(album_names):
    current_albums = {}
    for item in album_names:
        current_albums[item] = year.get(item)
    
    #sort according to release year
    sorted_albums = {key: val for key, val in sorted(current_albums.items(), key = lambda ele: ele[1])}
    
    return sorted_albums

def sort_tracks(track_names):
    current_tracks = {}
    for item in track_names:
        current_tracks[item] = tracknumber.get(item)
    
    #sort according to title number
    sorted_tracks = {key: val for key, val in sorted(current_tracks.items(), key = lambda ele: ele[1])}
    return sorted_tracks



"""
Functions for the buttons and playing songs per double click
"""

def play_on_click(event):
    global current_track

    #update current track
    index = listbox.nearest(event.y)
    current_track = tracklist[index-1]
    
    play()
    
def intermediate_play(event):
    play()

def play():
    global is_playing
    global is_paused
    global current_track
    
    path = tracks.get(current_track)

    #for pause/unpause current playing song
    if is_playing == True:
        if is_paused == False:
            mixer.music.pause()
            is_paused = True  
        elif is_paused == True:
            mixer.music.unpause()
            is_paused = False

    #play song selected from listbox or restart song after stop       
    if is_playing == False:
        mixer.music.load(path)
        mixer.music.play()
        currently_playing()
        song_time()
        is_playing = True

def stop():
    global is_playing
    
    mixer.music.stop()
    is_playing = False

def previous():
    global current_track
    
    if current_track in tracklist:
        index = tracklist.index(current_track)

    #update current track to previous track if possible
    if index != 0:
        current_track = tracklist[index-1]
    else:
        return  #do nothing

    stop()      #to reset the raw time
    play()

def next():
    global current_track

    if current_track in tracklist:
        index = tracklist.index(current_track)
    
    #update current track to next track if possible
    if index < len(tracklist)-1:
        current_track = tracklist[index+1]
    else:
        return  #do nothing
    
    stop()      #to reset the raw time
    play()

def song_time():
    global is_playing
    global current_track
    global song_length
    
    #get current playtime
    raw_time = mixer.music.get_pos()/1000
    converted_time = strftime("%H:%M:%S",gmtime(raw_time))
    
    #get overall playtime
    song_type = MP3(tracks.get(current_track))
    song_length = strftime("%H:%M:%S", gmtime(song_type.info.length))
    
    #update timebar
    if is_playing == True:
        song_time_bar.config(text="Songtime: " + str(converted_time) + " of " + str(song_length))
    else:
        song_time_bar.config(text="Songtime: 00:00:00 of " + str(song_length))

    if raw_time < 0:
        if is_playing == True:
            stop()
            next()
    #call function recursively every 1 sec
    song_time_bar.after(1000,song_time)



"""
Function for updating the currently playing frame
"""

def currently_playing():
    global song_frame
    global current_track
    global current_artist
    global window
    global song_lbl
    global album_lbl
    global artist_lbl

    #current song
    if song_lbl:
        song_lbl.after(100, song_lbl.destroy())
    song_lbl = Label(song_frame, text=current_track, wraplength=126)
    song_lbl.place(x=45, y=10)
    
    #current album
    #my_album = [key for key, val in albums.items() if any(y in [val] for y in current_track)]
    for key in albums:
        list_val = albums[key]
        for val in list_val:
            if val == current_track:
                my_album = key
    
    if album_lbl:
        album_lbl.after(100, album_lbl.destroy())
    album_lbl = Label(song_frame, text=my_album, wraplength=126)
    album_lbl.place(x=45, y=110)
    
    #current artist
    #my_artist = [key for key, val in artists.items() if any(y in [val] for y in my_album)]
    for key in artists:
        list_val = artists[key]
        for val in list_val:
            if val == my_album:
                current_artist = key
                
    if artist_lbl:
        artist_lbl.after(100, artist_lbl.destroy())
    artist_lbl = Label(song_frame, text=current_artist, wraplength=126)
    artist_lbl.place(x=45, y=70)

