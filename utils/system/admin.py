import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin(program_path):
    """execute the command with admin rights"""
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, program_path, None, 3)
