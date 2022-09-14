from tkinter import *
from tkinter import messagebox, font
from gui.ScanTypes import ScanTypes
from gui.JogControl import JogControl
from motion.Motion import Motion
from motion.Axis import Axis
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class UserInterface:
    def __init__(self):
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
        self.header = Frame(self.root)
        self.body = Frame(self.root)
        self.scan_frame = Frame(self.root)
        self.jog_frame = Frame(self.root)
        self.footer = Frame(self.root)

        # Header Elements
        self.HeaderElement = None

        # Scan Frame
        self.selected_scan_mode = None
        self.scan_types = ScanTypes()
        self.scan_controls = None

        # Jog Frame Elements
        self.jog_controls = [JogControl(self.jog_frame, Axis, self.colors)]

        # Footer Elements
        self.connection_status_display = None

        # Draw UI
        self.draw_header()
        self.create_menubar()
        self.draw_body()
        self.draw_scan_frame()
        self.draw_jog_frame()
        self.draw_footer()

        # Update Loop
        self.stop_update = False
        self.update_loop_time = 200

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
            command=lambda: connection_manager.open_client(application_settings.settings["ControllerIP"])
        )
        system_menu.add_command(
            label="Disconnect From PLC",
            command=connection_manager.disconnect
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

    def draw_header(self):
        button_x = 10
        button_y = 3

        self.header.configure(bg=self.colors[2])
        self.header.grid(row=0, column=0, columnspan=2, sticky=N + E + W)
        self.header.grid_columnconfigure(100, weight=1)

        do_not_push_button = Button(self.header)
        do_not_push_button.configure(
            text="Do Not\nPush", width=button_x, height=button_y,
            command=lambda: motion.commands.command(connection_manager.client, "RedefineAxes"),
            bg=self.colors[3])
        do_not_push_button.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        disconnect_button = Button(self.header)
        disconnect_button.configure(
            text="I Do\nNothing", width=button_x, height=button_y,
            command=self.dummy_function,
            bg=self.colors[3])
        disconnect_button.grid(row=0, column=1, sticky=W, pady=10)

        clear_error_button = Button(self.header)
        clear_error_button.configure(
            text="Reset", width=button_x, height=button_y, bg=self.colors[3],
            command=lambda: motion.commands.command(connection_manager.client, "Reset")
        )
        clear_error_button.grid(row=0, column=100, sticky=E, padx=10, pady=10)

    def draw_body(self):
        self.body.configure(bg=self.colors[0])
        self.body.grid(row=1, column=0, sticky=N + E + S + W)

    def draw_scan_frame(self):

        self.scan_frame.configure(bg=self.colors[3])
        self.scan_frame.grid(row=1, column=1, rowspan=2, sticky=E + N + S)

        if self.selected_scan_mode is None:
            self.selected_scan_mode = motion.machine_config.default_scan_type

        self.scan_controls = self.scan_types.scan_types[self.selected_scan_mode](self.scan_frame, self.colors)
        self.scan_controls.draw()

    def draw_jog_frame(self):
        self.jog_frame.configure(bg=self.colors[1])
        self.jog_frame.grid(row=2, column=0, sticky=S + E + W)

        for child in self.jog_frame.winfo_children():
            child.destroy()

        self.jog_controls = []
        row = 0
        column = 0
        for i in range(len(motion.axis_list)):
            self.jog_controls.append(JogControl(
                self.jog_frame, motion.axis_list[i], self.colors,
                connection_manager, application_settings
            ))
            self.jog_controls[i].draw(row, column)
            row += 1
            if row > int(application_settings.settings["JogControlHeight"]) - 1:
                row = 0
                column += 1

    def draw_footer(self):

        self.footer.configure(bg=self.colors[2], height=20)
        self.footer.columnconfigure(100, weight=1)
        self.footer.grid(row=3, column=0, columnspan=2, sticky=S + E + W)
        local_font = ("Arial", 10)

        for child in self.footer.winfo_children():
            child.destroy()

        self.connection_status_display = Label(self.footer)
        self.connection_status_display.configure(text="Disconnected", bg=self.colors[2], font=local_font)
        self.connection_status_display.grid(row=0, column=100, padx=10, sticky=E)

    def startup(self):
        # Connect To OPCUA Server
        if application_settings.settings["ConnectAtStartup"] == "True":
            connection_manager.open_client(application_settings.settings["ControllerIP"])

        # Loop
        if not self.stop_update:
            self.root.after(self.update_loop_time, self.update_loop)

    def update_loop(self):
        # On Connect To PLC
        if connection_manager.is_connected() and (self.connection_status_display["text"] == "Disconnected"):
            # Get Data From PLC
            motion.read_axes_from_system(connection_manager.client)
            motion.machine_config.read_config_from_system(connection_manager.client)
            motion.commands.populate_commands(connection_manager.client)

            # Update UI
            self.connection_status_display.configure(text="Connected")
            self.draw_jog_frame()

        # On Disconnect From PLC
        if not connection_manager.is_connected() and (self.connection_status_display["text"] == "Connected"):
            self.connection_status_display.configure(text="Disconnected")

        # Check For Connection Management Error
        if connection_manager.error:
            connection_manager.error = False
            messagebox.showerror(title="Connection Error", message=connection_manager.error_message)

        # Update Axis Data
        if connection_manager.is_connected():
            for axis in motion.axis_list:
                axis.axis_data.update(connection_manager.client)

        # Update Jog Controls
        for x in self.jog_controls:
            x.update()

        # Loop
        if not self.stop_update:
            self.root.after(self.update_loop_time, self.update_loop)

    def cleanup(self):
        connection_manager.disconnect()
        self.stop_update = True
        self.root.update()
        self.root.destroy()
        exit()

    def dummy_function(self):
        return


def main():
    # Tkinter Main Loop
    user_interface.root.after(user_interface.update_loop_time, user_interface.startup)
    user_interface.root.mainloop()


if __name__ == "__main__":
    # Create Global Instances of Class Objects
    application_settings = ApplicationSettings()
    motion = Motion()
    connection_manager = ConnectionManagement()
    user_interface = UserInterface()

    main()
