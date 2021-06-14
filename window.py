import tkinter as tk
from gui import DailyValorantSkins

if __name__ == "__main__":
    root = tk.Tk()
    gui = DailyValorantSkins(root)
    gui.create_ui()
    root.mainloop()