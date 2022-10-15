import tkinter as tk
from multiprocessing import Process, Pipe, parent_process
import sys

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

    def end_countdown(self, event):
        if self.bomb:
            self.after_cancel(self.bomb)
        self.attributes('-alpha', self.opacity)

    def start_countdown(self, event):
        self.bomb = self.after(3000, self.fade_away)

    def fade_away(self, speed=0.01):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            alpha -= speed
            self.attributes("-alpha", alpha)
            self.bomb = self.after(10, self.fade_away)
        else:
            self.destroy()
            self.is_dead = True

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
        self.label.place(x=-10,y=-5,)


def notify_mainloop():
    if not isinstance(ROOT, tk.Tk):
        raise Exception("root not initiated")
    window = None
    while True:
        new_args = RECEIVER.recv()
        if new_args == 0:
            pass
        elif new_args is None:
            return
        elif new_args != 0:
            if window:  # Not first window / there is a existing window
                window.destroy()
                extra = RECEIVER.recv()
                if extra != 0 and extra[0] is None:
                    return
            window = Notification(*new_args)
        if window and window.is_dead:
            window = None
        else:
            SENDER.send(0)
        ROOT.update_idletasks()
        ROOT.update()


def tk_notify(text="1\n2\n3",font=15):
    if SENDER is None:
        raise Exception("main program is not called by initiating caller, notification wont work without tk mainloop")
    SENDER.send((text, font))


def set_up(target, args, receiver, sender):
    global RECEIVER, SENDER
    RECEIVER, SENDER = receiver, sender
    sys.stdin = open(0)
    target(*args)
    SENDER.send(None)


def initiating_caller(target, args=()):
    global RECEIVER, SENDER, ROOT
    ROOT = tk.Tk()
    ROOT.withdraw()
    RECEIVER, SENDER = Pipe(False)
    process = Process(target=set_up,args=(target,args,RECEIVER,SENDER))
    process.start()
    notify_mainloop()


# known that we wont run tk as main program
ROOT = None
RECEIVER, SENDER = None, None


def main():
    import time
    tk_notify("hahahahah yessss")
    time.sleep(1)
    tk_notify("i\nam\nlegend")
    time.sleep(1)


if __name__ == '__main__':
    initiating_caller(main)