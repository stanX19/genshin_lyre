try:
    from ...classes import *
    from ...utils import print_cmd_color
    from ...utils.print_functions import print_rows as print_list
except ImportError:
    from classes import *
    from utils import print_cmd_color
    from utils.print_functions import print_rows as print_list
from rdwr_order import read_order
import pathlib
import re


def read_txt_scores():
    """reads through midi folder, txt folder, nightly folder
    and redefine Songs.songs"""
    Songs.songs = {}
    # local variable to be used
    all_types = {}
    missing_txt = []
    Songs.songs_order = read_order()
    # loop through all file storing the scores
    # end is the file format stored in each file, set at Paths.file_type
    for file_dir, ext in Paths.file_type.items():
        all_songs_in_file = pathlib.Path(file_dir).glob(f'*.{ext}')
        for song_path in all_songs_in_file:
            song_name = str(song_path).replace(f".{ext}", "").replace(file_dir + "\\", "").lower()
            all_types[song_name] = str(song_path)

    # sort by time created
    all_txt = [name for name,path in sorted(all_types.items(), key= lambda f: os.path.getmtime( f[1] ))]
    if not Songs.songs_order:
        PlayVaria.warnings.append(
            "Scores_order.txt is not found, songs will be sorted by name" +
            "You can create new scores_order.txt by using [order] command")

    # please make sure names in scores_order.txt is exactly same as names used by txt file
    # example 'AOT call of silence' must be named 'AOT call of silence.txt'
    if Settings.follow_order:
        all_txt = list(dict.fromkeys(Songs.songs_order + all_txt))  # kill repeated
    for txt_file in all_txt:
        if txt_file == "":
            continue
        if os.path.exists(f"{Paths.score_path}\\{txt_file}.txt"):
            with open(f"{Paths.score_path}\\{txt_file}.txt", encoding="utf-8") as f:
                raw_score = f.read()
                raw_beat = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", raw_score)
                raw_beat = float(raw_beat[0]) if raw_beat != [] else 0.15
                # old and new music_score have difference, but all new scores from now uses new
                if "old_music_score" in raw_score:
                    raw_score = str(raw_score).replace("old_music_score", "").strip()
                    old_music_score(raw_score, beat=raw_beat, name=txt_file)
                else:
                    music_score(raw_score, beat=raw_beat, name=txt_file)
                # music score and old music score automatically appends itself to songs.songs
        elif os.path.exists(f"{Paths.mid_path}\\{txt_file}.mid"):
            midi_path = f"{Paths.mid_path}\\{txt_file}.mid"
            try:
                midi_file = Midi(midi_path)
                midi_file.name = txt_file
                Songs.songs[txt_file] = midi_file
            except ValueError as exc:
                print_cmd_color(f"DarkYellow", f"""Error: {exc}""")
            except Exception as exc:
                print_cmd_color(f"DarkYellow", f"""Error: {exc}
            This midi file may not be suitable for windstrong lyre""")
        elif os.path.exists(f"{Paths.nightly_path}\\{txt_file}.json"):
            nightly_path = f"{Paths.nightly_path}\\{txt_file}.json"
            try:
                nightly_file = Nightly(nightly_path)
                nightly_file.name = txt_file
                Songs.songs[txt_file] = nightly_file
            except Exception as exc:
                print_cmd_color(f"DarkYellow", f"""Error: {exc}""")
        else:
            missing_txt.append(f"'{txt_file}'")

    # inform missing txt
    if missing_txt: PlayVaria.warnings.append(
        ", ".join(missing_txt) + f" is missing from {Paths.score_path}, please confirm")

def print_song_list():
    print_list(list(Songs.songs.keys()), "Song List", max_length=Settings.name_max_length)

def refresh_song_list():
    read_txt_scores()
    print_song_list()