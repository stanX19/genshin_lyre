try:
    from ...classes import Paths, Songs
    from ...srcs import controller
except ImportError:
    from classes import Paths, Songs
    import controller
from send2trash import send2trash
import os


def delete_score(*targets: int):
    for idx in targets:
        if float(idx).is_integer() and float(idx) <= len(Songs.songs):
            target = list(Songs.songs.keys())[int(idx) - 1]
        else:
            print(f"Invalid index: {idx}")
            continue
        for file_dir, ext in Paths.file_type.items():
            if os.path.exists(rf"{file_dir}\{target}.{ext}"):
                target_path = rf"{file_dir}\{target}.{ext}"
                break
        else:
            print("file was not saved in genshin_lyre")
            continue
        lock = input(f"are you sure you want to delete {target}? [Y/n]: ")
        if lock.lower() == 'y':
            send2trash(target_path)
            if target in Songs.songs_order:
                Songs.songs_order.pop(Songs.songs_order.index(target))
            print(f"{target} has been moved to recycle bin\n")
        else:
            print("Delete canceled")
    controller.order.sync()
    controller.song_list.refresh()
