import pathlib
try:
    from ....classes import *
    from ....srcs import controller
    from ... import enter
except ImportError:
    from classes import *
    from srcs import controller
    import enter

def refresh_list():
    "ls, list"
    corresponding_path = {
        "test":Paths.test_path,
        "mid":Paths.mid_path,
        "txt":Paths.test_path,
        "scores": Paths.test_path,
        "nightly":Paths.nightly_path,
    }
    if "all" in enter:
        print("\n".join(list(Songs.songs)))
        return
    for keyword,file_path in corresponding_path.items():
        if keyword in enter:
            os.startfile(file_path)
            file_ext = Paths.file_type.get(file_path,"txt")
            all_songs_in_file = pathlib.Path(file_path).glob(f'*.{file_ext}')
            for song_path in all_songs_in_file:
                song_name = str(song_path).replace(f".{file_ext}", "").replace(file_path + "\\", "")
                print(song_name)
            print()
            break
    else:
        os.system('cls')
        controller.song_list.refresh()