import keyboard
import pyautogui
from .print_functions import print_circle

def return_mouse_coordinate(name="target"):
    print(f"Hover your mouse above the icon of {name} and then press space")
    keyboard.wait("space")
    ICON = pyautogui.position()
    centerX, centerY = pyautogui.size()
    centerX /= 2
    centerY /= 2
    pyautogui.moveTo(centerX, centerY)
    print_circle(radius=50, coordinate=ICON)
    print("  Recorded position is printed red")
    x, y = ICON
    return (x, y)