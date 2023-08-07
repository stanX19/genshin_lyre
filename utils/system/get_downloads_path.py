import os
import platform
import winreg as reg


def get_windows_downloads_path():
    if platform.system() != 'Windows':
        raise OSError("This function is for Windows only.")

    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
        value, _ = reg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")
        download_path = os.path.expandvars(value)
        return download_path
    except Exception as e:
        raise OSError(f"Error retrieving download path: {e}")


if __name__ == '__main__':
    download_path = get_windows_downloads_path()
    print("Default download path:", download_path)