from classes import *
from utils import notify

def play_song(song_idx):
    print(f"currently playing: {list(Songs.songs.keys())[song_idx]} ({song_idx + 1})")
    if Settings.notification:
        current_song = list(Songs.songs.keys())[song_idx]
        try:
            next_song = list(Songs.songs.keys())[song_idx + 1]
        except IndexError:
            next_song = list(Songs.songs.keys())[0]
        try:
            last_song = list(Songs.songs.keys())[song_idx - 1]
        except IndexError:
            last_song = list(Songs.songs.keys())[len(Songs.songs) - 1]
        notify(f"currently playing: {current_song}\npre: {last_song}\nnext: {next_song}")
    time.sleep(1)
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

        if UserVaria.song_loop and PlayVaria.allow_autoplay:
            song_idx = (song_idx + 1) if song_idx < len(Songs.songs) - 1 else 0
            print(
                f"currently playing: {list(Songs.songs.keys())[song_idx]} ({song_idx + 1})")

            # pyautogui.press("win")
            # time.sleep(0.1)
            # pyautogui.press("win")
            if Settings.notification:
                current_song = list(Songs.songs.keys())[song_idx]
                try:
                    next_song = list(Songs.songs.keys())[song_idx + 1]
                except IndexError:
                    next_song = list(Songs.songs.keys())[0]
                try:
                    last_song = list(Songs.songs.keys())[song_idx - 1]
                except IndexError:
                    last_song = list(Songs.songs.keys())[len(Songs.songs) - 1]
                notify(f"currently playing: {current_song}\npre: {last_song}\nnext: {next_song}")
                # time.sleep(0.3)
            # pyautogui.click(Settings.genshin_app_coordinate)
            # for i in range(260):
            #     time.sleep(0.01)
            #     if keyboard.is_pressed("shift"):
            #         PlayVaria.allow_autoplay = False
            #         break
            PlayVaria.song_index = 0

        if keyboard.is_pressed(".") or keyboard.is_pressed(","):
            if keyboard.is_pressed("."):
                while keyboard.is_pressed("."):
                    pass
                song_idx = (song_idx + 1) if song_idx < len(
                    Songs.songs) - 1 else 0

            elif keyboard.is_pressed(","):
                while keyboard.is_pressed(","):
                    pass
                song_idx = (song_idx - 1) if song_idx != 0 else len(
                    Songs.songs) - 1

            print(
                f"currently playing: {list(Songs.songs.keys())[song_idx]} ({song_idx + 1})")

            # keyboard.block_key(",")  # prevent typing in search bar
            # keyboard.block_key(".")
            # pyautogui.press("win") #back to desktop
            # time.sleep(0.1)
            # pyautogui.press("win")
            # keyboard.unhook_all()  # unlock the blocks

            escape_time = time.time() + 0.5  # time before confirming what songs to play
            while time.time() < escape_time:

                if keyboard.is_pressed("."):
                    while keyboard.is_pressed("."):
                        pass
                    song_idx = (song_idx + 1) if song_idx < (
                                len(Songs.songs) - 1) else 0
                    escape_time = time.time() + 1
                    print(
                        f"currently playing: {list(Songs.songs.keys())[song_idx]} ({song_idx + 1})")
                elif keyboard.is_pressed(","):
                    while keyboard.is_pressed(","):
                        pass
                    song_idx = (song_idx - 1) if song_idx != 0 else len(
                        Songs.songs) - 1
                    escape_time = time.time() + 1
                    print(
                        f"currently playing: {list(Songs.songs.keys())[song_idx]} ({song_idx + 1})")

            if Settings.notification:
                current_song = list(Songs.songs.keys())[song_idx]
                try:
                    next_song = list(Songs.songs.keys())[song_idx + 1]
                except IndexError:
                    next_song = list(Songs.songs.keys())[0]
                try:
                    last_song = list(Songs.songs.keys())[song_idx - 1]
                except IndexError:
                    last_song = list(Songs.songs.keys())[len(Songs.songs) - 1]
                notify(f"pre: {last_song}\ncurrently playing: {current_song}\nnext: {next_song}")
                # time.sleep(0.3)
            # pyautogui.click(Settings.genshin_app_coordinate)
            PlayVaria.song_index = 0
            last_action = time.time()