import os
import shutil
try:
    import controller
    import test_session
    from ...classes import *
    from ...utils import *
except ImportError:
    import controller
    import test_session
    from classes import *
    from utils import *

test_session = test_session.test_session
def import_nightly(nightly_path, quiet=False):
    try:
        new_nightly = Nightly(nightly_path)
        name = nightly_path.replace("/", "\\").split("\\")[-1].replace(".json", "").replace(".genshinsheet","")
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

        if quiet or input("Proceed? (Y/n): ").lower() in ["y", "yes"]:
            shutil.copy2(nightly_path,dest_nightly_path)
            print(f"Saved in {Paths.nightly_path}")
        else:
            print("  Cancelled saving")
            print("nightly file will be temporarily added to the song list")
        new_nightly.name = name
        Songs.songs[name] = new_nightly
    except Exception as exc:
        print(f"  Error: {exc}")
    return 1

def import_midi(midi_path, quiet=False):
    try:
        new_midi = Midi(midi_path)
        name = midi_path.replace("/", "\\").split("\\")[-1].replace(".mid", "")
        print(f"File found: '{midi_path}'")
        lowest_sharp, total_key = new_midi.tune_to_c()
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

        if quiet or input("Proceed? (Y/n): ").lower() in ["y", "yes"]:
            shutil.copy2(midi_path,dest_midi_path)
            print(f"Saved in {Paths.score_path}")
        else:
            print("  Cancelled saving")
            print("Edit and save as test score instead? ",end='')
            if input("(Y/n): ").lower() in ["y", "yes"]:
                return test_session(score=new_midi.raw_keys, new=True)
            print("  Midi file will be temporarily added to the song list")
        new_midi.name = name
        Songs.songs[name] = new_midi
    except Exception as exc:
        print(f"  Error: {exc}")


def midi_or_nightly(path, quiet=False):
    if not os.path.exists(path):
        print(f"  Invalid path: {path}")
        return 0
    if path.endswith(".json"):
        import_nightly(path, quiet)
    else:
        import_midi(path, quiet)


def new_midi():
    paths = fileopenbox(title="Open", msg="Select files to be imported", default=Paths.desktop_path+'\\\\', multiple=True)
    if not paths:
        print("  Cancelled")
        return 0
    if len(paths) == 1:
        midi_or_nightly(paths[0])
        return

    for path in paths:
        midi_or_nightly(path, quiet=True)
        print()
    return 0