try:
    from ...classes import *
except ImportError:
    from classes import *

def get_settings_dict():
    Settings_list = dict(Settings.__dict__.items())
    if 'backup' in Settings_list:
        del Settings_list["backup"]
    Settings_list = {key: val for key, val in Settings_list.items() if not key.startswith("__")}
    return Settings_list

def read_settings():
    """read settings.txt using json, will create new settings.txt if OSError"""
    Settings.backup = get_settings_dict()
    Excluded_backup = Settings.backup
    try:
        with open(Paths.settings_path, encoding="utf-8") as f:
            user_settings = json.load(f)
        if list(Excluded_backup) == list(user_settings):
            for key in Excluded_backup:
                setattr(Settings, key, user_settings[key])
            return 1
        else:
            save_settings()
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        save_settings()
    return 0

def save_settings():
    Excluded_backup = get_settings_dict()
    with open(Paths.settings_path, "w+") as f:
        json.dump(Excluded_backup, f)
    return True