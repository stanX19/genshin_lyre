import os


class Songs:
    songs = {}
    songs_order = []


class Settings:
    genshin_app_coordinate = (955, 1052)
    notification = True
    include_sharps = True
    follow_order = True
    midi_beat_threshold = 0
    midi_offset = 0
    midi_kill_delay = True
    name_max_length = 30
    backup = {}


class Paths:
    nightly_path = 'genshin_assets\\nightly'
    score_path = 'genshin_assets\\scores'
    mid_path = 'genshin_assets\\midi'
    test_path = 'genshin_assets\\test'
    order_path = 'genshin_assets\\scores_order.txt'
    settings_path = 'genshin_assets\\settings.txt'
    help_path = 'genshin_assets\\help.txt'
    export_paths = []
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    if not os.path.exists(desktop_path):
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive\\桌面')
    nightly_website = 'genshin_assets\\Genshin Music Nightly.url'
    # add new types of file directory and its file extension here:
    file_type = {nightly_path: 'json',
                 score_path: 'txt',
                 mid_path: 'mid'}
    self_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class PlayVaria:
    song_index = 0
    temp_beat = 0
    speed = 1
    allow_autoplay = False
    warnings = []


class UserVaria:
    notification = True
    song_loop = False