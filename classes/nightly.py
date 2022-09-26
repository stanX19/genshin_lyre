import json
import keyboard
import pyautogui
import time
from utils import score_list_to_score
from data import *
from functools import cached_property

class Nightly():
    def __init__(self,text: str):
        try:
            with open(text, encoding="utf-8") as f:
                text = json.load(f)[0]
            notes = text['columns']
        except Exception:
            raise Exception('The given text is not a Genshin nightly file')
        try:
            bpm = text["bpm"]
        except KeyError:
            raise Exception('Cannot process recorded version of nightly file')
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
            self.score_list[-1] += beat / (data[0]+1)

    @property
    def raw_keys(self):
        return self.score
    @cached_property
    def score(self):
        return score_list_to_score(self.score_list)

    def play(self, waitForK=False):
        pyautogui.PAUSE = 0
        if waitForK:
            keyboard.wait("k")

        # to score
        score_list = self.score_list
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
                time.sleep(0.1)  # the original delay of pyautogui
            else:
                if type(msg) == float:
                    fixed_time += msg / PlayVaria.speed  # time that should've pass
                actual_playback_time = time.time() - start_time
                duration_to_next_event = fixed_time - actual_playback_time
                # to cancel out any delay
                if duration_to_next_event > 0.0:
                    time.sleep(duration_to_next_event)
                elif duration_to_next_event < threshold:
                    start_time = time.time() - fixed_time + threshold

            if type(msg) == str:
                pyautogui.typewrite(msg)
            PlayVaria.song_index += 1