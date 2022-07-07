from classes import *
from utils import notify

def play_song(selected_song_number):
    print(f"currently playing: {list(Songs.songs.keys())[selected_song_number]} ({selected_song_number + 1})")
    if Settings.notification:
        current_song = list(Songs.songs.keys())[selected_song_number]
        try:
            next_song = list(Songs.songs.keys())[selected_song_number + 1]
        except IndexError:
            next_song = list(Songs.songs.keys())[0]
        try:
            last_song = list(Songs.songs.keys())[selected_song_number - 1]
        except IndexError:
            last_song = list(Songs.songs.keys())[len(Songs.songs) - 1]
        notify(f"currently playing: {current_song}",
               f"pre: {last_song}\nnext: {next_song}")
    time.sleep(1)
    pyautogui.click(Settings.genshin_app_coordinate)
    last_action = time.time()
    while not keyboard.is_pressed('i'):

        if keyboard.is_pressed('k') or PlayVaria.allow_autoplay:
            PlayVaria.song_index = 0
            if UserVaria.song_loop:
                PlayVaria.allow_autoplay = True
            Songs.songs[list(Songs.songs.keys())[selected_song_number]].play()
            last_action = time.time()
        if keyboard.is_pressed("["):
            if UserVaria.song_loop:
                PlayVaria.allow_autoplay = True
            Songs.songs[list(Songs.songs.keys())[selected_song_number]].play()
            last_action = time.time()

        if keyboard.is_pressed('n'):
            pyautogui.press("win")
            time.sleep(0.1)
            pyautogui.click(x=902, y=1059)
            time.sleep(0.01)
            pyautogui.click(x=893, y=1007)
            keyboard.press("enter")
            break

        if keyboard.is_pressed("=") or time.time() >= last_action + 5:
            time.sleep(1)
            keyboard.wait("shift")
            last_action = time.time()

        if UserVaria.song_loop and PlayVaria.allow_autoplay:
            selected_song_number = (selected_song_number + 1) if selected_song_number < len(Songs.songs) - 1 else 0
            print(
                f"currently playing: {list(Songs.songs.keys())[selected_song_number]} ({selected_song_number + 1})")

            pyautogui.press("win")
            time.sleep(0.1)
            pyautogui.press("win")
            if Settings.notification:
                current_song = list(Songs.songs.keys())[selected_song_number]
                try:
                    next_song = list(Songs.songs.keys())[selected_song_number + 1]
                except IndexError:
                    next_song = list(Songs.songs.keys())[0]
                try:
                    last_song = list(Songs.songs.keys())[selected_song_number - 1]
                except IndexError:
                    last_song = list(Songs.songs.keys())[len(Songs.songs) - 1]
                notify(f"currently playing: {current_song}",
                       f"pre: {last_song}\nnext: {next_song}")
                time.sleep(0.3)
            pyautogui.click(Settings.genshin_app_coordinate)
            for i in range(260):
                time.sleep(0.01)
                if keyboard.is_pressed("shift"):
                    PlayVaria.allow_autoplay = False
                    break
            PlayVaria.song_index = 0

        if keyboard.is_pressed(".") or keyboard.is_pressed(","):
            if keyboard.is_pressed("."):
                selected_song_number = (selected_song_number + 1) if selected_song_number < len(
                    Songs.songs) - 1 else 0

            elif keyboard.is_pressed(","):
                selected_song_number = (selected_song_number - 1) if selected_song_number != 0 else len(
                    Songs.songs) - 1

            print(
                f"currently playing: {list(Songs.songs.keys())[selected_song_number]} ({selected_song_number + 1})")

            keyboard.block_key(",")  # prevent typing in search bar
            keyboard.block_key(".")
            pyautogui.press("win") #back to desktop
            time.sleep(0.1)
            pyautogui.press("win")
            keyboard.unhook_all()  # unlock the blocks

            escape_time = time.time() + 0.5  # time before confirming what songs to play
            while time.time() < escape_time:

                if keyboard.is_pressed("."):
                    while keyboard.is_pressed("."):
                        pass
                    selected_song_number = (selected_song_number + 1) if selected_song_number < (
                                len(Songs.songs) - 1) else 0
                    escape_time = time.time() + 1
                    print(
                        f"currently playing: {list(Songs.songs.keys())[selected_song_number]} ({selected_song_number + 1})")
                elif keyboard.is_pressed(","):
                    while keyboard.is_pressed(","):
                        pass
                    selected_song_number = (selected_song_number - 1) if selected_song_number != 0 else len(
                        Songs.songs) - 1
                    escape_time = time.time() + 1
                    print(
                        f"currently playing: {list(Songs.songs.keys())[selected_song_number]} ({selected_song_number + 1})")

            if Settings.notification:
                current_song = list(Songs.songs.keys())[selected_song_number]
                try:
                    next_song = list(Songs.songs.keys())[selected_song_number + 1]
                except IndexError:
                    next_song = list(Songs.songs.keys())[0]
                try:
                    last_song = list(Songs.songs.keys())[selected_song_number - 1]
                except IndexError:
                    last_song = list(Songs.songs.keys())[len(Songs.songs) - 1]
                notify(f"currently playing: {current_song}",
                       f"pre: {last_song}\nnext: {next_song}")
                time.sleep(0.3)
            pyautogui.click(Settings.genshin_app_coordinate)
            PlayVaria.song_index = 0
            last_action = time.time()