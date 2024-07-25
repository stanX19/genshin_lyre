import math
import time
from functools import cached_property

import Settings
import keyboard
import pyautogui
from config_data import *
from mido import MidiFile

try:
    from ... import utils
except ImportError:
    import utils


def is_note_on(msg):
    return hasattr(msg, 'note') and msg.type == "note_on" and msg.velocity != 0


LINE_BOT = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
LINE_MID = ['A', 'S', 'D', 'F', 'G', 'H', 'J']
LINE_TOP = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U']


def merge_keys(keys: str):
    return "".join(set(keys))


def init_pressed_keys() -> dict[str, int]:
    return {k: 0 for k in LINE_BOT + LINE_MID + LINE_TOP + ['']}


def release_pressed_keys(pressed_keys: dict[str, int]) -> None:
    for c, n in pressed_keys.items():
        if not n:
            continue
        pyautogui.keyUp(c.lower())
        pressed_keys[c] = 0


class Msg:
    def __init__(self, delay: float, on_keys: str, off_keys: str):
        self.time: float = float(delay)
        self.on_keys: str = on_keys
        self.off_keys: str = off_keys

    def empty(self):
        return self.on_keys == "" and self.off_keys == ""

    def merge_with(self, other):
        if other.time > 0.0:
            raise ValueError("Other should not have time delay")
        self.off_keys = merge_keys(self.off_keys + other.off_keys)
        self.on_keys = merge_keys(self.on_keys + other.on_keys)

    def __str__(self):
        return f"{self.time:.2f} on={self.on_keys:10} off={self.off_keys:10}"

    def __repr__(self):
        return self.__str__()


class Midi:
    def __init__(self, midi_path: str, name=""):
        if not midi_path.endswith(".mid"):
            raise ValueError(f"Expecting midi file type, got '.{midi_path.split('.')[-1]}' file type instead")
        self.path = midi_path
        self.name = name
        self.track_len = 0
        self.best_possible = []
        self._is_tuned_to_c = False
        self._midi_file = None
        self._score_list: list[Msg] = []

    @property
    def midi_file(self):
        if not self._midi_file:
            self._midi_file = [i for i in MidiFile(self.path)]
            self.tune_to_c()
        return self._midi_file

    @midi_file.setter
    def midi_file(self, val):
        self._midi_file = val

    @cached_property
    def score(self):
        return self.raw_keys

    @cached_property
    def raw_keys(self):
        return utils.score_list_to_score(self.score_list)

    @cached_property
    def score_list(self):
        self.tune_to_c()
        self.init_score_list()
        score_list = []
        for msg in self._score_list:
            if msg.on_keys:
                score_list.append(msg.time)
                score_list.append(msg.on_keys)
        return score_list

    @cached_property
    def note_keys(self):
        """notes range finding, minimum sharp will still be high for unsuitable midi"""
        midi = self.midi_file
        difference = [2, 2, 1, 2, 2, 2, 1]

        # notes range finding
        midi_notes = sorted([i.note for i in midi if is_note_on(i)])

        # min and max
        max_midi_note = midi_notes[-1]
        min_midi_note = midi_notes[0]
        lowest_row_start = min_midi_note - min_midi_note % 12
        highest_row_start = max_midi_note - max_midi_note % 12

        # print(lowest_row_start, highest_row_start)
        if highest_row_start - lowest_row_start <= 12:  # small range of data
            middle_row_start = lowest_row_start
        elif highest_row_start - lowest_row_start <= 24:  # small range of data
            middle_row_start = lowest_row_start + 12
        else:
            # quartile
            third_quartile_note = midi_notes[round(len(midi_notes) / 6 * 5)]
            first_quartile_note = midi_notes[round(len(midi_notes) / 6)]
            third_quartile_start = third_quartile_note - third_quartile_note % 12
            first_quartile_start = first_quartile_note - first_quartile_note % 12

            # preventing middle_row from being weird
            # changing middle row to be close to the median but not the highest/lowest row
            if third_quartile_start - first_quartile_start == 24:
                middle_row_start = third_quartile_start - 12
            elif third_quartile_start - first_quartile_start > 24:
                all_row_start = {}
                for note in midi_notes:
                    NOTE_ROW = note - note % 12
                    all_row_start[NOTE_ROW] = all_row_start.get(NOTE_ROW, 0) + 1

                for ROW_START in list(all_row_start):
                    if ROW_START <= first_quartile_start or ROW_START >= third_quartile_start:
                        del all_row_start[ROW_START]
                interquartile_start = dict(sorted(all_row_start.items(), key=lambda item: item[1]))
                middle_row_start = list(interquartile_start)[0]
            else:
                middle_row_start = third_quartile_start
                # small range notes

        # adding offset to middle_row_start
        middle_row_start += Settings.midi_offset * 12
        # filling in NOTES(range) of notes
        number_of_rows = int((highest_row_start - lowest_row_start) / 12 + 1)
        NOTES = []
        index = lowest_row_start
        for i in difference * number_of_rows:
            NOTES.append(index)
            index += i

        # filling in LYRE_KEYS (range), low row and lower + mid-row + high row and higher
        low_row = (middle_row_start - lowest_row_start) // 12
        high_row = (highest_row_start - middle_row_start) // 12
        if Settings.rows_count >= 3:
            LYRE_KEYS = LINE_BOT * low_row + LINE_MID + LINE_TOP * high_row
        elif Settings.rows_count == 2:
            LYRE_KEYS = LINE_MID * (low_row + 1) + LINE_TOP * high_row
        elif Settings.rows_count == 1:
            LYRE_KEYS = (low_row + high_row + 1) * LINE_TOP
        else:
            raise ValueError(f"Expected row count > 0, got {Settings.rows_count} instead")

        NOTE_KEY = dict(zip(NOTES, LYRE_KEYS))
        return NOTE_KEY

    def tune_to_c(self):
        if self._is_tuned_to_c:
            return self.best_possible, self.track_len

        track = [i.note for i in self.midi_file if is_note_on(i)]
        sharps_idx = [1, 3, 6, 8, 10]

        all_types = {i: 0 for i in range(12)}
        for note in track:
            all_types[note % 12] += 1

        best_possible_major = 0
        min_sharps = float('inf')

        for major_idx in range(12):
            sharps = sum(all_types[(idx - major_idx) % 12] for idx in sharps_idx)

            if sharps == 0:
                best_possible_major = major_idx
                min_sharps = sharps
                break

            if sharps < min_sharps:
                best_possible_major = major_idx
                min_sharps = sharps

        offset = best_possible_major
        New_midi = []
        for msg in self.midi_file:
            if 'note' in dir(msg):
                msg.note += offset
            New_midi.append(msg)
        self.best_possible = min_sharps
        self.track_len = len(track)
        self.midi_file = New_midi
        return self.best_possible, len(track)

    def insert_off_in_score(self, key: str):
        OFF_THRESHOLD = 0.1

        idx = len(self._score_list) - 1
        backtracked_time = 0.0
        while backtracked_time + self._score_list[idx].time < OFF_THRESHOLD \
                and idx >= 0 and key not in self._score_list[idx].on_keys:
            backtracked_time += self._score_list[idx].time
            idx -= 1

        # impossible, if key needs to be turned off it must appear before reaching -1
        if idx == -1:
            return
        # remove existing off
        for msg in self._score_list[idx:]:
            if key in msg.off_keys:
                msg.off_keys = msg.off_keys.replace(key, "")

        # turn off after press
        if key in self._score_list[idx].on_keys:
            self._score_list[idx].off_keys += key + "#"
            return
        # now idx is the place to insert off msg
        # base case
        A = OFF_THRESHOLD - backtracked_time  # remaining time for the note at idx
        B = self._score_list[idx].time - A  # time for the inserted msg
        self._score_list[idx].time = A
        self._score_list.insert(idx, Msg(B, "", key))

    # def clean_score_list(self):
    #     cleaned = []
    #     pressed_keys: dict[str, int] = {k: 0 for k in LINE_BOT + LINE_MID + LINE_TOP}
    #     time_bucket = 0.0
    #     for msg in self._score_list:
    #         time_bucket += msg.time
    #         new_on_keys = ""
    #         for c in set(msg.on_keys):
    #             pressed_keys[c] += 1
    #             if pressed_keys[c] != 1:
    #                 continue
    #             new_on_keys += c
    #         new_off_keys = ""
    #         for c in set(msg.off_keys):
    #             pressed_keys[c] -= 1
    #             if pressed_keys[c] <= 0:
    #                 new_off_keys += c
    #         new_msg = Msg(time_bucket, new_on_keys, new_off_keys)
    #         if new_msg.empty():
    #             continue
    #         if new_msg.time == 0.0 and cleaned != []:
    #             cleaned[-1].merge_with(new_msg)
    #         else:
    #             cleaned.append(new_msg)
    #         time_bucket = 0.0
    #
    #     self._score_list = cleaned

    def init_score_list(self):
        midi = self.midi_file
        self._score_list = [Msg(0.0, "", "")]
        keys_history = [""]
        pressed_keys: dict[str, int] = init_pressed_keys()
        for idx, msg in enumerate(midi):
            # add and merge
            if msg.time > 0.0 and not self._score_list[-1].empty():
                self._score_list.append(Msg(msg.time, "", ""))
                if is_note_on(msg):
                    keys_history.append("")
            elif msg.time > 0.0:
                self._score_list[-1].time += msg.time
            if not hasattr(msg, 'note'):
                continue

            key = self.note_keys.get(msg.note, '')
            #  sharp handling
            if key == '' and Settings.midi_include_sharps:
                minus1 = self.note_keys.get(msg.note - 1, '')
                key = minus1

            if is_note_on(msg):
                pressed_keys[key] += 1
                if key in self._score_list[-1].off_keys:
                    self._score_list.append(Msg(0.0, "", ""))
                    keys_history.append("")
                if key not in self._score_list[-1].on_keys:
                    self._score_list[-1].on_keys += key
                    keys_history[-1] += key
            else:
                pressed_keys[key] -= 1
                if pressed_keys[key] <= 0 and key not in self._score_list[-1].off_keys:
                    self._score_list[-1].off_keys += key

        # for c, i in pressed_keys.items():
        #     if i:
        #         print(c, ":", i)
        # print()
        temp = self._score_list
        self._score_list = [Msg(0.0, "", "")]
        for msg in temp:
            # adding off before on
            for c in msg.on_keys:
                self.insert_off_in_score(c)
            self._score_list.append(msg)

        # self.clean_score_list()
        return self._score_list

    def play(self):
        pyautogui.PAUSE = 0
        self.tune_to_c()

        # to score
        _ = self.score_list
        start_time = time.time()

        pressed_keys: dict[str, int] = init_pressed_keys()
        threshold = Settings.midi_beat_threshold
        fixed_time = 0.0
        while PlayVaria.song_index < len(self._score_list):
            msg = self._score_list[PlayVaria.song_index]
            print(msg)
            if keyboard.is_pressed("shift"):
                break
            if keyboard.is_pressed("left"):
                while keyboard.is_pressed("left"):
                    pass
                release_pressed_keys(pressed_keys)
                PlayVaria.song_index = PlayVaria.song_index - 50 if PlayVaria.song_index > 49 else 0
                continue
            if keyboard.is_pressed("right"):
                time.sleep(0.01)
            else:
                fixed_time += msg.time / PlayVaria.speed  # time that should've pass
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

            for c in msg.on_keys:
                pyautogui.keyDown(c.lower())
                pressed_keys[c] = 1
            for c in msg.off_keys:
                pyautogui.keyUp(c.lower())
                pressed_keys[c] = 0

            PlayVaria.song_index += 1

        # release all keys before returning
        release_pressed_keys(pressed_keys)

    def __str__(self):
        score_list = [val for val in self.score_list if type(val) == float]
        total_length = sum(score_list)
        if total_length > 60:
            song_length = f"{math.floor(total_length / 60)}m {round(total_length % 60)}s"
        else:
            song_length = f"{round(total_length)}s"
        lowest_sharp, total_key = self.tune_to_c()
        percentage = round(lowest_sharp / total_key * 100, 1)
        if lowest_sharp > 0:
            suitability = f"lowest sharp is {lowest_sharp} out of {total_key} keys"
            if percentage > 0:
                suitability += f" -{percentage}%-, score may sound weird"
        else:
            suitability = "midi is tuned to C"
        return f"""    STATS FOR {self.name}:
      TYPE        : Midi file
      SAVED AS    : {self.name}.mid
      LENGTH      : {song_length}
      SUITABILITY : {suitability}
    """


def main():
    path = r"C:\Users\DELL\PycharmProjects\pythonProject\genshin_lyre\genshin_lyre\genshin_assets\midi\httyd workplace (6).mid"
    m = Midi(path)
    print(m._score_list)
    keyboard.wait('k')
    m.play()


if __name__ == '__main__':
    main()
