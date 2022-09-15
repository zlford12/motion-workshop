from tkinter import *
from gui.scan_types.P2P import P2P
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class ScanFrame:
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
        self.scan_frame = Frame(self.root)

        # Scan Frame Elements
        self.selected_scan_mode = None
        self.scan_controls = None

        # Scan Types
        self.scan_types = {
            "P2P": P2P
        }

    def draw(self):

        self.scan_frame.configure(bg=self.colors[3])
        self.scan_frame.grid(row=1, column=1, rowspan=3, sticky=E + N + S)

        if self.selected_scan_mode is None:
            self.selected_scan_mode = self.motion.machine_config.default_scan_type

        self.scan_controls = self.scan_types[self.selected_scan_mode](self.scan_frame, self.colors)
        self.scan_controls.draw()
