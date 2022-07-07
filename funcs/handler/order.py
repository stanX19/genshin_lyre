from classes import *
from utils import reduceLineBreak


def read_order():
    """return ordered text (list), if none None"""
    if Paths.order_path is not None:
        with open(Paths.order_path, "r") as f:
            # everything done is to prevent repeated element and kill excessive line break from scores_order.txt
            ordered_txt = list(dict.fromkeys(reduceLineBreak(f.read().strip()).split("\n")))
    else:
        ordered_txt = []

    return ordered_txt


def write_order(txt):
    if isinstance(txt, list):
        txt = "\n".join(txt)
    if Paths.order_path != None:
        try:
            with open(Paths.order_path, "w+") as f:
                f.write(txt)
            return True
        except OSError as exc:
            print(f"failed to edit due to: {exc}")
    else:
        if (input("Cannot find scores_order.txt, create new one instead? (Y/n): ")).lower() in ['y', 'yes', 'confirm']:
            try:
                with open('genshin_assets\\scores_order.txt', "w+") as f:
                    f.write(txt)
                return True
            except OSError as exc:
                print(f"failed to create scores_order.txt due to: {exc}")
        else:
            print("cancelled")
        return False


def sync_order():
    write_order(Songs.songs_order)

def edit_order(command, song_name=""):
    if Paths.order_path is None:
        if (input("Cannot find scores_order.txt, create new one instead? (Y/n): ")).lower() in ['y', 'yes',
                                                                                                'confirm']:
            Paths.order_path = 'genshin_assets\\scores_order.txt'
            try:
                with open(Paths.order_path, "w+"):
                    pass
                print(f"created successfully at {Paths.self_path}\\genshin_assets")
                os.startfile(Paths.order_path)
                return True
            except OSError as exc:
                print(f"failed to create due to: {exc}")
        else:
            print("cancelled")
            return 0

    its_a_add = False
    target = ""
    no = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", command)

    # ordered_txt = ['song name', 'song name', 'song name', ...]

    def before_after(command):
        if 'before' in command or 'after' in command or ' at ' in command:
            if 'before' in command or 'at' in command.split(" "):
                if ' at ' in command:
                    before_index = command.find(' at ')
                    bef_command = command[before_index:].replace(" at ", "").strip()
                    exist = 'at'
                else:
                    before_index = command.find('before')
                    bef_command = command[before_index:].replace("before", "").strip()
                    exist = 'before'

                if bef_command == "":
                    print(f"missing argument behind '{exist}': Name/Index")
                    insert_index = before_after(
                        input(f"\nWhere do you want to add '{target}' in order? (before xxx/ after xxx): ").lower())
                    if insert_index is None:
                        return None
                    else:
                        return insert_index

                insert_index = get_song_index(bef_command)
                if insert_index != None:
                    if insert_index <= len(Songs.songs_order):
                        return insert_index
                    else:
                        print("'{}' is out of ordered list's range, last: {}({})".format(
                            bef_command,
                            Songs.songs_order[-1],
                            list(Songs.songs).index(Songs.songs_order[-1])
                        ))
                        return None
                else:
                    print(f"'{bef_command}' is not a valid song name")
                    return None

            else:
                after_index = command.find('after')
                aft_command = command[after_index:].replace("after", "").strip()

                if aft_command == "":
                    print("missing argument behind 'after': Name/Index")
                    insert_index = before_after(
                        input(f"\nWhere do you want to add '{target}' in order? (before xxx/ after xxx): ").lower())
                    if insert_index is None:
                        return None
                    else:
                        return insert_index

                insert_index = get_song_index(aft_command)
                if insert_index is not None:  # if not None then must be int
                    if insert_index < len(Songs.songs_order):
                        return insert_index + 1
                    else:
                        print("'{}' is out of ordered list's range, last: {}({})".format(
                            aft_command,
                            Songs.songs_order[-1],
                            list(Songs.songs).index(Songs.songs_order[-1])
                        ))

                else:
                    print(f"'{aft_command}' is not a valid song name")
                    return None
        return None

    if command == 'order' or 'txt' in command:
        if Paths.order_path is not None:
            os.startfile(Paths.order_path)

    elif 'edit' in command or 'delete' in command:
        if no != []:
            if int(no[0]) - 1 < len(Songs.songs.keys()):
                target = list(Songs.songs.keys())[int(no[0]) - 1]
            else:
                print("invalid index")
                return 0
        else:
            target = input("name of song you want to add or delete: ")
            if not target in Songs.songs_order:
                no = first_int(target)
                if no != None:
                    if no <= len(Songs.songs_order):
                        target = Songs.songs_order[no - 1]
                    else:
                        print("'{}' is out of ordered list's range, last: {}({})".format(
                            no,
                            Songs.songs_order[-1],
                            list(Songs.songs).index(Songs.songs_order[-1])
                        ))
                        return 0
                else:
                    no = []

        if target == "":
            return 0
        if target in Songs.songs_order:
            if (input(f"Are you sure you want to remove {target} from order? (Y/N): ")).lower() in ['y', 'yes',
                                                                                                    'confirm']:
                Songs.songs_order.remove(target)
                txt = "\n".join(Songs.songs_order)
                result = write_order(txt)
                if result:
                    print(f"Removed {target} from order")
                    return 1
        else:
            its_a_add = 1

    if 'add' in command or its_a_add:
        if no != []:
            if int(no[0]) - 1 < len(Songs.songs.keys()):
                target = list(Songs.songs.keys())[int(no[0]) - 1]
            else:
                print("invalid index")
                return 0
        elif song_name != "":
            target = song_name

        elif target == "":
            target = input("name of song want to add or delete: ")
            if not target in Songs.songs_order:
                no = first_int(target)
                if no != None:
                    if no <= len(Songs.songs_order):
                        target = Songs.songs_order[no - 1]
                    else:
                        print("'{}' is out of ordered list's range, last: {}({})".format(
                            no,
                            Songs.songs_order[-1],
                            list(Songs.songs).index(Songs.songs_order[-1])
                        ))
                        return 0
                else:
                    no = []
        if target == "":
            return 0

        insert_index = before_after(command)
        if insert_index is None:
            if "before" in command: command = command[:command.find("before")]
            if "after" in command: command = command[:command.find("after")]

            command += " " + (input(f"Where do you want to add '{target}' in order? (before xxx/ after xxx): ")).lower()
            insert_index = before_after(command)
            if insert_index is None:
                return 0

        msg = ""
        if insert_index < len(Songs.songs_order) + 1:
            if insert_index < len(Songs.songs_order):
                msg += f"before {Songs.songs_order[insert_index]}"
            if insert_index != 0:
                if insert_index != len(Songs.songs_order):
                    msg += f" | "
                msg += f"after {Songs.songs_order[insert_index - 1]}"
        else:
            return 0

        confirmation = input("Adding {} to order at {} ({}), confirm? (Y/N): ".format(
            target,
            insert_index + 1,
            msg
        ))

        if confirmation in ['y', 'yes', 'confirm']:
            Songs.songs_order.insert(insert_index, target)
            txt = "\n".join(Songs.songs_order)
            result = write_order(txt)
            if result:
                print(f"    Added '{target}' to order")
                return 1
        else:
            return 0