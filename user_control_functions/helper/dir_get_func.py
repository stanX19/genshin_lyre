import os
import glob
import importlib

def get_all_func(dir_path):
    """read and return all function in directory"""
    all_func = []

    if not os.path.exists(dir_path):
        return all_func
    for module_name in glob.glob(dir_path + "\\*.py"):
        module_name = module_name[len(dir_path) + 1:-3]
        # C:/Users/DELL/PycharmProjects/pythonProject/foo.py -> foo
        module = importlib.import_module(module_name)
        # loop through all function in module
        for attr in [getattr(module, key) for key in dir(module)]:
            if callable(attr):
                all_func.append(attr)

    return all_func