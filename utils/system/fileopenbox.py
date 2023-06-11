import os

try:
    from easygui import fileopenbox
    def deco(func):
        def new_func(*wargs, **kwargs):
            print("Select files to be imported")
            kwargs["multiple"] = True
            try:
                paths = func(*wargs, **kwargs)
                mod_times = [os.stat(path).st_mtime for path in paths]
                sorted_paths = [path for _, path in sorted(zip(mod_times, paths))]
                return sorted_paths
            except Exception:
                return [input("  Error occurred, restart the app tu use gui\n  Enter your file path here: ")]
        return new_func
    fileopenbox = deco(fileopenbox)
except ImportError:
    def fileopenbox():
        return input("  Enter your file path here: ")


if __name__ == '__main__':
    print(fileopenbox(title="Open", msg="Select files to be imported", multiple=True))