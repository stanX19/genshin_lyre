try:
    from ...classes import *
except ImportError:
    from classes import *
import controller
import song_editor
from send2trash import send2trash


def test_session(name="", score="", new=False):
    test_score = song_editor.main(name, score, new)
    while input("add to saved? (yes/no): ") == 'yes':
        name = input("name? ").lower()
        name = name if name != "" else "Atest_score"
        if name in Songs.songs:
            confirm = input("File already exists, are you sure you want to override it? (yes/no): ")
            if confirm != 'yes':
                continue
            else:
                for file_dir, ext in Paths.file_type.items():
                    if os.path.exists(rf"{file_dir}\{name}.{ext}"):
                        send2trash(rf"{Paths.self_path}\{file_dir}\{name}.{ext}")
        with open(f"{Paths.score_path}\\{name}.txt", "w+") as f:
                f.write(test_score)
        print(f"Saved in {Paths.self_path}\\{Paths.score_path}")
        time.sleep(1)
        break
    else:
        print("Exited test\n")
        return 0

    Songs.songs_order = controller.order.read()
    if not (name in Songs.songs_order):
        if input("do you want to add this song to order? (Y/N): ").lower() in ['y', 'yes', 'confirm']:
            controller.song_list.print()
            print()
            if controller.order.edit("add to order", name) == 0:
                print("cancelled order editing")
    controller.song_list.refresh()