import pyautogui
import keyboard
import time
import os
from utils import prompt_control_function


class macros():
    def continued_movement(self):

        records = []

        while not keyboard.is_pressed("shift"):
            pyautogui.typewrite("f")
            time.sleep(0.2)
            records.append(keyboard.read_key())
            if records[-6:-1].count(records[-1]) >= 5:
                key = records[-1]
                print(f"{records[-6:-1]} | {key}")
                pyautogui.keyDown(key)
                keyboard.block_key(key)
                keyboard.read_key()
                keyboard.unhook(key)
                pyautogui.keyUp(key)

    def auto_click(self):
        print("press 'k' to start")
        keyboard.wait("k")
        print("press 'shift' to exit")
        while not keyboard.is_pressed("shift"):
            pyautogui.click()
            time.sleep(0.1)
        pass

    def  auto_f(self):
        print("press 'k' to start")
        keyboard.wait("k")
        print("press 'shift' to exit")
        while not keyboard.is_pressed("shift"):
            pyautogui.typewrite("f")
        pass

    def typewrite_all(self, text=""):
        print("press enter to start, 'q' to quit")
        text = str(text)
        keyboard.read_key()
        while not keyboard.is_pressed("enter"):
            if keyboard.is_pressed("q"):
                break
        else:
            for line in text.split("\n"):
                if keyboard.is_pressed("shift") or keyboard.is_pressed("q"):
                    return
                pyautogui.typewrite(line + "\n")
                time.sleep(1.2)

    def chat_countdown(self,secs=10,interval=2):
        all_no  = sorted(list(range(secs)),reverse=True)
        print("press enter to start, 'q' to quit")
        keyboard.read_key()
        while not keyboard.is_pressed("enter"):
            if keyboard.is_pressed("q"):
                break
        else:
            for no in all_no:
                if keyboard.is_pressed("shift") or keyboard.is_pressed("q"):
                    return
                pyautogui.typewrite(str(no) + "\n")
                time.sleep(interval)
    def chat_timer(self,interval=2):
        import math

        print("press enter to start, 'q' to quit, 'space' to stop")
        while not keyboard.is_pressed("enter"):
            if keyboard.is_pressed("q"):
                return
        secs = 0.0
        start_time = time.time()
        while not keyboard.is_pressed("space"):
            pyautogui.typewrite(str(int(secs)) + "\n")
            secs += interval

            current_time = time.time()
            time_passed = current_time - start_time
            to_sleep = secs - time_passed
            if to_sleep> 0.0: time.sleep(to_sleep)
        else:
            secs = round(time.time() - start_time)
            final_time = ""
            min = math.floor(secs/60)
            hour = math.floor(secs/3600)
            if min: secs = math.floor(secs % 60)
            if hour: min = math.floor(min%60)
            if hour: final_time += str(hour) + "h"
            if min: final_time += str(min) + "m"
            if secs: final_time += str(secs) + "s"
            pyautogui.typewrite(final_time)
            return final_time

    def teapot_speed_up_macro(self):
        while True:
            pressed = keyboard.read_key()
            if pressed == "shift":
                return
            i = 0
            while not keyboard.is_pressed("shift") and i < 5:
                pyautogui.click(1762, 1021)
                time.sleep(0.2)
                pyautogui.click(1144, 761)
                time.sleep(1.5)
                pyautogui.click(982, 905)
                time.sleep(0.1)
                i+=1

if __name__ == '__main__':
    prompt_control_function(macros())
