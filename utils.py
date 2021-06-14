import os
import sys
import base64
import pathlib
import tkinter as tk
from os import environ, path
from urllib.request import urlopen

import constants


class io_helper_utils(object):

    def __init__(self):
        self.credentials_filepath_dir = path.join(
            environ['APPDATA'], constants.APPDATA_DIRECTORY_NAME)
        self.credentials_filepath = self.credentials_filepath_dir + \
            constants.CREDENTIALS_FILE_CONFIG_NAME

    def write_credentials(self, credentials_filepath, content):
        try:
            with open(credentials_filepath, "w+") as f:
                f.write('\n'.join(content))
        except:
            pass
        # messagebox.showerror("showerror", "Cannot remember credentials as access is denied to store them")

    def read_credentials(self, credentials_filepath):
        try:
            with open(credentials_filepath) as f:
                credentials = [line.rstrip() for line in f]
                print("read credentials as", credentials)
        except Exception as e:
            credentials = []

        return credentials

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def handle_credentials(self):

        if not os.path.exists(self.credentials_filepath_dir):
            pathlib.Path(self.credentials_filepath_dir).mkdir(
                parents=True, exist_ok=True)
            self.write_credentials(self.credentials_filepath, [])
            print("Made new credentials file")
            credentials = []
        else:
            credentials = self.read_credentials(self.credentials_filepath)
        return credentials, self.credentials_filepath


io_helper = io_helper_utils()


def create_static_ui(root, tk):

    canvas = tk.Canvas(
        root,
        bg=constants.WHITE_COLOR,
        height=700,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        # 44, 67, 44+912, 67+588,
        0, 0, 7000, 1000,
        fill=constants.CANVAS_COLOR,
        outline="")
    canvas.create_text(
        70.0, 117.0,
        text=constants.HEADING_TEXT,
        fill=constants.GRAY_COLOR,
        font=("Helvetica", int(44.0), "bold"),
        anchor='nw')

    canvas.create_text(
        70.0, 267.0,
        text=constants.SUBHEADING_TEXT,
        fill="#2ed6af",
        font=("None", int(20.0)),
        anchor='nw')

    canvas.create_text(
        70.0, 338.5+20,
        text=constants.DISCLAIMER_TEXT,
        fill=constants.BLACK_COLOR,
        font=("None", int(13.0)),
        anchor='nw')

    canvas.create_line(450, 100, 450, 600, fill="gray")

    canvas.create_text(
        672.5, 148.5,
        text="Enter Details",
        fill=constants.GRAY_COLOR,
        font=("None", int(22.0)))

    canvas.create_text(
        676.0, 184.5,
        text=constants.CREDENTIALS_INFORMATION_TEXT,
        fill=constants.BLACK_COLOR,
        font=("None", int(14.0)))

    canvas.create_text(
        672.5, 389.0,
        text="Select Region :",
        fill=constants.BLACK_COLOR,
        font=("None", int(15.0)))

    return canvas


def instantiate_login_inputs_ui(canvas, root, name_var, passw_var):
    username_field_img = tk.PhotoImage(
        file=io_helper.resource_path("textfield.png"))
    username_field_bg = canvas.create_image(
        673.0, 257.0,
        image=username_field_img)
    username_field = tk.Entry(
        bd=0,
        bg="#e8f0fe",
        highlightthickness=0, textvariable=name_var, font=constants.CALIBRE_FONT)
    username_field.place(
        x=518, y=232,
        width=310,
        height=48)

    password_field_img = tk.PhotoImage(
        file=io_helper.resource_path("textfield.png"))
    password_field_bg = canvas.create_image(
        673.0, 323.0,
        image=password_field_img)
    password_field = tk.Entry(
        bd=0,
        bg="#e8f0fe",
        highlightthickness=0, textvariable=passw_var, font=constants.CALIBRE_FONT, show="*")
    password_field.place(
        x=518, y=298,
        width=310,
        height=48)


def instantiate_radio_buttons(root, tk, region_var):
    eu_button = tk.Radiobutton(root, text="Europe", variable=region_var,
                               value="eu", bg=constants.CANVAS_COLOR).place(
                                   x=518, y=400)
    ap_button = tk.Radiobutton(root, text="Asia Pacific", variable=region_var,
                               value="ap", bg=constants.CANVAS_COLOR).place(
                                   x=600, y=400)
    na_button = tk.Radiobutton(root, text="North America", variable=region_var,
                               value="na", bg=constants.CANVAS_COLOR).place(
                                   x=700, y=400)
    kr_button = tk.Radiobutton(root, text="Korea", variable=region_var,
                               value="kr", bg=constants.CANVAS_COLOR).place(
                                   x=600, y=420)


def instantiate_login_variables(root, tk, credentials):
    if len(credentials) != 0:
        name_var = tk.StringVar(root, value=credentials[0])
        passw_var = tk.StringVar(root, value=credentials[1])
        remember_checkbox_var = tk.IntVar(root, value=1)
    else:
        name_var = tk.StringVar()
        passw_var = tk.StringVar()
        remember_checkbox_var = tk.IntVar(root, value=0)

    remember_checkbox_button = tk.Checkbutton(root, text="Remember me", variable=remember_checkbox_var,
                                              onvalue=1, offvalue=0, bg=constants.CANVAS_COLOR).place(x=518, y=350)

    region_var = tk.StringVar()
    region_var.set("ap")

    return name_var, passw_var, remember_checkbox_var, region_var


def instantiate_skin_display(root, tk, skins):
    row_gap = 1  # to increment rows by 1 for images
    for skin in skins:
        image_url = skin['displayIcon']
        try:
            image_b64 = base64.b64encode(urlopen(image_url).read())
            photo = tk.PhotoImage(data=image_b64)
            test_photo_label = tk.Label(
                root, image=photo, text=skin['displayName'], compound='top', font=constants.CALIBRE_FONT)
            test_photo_label.image = photo
            test_photo_label.grid(row=1+row_gap, column=5)
        except Exception as e:  # if the server sends anything other than 200 OK
            test_photo_label = tk.Label(
                root, text=skin['displayName'], font=constants.CALIBRE_FONT)
            test_photo_label.grid(row=1+row_gap, column=5)
        row_gap = row_gap+1
