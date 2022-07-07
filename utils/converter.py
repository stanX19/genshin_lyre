import statistics
import math
import json
from .common import first_float

def score_list_to_score(score_list):
    all_keys = "ZXCVBNMASDFGHJQWERTYU"
    all_time = [i for i in score_list if type(i) == float]
    try:
        average_time = statistics.mode(all_time) #mode
    except statistics.StatisticsError: #if no mode or 2 mode
        average_time = None
    if not average_time or all_time.count(average_time) < len(all_time)/4:
        average_time = sorted(all_time)[round(len(all_time) / 2)]  # use median

    # edit average dashes here: ↓
    lowest_lim = average_time / 4
    lowest_time = min([i for i in all_time if i >= lowest_lim])

    score = ""
    for msg in score_list:
        if type(msg) == float:
            msg = (round(msg / lowest_time)) * "-"
        elif len(msg) > 1:
            msg = [key for key in msg if key in all_keys]
            msg = f"({''.join(set(msg))})"
        score += msg

    # score has been created but have no line break
    # so it is created here
    # edit length of each line below:
    line_break = 70
    to_break = line_break
    score = score.replace("-", " ").strip().replace(" ", "-")
    score = list(score)
    for idx, key in enumerate(score):
        if idx > to_break and key == "-" and idx != len(score) - 1 and score[idx + 1] != '-':
            score[idx] = "\n"
            to_break += line_break
    #                         0.0059 is delay by time.sleep() function
    score = f"(beat{round(lowest_time - 0.0059, 3)})-\n{''.join(score)}"
    return score

def key_list_to_score_list(key_list:list):
    score_list = [0.0]
    temp_beat = 0.15
    for key in key_list:
        if "beat" in key.lower():
            temp_beat = first_float(key)
        elif key == "-":
            score_list[-1] += temp_beat + 0.0059
        elif key.isnumeric():
            score_list[-1] += (temp_beat * (float(key)/10)) + 0.0059
        else:
            score_list.append(key)
            score_list.append(0.109)
    return score_list

def score_list_to_nightly(score_list:list, name="Undefined"):
    all_time = [i for i in score_list if type(i) == float]
    try:
        average_time = statistics.mode(all_time)  # mode
    except statistics.StatisticsError:  # if no mode or 2 mode
        average_time = None
    if not average_time or all_time.count(average_time) < len(all_time) / 4:
        average_time = sorted(all_time)[round(len(all_time) / 2)]  # use median

    #  edit average dashes here: ↓
    lowest_time = average_time / 4

    bpm = round(60 / lowest_time)
    jsonFile = {"data": {"isComposed": True, "isComposedVersion": True, "appName": "Genshin"}, "name": name, "bpm": bpm,
                "pitch": "C", "breakpoints": [0], "instruments": ["Lyre", "Lyre", "Lyre"]}
    KEYS = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
    NOTES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    KN = dict(zip(KEYS, NOTES))
    def get_representative_key(note:list,ratio:float)->list:
        if ratio == 1:
            return [[0, note]]
        elif ratio < 0.125:
            return [[3, note]]
        noOf125Left = ratio / 0.125
        ratio_key = {8: 0, 4: 1, 2: 2, 1: 3}
        final_keys = []
        for value, note_type in ratio_key.items():
            needed_no = math.floor(noOf125Left / value)
            if needed_no:
                final_keys += [note_type] * needed_no
                noOf125Left %= value
        final_keys.sort()
        self_note = final_keys[0]
        extra_note = [[note_type, []] for note_type in final_keys[1:]]

        return [[self_note,note]] + extra_note

    columns = []
    idx = 0
    while idx < len(score_list):
        if isinstance(score_list[idx], float):
            ratio = score_list[idx] / lowest_time
            columns += get_representative_key([],ratio)
            idx += 1
            continue
        #current note is str
        note = [[KN[key],"100"] for key in score_list[idx].upper() if key in KN]
        try:
            length = score_list[idx+1]
            ratio = length / lowest_time
        except IndexError:
            ratio = 1
        except ValueError:
            ratio = 0.109/lowest_time
        notes_list = get_representative_key(note, ratio)
        columns += notes_list
        idx+=2
    jsonFile["columns"] = columns
    jsonFile = json.dumps([jsonFile])
    return jsonFile