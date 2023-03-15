from tkinter import *
from gui.scan_types.FileSpline import FileSpline
from gui.scan_types.Mesh import Mesh
from gui.scan_types.NoScan import NoScan
from gui.scan_types.P2P import P2P
from gui.scan_types.Raster_3D import Raster3D
from gui.scan_types.Shaft import Shaft
from gui.scan_types.Spline import Spline
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
        self.drawn_scan_type = ""
        self.scan_controls = None

        # Scan Types
        self.scan_types = {
            "NoScan": NoScan,
            "Raster_3D": Raster3D,
            "P2P": P2P,
            "Spline": Spline,
            "Shaft": Shaft,
            "Mesh": Mesh,
            "FileSpline": FileSpline
        }

    def draw(self):

        self.scan_frame.configure(bg=self.colors[3])
        self.scan_frame.grid(row=1, column=2, rowspan=3, sticky=E + N + S)

        if self.motion.machine_config.selected_scan_type == "":
            self.motion.machine_config.selected_scan_type = self.motion.machine_config.default_scan_type

        self.drawn_scan_type = self.motion.machine_config.selected_scan_type

        self.scan_controls = \
            self.scan_types[self.motion.machine_config.selected_scan_type](
                self.scan_frame, self.colors, self.connection_manager, self.motion
            )
        self.scan_controls.draw_controls()

    def update_scan_type(self):
        if self.connection_manager.is_connected():
            index = self.connection_manager.node_list.selected_scan_type.get_value()
            self.motion.machine_config.selected_scan_type = self.motion.machine_config.available_scan_types[index]

        if not (self.motion.machine_config.selected_scan_type in self.scan_types):
            self.motion.machine_config.selected_scan_type = "NoScan"

        if self.drawn_scan_type != self.motion.machine_config.selected_scan_type:
            for child in self.scan_frame.winfo_children():
                child.destroy()

            self.draw()

        if hasattr(self.scan_controls, "update") and callable(self.scan_controls.update):
            self.scan_controls.update()
