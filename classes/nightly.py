import json
import math
import time
from functools import cached_property

import keyboard
import pyautogui
from config_data import *

try:
    from ... import utils
except ImportError:
    import utils


class Nightly:
    def __init__(self, path: str, name=""):
        self.path = path
        self.name = name
        self.score_list = []
        try:
            with open(path, encoding="utf-8") as f:
                json_data = json.load(f)[0]
            self.is_composed = json_data["data"]['isComposedVersion']
        except Exception as exc:
            raise Exception(f'The given text is not a Genshin nightly file path, missing key: {exc}')

        if self.is_composed:
            self.init_as_composed(json_data)
        else:
            self.init_as_recorded(json_data)

    def init_as_composed(self, json_data):
        try:
            bpm = json_data["bpm"]
            notes = json_data["columns"]
        except KeyError as exc:
            raise Exception(f"Missing key for composed genshinsheet score: {exc}")

        KEYS = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
        NOTES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        NOTE_KEY = dict(zip(NOTES, KEYS))
        beat = round((60 / bpm), 3)
        self.score_list = [0.0]
        for data in notes:
            temp_store = ''
            # collect all note in one column
            for note in data[1]:
                note_no = note[0]
                if note_no not in NOTES:
                    pass
                temp_store += NOTE_KEY[note_no]

            # there is note
            if temp_store:
                temp_store = "".join(set(temp_store))  # kill repeat
                self.score_list.append(temp_store)
                self.score_list.append(0.0)
            self.score_list[-1] += beat / (data[0] + 1)

    def init_as_recorded(self, json_data):
        try:
            notes = json_data["notes"]
        except KeyError as exc:
            raise Exception(f"Missing key for recorded genshinsheet score: {exc}")

        KEYS = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
        NOTES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        NOTE_KEY = dict(zip(NOTES, KEYS))

        previous_time = 0.0
        self.score_list = []
        for note in notes:
            key = NOTE_KEY[note[0]]
            play_time = note[1] / 1000
            delay = play_time - previous_time
            self.score_list += [delay, key]

            previous_time = play_time

    def __str__(self):
        all_interval = [val for val in self.score_list if isinstance(val, float)]
        total_length = sum(all_interval)
        if total_length > 60:
            song_length = f"{math.floor(total_length / 60)}m {round(total_length % 60)}s"
        else:
            song_length = f"{round(total_length)}s"
        return f"""    STATS FOR {self.name}:
      TYPE        : nightly score
      SAVED AS    : {self.name}.json
      LENGTH      : {song_length}
      FORMAT      : {"composed" if self.is_composed else "recorded"}, total {len(all_interval) + 1} keys"
                """

    @property
    def raw_keys(self):
        return self.score

    @cached_property
    def score(self):
        return utils.score_list_to_score(self.score_list)

    def play(self, waitForK=False):
        pyautogui.PAUSE = 0
        if waitForK:
            keyboard.wait("k")

        # to score
        score_list = self.score_list

        while isinstance(score_list[0], float):
            score_list.pop(0)

        start_time = time.time()
        threshold = Settings.midi_beat_threshold
        fixed_time = 0.0
        while PlayVaria.song_index < len(score_list):
            msg = score_list[PlayVaria.song_index]
            if keyboard.is_pressed("shift"):
                break
            if keyboard.is_pressed("left"):
                while keyboard.is_pressed("left"):
                    pass
                PlayVaria.song_index -= 50 if PlayVaria.song_index > 49 else 0
                continue
            if keyboard.is_pressed("right"):
                time.sleep(0.01)  # the original delay of pyautogui
            else:
                if type(msg) == float:
                    fixed_time += msg  # time that should've pass
                actual_playback_time = time.time() - start_time
                duration_to_next_event = fixed_time - actual_playback_time
                # to cancel out any delay
                if duration_to_next_event > 0.0:
                    _stop_waiting = time.time() + duration_to_next_event
                    while time.time() < _stop_waiting:
                        time.sleep(0.001)
                        for key in ["shift", "left", "right"]:
                            if keyboard.is_pressed(key):
                                break
                        else:
                            continue
                        break
                    # time.sleep(duration_to_next_event)
                elif duration_to_next_event < threshold:
                    start_time = time.time() - fixed_time + threshold

            if type(msg) == str:
                pyautogui.typewrite(msg)
            PlayVaria.song_index += 1


if __name__ == '__main__':
    p = r"C:\Users\DELL\PycharmProjects\pythonProject\genshin_lyre\genshin_lyre\genshin_assets\nightly\zoltraak - frieren.json"
    n = Nightly(p)
    n.play(True)
