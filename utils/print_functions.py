# -- coding: utf-8 --

import inspect
import random
import math
import win32gui, win32con, sys, os

class WindowsBalloonTip:
    def notify(self, msg, title):
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map  # could also specify a wndproc.
        try:
            win32gui.DestroyWindow(self.hwnd)
        except Exception as exc:
            self.classAtom = win32gui.RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(self.classAtom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join(sys.path[0], "balloontip.ico"))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = win32gui.LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "tooltip")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY,(self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER + 20,hicon, "Balloon  tooltip", title, 200, msg))

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

Notifier = WindowsBalloonTip()
def notify(title="test", description="successful"):

    Notifier.notify(title, description)

def print_rows(printed_list, title="list", parentheses=".",  indent="",end="\n",max_length=30):
    try:
        printed_list = list(printed_list)
    except:
        return 0
    printed_list = [i if len(i) <= max_length else i[:max_length-8] + '...' + i[-5:] for i in printed_list]
    printed_list_length = len(printed_list)
    if printed_list_length == 0:
        return 0
    if printed_list_length <= 10:
        rows = 1
    else:
        rows = 2
        for i in range(2, 5):  # i is the number of rows, starts with 2
            left = rows * math.ceil(len(printed_list) / rows) - printed_list_length
            current = i * math.ceil(len(printed_list) / i) - printed_list_length
            if current <= left:
                rows = i
        while rows != 5 and math.ceil(len(printed_list) / rows) >15:
            rows += 1

    columns = math.ceil(len(printed_list) / rows)

    for i in range(rows * columns - printed_list_length):
        printed_list.append("empty")

    if title: print(f">>>{title}<<<")

    max_printed_text_len = len(max(printed_list, key=len)) + len(parentheses) + 6  # change text gap here

    for e in range(columns):
        print(indent,end="")
        for i in range(rows):
            if printed_list[e + i * columns] != "empty":
                printed_text = f"{e + i * columns + 1}{parentheses} {printed_list[e + i * columns]}"
                print(printed_text + ' ' * ((max_printed_text_len) - len(printed_text)), end="")
        print()
    print(end,end="")

def print_circle(radius=50, RGB=(225,0,0),coordinate=(0,0)):
    try:
        import pyautogui
        import win32api
        import win32gui
    except ImportError as exc:
        print(f"{exc}")
        return
    if coordinate == (0,0):
        coordinate = pyautogui.position()
    x_axis, y_axis = pyautogui.size()
    dc = win32gui.GetDC(0)
    color = win32api.RGB(*RGB)
    x, y = coordinate
    for i in range(int(200*radius)):  ##  range(100)
        x_rand = min(max(random.randint(-radius, radius), -1 * x), x_axis - x - 1)

        limit = int(math.sqrt(radius ** 2 - x_rand ** 2))
        y_rand = min(max(random.randint(-limit, limit), -1 * y), y_axis - y - 1)

        win32gui.SetPixel(dc, x + x_rand, y + y_rand, color)





def prompt_control_function(_class_):
    """controls a list of functions from a class or dict like globals()"""
    if isinstance(_class_,dict):
        methods = {name: _class_[name] for name in _class_ if inspect.isfunction(_class_[name])}
    else:
        methods = {name: getattr(_class_, name) for name in dir(_class_) if inspect.ismethod(getattr(_class_, name))}
    methods_name_list = list(methods)
    if methods_name_list == []:
        return 0
    while True:
        print_rows(methods_name_list,False,")",indent="    ")
        command = input("Which function do you want to activate? (index/q): ").lower()
        while True:
            if command == "q":
                return 0
            else:
                try:
                    specified_func = methods[methods_name_list[int(command)-1]]
                    func_parameters = inspect.signature(specified_func).parameters
                    inputed_parameters = []
                    for parameters in func_parameters:
                        print("Filling in function Parameters, enter none for default (if there is one)")
                        current_key_in = input("{} : ".format(
                            #parameters for name only
                            str(func_parameters[parameters]).replace("=",":")
                        ))
                        key_in = ""
                        while current_key_in:
                            key_in += "\n" + current_key_in
                            current_key_in = input("...")

                        if key_in !="":
                            try:
                                inputed_parameters.append(eval(key_in))
                            except:
                                inputed_parameters.append(key_in)
                        else:
                            default_value = func_parameters[parameters].default
                            if default_value != inspect._empty:
                                inputed_parameters.append(default_value)
                            else:
                                inputed_parameters.append("")

                    print(f"Activated {methods_name_list[int(command) - 1]}")
                    try:
                        import keyboard
                        while keyboard.is_pressed("enter"):
                            pass
                    except:
                        pass
                    returned = specified_func(*inputed_parameters)

                    if returned is not None:
                        input(f"{returned} (press enter)")
                    print(f"... Ended {methods_name_list[int(command) - 1]}\n")
                    break
                except ValueError:
                    try:
                        command = methods_name_list.index(command)+1
                    except ValueError:
                        break
                except Exception as exc:
                    print(f"    Error due to: {exc}\n")
                    break

def print_cmd_color(color="cyan", text="text"):
    """Black, DarkBlue, DarkGreen, DarkCyan, DarkRed, DarkMagenta, DarkYellow, Gray, DarkGray, Blue, Green, Cyan, Red,
    Magenta, Yellow, White"""

    available_color = ['black', 'darkblue', 'darkgreen', 'darkcyan', 'darkred', 'darkmagenta', 'darkyellow', 'gray',
                       'darkgray', 'blue', 'green', 'cyan', 'red', 'magenta', 'yellow', 'white']
    text = text.replace(",", ".").replace("(", "[").replace(")", "]")
    if color.lower() not in available_color:
        return 0
    format_ = f"powershell write-host -fore {color} "
    for line in text.split("\n"):
        os.system(format_ + line)
    return 1

if __name__ =="__main__":

    print_rows(["Black", "DarkBlue","DarkGreen","DarkCyan","DarkRed"
                   ,"DarkMagenta","DarkYellow","Gray","DarkGray","Blue"
                   ,"Green","Cyan","Red","Magenta","Yellow","White"]
                ,""
               ,parentheses=")",indent="    ")

    prompt_control_function(globals())


