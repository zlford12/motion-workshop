from tkinter import *
from tkinter import messagebox, font
from background_tasks import ConnectionManagement, ApplicationSettings, Motion
from scan_types import ScanTypes


class UserInterface:
    def __init__(self):
        # Color Scheme
        self.colors = [
            "#000000",  # main frame, jog control background, dark text color
            "#333333",  # jog control frame background
            "#555555",  # header and footer background
            "#999999",  # header button color, scan frame background
            "#cccccc",  # scan frame button color
            "#FFFFFF"  # light text color
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
        self.jog_controls = [self.JogControl(self.jog_frame, motion.Axis, self.colors)]

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

        open_client_button = Button(self.header)
        open_client_button.configure(
            text="I Do\nNothing", width=button_x, height=button_y,
            command=self.dummy_function,
            bg=self.colors[3])
        open_client_button.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        disconnect_button = Button(self.header)
        disconnect_button.configure(
            text="I Do\nNothing", width=button_x, height=button_y,
            command=self.dummy_function,
            bg=self.colors[3])
        disconnect_button.grid(row=0, column=1, sticky=W, pady=10)

        clear_error_button = Button(self.header)
        clear_error_button.configure(
            text="Reset", width=button_x, height=button_y, command=self.dummy_function, bg=self.colors[3])
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
            self.jog_controls.append(self.JogControl(self.jog_frame, motion.axis_list[i], self.colors))
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
                axis.AxisData.update(connection_manager.client)

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

    class JogControl:
        def __init__(self, frame, axis, colors):
            # Create Frame
            self.frame = frame
            self.axis = axis
            self.colors = colors
            self.subframe = Frame(self.frame)

            # Create Widgets
            self.jog_negative_button = Button(self.subframe)
            self.jog_negative_slow_button = Button(self.subframe)
            self.axis_position_label = Label(self.subframe)
            self.go_to_entry = Entry(self.subframe)
            self.go_to_button = Button(self.subframe)
            self.jog_positive_button = Button(self.subframe)
            self.jog_positive_slow_button = Button(self.subframe)

        def configure(self):
            # Unit
            if self.axis.AxisData.Rotary:
                unit_string = "°"
            else:
                unit_string = "mm"

            # Configure Frame
            self.subframe.configure(bg=self.colors[0], width=350, height=115)
            self.subframe.columnconfigure(2, weight=1)
            self.subframe.grid_propagate(False)

            # Configure Widgets
            self.jog_negative_button.configure(
                text="<<", width=2, height=5, bg=self.colors[3]
            )
            self.jog_negative_slow_button.configure(
                text="<", width=2, height=5, bg=self.colors[3]
            )
            self.axis_position_label.configure(
                text=self.axis.AxisData.Name + " \n" +
                str(round(self.axis.AxisData.Position, 2)) + " " + unit_string,
                bg=self.colors[0], fg=self.colors[5], justify=LEFT, font=("Arial Black", 12)
            )
            self.go_to_entry.configure(
                width=10, bg=self.colors[3]
            )
            self.go_to_button.configure(
                text="Go To", width=5, height=1, bg=self.colors[3], command=self.go_to
            )
            self.jog_positive_slow_button.configure(
                text=">", width=2, height=5, bg=self.colors[3]
            )
            self.jog_positive_button.configure(
                text=">>", width=2, height=5, bg=self.colors[3]
            )

            # Bind Widgets
            self.jog_negative_button.bind(
                "<ButtonPress>", lambda state: self.jog_negative(True, False)
            )
            self.jog_negative_button.bind(
                "<ButtonRelease>", lambda state: self.jog_negative(False, False)
            )
            self.jog_negative_slow_button.bind(
                "<ButtonPress>", lambda state: self.jog_negative(True, True)
            )
            self.jog_negative_slow_button.bind(
                "<ButtonRelease>", lambda state: self.jog_negative(False, True)
            )
            self.jog_positive_button.bind(
                "<ButtonPress>", lambda state: self.jog_positive(True, False)
            )
            self.jog_positive_button.bind(
                "<ButtonRelease>", lambda state: self.jog_positive(False, False)
            )
            self.jog_positive_slow_button.bind(
                "<ButtonPress>", lambda state: self.jog_positive(True, True)
            )
            self.jog_positive_slow_button.bind(
                "<ButtonRelease>", lambda state: self.jog_positive(False, True)
            )

        def draw(self, row, column):
            # Configure Widgets
            self.configure()

            # Draw Frame
            if column == 0:
                pad_l = 20
            else:
                pad_l = 10
            pad_r = 10
            if row == 0:
                pad_t = 20
            else:
                pad_t = 10
            if row == 2:
                pad_b = 20
            else:
                pad_b = 10
            self.subframe.grid(row=row, column=column, padx=(pad_l, pad_r), pady=(pad_t, pad_b))

            # Draw Widgets
            self.jog_negative_button.grid(
                row=0, column=0, rowspan=2, padx=(5, 0), pady=5
            )
            self.jog_negative_slow_button.grid(
                row=0, column=1, rowspan=2, pady=5
            )
            self.axis_position_label.grid(
                row=0, column=2, padx=30, pady=5, rowspan=2, sticky=W
            )
            self.go_to_entry.grid(
                row=0, column=3, padx=10, pady=(10, 0), sticky=S
            )
            self.go_to_button.grid(
                row=1, column=3, padx=5, pady=5
            )
            self.jog_positive_slow_button.grid(
                row=0, column=4, rowspan=2, pady=5
            )
            self.jog_positive_button.grid(
                row=0, column=5, rowspan=2, padx=(0, 5), pady=5
            )

        def update(self):
            # Unit
            if self.axis.AxisData.Rotary:
                unit_string = "°"
            else:
                unit_string = "mm"

            # Update Widgets
            self.axis_position_label.configure(
                text=self.axis.AxisData.Name + " \n" +
                str(round(self.axis.AxisData.Position, 2)) + " " + unit_string,
                bg=self.colors[0], fg=self.colors[5], justify=LEFT, font=("Arial Black", 12)
            )

        def jog_positive(self, button_state, half_speed):
            if connection_manager.is_connected():
                client = connection_manager.client
                i = self.axis.AxisData.AxisNo
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arHalfSpeed[" + str(i) + "]"
                ).set_value(half_speed)
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arJogPositive[" + str(i) + "]"
                ).set_value(button_state)

        def jog_negative(self, button_state, half_speed):
            if connection_manager.is_connected():
                client = connection_manager.client
                i = self.axis.AxisData.AxisNo
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arHalfSpeed[" + str(i) + "]"
                ).set_value(half_speed)
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arJogNegative[" + str(i) + "]"
                ).set_value(button_state)

        def go_to(self):
            if connection_manager.is_connected():
                client = connection_manager.client
                i = self.axis.AxisData.AxisNo
                print(self.go_to_entry.get())
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arGoToPosition[" + str(i) + "]"
                ).set_value(float(self.go_to_entry.get()))
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arGoToCommand[" + str(i) + "]"
                ).set_value(True)


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
