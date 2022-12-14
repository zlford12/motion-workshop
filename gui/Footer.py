from tkinter import *
from tkinter import ttk
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class Footer:
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
        self.footer = Frame(self.root)

        # Footer Elements
        self.connection_status_display = Label
        self.loop_time_display = Label

    def draw(self):
        self.footer.configure(bg=self.colors[2], height=20)
        self.footer.columnconfigure(0, weight=1)
        self.footer.grid(row=4, column=0, columnspan=3, sticky=S + E + W)
        local_font = ("Arial", 10)

        for child in self.footer.winfo_children():
            child.destroy()

        self.connection_status_display = Label(self.footer)
        self.connection_status_display.configure(text="Disconnected", bg=self.colors[2], font=local_font)
        self.connection_status_display.grid(row=0, column=100, padx=10, sticky=E)

        ttk.Separator(self.footer, orient=VERTICAL).grid(row=0, column=99)

        self.loop_time_display = Label(self.footer)
        self.loop_time_display.configure(text="0s", bg=self.colors[2], font=local_font)
        self.loop_time_display.grid(row=0, column=98, padx=10, sticky=E)
