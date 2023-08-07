import sys
import os

def block_print():
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    if "close" in sys.stdout:
        sys.stdout.close()
    sys.stdout = sys.__stdout__

def get_confirmation(prompt="confirm? [Y/n]: "):
    while True:
        user_input = input(prompt).lower()
        if user_input in ["y", "yes"]:
            return True
        elif user_input in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' or 'n'.")