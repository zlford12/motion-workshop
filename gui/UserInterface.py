import threading
import time
from tkinter import *
from tkinter import messagebox, font
from gui.Header import Header
from gui.JogFrame import JogFrame
from gui.ScanTypes import ScanTypes
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
            "#FFFFFF"   # 5 - light text color
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
        self.menu_bar = Menu(self.root)
        self.header = Header(self.colors, self.root, connection_manager, application_settings, motion)
        self.body = Frame(self.root)
        self.jog_frame = JogFrame(self.colors, self.root, connection_manager, application_settings, motion)
        self.scan_frame = Frame(self.root)
        self.footer = Frame(self.root)

        # Scan Frame Elements
        self.selected_scan_mode = None
        self.scan_types = ScanTypes()
        self.scan_controls = None

        # Header Elements
        self.HeaderElement = None

        # Footer Elements
        self.connection_status_display = None

        # Update Loop
        self.stop_update = True
        self.update_loop_wait_time = 200
        self.last_update_loop_time = None

    def create_menubar(self):
        # File Menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(
            label="Open",
            command=self.dummy_function
        )
        file_menu.add_command(
            label="Application Settings",
            command=self.dummy_function
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

    def draw_body(self):
        self.body.configure(bg=self.colors[0])
        self.body.grid(row=1, column=0, sticky=N + E + S + W)

    def draw_scan_frame(self):

        self.scan_frame.configure(bg=self.colors[3])
        self.scan_frame.grid(row=1, column=1, rowspan=3, sticky=E + N + S)

        if self.selected_scan_mode is None:
            self.selected_scan_mode = self.motion.machine_config.default_scan_type

        self.scan_controls = self.scan_types.scan_types[self.selected_scan_mode](self.scan_frame, self.colors)
        self.scan_controls.draw()

    def draw_footer(self):

        self.footer.configure(bg=self.colors[2], height=20)
        self.footer.columnconfigure(100, weight=1)
        self.footer.grid(row=4, column=0, columnspan=2, sticky=S + E + W)
        local_font = ("Arial", 10)

        for child in self.footer.winfo_children():
            child.destroy()

        self.connection_status_display = Label(self.footer)
        self.connection_status_display.configure(text="Disconnected", bg=self.colors[2], font=local_font)
        self.connection_status_display.grid(row=0, column=100, padx=10, sticky=E)

    def startup(self, loop_thread: threading.Thread):
        # Connect To OPCUA Server
        if self.application_settings.settings["ConnectAtStartup"] == "True":
            self.connection_manager.open_client(self.application_settings.settings["ControllerIP"])

        # Draw UI
        self.header.draw_header()
        self.create_menubar()
        self.draw_body()
        self.draw_scan_frame()
        self.jog_frame.draw()
        self.draw_footer()

        # Start Update Loop
        self.stop_update = False
        loop_thread.start()

    def update_loop(self):
        while not self.stop_update:
            # Measure Start Time
            start_time = time.time()

            # On Connect To PLC
            if self.connection_manager.is_connected() and (self.connection_status_display["text"] == "Disconnected"):
                # Get Data From PLC
                self.motion.read_axes_from_system(self.connection_manager.client)
                self.motion.machine_config.read_config_from_system(self.connection_manager.client)
                self.motion.commands.populate_commands(self.connection_manager.client)

                # Update UI
                self.connection_status_display.configure(text="Connected")
                self.jog_frame.draw()

            # On Disconnect From PLC
            if not self.connection_manager.is_connected() and (self.connection_status_display["text"] == "Connected"):
                self.connection_status_display.configure(text="Disconnected")

            # Update Axis Data
            for axis in self.motion.axis_list:
                if self.connection_manager.is_connected():
                    axis.axis_data.update(self.connection_manager.client)

            # Check For Connection Management Error
            if self.connection_manager.error:
                self.connection_manager.error = False
                messagebox.showerror(title="Connection Error", message=self.connection_manager.error_message)

            # Check For Axis Data Error
            for axis in self.motion.axis_list:
                if axis.axis_data.communication_error:
                    axis.axis_data.communication_error = False
                    if self.connection_manager.connection_desired:
                        messagebox.showerror(title="Connection Error", message="Failed To Get Axis Data")

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

    def dummy_function(self):
        return
