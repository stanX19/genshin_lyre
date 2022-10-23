from mido import MidiFile
from functools import cached_property
from data import *
import keyboard
import pyautogui
import time
import math
try:
    from ...utils import *
except ImportError:
    from utils import *


class Midi:

    def __init__(self, midi_path: str, name=""):
        if midi_path.endswith(".mid"):
            self.path = midi_path
            self.name = name
            self._MIdiFile = None
        else:
            raise ValueError(f"Expecting midi file type, got '.{midi_path.split('.')[-1]}' file type instead\n")

    def __str__(self):
        score_list = [val for val in self.to_score_list() if type(val) == float]
        total_length = sum(score_list)
        if total_length > 60:
            song_length = f"{math.floor(total_length / 60)}m {round(total_length % 60)}s"
        else:
            song_length = f"{round(total_length)}s"
        lowest_sharp, total_key = self.tune_to_C()
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
    @property
    def MIdiFile(self):
        if not self._MIdiFile:
            self._MIdiFile = [i for i in MidiFile(self.path) if not i.is_meta]
            self.tune_to_C()
        return self._MIdiFile
    @MIdiFile.setter
    def MIdiFile(self,val):
        self._MIdiFile = val
    @cached_property
    def score(self):
        return self.raw_keys
    @cached_property
    def raw_keys(self):
        self.tune_to_C()
        return score_list_to_score(self.to_score_list())
    @cached_property
    def score_list(self):
        self.tune_to_C()
        return self.to_score_list()
    @cached_property
    def note_keys(self):
        """notes range finding, minimum sharp will still be high for unsuitable score"""
        midi = self.MIdiFile
        LINE1 = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        LINE2 = ['A', 'S', 'D', 'F', 'G', 'H', 'J']
        LINE3 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U']
        difference = [2, 2, 1, 2, 2, 2, 1]

        # notes range finding
        midi_notes = sorted([i.note for i in midi if hasattr(i, 'note') and i.type == "note_on"])

        # min and max
        max_midi_note = max(midi_notes)
        min_midi_note = min(midi_notes)
        lowest_row_start = min_midi_note - min_midi_note % 12
        highest_row_start = max_midi_note - max_midi_note % 12

        if highest_row_start - lowest_row_start <= 24:
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

        # filling in LYRE_KEYS (range), low row and lower + mid row + high row and higher
        low_row = int((middle_row_start - lowest_row_start) / 12)
        high_row = int((highest_row_start - middle_row_start) / 12)
        LYRE_KEYS = LINE1 * low_row + LINE2 + LINE3 * high_row

        NOTE_KEY = dict(zip(NOTES, LYRE_KEYS))
        return NOTE_KEY

    def tune_to_C(self):
        if hasattr(self, "best_possible"):
            return self.best_possible, self.track_len

        track = [i.note for i in self.MIdiFile if 'note' in dir(i) and i.type == 'note_on']
        all_possible_major = {}
        sharps_idx = [1, 3, 6, 8, 10]

        for major_idx in range(12):
            sharps = 0
            for note in track:
                if (note + major_idx) % 12 in sharps_idx:
                    sharps += 1
            all_possible_major[sharps] = major_idx
            if sharps == 0:
                break

        best_possible = list(sorted(all_possible_major))[0]
        offset = all_possible_major[best_possible]
        New_midi = []
        for msg in self.MIdiFile:
            if 'note' in dir(msg):
                msg.note += offset
            New_midi.append(msg)
        self.best_possible = best_possible
        self.track_len = len(track)
        self.MIdiFile = New_midi
        return self.best_possible, len(track)

    def to_score_list(self):
        midi = self.MIdiFile
        score_list = [0.0]
        for idx, msg in enumerate(midi):
            # if msg.is_meta: continue
            if msg.time > 0.0:
                try:
                    score_list[-1] += msg.time
                except (TypeError, IndexError):
                    score_list.append(msg.time)

            if 'note' in dir(msg) and msg.type == 'note_on':
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

    def play(self, waitForK=False):
        pyautogui.PAUSE = 0
        self.tune_to_C()
        if waitForK:
            keyboard.wait("k")

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
                PlayVaria.song_index -= 50 if PlayVaria.song_index > 49 else 0
                continue
            if keyboard.is_pressed("right"):
                time.sleep(0.01)
            else:
                if type(msg) == float:
                    fixed_time += msg/PlayVaria.speed  # time that should've pass
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