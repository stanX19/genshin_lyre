import os
import sys
sys.path.append(os.path.dirname(__file__))
from .common import *
from .converter import *
from .print_functions import *
from .return_mouse_coordinate import return_mouse_coordinate
from .unique_name import unique_name
from .user_input_best_match import user_input_best_match
from .tk_notify import tk_notify, initiating_caller

from .system import fileopenbox, get_desktop_path, run_as_admin, is_admin

notify = tk_notify

# def notify(text):
#     text = text.split('\n', 1)
#     windows_notify(*text)
