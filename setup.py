import os

print("===============Genshin Lyre Setup================\ndownloading dependencies, this process may take awhile...")
os.system("py -m pip install --upgrade pip")
os.system("py -m pip install wheel")
os.system("py -m pip install pypiwin32")
os.system("py -m pip install -r requirements.txt")

import shutil, time
from pathlib import Path
from utils import get_system_path, CSIDL_List


def print_cmd_color(color="cyan", text="text"):
    format = f"powershell write-host -fore {color} "
    text = text.replace("(", "[").replace(")", "]").replace(";", ".")
    for i in text.split("\n"):
        if os.system(format + i):
            raise OSError("failed to call powershell")


if "PycharmProjects" in os.path.realpath(__file__):
    print_cmd_color("DarkRed", "Stop Right There!")
    if input("dude are you serius? this is your whole fking pycharm file! [execute]: ").lower() == "execute":
        print("continuing...")
    else:
        print("exit")
        exit()
try:
    print_cmd_color("darkYellow", "started setting up. do not close this program...")
except OSError:
    print("started setting up, do not close this program...")


    def print_cmd_color(color="cyan", text="text"):
        print(text)

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = Path(current_path).parent.absolute()
destination_path = os.path.join(os.path.expanduser("~"), "genshin_lyre")

# if this is an update
if os.path.exists(destination_path) and str(parent_path) != str(destination_path):
    print(f"\n       original file found at {destination_path}")
    print("\n       handling user created score (existing score)... ")
    user_scores_path = os.path.join(destination_path, "app\\genshin_assets\\scores")
    user_midi_path = os.path.join(destination_path, "app\\genshin_assets\\midi")
    user_nightly_path = os.path.join(destination_path, "app\\genshin_assets\\nightly")

    imported_midi = os.listdir(os.path.join(current_path, "genshin_assets\\midi"))
    imported_scores = os.listdir(os.path.join(current_path, "genshin_assets\\scores"))
    imported_nightly = os.listdir(os.path.join(current_path, "genshin_assets\\nightly"))

    # if user created scores
    if os.path.exists(user_scores_path) or os.path.exists(user_midi_path) or os.path.exists(user_nightly_path):
        # ask if want to overwrite songs with same name
        overwrite = input(
            """\n         do you want to replace the old scores with the newest version? (highly recommended if you didnt edit the old scores)
             The scores you created will be preserved (Y/n): """
        ).lower() in ["y", "yes"]
        print('\n')

        try:
            if overwrite:
                user_created_score = [os.path.join(user_scores_path, f) for f in os.listdir(user_scores_path) if
                                      f not in imported_scores]
                user_created_nightly = [os.path.join(user_nightly_path, f) for f in os.listdir(user_nightly_path) if
                                        f not in imported_nightly]
                user_created_midi = [os.path.join(user_midi_path, f) for f in os.listdir(user_midi_path) if
                                     f not in imported_midi]
            else:
                user_created_score = [os.path.join(user_scores_path, f) for f in os.listdir(user_scores_path)]
                user_created_nightly = [os.path.join(user_nightly_path, f) for f in os.listdir(user_nightly_path)]
                user_created_midi = [os.path.join(user_midi_path, f) for f in os.listdir(user_midi_path)]

            imported_score_path = os.path.join(current_path, "genshin_assets\\scores")
            imported_nightly_path = os.path.join(current_path, "genshin_assets\\nightly")
            imported_midi_path = os.path.join(current_path, "genshin_assets\\midi")


            # there is scores that is created by user
            def replace_files(src_files: list, dst_path):
                for file_path in src_files:
                    file_name = file_path[file_path.find("\\"):]
                    shutil.move(file_path, os.path.join(dst_path, file_name))


            if user_created_score:
                print("Adding existing scores to new scores list... ")
                replace_files(user_created_score, imported_score_path)
                print_cmd_color("White", "... successfully moved all existing scores to new scores list\n")

            if user_created_nightly:
                print("Adding existing nightly scores to new nightly list... ")
                replace_files(user_created_nightly, imported_nightly_path)
                print_cmd_color("White", "... successfully moved all existing nightly scores to new nightly list\n")

            if user_created_midi:
                print("Adding existing midi to new midi list... ")
                replace_files(user_created_midi, imported_midi_path)
                print_cmd_color("White", "... successfully moved all existing midi to new midi list\n")

        except Exception as exc:
            print(f"Failed to move existing scores to new scores list due to: {exc}")
            input("Are you sure you want to continue? you may lose the score forever (press enter)")

    else:
        print_cmd_color("white", "no user created scores found, proceeding to the next step")

    # moving user created test file (preserve)
    user_test_path = os.path.join(destination_path, "app\\genshin_assets\\test")
    imported_tests = os.path.join(current_path, "genshin_assets\\test")
    print("saving user created test files")
    for i in range(5):
        try:
            # if imported test file not empty will raise
            shutil.rmtree(imported_tests)
            shutil.move(user_test_path, imported_tests)
            print_cmd_color("white", "...success")
            break
        except Exception as exc:
            print(exc)
            print("moving test files failed, retrying...")
    else:
        input("unable to save your test files, continue anyways? (press enter)")

    # preserving user created order
    print("Do you want to use the new version of scores_order? if you have never heard of this before, just choose [y]")
    confirm = input("Overwrite existing scores_order(Y/n): ")
    if confirm in ["n", 'no']:
        user_scores_order_path = os.path.join(destination_path, "app\\genshin_assets\\scores_order.txt")
        imported_scores_order = os.path.join(current_path, "genshin_assets\\scores_order.txt")
        os.remove(imported_scores_order)
        shutil.move(user_scores_order_path, imported_scores_order)

    # preserving user settings
    user_settings_path = os.path.join(destination_path, "app\\genshin_assets\\settings.json")
    imported_settings_path = os.path.join(current_path, "genshin_assets\\settings.json")
    os.remove(imported_settings_path)
    shutil.move(user_settings_path, imported_settings_path)

    # deleting whole existing genshin_lyre
    print(f"Deleting the whole existing genshin_lyre at {destination_path}...")
    try:
        shutil.rmtree(destination_path)
        print_cmd_color("White", "\n... Deleted existing genshin_lyre")
    except Exception:
        print_cmd_color("DarkYellow", f"""\n... Failed to delete old genshin_lyre
...        {destination_path} still exsists, please delete it manually before proceeding""")
        input(f"  Press enter to open {destination_path}")
        os.startfile(destination_path)
        input("        if you have deleted the old folder, press enter to proceed")

if str(parent_path) != str(destination_path):
    try:
        shutil.copy(parent_path, destination_path)
    except Exception:
        pass
    print("\nSaving genshin_lyre....")
    if os.path.exists(os.path.join(destination_path, "app//genshin_lyre.py")):
        print_cmd_color("White",
                        f"... genshin_lyre is saved at {destination_path} ,you can now delete the original file")
        self_path = os.path.join(destination_path, "app")

    elif os.path.exists(os.path.join(current_path, "genshin_lyre.py")):
        self_path = current_path
        print(
            f"\n... genshin_lyre will be saved at {parent_path} (same place)")
    else:
        print_cmd_color("darkRed", "\n... something went wrong, specified folder cannot be found. please contact me")
        self_path = None
        time.sleep(36000)
        exit()
else:
    print("\nSaving genshin_lyre....       ")
    self_path = current_path
    print_cmd_color("White", f"genshin_lyre is saved at {parent_path} (same place)")

print("creating activation file...     ")

new_parent_path = str(Path(self_path).parent.absolute())
shortcut_content = f"py \"{self_path}\\genshin_lyre.py\""
try:
    with open(new_parent_path + "\\genshin_lyre.bat", "w+") as fd:
        fd.write(shortcut_content)
except Exception as exc:
    pass

if os.path.exists(os.path.join(new_parent_path, "genshin_lyre.bat")):
    print_cmd_color("White", f"... activation file created at {new_parent_path}\\genshin_lyre.bat")
else:
    print_cmd_color("DarkRed",
                    f"Failed to create activation file at {new_parent_path}, please contact me if you see this message")
    time.sleep(3600)

print("\ncreating shortcut for activation file...")

desktop = get_system_path(CSIDL_List.CSIDL_DESKTOP)
shortcut_path = os.path.join(desktop, 'genshin_lyre.lnk')
target = os.path.join(new_parent_path, 'genshin_lyre.bat')
icon = os.path.join(new_parent_path, 'genshin_lyre.bat')
# create shortcut
try:
    import win32com.client

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target
    shortcut.IconLocation = icon
    shortcut.save()
except Exception as exc:
    print_cmd_color("DarkYellow",
                    f"Faliled to create new shortcut due to: {exc}\nhowever if you are updating and already have a existing genshin_lyre shortcut you can ignore this")

if os.path.exists(shortcut_path):

    print_cmd_color("cyan", f"""+-----------------------------------------------------------------------------------------------------------------------
...                Shortcut formed at {shortcut_path}                
             
...        Everything is configured, you can choose to right-click the shortcut on your desktop, and choose:
""")
    print("""               Properties --> Advanced --> and check 'Run As Administrator' --> ok --> ok""")
    print_cmd_color("cyan", """  
...                This is to let the program start at adminstrator level
+-----------------------------------------------------------------------------------------------------------------------
""")

else:
    print_cmd_color("cyan",
                    f"""+-----------------------------------------------------------------------------------------------------------------------
...            Could not detect shortcut at {shortcut_path}  
...            You will need to find 'genshin_lyre.bat' at {new_parent_path} and create a shortcut
...            And move the shortcut to your desktop""")

    if input(f"press enter to open {new_parent_path}, enter 'q' to skip this process: ").lower() != "q":
        os.startfile(new_parent_path)
        print_cmd_color("cyan", """            
...            After you create your shortcut now you just need to rigitclick the shortcut on your desktop, and choose:
""")
    else:
        print_cmd_color("cyan",
                        "...        Everything is configured, you can choose to right-click the shortcut on your desktop, and choose:\n")
    print("""               Properties --> Advanced --> and check 'Run As Administrator' --> ok --> ok""")
    print_cmd_color("cyan", """
...            This is to let the program start at adminstrator level
+-----------------------------------------------------------------------------------------------------------------------
""")

print(
    "Finally go to desktop and double click the shortcut, you should see a list of songs and instructions\nyou can now close this program")

time.sleep(3600)
