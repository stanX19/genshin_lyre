try:
    from .user_input_control import *
except ImportError:
    from user_input_control import *
import os

class Libs:
    LIBS = {'pyautogui': 'py -m pip install pyautogui',
            'keyboard': 'py -m pip install keyboard',
            'send2trash': 'py -m pip install send2trash',
            'mido': 'py -m pip install mido'}
    ToInstall = []

for libname in Libs.LIBS:
    try:
        __import__(libname)
    except ImportError as ine:
        Libs.ToInstall.append(libname)
        print(f"  {ine}")
if Libs.ToInstall:
    print("""It is highly recommended to install missing packages before running the app, Installing: """.format(
        '\n    '.join(Libs.ToInstall)))
    if input("Proceed? (Y/n): ").lower() in ["y", "yes"]:
        for libname in Libs.ToInstall:
            os.system(Libs.LIBS[libname])
    else:
        input("program refuse to operate with bugs (press enter)")
        exit()

from mido import MidiFile
import pyautogui
import tkinter as tk
import keyboard
from send2trash import send2trash

def run():
    # with this moving mouse to corner wont activate failsafe
    # but you will need be very careful with pyautogui
    pyautogui.FAILSAFE = Settings.pyautoguiFAILSAFE
    # reset variables
    UserVaria.song_loop = False
    PlayVaria.speed = 1

    # take scores from /scores directory
    os.chdir(Paths.self_path)
    # must read settings first
    controller.settings.read()
    controller.song_list.refresh()
    # temporary test
    # end of temp test
    if Settings.notification:
        try:
            notify("testing...\nscript ready")
        except Exception:
            Settings.notification = False

    if PlayVaria.warnings:
        print_cmd_color("Darkyellow", "\n".join(PlayVaria.warnings))
    print("enter song key to play, enter 'help' for details, enter 'i' to exit")
    return user_input_control()

def safeloop():
    while True:
        try:
            run()
            break
        except Exception as exc:
            print_cmd_color("darkYellow", f"\nError due to: {exc}\n")
            time.sleep(1)
            print("restarting program...")
            time.sleep(1)

def main():
    initiating_caller(target=safeloop)

if __name__ == "__main__":
    main()