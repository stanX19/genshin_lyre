import ctypes
from ctypes import wintypes, windll

def get_system_path(CSIDL):
    """Gets the path of a Windows special folder based on the given CSIDL value.

    Args:
        CSIDL (int): The CSIDL (Constant Special Item ID List) value corresponding to
            a specific Windows special folder.

    Returns:
        str: The full path of the Windows special folder.

    Raises:
        OSError: If the SHGetFolderPathW function call fails to retrieve the folder path.
    """

    _SHGetFolderPath = windll.shell32.SHGetFolderPathW
    _SHGetFolderPath.argtypes = [wintypes.HWND,
                                 ctypes.c_int,
                                 wintypes.HANDLE,
                                 wintypes.DWORD, wintypes.LPCWSTR]

    path_buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    result = _SHGetFolderPath(0, CSIDL, 0, 0, path_buf)
    return path_buf.value

class CSIDL_List:
    CSIDL_DESKTOP = 0
    CSIDL_INTERNET = 1
    CSIDL_PROGRAMS = 2
    CSIDL_CONTROLS = 3
    CSIDL_PRINTERS = 4
    CSIDL_PERSONAL = 5
    CSIDL_FAVORITES = 6
    CSIDL_STARTUP = 7
    CSIDL_RECENT = 8
    CSIDL_SENDTO = 9
    CSIDL_BITBUCKET = 10
    CSIDL_STARTMENU = 11
    CSIDL_MYDOCUMENTS = 12
    CSIDL_MYMUSIC = 13
    CSIDL_MYVIDEO = 14
    CSIDL_DESKTOPDIRECTORY = 16
    CSIDL_NETHOOD = 19
    CSIDL_FONTS = 20
    CSIDL_TEMPLATES = 21
    CSIDL_COMMON_STARTMENU = 22
    CSIDL_COMMON_PROGRAMS = 23
    CSIDL_COMMON_STARTUP = 24
    CSIDL_COMMON_DESKTOPDIRECTORY = 25
    CSIDL_APPDATA = 26
    CSIDL_PRINTHOOD = 27
    CSIDL_LOCAL_APPDATA = 28
    CSIDL_ALTSTARTUP = 29
    CSIDL_COMMON_ALTSTARTUP = 30
    CSIDL_COMMON_FAVORITES = 31
    CSIDL_INTERNET_CACHE = 32
    CSIDL_COOKIES = 33
    CSIDL_HISTORY = 34
    CSIDL_COMMON_APPDATA = 35
    CSIDL_WINDOWS = 36
    CSIDL_SYSTEM = 37
    CSIDL_PROGRAM_FILES = 38
    CSIDL_MYPICTURES = 39
    CSIDL_PROFILE = 40
    CSIDL_SYSTEMX86 = 41
    CSIDL_PROGRAM_FILESX86 = 42
    CSIDL_PROGRAM_FILES_COMMON = 43
    CSIDL_PROGRAM_FILES_COMMONX86 = 44
    CSIDL_COMMON_TEMPLATES = 45
    CSIDL_COMMON_DOCUMENTS = 46
    CSIDL_COMMON_ADMINTOOLS = 47
    CSIDL_ADMINTOOLS = 48
    CSIDL_CONNECTIONS = 49
    CSIDL_COMMON_MUSIC = 53
    CSIDL_COMMON_PICTURES = 54
    CSIDL_COMMON_VIDEO = 55

if __name__ == '__main__':
    # test
    for name, value in vars(CSIDL_List).items():
        if not name.startswith("__") and isinstance(value, int):
            path = get_system_path(value)
            print(f"{name}: {path}")
