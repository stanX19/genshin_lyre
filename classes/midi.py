import math
import time
from functools import cached_property

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


class Midi:
    def __init__(self, midi_path: str, name=""):
        if midi_path.endswith(".mid"):
            self.path = midi_path
            self.name = name
            self.track_len = 0
            self.best_possible = []
            self._is_tuned_to_c = False
            self._midi_file = None
        else:
            raise ValueError(f"Expecting midi file type, got '.{midi_path.split('.')[-1]}' file type instead\n")

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
        self.tune_to_c()
        return utils.score_list_to_score(self.to_score_list())

    @cached_property
    def score_list(self):
        self.tune_to_c()
        return self.to_score_list()



    @cached_property
    def note_keys(self):
        """notes range finding, minimum sharp will still be high for unsuitable midi"""
        midi = self.midi_file
        LINE1 = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        LINE2 = ['A', 'S', 'D', 'F', 'G', 'H', 'J']
        LINE3 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U']
        difference = [2, 2, 1, 2, 2, 2, 1]

        # notes range finding
        midi_notes = sorted([i.note for i in midi if is_note_on(i)])

        # min and max
        max_midi_note = midi_notes[-1]
        min_midi_note = midi_notes[0]
        lowest_row_start = min_midi_note - min_midi_note % 12
        highest_row_start = max_midi_note - max_midi_note % 12

        if highest_row_start - lowest_row_start <= 24:  # small range of data
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
        low_row = int((middle_row_start - lowest_row_start) / 12)
        high_row = int((highest_row_start - middle_row_start) / 12)
        LYRE_KEYS = LINE1 * low_row + LINE2 + LINE3 * high_row

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

    def to_score_list(self):
        midi = self.midi_file
        score_list = [0.0]
        for idx, msg in enumerate(midi):
            if msg.time > 0.0:
                try:
                    score_list[-1] += msg.time
                except (TypeError, IndexError):
                    score_list.append(msg.time)

            if is_note_on(msg):
                stated_note = self.note_keys.get(msg.note, '')

                if type(score_list[-1]) == str:
                    #  sharp handling
                    if stated_note == '' and Settings.midi_include_sharps:
                        minus1 = self.note_keys[msg.note - 1]
                        if len(score_list) < 5 or minus1 in score_list[-3] or minus1 in score_list[-5]:
                            stated_note = self.note_keys[msg.note + 1]
                        else:
                            stated_note = self.note_keys[msg.note - 1]
                    score_list[-1] += stated_note
                else:  # prev element is float
                    #  sharp handling
                    if stated_note == '' and Settings.midi_include_sharps:
                        minus1 = self.note_keys[msg.note - 1]
                        if len(score_list) < 4 or minus1 in score_list[-2] or minus1 in score_list[-4]:
                            stated_note = self.note_keys[msg.note + 1]
                        else:
                            stated_note = self.note_keys[msg.note - 1]
                    score_list.append(stated_note)

        while isinstance(score_list[0], float):
            score_list.pop(0)
        while isinstance(score_list[-1], float):
            score_list.pop(-1)
        return score_list

    def play(self):
        pyautogui.PAUSE = 0
        self.tune_to_c()

        # to score
        score_list = self.to_score_list()
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
                PlayVaria.song_index = PlayVaria.song_index - 50 if PlayVaria.song_index > 49 else 0
                continue
            if keyboard.is_pressed("right"):
                time.sleep(0.01)
            else:
                if type(msg) == float:
                    fixed_time += msg / PlayVaria.speed  # time that should've pass
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

    def __str__(self):
        score_list = [val for val in self.to_score_list() if type(val) == float]
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

