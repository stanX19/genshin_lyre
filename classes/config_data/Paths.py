import os
from utils import get_system_path, CSIDL_List, get_windows_downloads_path

#dirs
nightly_path = 'genshin_assets\\nightly'
score_path = 'genshin_assets\\scores'
mid_path = 'genshin_assets\\midi'
test_path = 'genshin_assets\\test'
input_dir = 'genshin_assets\\input'
output_dir = 'genshin_assets\\output'

#files
order_path = 'genshin_assets\\scores_order.txt'
settings_path = 'genshin_assets\\settings.json'
help_path = 'genshin_assets\\help.txt'
export_paths = []
desktop_path = get_system_path(CSIDL_List.CSIDL_DESKTOP)
downloads_path = get_windows_downloads_path()

nightly_website = 'genshin_assets\\Genshin Music Nightly.url'

# exe
notepad_path = "notepad.exe"

# add new types of file directory and its file extension here:
file_type = {nightly_path: 'json',
             score_path: 'txt',
             mid_path: 'mid'}
parent = os.path.dirname
self_path = parent(parent(parent((os.path.realpath(__file__)))))


