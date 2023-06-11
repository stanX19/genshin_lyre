from srcs import *
from utils import *
from classes import *
import pathlib
#from collections import Counter
try:
    from .play_song import play_song
except ImportError:
    from play_song import play_song
try:
    import genshin_automation
except ImportError:
    class genshin_automation():
        @classmethod
        def macros(cls):
            print("genshin_automation.py is not found")


def user_input_control(enter=''):
    """execute various function via cmd, mainly playing songs in Songs.songs
    does not return any value"""
    loop = not enter  # no loop if specific command(enter) is given
    while loop:
        if loop:  # always true if no default enter is given
            enter = input("song name: ").lower()
        if enter != "":
            no_result = False
            integer_not_used = False

            if enter.isnumeric():
                if int(enter) <= len(Songs.songs):
                    play_song(int(enter) - 1)
                    print("{}".format(
                        'note: Speed is still set at {}x, enter new speed or enter \'reset\' to reset all variables\n'.format(
                            int(PlayVaria.speed)) if PlayVaria.speed != 1 else ''), end="")
                    continue  # you don't want the song to play twice, theres another player down there

            # convert names to index
            if "speed" not in enter:
                for song_name in sorted(list(Songs.songs.keys()), reverse=True):
                    if song_name in enter:
                        enter = enter.replace(song_name, f"{list(Songs.songs).index(song_name) + 1}")

            # ignore the number if it starts with '#'
            search_string = ' '.join([word for word in enter.split() if word[0] != '#'])
            no = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", search_string)

            # commands that dont need to deal with number, (can be used together with song index to play song)
            if "list" in enter or "ls" in enter:
                corresponding_path = {
                    "test":Paths.test_path,
                    "mid":Paths.mid_path,
                    "txt":Paths.test_path,
                    "scores": Paths.test_path,
                    "nightly":Paths.nightly_path,
                    "json": Paths.nightly_path,
                }
                if "all" in enter:
                    print("\n".join(list(Songs.songs)))
                    continue
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
                continue

            elif "reset" in enter:
                if "all" in enter:
                    print("  Resetting all users settings, inculding:")
                    for var in controller.settings.get_dict():
                        print(f"    | {var}")
                    if input("are you sure? (Y/n): ").lower() in ["yes", "y"]:
                        for key, val in Settings.backup.items():
                            setattr(Settings, key, val)
                        controller.settings.save()
                        print("  All settings resetted")
                else:
                    UserVaria.song_loop = False
                    PlayVaria.speed = 1
                    print("song loop turned off, Playback speed reset to 1")
            elif "help" in enter:
                if os.path.exists(Paths.help_path):
                    try:
                        with open(Paths.help_path, "r", encoding="utf-8") as f:
                            print(r"{}".format(f.read()))
                    except FileNotFoundError as exc:
                        print(f"An error occured while reading help.txt: {exc}")
                else:
                    print("Help.txt is missing")
                no_result = False
            elif 'record' in enter:
                with open('record.py', "r") as record:
                    exec(str(record))
            elif 'nightly' in enter:
                os.startfile(Paths.nightly_website)
            elif 'cls' == enter:
                os.system('cls')
            elif 'bright' in enter:
                os.system('color f0')
            elif 'dark' in enter:
                os.system('color 07')
            elif "clean" in enter:
                controller.export.clean()
            elif "sort" in enter or "by" in enter.split():
                if "date" in enter or "time" in enter:
                    if Settings.follow_order:
                        print("  Song list will now be sorted by date created")
                        Settings.follow_order = False
                        controller.song_list.refresh()
                    else:
                        print("  Song list is already sorted by date created")
                elif "order" in enter:
                    if not Settings.follow_order:
                        print("  Song list will now follow [order]")
                        Settings.follow_order = True
                else:
                    print("  Song list is sorted by{}".format("[order]" if Settings.follow_order else "date created"))
                controller.settings.save()

            # notification toggling
            elif "notif" == enter or 'notification' in enter or (
                    ("notif" in enter.split()) and ("on" in enter or "off" in enter)):
                if "on" in enter.split(" ") or enter.find("true") >= 0:
                    print("Turned notification on") if not Settings.notification else print(
                        "Notification is already activated")
                    Settings.notification = True
                elif "off" in enter or "false" in enter:
                    print("Turned notification off") if Settings.notification else print(
                        "Notification is already deactivated")
                    Settings.notification = False

                else:
                    print(
                        f"currently turned {'on' if Settings.notification else 'off'}, include 'on' or 'off' to toggle notification")
                controller.settings.save()

            elif "auto" == enter:
                prompt_control_function(genshin_automation.macros())
            # song_loop toggling
            elif "loop" in enter:

                if enter.find("off") >= 0 or enter.find("false") >= 0 or enter.find("no") >= 0 or enter.find(
                        "loop'") >= 0:
                    print("Turned song loop off, songs now wont loop automatically") if UserVaria.song_loop else print(
                        "song loop is already turned off")
                    UserVaria.song_loop = False
                else:
                    print(
                        "Turned song loop on, songs will now play continually without toggling") if not UserVaria.song_loop else print(
                        "song loop is already turned on")
                    UserVaria.song_loop = True

            elif enter.lower() == 'i':
                return False
            else:
                no_result = True

            # commands that need to deal with number
            if 'order' in enter:
                result = controller.order.edit(enter)
                if result == 0:
                    print("exited editing\n")
                else:
                    print()
                    controller.song_list.refresh()
                no_result = False

            elif "export" in enter:
                if no:
                    no = int(no[0]) - 1
                else:
                    index = input("Song index of song?: ")
                    no = get_song_index(index)
                if no is None:
                    continue
                try:
                    selected_song = list(Songs.songs.values())[no]
                    controller.export.export_as_nightly(selected_song)
                except IndexError:
                    print("Invalid index")
                continue

            elif 'stats' in enter or 'info' in enter or 'data' in enter:
                no_result = False
                if no:
                    no = int(no[0])-1
                else:
                    index = input("Song index of song?: ")
                    no = get_song_index(index)
                if no is None:
                    continue
                try:
                    print_stats(no)
                except IndexError:
                    print("Invalid index")
                continue

            elif "txt" in enter or "key" in enter or "score" in enter:
                no_result = False
                if no == []:
                    no = get_song_index(enter)  # returns int or None ONLY
                    if no is not None:
                        no = [str(no + 1)]
                    else:
                        temp = input("song name or song index? ")
                        no = get_song_index(temp)  # returns int or None ONLY
                        if no is None:
                            no_result = True
                            print("invalid song name or index :(\n")
                        else:
                            no = [str(no + 1)]

                if no != [] and not no_result:  # no_result is used here as a local variable
                    no = int(no[0])
                    if no <= len(Songs.songs):
                        selected_song = list(Songs.songs.values())[no - 1]
                        if isinstance(selected_song,old_music_score):
                            if type(selected_song) == old_music_score:
                                keys = [i for keys in selected_song.keys for i in [keys,"-"]]
                            else:
                                keys = selected_song.keys
                            raw_keys = score_list_to_score(key_list_to_score_list(keys))
                        else:
                            raw_keys = selected_song.score
                        if "raw" in enter:
                            pass
                        else:
                            spaced_key = "\n".join(
                                [i.replace("-", " ").strip() for i in raw_keys.splitlines()])
                            if "space" in enter:
                                raw_keys = spaced_key
                            else:
                                stripped_key = " ".join([i for i in spaced_key.split(" ") if i and "BEAT" not in i])
                                raw_keys = stripped_key
                                print("you can try: [space key] or [raw key]")

                        print(f"\n>>>{list(Songs.songs.keys())[no - 1].capitalize()}<<<")
                        print(raw_keys)

                        if 'txt' in enter:
                            if os.path.exists(f"{Paths.score_path}\\{list(Songs.songs.keys())[no - 1]}.txt"):
                                os.startfile(f"{Paths.score_path}\\{list(Songs.songs.keys())[no - 1]}.txt")
                            else:
                                if input(f"'{list(Songs.songs.keys())[no - 1]}' is a midi file, start anyways? (Y/n): ").lower() in ["yes", 'y']:
                                    os.startfile(f"{Paths.mid_path}\\{list(Songs.songs.keys())[no - 1]}.mid")
                    else:
                        print(f"""    song index is out of range, maximum index is {len(Songs.songs)}""")

                no_result = False

            elif 'midi' in enter:
                if 'new' in enter:
                    new_midi()
                else:
                    print("Did you mean [midi list]?")
                no_result = False

            elif "test" in enter or 'new' in enter or "edit" in enter:
                NEW = True  # if not 'test' in enter / if 'new' in enter or 'edit' in enter

                if no != [] and int(no[0]) <= len(Songs.songs.keys()) and "edit" in enter:
                    selected_song = list(Songs.songs.values())[int(no[0]) - 1]
                    NAME = no[0]
                    TEST_SCORE = selected_song.score
                    if type(selected_song) == old_music_score:
                        TEST_SCORE = "-".join(selected_song.raw_key_list)

                    print("switched to test session, any changes here wont affect the original song")
                    print(
                        "if you want to access this test score again, just enter 'test' followed by its file number to open it\n")
                else:
                    if "test" in enter:
                        NAME = enter.replace("test", "").strip()
                        NEW = False
                    else:
                        NAME = ""
                    TEST_SCORE = ""
                test_session(NAME, TEST_SCORE, NEW)
                no_result = False

            elif 'set' in enter.split():
                set_settings(enter)
                no_result = False

            elif "rename" in enter:
                if rename_song(enter) != 0:
                    controller.song_list.refresh()
                no_result = False

            # Playback speed
            elif "speed" in enter:
                if no:  # != []:
                    gained_integer = min(float(no[0]),10.0)
                    PlayVaria.speed = gained_integer
                    print(f"Playback speed set to {gained_integer}x")
                else:
                    print(f"speed is currently set to {PlayVaria.speed}x,\
                     include a amplifier e.g. '1.5x' for 1.5 times faster to change the speed")
                no_result = False

            # score deleter
            elif "delete" in enter or "rm" in enter.split():
                # no = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", enter)
                if no:
                    delete_score(*no)
                else:
                    target = input("Score name or integer: ")
                    no = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", target)
                    best_match = user_input_best_match(enter, Songs.songs,
                                                       Settings.search_max_missing,
                                                       Settings.search_break_weight_ratio)
                    if best_match:
                        delete_score(list(Songs.songs).index(target) + 1)
                    elif no:
                        delete_score(*no)
                    else:
                        print("invalid input")
                no_result = False

            # all the above didn't use the integer inputted
            else:
                integer_not_used = True

            # try to find song_no from unused command
            song_no = None
            if integer_not_used and no and '.' not in no[0] and int(no[0]) <= len(Songs.songs):
                song_no = int(no[0]) - 1

            elif enter in Songs.songs:
                song_no = list(Songs.songs.keys()).index(enter)

            elif no_result and len(enter) >= 2:
                # change short form to song name
                best_match = user_input_best_match(enter, Songs.songs,
                                                   Settings.search_max_missing,
                                                   Settings.search_break_weight_ratio)
                if best_match:
                    song_no = list(Songs.songs.keys()).index(best_match)

            if song_no is not None:
                PlayVaria.song_index = 0
                play_song(song_no)
                if PlayVaria.speed != 1:
                    print(f'note: Playback speed is still turned on, set at {PlayVaria.speed}x,\
enter new speed or enter \'reset\' to reset all variables\n', end="")

            elif no_result:
                print("key not found, enter 'i' to exit")
