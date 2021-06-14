import socket
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import utils
from constants import WHITE_COLOR
from valorant import ValorantAPI


class DailyValorantSkins(object):
    def __init__(self, root):
        self.root = root
        self.root.title("Valorant Daily Skins")
        width, height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (width, height))
        self.root.configure(bg=WHITE_COLOR)
        self.favicon = tk.PhotoImage(file=utils.io_helper.resource_path("favicon.ico"))
        self.root.tk.call('wm', 'iconphoto', root._w, self.favicon)
        self.root.grid_columnconfigure(4, weight=1)
        self.credentials, self.credentials_filepath = utils.io_helper.handle_credentials()
        self.ip_address = socket.gethostbyname(socket.gethostname())

    def create_ui(self):
        self.canvas = utils.create_static_ui(self.root, tk)
        self.name_var, self.passw_var, self.remember_checkbox_var, self.region_var = utils.instantiate_login_variables(
            self.root, tk, self.credentials)
        utils.instantiate_login_inputs_ui(
            self.canvas, self.root, self.name_var, self.passw_var)
        utils.instantiate_radio_buttons(self.root, tk, self.region_var)
        self.progressbar = ttk.Progressbar(
            self.root, length=100, mode='indeterminate')
        self.place_submit_button()

    def submit(self):
        self.progressbar.place(x=620, y=510)
        self.progressbar.start()
        name = self.name_var.get()
        password = self.passw_var.get()
        region = self.region_var.get()
        remember_preference = self.remember_checkbox_var.get()

        mandatory_params = [name, password, region]
        if not all(mandatory_params):
            messagebox.showerror(
                "showerror", "Username/Password/Region cannot be empty")
            return
        if remember_preference:
            pref_args = [name, password]
        else:
            pref_args = []
        utils.io_helper.write_credentials(self.credentials_filepath, pref_args)
        try:
            valorant_login = ValorantAPI(
                name, password, region, self.ip_address)
            skins = valorant_login.player_store
            utils.instantiate_skin_display(self.root, tk, skins)
        except Exception as error:
            messagebox.showerror(
                "showerror", str(error)+"; Please try again")
            return

    def start_submit_thread(self, event):
        global submit_thread
        submit_thread = threading.Thread(target=self.submit)
        submit_thread.daemon = True
        self.progressbar.start()
        submit_thread.start()
        self.root.after(5, self.check_submit_thread)

    def check_submit_thread(self):
        if submit_thread.is_alive():
            self.root.after(5, self.check_submit_thread)
        else:
            self.progressbar.stop()

    def place_submit_button(self):
        self.img0 = tk.PhotoImage(
            file=utils.io_helper.resource_path("img0.png"))
        b0 = tk.Button(
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.start_submit_thread(None),
            relief="flat")
        b0.place(
            x=518, y=451,
            width=310,
            height=50)
