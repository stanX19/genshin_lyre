try:
    from easygui import fileopenbox
    def deco(func):
        def new_func(*wargs, **kwargs):
            print("Select the file to be imported")
            try:
                result = func(wargs, kwargs)
                if result:
                    return result
                return ''
            except Exception:
                return input("  Error occurred restart the app for file open box\n  Enter your file path here: ")
        return new_func
    fileopenbox = deco(fileopenbox)
except ImportError:
    def fileopenbox():
        return input("  Enter your file path here: ")