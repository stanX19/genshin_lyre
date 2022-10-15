import os
try:
    from ...utils import get_desktop_path
except ImportError:
    from utils import get_desktop_path

nightly_path = 'genshin_assets\\nightly'
score_path = 'genshin_assets\\scores'
mid_path = 'genshin_assets\\midi'
test_path = 'genshin_assets\\test'
order_path = 'genshin_assets\\scores_order.txt'
settings_path = 'genshin_assets\\settings.txt'
help_path = 'genshin_assets\\help.txt'
export_paths = []
desktop_path = get_desktop_path()

nightly_website = 'genshin_assets\\Genshin Music Nightly.url'
# add new types of file directory and its file extension here:
file_type = {nightly_path: 'json',
             score_path: 'txt',
             mid_path: 'mid'}
parent = os.path.dirname
self_path = parent(parent(parent((os.path.realpath(__file__)))))


