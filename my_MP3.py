from tkinter import *
from tkinter import filedialog
from pygame import mixer

class MusicPlayer:
    def __init__(self, window ):

        window.geometry('320x45'); window.title('Player'); window.resizable(0,0)
        mixer.init()
        Load = Button(window, text = 'Load list',  width = 10, font = ('Times', 10), command = self.load)
        Play = Button(window, text = '▷∥',  width = 2,font = ('Times', 10), command = self.play)
        Next_Sound = Button(window, text='▷▷∣', width=3, font=('Times', 10), command=self.Next_Track)
        Prev_Sound = Button(window, text='∣◁◁', width=3, font=('Times', 10), command=self.Prev_Track)
        INFO_DEBUG = Button(window, text='Info', width=5, font=('Times', 10), command=self.info)
        self.Name_Sound = Label(width = 45, bg='black', fg='white')
        self.Volume_count = Label(width=3, bg='black', fg='white')

        Volume = Scale(window, from_=0, to=100, orient=HORIZONTAL, showvalue=False, length=122, command=self.Volume_chenges)
        Volume.set(1)

        self.Name_Sound.place(x=0, y=0);Load.place(x=0,y=20);Prev_Sound.place(x=80,y=20);Play.place(x=111,y=20);Next_Sound.place(x=135,y=20)
        self.Volume_count.place(x=168,y=23);Volume.place(x=193,y=23)#;INFO_DEBUG.place(x=274,y=73)

        self.now_music_file = False
        self.playing_state = False
        self.nList = 0

    def formating_files(self, files):
        self.list_music = []
        for i in files:
            ext =  i[-3:-1]+i[-1]
            if ext.upper() == "MP3" or ext.upper() == "WAV" or ext.upper() == "OGG":
                self.list_music.append(i)
    def Volume_chenges(self,volume):
        self.Volume_count["text"] = volume
        mixer.music.set_volume(int(volume)/100)
    def load_music(self):
        self.now_music_file = self.list_music[self.nList]
        self.Name_Sound['text'] = ''.join(self.now_music_file.split("/")[-1])
        mixer.music.load(self.now_music_file)
        for i in range(self.nList+1,len(self.list_music)):
            mixer.music.queue(self.list_music[i])
        for i in range(0, self.nList):
            mixer.music.queue(self.list_music[i])
        self.first_playing = True

    def load(self):
        files = filedialog.askopenfilenames()
        self.formating_files(files)
        if self.list_music == []:
            return 0
        self.nList = 0
        self.load_music()

    def info(self):
        if self.now_music_file==False:
            return 0
        print("Debug")
        print(f"Прошло: {mixer.music.get_pos()//1000}с")
        from mutagen.mp3 import MP3
        f = MP3(self.list_music[self.nList])
        print(f"Кончается в {int(f.info.length)}с")

    def play(self):
        if self.now_music_file==False:
            return 0
        if self.first_playing:
            mixer.music.play()
            self.first_playing = False
        else:
            if not self.playing_state:
                mixer.music.pause()
                self.playing_state=True
            else:
                mixer.music.unpause()
                self.playing_state = False

    def Next_Track(self):
        if self.now_music_file==False:
            return 0
        #print(self.nList+1, len(self.list_music))
        if self.nList+1<len(self.list_music):
            self.nList += 1
        else:
            self.nList = 0
        mixer.music.stop()
        self.load_music()
        self.first_playing = False
        mixer.music.play()

    def Prev_Track(self):
        if self.now_music_file==False:
            return 0
        #print(self.nList+1, len(self.list_music))
        if self.nList-1>=0:
            self.nList -= 1
        else:
            self.nList = len(self.list_music)-1
        mixer.music.stop()
        self.load_music()
        self.first_playing = False
        mixer.music.play()


root = Tk()
app = MusicPlayer(root)
root.mainloop()
