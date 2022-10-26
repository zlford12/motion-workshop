from tkinter import *
from utility.ConnectionManagement import ConnectionManagement


class NoScan:
    def __init__(self, frame, colors, c: ConnectionManagement):
        # Create Frames
        self.frame = frame
        self.colors = colors
        self.control_frame = Frame(self.frame)

        # Connection Manager
        self.c = c

        # Create Widgets
        self.no_scan_label = Label(self.control_frame)

    def configure(self):
        # Configure Frame
        self.control_frame.configure(bg=self.colors[3], width=500)

        # Parameters
        label_font = ("Arial Black", 10)

        # Configure Widgets
        self.no_scan_label.configure(
            text="No Scan\nType Selected", bg=self.colors[3], font=label_font, justify=LEFT
        )

    def draw_controls(self):
        # Configure Widgets
        self.configure()

        # Draw Frames
        self.control_frame.grid(row=0, column=0)

        # Draw Widgets
        self.no_scan_label.grid(
            row=0, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=N + E + S + W
        )
