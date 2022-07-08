import os
import shutil
try:
    from ..handler import print_song_list
    import test_session
    from ...classes import *
    from ...utils import *
except ImportError:
    from handler import print_song_list
    import test_session
    from classes import *
    from utils import *

test_session = test_session.test_session
def new_nightly(nightly_path=""):
    if not nightly_path:
        nightly_path = fileopenbox().strip().lower()
    if not nightly_path:
        print("  Cancelled")
        return 0
    if not os.path.exists(nightly_path):
        print("  Invalid path")
        return 0
    try:
        new_nightly = Nightly(nightly_path)
        name = nightly_path.replace("/", "\\").split("\\")[-1].replace(".genshinsheet.json", "")
        print(f"File found: '{nightly_path}'")
        print("  Processing complete, ", end='')
        print("Saving permanently json file...")

        if name in Songs.songs:
            nightly_name = unique_name(f"{Paths.nightly_path}\\{name}", "json")
            name = nightly_name.replace("/", "\\").split("\\")[-1].replace(".json", "")
            # run through txt file for dupes
            txt_name = unique_name(f"{Paths.score_path}\\{name}", "txt")
            name = txt_name.replace("/", "\\").split("\\")[-1].replace(".txt", "")
            # run through mid file for dupes
            txt_name = unique_name(f"{Paths.mid_path}\\{name}", "mid")
            name = txt_name.replace("/", "\\").split("\\")[-1].replace(".mid", "")
            # now name is confirmed to be not a dupe
        dest_nightly_path = f"{Paths.nightly_path}\\{name}.json"

        if input("Proceed? (Y/n): ").lower() in ["y", "yes"]:
            shutil.copy2(nightly_path,dest_nightly_path)
            print(f"Saved in {Paths.score_path}\n  Ready to play")
        else:
            print("  Cancelled saving")
            print("nightly file will be temporarily added to the song list")
        new_nightly.name = name
        Songs.songs[name] = new_nightly
        print_song_list()
    except Exception as exc:
        print(f"  Error: {exc}")
    return 1

def new_midi():
    midi_path = fileopenbox().strip().lower()
    if midi_path.endswith(".json"):
        return new_nightly(midi_path)
    if not midi_path:
        print("  Cancelled")
        return 0
    if not os.path.exists(midi_path):
        print("  Invalid path")
        return 0
    try:
        new_midi = Midi(midi_path)
        name = midi_path.replace("/", "\\").split("\\")[-1].replace(".mid", "")
        print(f"File found: '{midi_path}'")
        lowest_sharp, total_key = new_midi.tune_to_C()
        percentage = round(lowest_sharp / total_key * 100, 1)
        print("  Processing complete, ", end='')
        if lowest_sharp > 0:
            print(f"lowest sharp is {lowest_sharp} out of {total_key} keys",end='')
            if percentage>0:
                print(f" -{percentage}%-, score may sound weird")
        else:
            print("no sharps found, midi is tuned to C")
        print("  Saving permanently as midi...")

        if name in Songs.songs:
            midi_name = unique_name(f"{Paths.mid_path}\\{name}", "mid")
            name = midi_name.replace("/", "\\").split("\\")[-1].replace(".mid", "")
            # run through midi file for dupes
            txt_name = unique_name(f"{Paths.score_path}\\{name}", "txt")
            name = txt_name.replace("/", "\\").split("\\")[-1].replace(".txt", "")
            # run through json file for dupes
            txt_name = unique_name(f"{Paths.nightly_path}\\{name}", "json")
            name = txt_name.replace("/", "\\").split("\\")[-1].replace(".json", "")
            # now name is confirmed to be not a dupe

        dest_midi_path = f"{Paths.mid_path}\\{name}.mid"

        if input("Proceed? (Y/n): ").lower() in ["y", "yes"]:
            shutil.copy2(midi_path,dest_midi_path)
            print(f"Saved in {Paths.score_path}\n  Ready to play")
        else:
            print("  Cancelled saving")
            print("Edit and save as test score instead? ",end='')
            if input("(Y/n): ").lower() in ["y", "yes"]:
                return test_session(score=new_midi.raw_keys, new=True)
            print("  Midi file will be temporarily added to the song list")
        new_midi.name = name
        Songs.songs[name] = new_midi
        print_song_list()
    except Exception as exc:
        print(f"  Error: {exc}")
    return 1