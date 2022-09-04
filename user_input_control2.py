from srcs import *
from utils import *
from classes import *
try:
    from .play_song import play_song
    from .user_control_functions import enter, process
except ImportError:
    from play_song import play_song
    from user_control_functions import enter, process
try:
    import genshin_automation
except ImportError:
    class genshin_automation():
        @classmethod
        def macros(cls):
            print("genshin_automation.py is not found")


def user_input_control(__enter__=''):
    """execute various function via cmd, mainly playing songs in Songs.songs
    does not return any value"""
    global enter
    loop = not __enter__  # no loop if specific command(enter) is given
    while loop:
        no_result = False
        if loop:  # always true if no default enter is given
            enter.set_raw(input("song name: ").lower())
        else:
            enter.set_raw(__enter__)
        if not enter.raw:
            continue
        if enter.isnumeric:
            if int(enter) <= len(Songs.songs):
                play_song(int(enter) - 1)
                print("{}".format(
                    'note: Speed is still set at {}x, enter new speed or enter \'reset\' to reset all variables\n'.format(
                        int(PlayVaria.speed)) if PlayVaria.speed != 1 else ''), end="")
                continue  # you don't want the song to play twice, theres another player down there

        # convert names to index
        # if "speed" not in enter:
        #     for i, e in enumerate(list(Songs.songs.keys())):
        #         if e in enter:
        #             enter = enter.replace(e, str(i + 1))
        #             enter.no = [str(i + 1)]
        #             break

        # commands that dont need to deal with number, (can be used together with song index to play song)


        elif enter.lower() == 'i':
            return False
        else:
            no_result = True
#did until here

        elif "rename" in enter:
            if rename_song(enter) != 0:
                controller.song_list.refresh()
            no_result = False

        # Playback speed
        elif "speed" in enter:
            if enter.no:  # != []:
                gained_integer = min(float(enter.no[0]),10.0)
                PlayVaria.speed = gained_integer
                print(f"Playback speed set to {gained_integer}x")
            else:
                print(f"speed is currently set to {PlayVaria.speed}x,\
                 include a amplifier e.g. '1.5x' for 1.5 times faster to change the speed")
            no_result = False

        # score deleter
        elif "delete" in enter or "rm" in enter.split():
            # no = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", enter)
            if enter.no != []:
                if float(enter.no[0]) <= len(Songs.songs) and float(enter.no[0]).is_integer():
                    target = list(Songs.songs.keys())[int(enter.no[0]) - 1]
                    delete_score(target)
                else:
                    print("Invalid integer")
            else:
                target = input("Score name or integer: ")
                enter.no = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", target)
                if target in list(Songs.songs.keys()):
                    delete_score(target)
                    controller.song_list.refresh()
                elif enter.no != []:
                    if float(enter.no[0]) <= len(Songs.songs) and float(enter.no[0]).is_integer():
                        target = list(Songs.songs.keys())[int(enter.no[0]) - 1]
                        delete_score(target)
                else:
                    print("invalid input")
            no_result = False

        elif enter.no != [] and "." not in enter.no[0] and int(enter.no[0]) <= len(Songs.songs):
            enter = list(Songs.songs.keys())[
                int(enter.no[0]) - 1]

        elif not enter in Songs.songs and len(enter) >= 2:  # if all above 'elif' cannot match song name
            # change short form to song name
            words_name = {}
            words = enter
            for names in list(Songs.songs.keys()):
                if words in names.split(" "):
                    words_name[names.find(words)] = names
                elif words in names:
                    words_name[names.find(words) + 1] = names

            if words_name != {}:
                enter = words_name[min(words_name.keys())]

        if enter in Songs.songs:
            PlayVaria.song_index = 0
            play_song(list(Songs.songs.keys()).index(enter))  # output (index of song)
            print("{}".format(
                'note: Playback speed is still turned on, set at {}x, enter new speed or enter \'reset\' to reset all variables\n'.format(
                    int(PlayVaria.speed)) if PlayVaria.speed != 1 else ''), end="")

        elif no_result:
            no_result = False
            print("key not found, enter 'i' to exit")