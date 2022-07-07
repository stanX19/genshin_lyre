try:
    from ...classes import *
    from ...utils import *
except ImportError:
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