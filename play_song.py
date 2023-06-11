from classes import *
from utils import notify

def notify_current_song(song_idx):
    all_songs = list(Songs.songs.keys())
    next_idx = song_idx + 1 if song_idx + 1 != len(all_songs) else 0
    last_idx = song_idx - 1 if song_idx > 0 else len(all_songs) - 1
    notify(f"({last_idx + 1}) {all_songs[last_idx]}\n\
({song_idx + 1}) {all_songs[song_idx]}           (currently playing)\n\
({next_idx + 1}) {all_songs[next_idx]}")

def play_song(song_idx):
    print(f"currently playing: {list(Songs.songs.keys())[song_idx]} ({song_idx + 1})")
    # if Settings.notification:
    #     current_song = list(Songs.songs.keys())[song_idx]
    #     try:
    #         next_song = list(Songs.songs.keys())[song_idx + 1]
    #     except IndexError:
    #         next_song = list(Songs.songs.keys())[0]
    #     try:
    #         last_song = list(Songs.songs.keys())[song_idx - 1]
    #     except IndexError:
    #         last_song = list(Songs.songs.keys())[len(Songs.songs) - 1]
    if Settings.notification:
        notify_current_song(song_idx)
    # time.sleep(1)
    pyautogui.click(Settings.genshin_app_coordinate)
    last_action = time.time()
    while not keyboard.is_pressed('i'):

        if keyboard.is_pressed('k') or PlayVaria.allow_autoplay:
            PlayVaria.song_index = 0
            if UserVaria.song_loop:
                PlayVaria.allow_autoplay = True
            Songs.songs[list(Songs.songs.keys())[song_idx]].play()
            last_action = time.time()
        if keyboard.is_pressed("["):
            if UserVaria.song_loop:
                PlayVaria.allow_autoplay = True
            Songs.songs[list(Songs.songs.keys())[song_idx]].play()
            last_action = time.time()

        if keyboard.is_pressed("=") or time.time() >= last_action + 5:
            keyboard.wait("shift")
            last_action = time.time()
        if keyboard.is_pressed("n"):
            if Settings.notification:
                notify_current_song(song_idx)
            while keyboard.is_pressed("n"):
                pass
        if UserVaria.song_loop and PlayVaria.allow_autoplay:
            if keyboard.is_pressed("shift"):
                PlayVaria.allow_autoplay = False
                continue
            song_idx = (song_idx + 1) if song_idx < len(Songs.songs) - 1 else 0
            print(
                f"currently playing: {list(Songs.songs.keys())[song_idx]} ({song_idx + 1})")

            if Settings.notification:
                notify_current_song(song_idx)

            for i in range(260):
                time.sleep(0.01)
                if keyboard.is_pressed("shift"):
                    PlayVaria.allow_autoplay = False
                    break
            PlayVaria.song_index = 0

        if keyboard.is_pressed(".") or keyboard.is_pressed(","):
            if keyboard.is_pressed("."):
                song_idx = (song_idx + 1) if song_idx < len(
                    Songs.songs) - 1 else 0

            elif keyboard.is_pressed(","):
                song_idx = (song_idx - 1) if song_idx != 0 else len(
                    Songs.songs) - 1

            print(f"currently playing: {list(Songs.songs.keys())[song_idx]} ({song_idx + 1})")
            if Settings.notification:
                notify_current_song(song_idx)
            PlayVaria.song_index = 0

            while keyboard.is_pressed(".") or keyboard.is_pressed(","):
                pass
            last_action = time.time()