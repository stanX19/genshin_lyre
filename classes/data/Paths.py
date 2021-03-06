import os
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
parent = os.path.dirname
self_path = parent(parent(parent((os.path.realpath(__file__)))))