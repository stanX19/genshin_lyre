try:
    from ...classes import *
except ImportError:
    from classes import *


def get_dict():
    Settings_list = dict(Settings.__dict__.items())
    if 'backup' in Settings_list:
        del Settings_list["backup"]
    Settings_list = {key: val for key, val in Settings_list.items() if not key.startswith("__")}
    return Settings_list


def read():
    """read settings.txt using json, will create new settings.txt if OSError"""
    Settings.backup = get_dict()
    Excluded_backup = Settings.backup
    try:
        with open(Paths.settings_path, encoding="utf-8") as f:
            user_settings = json.load(f)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return save()

    for key in Excluded_backup:
        if type(user_settings.get(key, None)) == type(Excluded_backup[key]):
            setattr(Settings, key, user_settings[key])
    save()



def save():
    Excluded_backup = get_dict()
    with open(Paths.settings_path, "w+") as f:
        json.dump(Excluded_backup, f, indent=2)
    return 0
