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

        for child in self.header.winfo_children():
            child.destroy()

        self.header.configure(bg=self.colors[2])
        self.header.grid(row=0, column=0, columnspan=3, sticky=N + E + W)
        self.header.grid_columnconfigure(99, weight=1)

        # Link Unlink Button
        if self.motion.link_status:
            link_button = Button(self.header)
            link_button.configure(
                text="Unlink", width=button_x, height=button_y, bg=self.colors[3],
                command=lambda: self.motion.commands.command(self.connection_manager, "Unlink")
            )
            link_button.grid(row=0, column=1, sticky=W, padx=10, pady=10)
        else:
            link_button = Button(self.header)
            link_button.configure(
                text="Link", width=button_x, height=button_y, bg=self.colors[3],
                command=lambda: self.motion.commands.command(self.connection_manager, "Link")
            )
            link_button.grid(row=0, column=1, sticky=W, padx=10, pady=10)

        # Reset Button
        clear_error_button = Button(self.header)
        clear_error_button.configure(
            text="Reset", width=button_x, height=button_y, bg=self.colors[3],
            command=lambda: self.motion.commands.command(self.connection_manager, "Reset")
        )
        clear_error_button.grid(row=0, column=99, sticky=E, padx=(10, 0), pady=10)

        # Stop All Axes Button
        stop_all_axes_button = Button(self.header)
        stop_all_axes_button.configure(
            text="Stop All\nAxes", width=button_x, height=button_y, bg=self.colors[3],
            command=lambda: self.motion.commands.command(self.connection_manager, "StopAllAxes")
        )
        stop_all_axes_button.grid(row=0, column=100, sticky=E, padx=10, pady=10)
