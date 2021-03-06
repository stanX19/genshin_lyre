try:
    from ...classes import Paths, Songs
    import controller
except ImportError:
    from classes import Paths, Songs
    import controller
from send2trash import send2trash
import os

def delete_score(target):
    for file_dir, ext in Paths.file_type.items():
        if os.path.exists(rf"{file_dir}\{target}.{ext}"):
            target_path = rf"{file_dir}\{target}.{ext}"
            break
    else:
        target_path = None
    lock = input(f"are you sure you want to delete {target}? [Y/n]: ")
    if lock.lower() == 'y':
        if target_path:
            send2trash(target_path)
        Songs.songs.pop(target)
        if target in Songs.songs_order:
            Songs.songs_order.pop(Songs.songs_order.index(target))
            controller.order.sync()
        print(f"{target} has been moved to recycle bin\n")
        controller.song_list.print()
    else:
        print("canceled deletion")