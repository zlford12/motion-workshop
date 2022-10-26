from tkinter import *
from gui.scan_types.NoScan import NoScan
from gui.scan_types.P2P import P2P
from gui.scan_types.Raster_3D import Raster3D
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
            "NoScan": NoScan,
            "Raster_3D": Raster3D,
            "P2P": P2P
        }

    def draw(self):

        self.scan_frame.configure(bg=self.colors[3])
        self.scan_frame.grid(row=1, column=2, rowspan=3, sticky=E + N + S)

        if self.selected_scan_mode is None:
            self.selected_scan_mode = self.motion.machine_config.default_scan_type

        if not (self.selected_scan_mode in self.scan_types):
            self.selected_scan_mode = "NoScan"

        self.scan_controls = \
            self.scan_types[self.selected_scan_mode](self.scan_frame, self.colors, self.connection_manager)
        self.scan_controls.draw_controls()

    def update_scan_type(self):

        for child in self.scan_frame.winfo_children():
            child.destroy()

        if self.connection_manager.is_connected():
            index = self.connection_manager.node_list.selected_scan_type.get_value()
            self.selected_scan_mode = self.motion.machine_config.available_scan_types[index]

        self.draw()
