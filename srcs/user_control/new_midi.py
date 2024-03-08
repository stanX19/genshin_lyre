import itertools
import os
import shutil
import Paths
import utils

try:
    import controller
    import test_session
    from ...classes import *
    from ...utils import *
    from .process_video import save_video_as_nightly
except ImportError:
    import controller
    import test_session
    from classes import *
    from utils import *
    from process_video import save_video_as_nightly

test_session = test_session.test_session


def unique_name_in_all(name):
    name = name.lower().strip()
    c = itertools.count()

    if name not in Songs.songs:
        return name
    for dir_path, ext in Paths.file_type.items():
        while os.path.exists(f"{dir_path}/{name}.{ext}"):
            name = f"{name} ({next(c)})"
    return name


def import_nightly(nightly_path, quiet=False):
    try:
        new_nightly = Nightly(nightly_path)
        name = nightly_path.replace("/", "\\").split("\\")[-1].replace(".json", "").replace(".genshinsheet","").lower()
        print(f"File found: '{nightly_path}'")
        print("  Processing complete, Saving permanently as json file...")

        name = unique_name_in_all(name)
        dest_nightly_path = f"{Paths.nightly_path}\\{name}.json"

        if quiet or input("Proceed? (Y/n): ").lower() in ["y", "yes"]:
            shutil.copy2(nightly_path, dest_nightly_path)
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
        name = midi_path.replace("/", "\\").split("\\")[-1].replace(".mid", "").lower()
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

        name = unique_name_in_all(name)
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
    elif path.endswith(".mid"):
        import_midi(path, quiet)
    elif path.endswith(".mp4"):
        save_video_as_nightly(Paths.nightly_path, [path])
    elif not quiet:
        print(f"Invalid file type: {path}; Expected type .json .mid or .mp4")


def new_midi():
    paths = fileopenbox(title="Open", msg="Select files to be imported", default=Paths.downloads_path+"\\", multiple=True)
    if not paths:
        print("  Cancelled")
        return 0
    if len(paths) == 1:
        midi_or_nightly(paths[0])
        controller.song_list.print()
        return

    for path in paths:
        midi_or_nightly(path, quiet=True)
        print()
    return 0
