import time
import pyautogui
import keyboard
import re
import os
import math
import json
from bisect import bisect_right, bisect_left

class MalfunctionedMediaPlayer():
    def __init__(self, *wargs, **kwargs):
        pass
    def play(self): pass
    def pause(self): pass
    def stop(self): pass
try:
    from vlc import MediaPlayer
except Exception:
    MediaPlayer = MalfunctionedMediaPlayer
try:
    from send2trash import send2trash
except ImportError:
    def send2trash(*wargs, **kwargs):
        print("unable to delete files because module send2trash is misssing")
from converter1 import separate, braket_wrap
score_path = 'genshin_assets\\scores'
os.chdir(os.path.dirname(os.path.realpath(__file__)))
class TestPaths:
    test_path = 'genshin_assets\\test\\test.txt'
    settings_path = 'genshin_assets\\test_settings.txt'

class TestSettings:
    song_library = {}
    selected_song = None
    
def read_song_lib():
    try:
        with open(TestPaths.settings_path, encoding="utf-8") as f:
            TestSettings.song_library = json.load(f)
            return 1
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        save_song_lib()
    return 0

def save_song_lib():
    with open(TestPaths.settings_path, "w+") as f:
        json.dump(TestSettings.song_library, f)
    return True

def add_new_song_to_test():
    print("Drag the path of the mp3 you want to add here", end="")
    if set_song():
        print(" (None to unassign song)", end="")
    song_path = input(": ").replace('"', '')
    if song_path == "" and set_song():
        if input("Unassign {}? (Y/n): ".format(
                TestSettings.song_library[TestPaths.test_path].split("\\")[-1]
        )).lower() in ["y", "yes"]:
            del TestSettings.song_library[TestPaths.test_path]
            print("  Unassigned song bound to {}".format(
                TestPaths.test_path.split("\\")[-1]
            ))
    elif os.path.exists(song_path):
        TestSettings.song_library[TestPaths.test_path] = song_path
        print("  New song assigned to {}: {}".format(
            TestPaths.test_path.split("\\")[-1],
            song_path.split("\\")[-1]
        ))
    else:
        print("  Invalid path")
    save_song_lib()

def set_song() -> int:
    if TestPaths.test_path in list(TestSettings.song_library):
        if os.path.exists(TestSettings.song_library[TestPaths.test_path]):
            TestSettings.selected_song = MediaPlayer(TestSettings.song_library[TestPaths.test_path])
            return 1
        else:
            del TestSettings.song_library[TestPaths.test_path]
            save_song_lib()
    TestSettings.selected_song = MalfunctionedMediaPlayer()
    return 0


def test(score, beat=0.07, waitForK=True):
    read_song_lib()
    multikey = False
    keys = []
    key_nodes = {}
    beat_change = {}
    temp_store = ""
    temp_beat = beat
    for i in range(len(score)):
        if multikey:  # in bracket
            if score[i] == ")":  # end of bracket
                if 'beat' in temp_store.lower():
                    x = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", temp_store)
                    if x:  # != []
                        temp_beat = float(x[0])
                        beat_change[len(keys)] = temp_beat
                    else:
                        raise Exception("wrong fotmat for [beat]")

                if temp_store == "$$":
                    key_nodes[(len(keys)-1)] = temp_beat
                else:
                    keys.append(temp_store)
                temp_store = ""
                multikey = False
            else:
                temp_store += score[i]

        elif score[i] == "(":  # start of bracket
            multikey = True

        elif score[i] == " ":
            keys.append("-")
        elif score[i] == "\n":
            keys.append("%")

        else:

            keys.append(score[i])

    if waitForK:
        pyautogui.click(x=961, y=1061)
        print("press k to play")
        keyboard.wait("k")

    if set_song():  # if there is a matching song with the name of test_path
        TestSettings.selected_song.play()
    temp_beat = beat
    i = 0
    while i < len(keys):
        e = keys[i]
        if keyboard.is_pressed("shift"):
            TestSettings.selected_song.stop()
            break
        elif keyboard.is_pressed("left"):
            while keyboard.is_pressed("left"):
                pass
            i = max(math.ceil(i-3/max(temp_beat, 0.05)), 1)
            left = bisect_left(list(beat_change), i) - 1  # -1 bcs bisect left actually returns an insert index
            upper_beat_index = list(beat_change)[left]   # so we minus 1 to get the index to the left of insert index
            temp_beat = beat_change[upper_beat_index]

        elif keyboard.is_pressed("right"):
            if 'beat' not in e and e not in ["-", "%"]:
                pyautogui.typewrite(e.lower())
                print(e, end="")
        elif keyboard.is_pressed("down"):
            while keyboard.is_pressed("down"):
                pass
            try:
                right = bisect_right(list(key_nodes), i)
                i = list(key_nodes)[right]
                temp_beat = key_nodes[i]
            except IndexError:  # no more checkpoints after this
                i = len(keys)
        elif keyboard.is_pressed("up"):
            while keyboard.is_pressed("up"):
                pass
            left = bisect_left(list(key_nodes), max(0, int(i-3/max(temp_beat, 10**-3))))-1
            i = list(key_nodes)[left] if left >= 0 else -1
            temp_beat = key_nodes[i] if i != -1 else beat

        elif keyboard.is_pressed("p"):
            TestSettings.selected_song.pause()
            while True:
                if keyboard.is_pressed("[") or keyboard.is_pressed("shift"):
                    TestSettings.selected_song.play()
                    break

        elif e == "-" or e == "%":
            if e == "%":
                print()
            else:
                print("-", end="")
            time.sleep(temp_beat)

        elif e.isnumeric():
            time.sleep(int(e) / 10 * temp_beat)

        elif e.lower().find("beat") >= 0 and re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", e) != []:
            temp_beat = float(re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", e)[0])

        else:
            pyautogui.typewrite(e.lower())
            print(e, end="")

        i += 1
    print("\n")
    TestSettings.selected_song.stop()
    return score, beat


def save_to_scores(test_score, name):
    with open(f"{score_path}\\{name}.txt", "w+") as f:
        f.write(test_score)

    print("Saved in {}\n".format(os.path.dirname(os.path.realpath(__file__)) + "\\" + score_path))

def reducLineBreak(the_string: str):
    while "\n\n" in the_string:
        the_string = the_string.replace("\n\n", "\n")
    return the_string

def read_test_txt():
    with open(TestPaths.test_path, "r+", encoding="utf-8") as f:
        score = reducLineBreak(f.read().strip())
    return score

def animuz(test_score):
    splitted_score = reducLineBreak(test_score).split("\n")
    dict_score = {e.count("-"): i+1 for i,e in enumerate(splitted_score)}
    MAX_DASH = max(dict_score)
    
    print(f"the maximum number of dash, \"-\" is {MAX_DASH}\nat line {dict_score[MAX_DASH]}: {splitted_score[dict_score[MAX_DASH]-1]}")
    DASH_IN_LINE = input("Increase to how many \"-\" per line?: ")
    try:
        DASH_IN_LINE = int(DASH_IN_LINE)
        print("Preview:")
        for i,line in enumerate(splitted_score):
            print(splitted_score[i] + max(DASH_IN_LINE - list(line).count("-"), 0)*"-")

        if input("\nConfirm?(Y/n): ").lower() in ["yes", "y"]:
            for i,line in enumerate(splitted_score):
                splitted_score[i] += max(DASH_IN_LINE - list(line).count("-"), 0)*"-"
    except Exception as exc:
        print(f"Error: {exc}")
    finally:
        return '\n'.join(splitted_score)

def format_sectioned_score(score:str,sep="--"):
    sectioned_score = score.replace("\n","").replace(" ",'-').split("/")
    new_score = ""
    for idx, section in enumerate(sectioned_score):
        section_bucket = []
        bucket = ""
        for key in section:
            if bucket:
                bucket+=key
                if key == ")":
                    section_bucket.append(bucket)
                    bucket = ""
            elif key == "(":
                bucket+=key
            elif key == "-":
                section_bucket.append('')
            else:
                section_bucket.append(key)
        if len(section_bucket) <= 4:
            section_bucket += [''] * (5 - len(section_bucket))
        else:
            section_bucket += [''] * (9 - len(section_bucket))
            # 9 instead of 8 because we are using .join() later, will need an extra character

        cur_sec_score = sep.join(section_bucket)
        if idx % 2 == 1 and cur_sec_score[-1] == "-":
                new_score += cur_sec_score[:-1] + "\n"
        else:
            new_score += cur_sec_score
    return new_score


def format_score(score:str):
    if score.count("/") > reducLineBreak(score).count("\n"):
        new_score =  format_sectioned_score(score,sep="--")
    else:
        breaked_score = score.splitlines()
        for index, lines in enumerate(breaked_score):
            if "(" not in lines or "-" not in lines:
                lines = lines.replace("/", "")
                if "-" not in lines:
                    NEWLINE = (separate(lines.replace(" ", "-"), sep="---"))

                else:
                    NEWLINE = braket_wrap(lines)

                breaked_score[index] = NEWLINE

        new_score = "\n".join(breaked_score)
    if score != new_score:
        global pre_score, formatted
        with open(TestPaths.test_path, "w+") as f:
            pre_score.append(score)
            f.write(new_score)
            formatted = True
        return new_score
    return score


pre_score = []
formatted = False

def main(name="",test_score="",New=False):
    global pre_score, formatted

    test_dir = "genshin_assets\\test"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    now = time.time()
    for fname in os.listdir(test_dir):
        with open(os.path.join(test_dir,fname),"r") as f:
            content = str(f.read()).strip()
            if len(content) < 30 and not os.path.exists(content):
                trash = True
            else:
                trash = False

        TXT_ABSOLUTE = os.path.join(test_dir,fname)

        if trash or (now - os.stat(TXT_ABSOLUTE).st_mtime) > 2592000:  # modified date > one month from now
            if trash:
                print(f"  Recycled {fname}, you can find it back in recycle bin | {fname} is empty")
            else:
                print(f"  Recycled {fname}, you can find it back in recycle bin | {fname} isn't modified for a month")
            send2trash(os.path.join(test_dir, fname))

    TestPaths.test_path = "genshin_assets\\test\\test{}.txt".format("_" + name if name != "" else "")
    if New:
        i = 1
        while os.path.exists(TestPaths.test_path):
            TestPaths.test_path = f"genshin_assets\\test\\test_{i}.txt"
            i += 1
        else:
            print(f"  New test file created: test_{i-1}.txt")


    if not os.path.exists(TestPaths.test_path) or test_score != "":
        with open(TestPaths.test_path, "w+") as f:
            f.write(test_score)
    os.startfile(TestPaths.test_path)

    while not keyboard.is_pressed("p"):

        print("press k to play, p to end")
        while not keyboard.is_pressed("k"):
            if keyboard.is_pressed("p"):
                break
            if keyboard.is_pressed("a") and keyboard.is_pressed("shift") and keyboard.is_pressed("ctrl"):
                while keyboard.is_pressed("a"):
                    pass
                pre_score.append(test_score)
                test_score = animuz(read_test_txt())
                with open(TestPaths.test_path, "w+") as f:
                    f.write(test_score)
                os.startfile(TestPaths.test_path)
            if keyboard.is_pressed("s") and keyboard.is_pressed("n"):
                add_new_song_to_test()
            if keyboard.is_pressed("z") and keyboard.is_pressed("ctrl"):
                while keyboard.is_pressed("z"):
                    pass
                if pre_score != []:
                    test_score = pre_score[-1]
                    del pre_score[-1]
                    with open(TestPaths.test_path, "w+") as f:
                        f.write(test_score)

                    os.startfile(TestPaths.test_path)

            if keyboard.is_pressed("n") and keyboard.is_pressed("shift"):
                while keyboard.is_pressed("n"):
                    pass
                test_score = format_score(read_test_txt())
                formatted = False
                os.startfile(TestPaths.test_path)

        if keyboard.is_pressed("p"):
            break

        # the read here only renews test_score to newest version of txt
        if test_score != read_test_txt():
            pre_score.append(test_score)
            test_score = read_test_txt()

        test_score = format_score(test_score)
        # test
        test(test_score,waitForK=False)
        os.startfile(TestPaths.test_path)

    def add_to_saved():
        command = input("add to saved? (yes/no): ")
        if command == 'yes':
            command = input("name? ").lower()
            command = command if command!="" else "Atest_score"

            if os.path.exists("genshin_assets\\scores\\{}.txt".format(command)):
                confirm = input("File already exists, are you sure you want to override it? (yes/no): ")
                if confirm == 'yes':
                    save_to_scores(read_test_txt(), command)
                else:
                    return add_to_saved()
            else:
                save_to_scores(read_test_txt(), command)
            time.sleep(1)
            return command
        else:
            print("Exited test\n")
            return 0

    if __name__ == '__main__':
        return add_to_saved()
    else:
        return read_test_txt()

if __name__ == "__main__":
    while True:
        main(input("no? (empty for default): ").replace("\\", ""))
