try:
    from ....srcs import *
    from ....classes import *
    from ....play_song import play_song
    from ... import enter
except ImportError:
    from srcs import *
    from classes import *
    from play_song import play_song
    import enter
try:
    import genshin_automation
except ImportError:
    class genshin_automation():
        @classmethod
        def macros(cls):
            print("genshin_automation.py is not found")

def reset():
    """reset"""
    if "all" in enter.split:
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

def print_help():
    """help"""
    if os.path.exists(Paths.help_path):
        try:
            with open(Paths.help_path, "r", encoding="utf-8") as f:
                print(r"{}".format(f.read()))
        except FileNotFoundError as exc:
            print(f"An error occured while reading help.txt: {exc}")
    else:
        print("Help.txt is missing")

def nightly():
    """nightly"""
    os.startfile(Paths.nightly_website)

def cls():
    """cls"""
    os.system('cls')
def bright():
    """bright, light"""
    os.system('color f0')
def dark():
    """dark"""
    os.system('color 07')
def clean():
    """clean"""
    controller.export.clean()

def list_sort_by():
    """sort"""
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

def notif():
    if not ("notif" == enter or 'notification' in enter or (
        ("notif" in enter.split()) and ("on" in enter or "off" in enter))
            ):
        return 0
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
    return 1

def auto():
    """auto"""
    prompt_control_function(genshin_automation.macros())

def loop():
    """loop"""
    if "off" in enter.split or "false" in enter.split\
            or "no" in enter.split:
        print("Turned song loop off, songs now wont loop automatically") if UserVaria.song_loop else print(
            "song loop is already turned off")
        UserVaria.song_loop = False
    else:
        print(
            "Turned song loop on, songs will now play continually without toggling") if not UserVaria.song_loop else print(
            "song loop is already turned on")
        UserVaria.song_loop = True

def change_settings():
    """set"""
    set_settings(enter.raw)