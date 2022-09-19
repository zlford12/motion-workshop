from tkinter import *
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class Header:
    def __init__(
            self, colors, root: Tk,
            connection_manager: ConnectionManagement, application_settings: ApplicationSettings, motion: Motion
    ):
        # Class Objects
        self.connection_manager = connection_manager
        self.application_settings = application_settings
        self.motion = motion
        self.root = root

        # Color Scheme
        self.colors = colors

        # Frame
        self.header = Frame(self.root)

    def draw(self):
        button_x = 10
        button_y = 3

        self.header.configure(bg=self.colors[2])
        self.header.grid(row=0, column=0, columnspan=2, sticky=N + E + W)
        self.header.grid_columnconfigure(100, weight=1)

        do_not_push_button = Button(self.header)
        do_not_push_button.configure(
            text="Do Not\nPush", width=button_x, height=button_y,
            command=lambda: self.motion.commands.command(self.connection_manager, "ReloadAxisInfo"),
            bg=self.colors[3])
        do_not_push_button.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        clear_error_button = Button(self.header)
        clear_error_button.configure(
            text="Reset", width=button_x, height=button_y, bg=self.colors[3],
            command=lambda: self.motion.commands.command(self.connection_manager, "Reset")
        )
        clear_error_button.grid(row=0, column=100, sticky=E, padx=10, pady=10)
