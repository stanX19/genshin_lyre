try:
    from ...utils import *
    from ...classes import *
    import controller
    from send2trash import send2trash
except ImportError:
    from utils import *
    from classes import *
    import controller
    from send2trash import send2trash

def rename_song(command):
    no = first_int(command)
    if no != None:
        no = no - 1
    else:
        try:
            no = int(input("index of song? ")) - 1
        except ValueError:
            return
    while True:
        if int(no) >= len(Songs.songs):
            print('invalid index')
            return 0
        original_name = list(Songs.songs.keys())[no]
        new_name = input(f"New name for {original_name} (None to cancel): ").lower()

        if new_name == original_name or new_name.lower() in ["none", ""]:
            break

        for file_dir,ext in Paths.file_type.items():
            # loop through possible original path
            original_path = rf"{file_dir}\{original_name}.{ext}"
            if os.path.exists(original_path):
                new_name_path = rf"{file_dir}\{new_name}.{ext}"
                break
        else:  # this file is not saved in the first place
            if new_name not in Songs.songs:
                Songs.songs[new_name] = Songs.songs[original_name]
                del Songs.songs[original_name]
                print(f"Temporary: '{original_name}' --> '{new_name}'\n")
                controller.song_list.print()
            else:
                print(f"New name already existed, plus this file is not saved in the first place\nCancelled renaming")
                break
            return 0

        # this now here only deals with a saved file
        if new_name in Songs.songs:
            for file_dir, ext in Paths.file_type.items():
                dupe_path = rf"{file_dir}\{new_name}.{ext}"
                if os.path.exists(dupe_path):
                    # delete duplicate (with confirmation)
                    if input("New file name already exists, overwrite? (Y/n): ") in ['y', 'yes']:
                        send2trash(dupe_path)
                        print(f"  Moved {dupe_path} to recycle bin")
                        command = 'y'
                    else:
                        command = "n"
                    break
        else:
            command = input("Renaming '{}' to '{}', confirm? (Y/n): ".format(original_name, new_name)).lower().strip()

        if command == 'y':
            os.chdir(Paths.self_path)
            try:
                os.rename(original_path, new_name_path)
            except FileNotFoundError as exc:
                if not os.path.exists(new_name_path):
                    print("  Renaming failed, just restart the app and try again")
                    break
                else:
                    raise exc

            if original_name in Songs.songs_order:
                index = Songs.songs_order.index(original_name)
                Songs.songs_order[index] = new_name
                controller.order.write(Songs.songs_order)

            print(f"Success: '{original_name}' --> '{new_name}'\n")
            return 1
    print("cancelled renaming")
    return 0