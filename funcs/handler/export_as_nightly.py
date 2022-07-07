try:
    from ...classes import *
    from ...utils import *
except ImportError:
    from classes import *
    from utils import *
from send2trash import send2trash

def export_as_nightly(song=None,score='',name=''):
    if not score or not name:
        if isinstance(song, old_music_score):
            if type(song) == old_music_score:
                key_list = [key for key_ in song.keys for key in [key_,"-"]]
            else:
                key_list = song.keys
            score = key_list_to_score_list(key_list)
        elif type(song) in [Midi, Nightly]:
            score = song.score_list
        else:
            print("current song is not supported for exporting")
            return 1
        name = song.name
    try:
        jsonfile = score_list_to_nightly(score,name)
        file_name = f"{name}.genshinsheet.json"
        Paths.export_paths.append(os.path.join(Paths.desktop_path, file_name))
        with open(Paths.export_paths[-1], "w+") as f:
            f.write(jsonfile)
            print(f"Exported {name} as '{file_name}' at {Paths.export_paths[-1]}\n    you can find or delete it on the desktop")
            print("Upload the file at: https://specy.github.io/genshinMusic/#/")
            print("    Use [nightly] command as a shortcut to this page")
            print("    follow player -> songs -> import song and you can select the exported file")
    except Exception as exc:
        print(f"Error: {exc}")

def clean_exported():
    if not Paths.export_paths:
        print("    no exported files to be cleaned")
        return
    for path in Paths.export_paths:
        send2trash(path)
        print(f"    deleted: {path}")
    Paths.export_paths = []