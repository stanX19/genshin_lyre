import sys
import threading
import tkinter as tk
from multiprocessing import Process
from typing import Union, Callable
import gc


def round_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    width = x2 - x1
    height = y2 - y1
    if radius > min(width, height):
        radius = min(width, height)

    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    canvas.create_polygon(points, **kwargs, smooth=True)
    return canvas


class Dragpad(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)

        # drag around
        self.bind("<ButtonPress-1>", self.start_move, add='+')
        self.bind("<ButtonRelease-1>", self.stop_move, add='+')
        self.bind("<B1-Motion>", self.do_move, add='+')
        self.x = None
        self.y = None

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry(f"+{x}+{y}")


class FadeAway(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.is_dead = False

        # default opacity:
        self.opacity = 0.7

        # ask Windows to ignore this window
        self.overrideredirect(True)
        self.wm_overrideredirect(True)

        # reset bomb
        self.bind("<ButtonPress-1>", self.end_countdown, add='+')
        self.bind("<ButtonRelease-1>", self.start_countdown, add='+')

        # fade away
        self.bomb = self.after(2000, self.fade_away)

        # hooks
        self._on_death_func = None

    def on_fadeout(self, func_hook):
        self._on_death_func = func_hook

    def end_countdown(self, *agrs, **kwargs):
        if self.bomb:
            self.after_cancel(self.bomb)
        self.attributes('-alpha', self.opacity)

    def start_countdown(self, *agrs, **kwargs):
        self.bomb = self.after(2000, self.fade_away)

    def fade_away(self, speed=0.01):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            alpha -= speed
            self.attributes("-alpha", alpha)
            self.bomb = self.after(10, self.fade_away)
        else:
            self.destroy()
            self.is_dead = True
            if self._on_death_func is not None:
                self._on_death_func()


class Notification(FadeAway):
    def __init__(self, text="", fontsize=25, *wargs, **kwargs):
        FadeAway.__init__(self, wargs, kwargs)

        # ask Windows to ignore this window
        self.overrideredirect(True)
        self.wm_overrideredirect(True)

        # layering
        self.attributes("-topmost", True)

        # location and size
        line_count = text.count('\n') + 1
        margin = 20
        width = 2 * margin + int(self.winfo_screenwidth() / 2)
        height = int(2 * margin + fontsize * line_count + 0.75 * fontsize * (line_count - 1)) + 10
        x_cor = int(self.winfo_screenwidth() / 2 - width / 2)
        y_cor = int(self.winfo_screenheight() - 300 - height)

        self.geometry("{}x{}+{}+{}".format(  # width, height, x-cor, y-cor
            width,
            height,
            x_cor,
            y_cor
        ))

        # constant
        radius = 100
        dragpad_width = 50
        dragpad_color = "#0d0d0d"

        # design
        self.configure(bg='blue')
        self.wm_attributes('-transparentcolor', 'blue')  # set blue as transparent
        self.opacity = 0.7
        self.attributes('-alpha', self.opacity)

        # background
        self.background = tk.Canvas(self, width=width - dragpad_width, height=height, highlightthickness=0)
        self.background.configure(bg="blue")
        self.background.pack(side="right")
        self.background.configure(bg="blue")
        round_rectangle(self.background, dragpad_width, 0, width - dragpad_width, height, radius=radius, fill="black")

        # dragpad
        self.dragpad = Dragpad(self, width=dragpad_width, height=height, highlightthickness=0)
        self.dragpad.configure(bg="blue")
        self.dragpad.pack(side="left", fill="y")
        round_rectangle(self.dragpad, 0, 0, dragpad_width + radius, height, radius=radius, fill=dragpad_color)

        # text
        self.label = tk.Label(self.background, text=text,
                              height=height,
                              bg='black',
                              fg="white",
                              font=("Courier", fontsize),
                              padx=margin + 20, pady=margin,
                              justify="left",
                              anchor="nw",
                              )
        self.label.place(x=-10, y=-5, )

    def reinit(self, text, fontsize):
        # Update the text and font size of the existing label
        self.label.config(text=text, font=("Courier", fontsize))

        # Adjust the size and position of the notification window if necessary
        line_count = text.count('\n') + 1
        margin = 20
        width = 2 * margin + int(self.winfo_screenwidth() / 2)
        height = int(2 * margin + fontsize * line_count + 0.75 * fontsize * (line_count - 1)) + 10
        x_cor = int(self.winfo_screenwidth() / 2 - width / 2)
        y_cor = int(self.winfo_screenheight() - 300 - height)

        self.geometry("{}x{}+{}+{}".format(width, height, x_cor, y_cor))
        self.background.config(width=width - 50, height=height)
        self.dragpad.config(height=height)
        self.label.config(height=height)
        self.background.delete("all")
        round_rectangle(self.background, 50, 0, width - 50, height, radius=100, fill="black")
        self.dragpad.delete("all")
        round_rectangle(self.dragpad, 0, 0, 50 + 100, height, radius=100, fill="#0d0d0d")

        # reset opacity
        self.end_countdown()
        self.start_countdown()


class Handler:
    def __init__(self):
        self.thread = None
        self.new_msg = None
        self.running = False
        self.window = None

    def start_notif(self, text: str, font: int):
        self.new_msg = (text, font)
        if self.running:
            return
        if isinstance(self.thread, threading.Thread):
            self.thread.join()
        self.thread = threading.Thread(target=self.main_loop)
        self.thread.start()

    def on_fadeout(self):
        self.running = False
        self.window = None

    def main_loop(self):
        root = tk.Tk()
        root.withdraw()
        self.window = None
        self.running = True
        while self.running:
            root.update()
            if self.new_msg is None:
                continue
            if isinstance(self.window, Notification):
                self.window.reinit(*self.new_msg)
            else:
                self.window = Notification(*self.new_msg)
                self.window.on_fadeout(self.on_fadeout)
            self.new_msg = None
        root.quit()
        root.destroy()
        # do not remove the below code, will cause "double free"
        self.window = None
        root = None
        gc.collect()


# globals for threads to access
HANDLER: Handler = Handler()


def tk_notify(text="1\n2\n3", font=15):
    global HANDLER
    HANDLER.start_notif(text, font)


def main():
    import time
    tk_notify("some\ntest 1\nstr")
    time.sleep(1)
    tk_notify("some\ntest 2\nstr")
    time.sleep(6)
    tk_notify("some\ntest 3\nstr")


if __name__ == '__main__':
    main()
