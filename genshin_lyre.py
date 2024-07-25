import os
import sys

sys.path.append(os.path.dirname(__file__))


class Libs:
    py = sys.executable
    LIBS = {'pyautogui': f'{py} -m pip install pyautogui',
            'keyboard': f'{py} -m pip install keyboard',
            'send2trash': f'{py} -m pip install send2trash',
            'mido': f'{py} -m pip install mido',
            'tkinter': f'{py} -m pip install tk',
            'win32api': f'{py} -m pip install pywin32'}
    ToInstall = []


for libname in Libs.LIBS:
    try:
        __import__(libname)
    except ImportError as ine:
        Libs.ToInstall.append(libname)
        print(f"  {ine}")
if Libs.ToInstall:
    print("""It is highly recommended to install missing packages before running the app, Installing: {}""".format(
        '\n    '.join(Libs.ToInstall)))
    if input("Proceed? (Y/n): ").lower() in ["y", "yes"]:
        for libname in Libs.ToInstall:
            os.system(Libs.LIBS[libname])
    else:
        input("program refuse to operate with bugs (press enter)")
        exit()
try:
    from .user_input_control import *
except ImportError:
    from user_input_control import *
import pyautogui


def run():
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
    command = os.path.abspath(__file__)
    if not is_admin():
        run_as_admin(command)
        return
    safeloop()


if __name__ == "__main__":
    # main()
    run() # for debugging
