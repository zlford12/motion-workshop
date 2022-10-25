from gui.menu_bar.ApplicationSettingsMenu import ApplicationSettingsMenu
from tkinter import *
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class MenuBar:
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
        self.menu_bar = Menu(self.root)

        # Menu Objects
        self.application_settings_menu = ApplicationSettingsMenu(
            self.colors, self.root, self.application_settings
        )

    def draw(self):
        # File Menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(
            label="Open",
            command=self.dummy_function
        )
        file_menu.add_command(
            label="Application Settings",
            command=self.application_settings_menu.open_settings
        )

        # System Menu
        system_menu = Menu(self.menu_bar, tearoff=0)
        system_menu.add_command(
            label="Connect To PLC",
            command=lambda: self.connection_manager.open_client(self.application_settings.settings["ControllerIP"])
        )
        system_menu.add_command(
            label="Disconnect From PLC",
            command=self.connection_manager.disconnect
        )
        system_menu.add_command(
            label="Machine Configuration",
            command=self.dummy_function
        )
        system_menu.add_command(
            label="Change Scan Type",
            command=self.dummy_function
        )

        # Display Menus
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="System", menu=system_menu)

        # Display Menubar
        self.root.configure(menu=self.menu_bar)

    def dummy_function(self):
        return
