import threading
import time
from tkinter import *
from tkinter import messagebox, font
from gui.Body import Body
from gui.Footer import Footer
from gui.Header import Header
from gui.JogFrame import JogFrame
from gui.MenuBar import MenuBar
from gui.ScanFrame import ScanFrame
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class UserInterface:
    def __init__(
            self, connection_manager: ConnectionManagement, application_settings: ApplicationSettings, motion: Motion
    ):
        # Class Objects
        self.connection_manager = connection_manager
        self.application_settings = application_settings
        self.motion = motion

        # Color Scheme
        self.colors = [
            "#000000",  # 0 - main frame, jog control background, dark text color
            "#333333",  # 1 - jog control frame background
            "#555555",  # 2 - header and footer background
            "#999999",  # 3 - header button color, scan frame background
            "#cccccc",  # 4 - scan frame button color
            "#FFFFFF",  # 5 - light text color
            "#000044"   # 6 - hover highlight color
        ]

        # Root Window
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.cleanup)
        self.root.title("Motion Workshop")
        self.root.geometry("1600x900")
        self.root.minsize(width=800, height=600)
        self.root.resizable(width=True, height=True)
        self.root.configure(bg=self.colors[2])
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Font
        self.default_font = font.nametofont("TkDefaultFont").configure(
            family="Arial Black",
            size=10,
            weight=font.BOLD
        )

        # Window Elements
        self.menu_bar = MenuBar(self.colors, self.root, connection_manager, application_settings, motion)
        self.header = Header(self.colors, self.root, connection_manager, application_settings, motion)
        self.body = Body(self.colors, self.root, connection_manager, application_settings, motion)
        self.jog_frame = JogFrame(self.colors, self.root, connection_manager, application_settings, motion)
        self.scan_frame = ScanFrame(self.colors, self.root, connection_manager, application_settings, motion)
        self.footer = Footer(self.colors, self.root, connection_manager, application_settings, motion)

        # Update Loop
        self.stop_update = True
        self.update_loop_wait_time = 200
        self.last_update_loop_time = None

    def startup(self, loop_thread: threading.Thread):
        # Connect To OPCUA Server
        if self.application_settings.settings["ConnectAtStartup"] == "True":
            self.connection_manager.open_client(self.application_settings.settings["ControllerIP"])

        # Draw UI
        self.header.draw()
        self.menu_bar.draw()
        self.body.draw()
        self.scan_frame.draw()
        self.jog_frame.draw()
        self.footer.draw()

        # Start Update Loop
        self.stop_update = False
        loop_thread.start()

    def update_loop(self):
        while not self.stop_update:
            # Measure Start Time
            start_time = time.time()

            # On Connect To PLC
            if self.connection_manager.is_connected() and \
                    (self.footer.connection_status_display["text"] == "Disconnected"):
                # Get Data From PLC
                self.motion.read_axes_from_system(self.connection_manager.client)
                self.motion.machine_config.read_config_from_system(self.connection_manager.client)
                self.motion.commands.populate_commands(self.connection_manager.client)
                self.body.create_status_labels()

                # Update UI
                self.footer.connection_status_display.configure(text="Connected")
                self.jog_frame.draw()

            # On Disconnect From PLC
            if not self.connection_manager.is_connected() and \
                    (self.footer.connection_status_display["text"] == "Connected"):
                self.footer.connection_status_display.configure(text="Disconnected")

            # Update Axis Data
            self.motion.update(self.connection_manager.client)

            # Update Status Labels
            if self.connection_manager.is_connected():
                self.body.update_status_labels()

            # Check For Connection Management Error
            if self.connection_manager.error:
                self.connection_manager.error = False
                messagebox.showerror(title="Connection Error", message=self.connection_manager.error_message)

            # Check For Axis Data Error
            if self.motion.communication_error:
                self.motion.communication_error = False
                if self.connection_manager.connection_desired:
                    messagebox.showerror(title="Connection Error", message="Failed To Get Axis Data\nDisconnecting...")

                    self.connection_manager.disconnect()

            # Update Jog Controls
            for x in self.jog_frame.jog_controls:
                x.update()

            # Wait
            time.sleep(self.update_loop_wait_time / 1000)

            # Measure Update Loop Time
            self.last_update_loop_time = time.time() - start_time

    def cleanup(self):
        self.stop_update = True
        time.sleep(self.last_update_loop_time)
        self.connection_manager.disconnect()
        self.root.update()
        self.root.destroy()
        exit()
