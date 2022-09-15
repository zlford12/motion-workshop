from tkinter import *
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class Body:
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
        self.body = Frame(self.root)

    def draw_body(self):
        self.body.configure(bg=self.colors[0])
        self.body.grid(row=1, column=0, sticky=N + E + S + W)
