import os
import sys
import helper
sys.path.append(os.path.dirname(__file__))

no_dependent = helper.get_all_func(os.path.dirname(__file__))