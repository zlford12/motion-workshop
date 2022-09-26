from gui.control_tabs.AxisStatus import AxisStatus
from gui.control_tabs.OffsetJog import OffsetJog
from tkinter import *
from tkinter import ttk
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class ControlTabs:
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

        # TTK Style
        s = ttk.Style()
        s.theme_use('default')
        s.configure('TNotebook', background=self.colors[0])
        s.configure('TNotebook', fg=self.colors[1])
        s.map("TNotebook", background=[("selected", self.colors[0])])

        # Tab Control
        self.control_tabs = ttk.Notebook(self.root)

        # Tabs
        self.offset_jog = OffsetJog(colors=colors, tabs=self.control_tabs, connection_manager=connection_manager,
                                    application_settings=application_settings, motion=motion)
        self.axis_status = AxisStatus(colors=colors, tabs=self.control_tabs, connection_manager=connection_manager,
                                      application_settings=application_settings, motion=motion)

    def draw(self):
        # Draw Tabs
        self.control_tabs.grid(row=1, column=1, sticky=N + S)

        # Populate Tabs
        self.axis_status.draw()
        self.offset_jog.draw()
