import keyboard
import pyautogui
import time
import re
import math
from config_data import *
from bisect import bisect_right, bisect_left


class old_music_score():
    def __init__(self, score_keys, beat=0.15, name=""):
        self.score = score_keys.replace(" ", "-")
        self.keys = []
        self.beat = beat
        self.name = name
        self.key_nodes = {}
        self.beat_change = {}
        self.raw_key_list = []
        multikey = False
        temp_store = ""
        temp_beat = beat
        for letter in self.score:
            if multikey:  # == True # in bracket
                if letter == ")":  # end of bracket
                    if 'beat' in temp_store.lower():
                        x = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", temp_store)
                        if x != []:
                            temp_beat = float(x[0])
                            self.beat_change[len(self.keys)] = temp_beat
                        self.keys.append(temp_store)
                        self.raw_key_list.append(f"({temp_store})")
                    elif temp_store == "$$":
                        self.key_nodes[(len(self.keys) - 1)] = temp_beat
                    else:
                        self.keys.append(temp_store)
                        self.raw_key_list.append(f"({temp_store})")
                    temp_store = ""
                    multikey = False
                else:
                    temp_store += letter

            elif letter == "(":  # start of bracket
                multikey = True

            elif letter == "\n":
                self.keys.append("-")
                self.raw_key_list.append("\n")
            else:
                self.keys.append(letter)
                if not letter.isnumeric():
                    self.raw_key_list.append(letter)
                elif int(letter) > 4:
                    self.raw_key_list.append("-")

        self.raw_keys = "".join([i for i in self.raw_key_list if 'beat' not in i.lower()])
        if name != "":
            Songs.songs[name.lower()] = self

    # old music score
    def play(self):
        pyautogui.PAUSE = 0.1
        PlayVaria.temp_beat = self.beat / PlayVaria.speed
        while PlayVaria.song_index < len(self.keys):

            if keyboard.is_pressed("right"):
                if self.keys[PlayVaria.song_index] not in ["-"] and 'beat' not in self.keys[
                        PlayVaria.song_index].lower():
                    pyautogui.typewrite(self.keys[PlayVaria.song_index].lower())
            else:
                time.sleep(PlayVaria.temp_beat)

                if keyboard.is_pressed("shift") or keyboard.is_pressed("z"):
                    PlayVaria.song_index -= math.ceil(0.2 / PlayVaria.temp_beat)
                    PlayVaria.song_index = 0 if PlayVaria.song_index < 0 else PlayVaria.song_index
                    PlayVaria.allow_autoplay = False
                    return 0

                elif keyboard.is_pressed("left"):
                    while keyboard.is_pressed("left"):
                        pass
                    PlayVaria.song_index = max(math.ceil(PlayVaria.song_index - 3 / max(PlayVaria.temp_beat, 0.03)), 1)
                    left = bisect_left(list(self.beat_change), PlayVaria.song_index) - 1
                    # -1 bcs bisect left actually returns an insert index
                    # so we minus 1 to get the index to the left of insert index
                    upper_beat_index = list(self.beat_change)[left]
                    PlayVaria.temp_beat = self.beat_change[upper_beat_index]
                elif keyboard.is_pressed("down"):
                    while keyboard.is_pressed("down"):
                        pass
                    try:
                        right = bisect_right(list(self.key_nodes),
                                             PlayVaria.song_index)  # find the closest next key node
                        PlayVaria.song_index = list(self.key_nodes)[right]
                        PlayVaria.temp_beat = self.key_nodes[PlayVaria.song_index]
                    except IndexError:  # no more checkpoints after this
                        PlayVaria.song_index = len(self.keys)

                elif keyboard.is_pressed("up"):
                    while keyboard.is_pressed("up"):
                        pass
                    left = bisect_left(list(self.key_nodes),
                                       max(0, int(PlayVaria.song_index - 3 / max(PlayVaria.temp_beat, 0.001)))) - 1
                    PlayVaria.song_index = list(self.key_nodes)[left] if left >= 0 else -1
                    PlayVaria.temp_beat = self.key_nodes[
                        PlayVaria.song_index] if PlayVaria.song_index != -1 else self.beat

                elif self.keys[PlayVaria.song_index] == "-":
                    time.sleep(PlayVaria.temp_beat)

                elif 'beat' in self.keys[PlayVaria.song_index].lower():
                    if re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?",self.keys[PlayVaria.song_index]):
                        PlayVaria.temp_beat = float(re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?",
                                                               self.keys[PlayVaria.song_index])[
                                                        0]) / PlayVaria.speed
                    else:
                        print(f">>>beat format error for {self.name} at {PlayVaria.song_index}")
                elif self.keys[PlayVaria.song_index].isnumeric():
                    time.sleep((int(self.keys[PlayVaria.song_index]) / 10) * PlayVaria.temp_beat)
                else:
                    pyautogui.typewrite(self.keys[PlayVaria.song_index].lower())
            PlayVaria.song_index += 1


class music_score(old_music_score):
    def play(self):
        pyautogui.PAUSE = 0.1
        if PlayVaria.song_index == 0:
            PlayVaria.temp_beat = self.beat / PlayVaria.speed
        while PlayVaria.song_index < len(self.keys):

            if keyboard.is_pressed("shift") or keyboard.is_pressed("z"):
                PlayVaria.song_index -= math.ceil(0.2 / PlayVaria.temp_beat)
                PlayVaria.song_index = 0 if PlayVaria.song_index < 0 else PlayVaria.song_index
                PlayVaria.allow_autoplay = False

                return 0
            elif keyboard.is_pressed("right"):
                if self.keys[PlayVaria.song_index] not in ["-"] and 'beat' not in self.keys[PlayVaria.song_index].lower():
                    pyautogui.typewrite(self.keys[PlayVaria.song_index].lower())
            elif keyboard.is_pressed("left"):
                while keyboard.is_pressed("left"):
                    pass
                PlayVaria.song_index = max(math.ceil(PlayVaria.song_index - 3 / max(PlayVaria.temp_beat, 0.03)), 1)
                left = bisect_left(list(self.beat_change), PlayVaria.song_index) - 1
                # -1 bcs bisect left actually returns an insert index
                # so we minus 1 to get the index to the left of insert index
                upper_beat_index = list(self.beat_change)[left]
                PlayVaria.temp_beat = self.beat_change[upper_beat_index]
            elif keyboard.is_pressed("down"):
                while keyboard.is_pressed("down"):
                    pass
                try:
                    right = bisect_right(list(self.key_nodes), PlayVaria.song_index)
                    PlayVaria.song_index = list(self.key_nodes)[right]
                    PlayVaria.temp_beat = self.key_nodes[PlayVaria.song_index]
                except Exception:  # no more checkpoints after this
                    PlayVaria.song_index = len(self.keys)
            elif keyboard.is_pressed("up"):
                while keyboard.is_pressed("up"):
                    pass
                left = bisect_left(list(self.key_nodes),
                                   max(0, int(PlayVaria.song_index - 3 / max(PlayVaria.temp_beat, 0.001)))
                                   ) - 1
                PlayVaria.song_index = list(self.key_nodes)[left] if left >= 0 else -1
                PlayVaria.temp_beat = self.key_nodes[PlayVaria.song_index] if PlayVaria.song_index != -1 else self.beat

            elif self.keys[PlayVaria.song_index] == "-":
                time.sleep(PlayVaria.temp_beat)

            elif self.keys[PlayVaria.song_index].isnumeric():
                time.sleep(int(self.keys[PlayVaria.song_index]) / 10 * PlayVaria.temp_beat)

            elif 'beat' in self.keys[PlayVaria.song_index].lower():
                if re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?",
                              self.keys[PlayVaria.song_index]):  # != []:
                    PlayVaria.temp_beat = float(re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?",
                                                           self.keys[PlayVaria.song_index])[
                                                    0]) / PlayVaria.speed
                else:
                    print(f">>>beat format error for {self.name} at {PlayVaria.song_index}")

            else:
                pyautogui.typewrite(self.keys[PlayVaria.song_index].lower())

            PlayVaria.song_index += 1
