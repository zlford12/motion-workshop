from motion.Motion import Motion
import opcua
from opcua import ua
from tkinter import *
from utility.ConnectionManagement import ConnectionManagement


class Helical:
    def __init__(self, frame, colors, c: ConnectionManagement, m: Motion):
        # Create Frames
        self.frame = frame
        self.colors = colors
        self.control_frame = Frame(self.frame)

        # Scan Status
        self.scan_running = False

        # Connection Manager
        self.c = c
        self.m = m

        # Create Widgets
        self.start_button = Button(self.control_frame)
        self.pause_button = Button(self.control_frame)
        self.scan_forwards_button = Button(self.control_frame)
        self.scan_backwards_button = Button(self.control_frame)
        self.index_width_label = Label(self.control_frame)
        self.index_width_entry = Entry(self.control_frame)
        self.index_width_unit = Label(self.control_frame)
        self.scan_speed_label = Label(self.control_frame)
        self.scan_speed_entry = Entry(self.control_frame)
        self.scan_speed_unit = Label(self.control_frame)
        self.scan_accel_label = Label(self.control_frame)
        self.scan_accel_entry = Entry(self.control_frame)
        self.scan_accel_unit = Label(self.control_frame)
        self.rotate_start_label = Label(self.control_frame)
        self.rotate_start_entry = Entry(self.control_frame)
        self.rotate_start_unit = Label(self.control_frame)
        self.x_start_label = Label(self.control_frame)
        self.x_start_entry = Entry(self.control_frame)
        self.x_start_unit = Label(self.control_frame)
        self.x_stop_label = Label(self.control_frame)
        self.x_stop_entry = Entry(self.control_frame)
        self.x_stop_unit = Label(self.control_frame)
        self.y_position_label = Label(self.control_frame)
        self.y_position_entry = Entry(self.control_frame)
        self.y_position_unit = Label(self.control_frame)
        self.z_position_label = Label(self.control_frame)
        self.z_position_entry = Entry(self.control_frame)
        self.z_position_unit = Label(self.control_frame)

        # Axes
        self.axes = self.m.axis_list
        self.axis_names = ["None"]
        for axis in self.axes:
            if not axis.axis_data.Offset:
                self.axis_names.append(axis.axis_data.Name)

        # Axis Labels
        self.scan_axis_label = Label(self.control_frame)
        self.index_axis_label = Label(self.control_frame)
        self.x_axis_label = Label(self.control_frame)
        self.y_axis_label = Label(self.control_frame)
        self.z_axis_label = Label(self.control_frame)
        self.r_axis_label = Label(self.control_frame)

        # Axis Selections
        self.scan_axis_selection = StringVar()
        self.index_axis_selection = StringVar()
        self.x_axis_selection = StringVar()
        self.y_axis_selection = StringVar()
        self.z_axis_selection = StringVar()
        self.r_axis_selection = StringVar()

        # Axis Menus
        self.scan_axis_menu = OptionMenu(self.control_frame, self.scan_axis_selection, *self.axis_names)
        self.index_axis_menu = OptionMenu(self.control_frame, self.index_axis_selection, *self.axis_names)
        self.x_axis_menu = OptionMenu(self.control_frame, self.x_axis_selection, *self.axis_names)
        self.y_axis_menu = OptionMenu(self.control_frame, self.y_axis_selection, *self.axis_names)
        self.z_axis_menu = OptionMenu(self.control_frame, self.z_axis_selection, *self.axis_names)
        self.r_axis_menu = OptionMenu(self.control_frame, self.r_axis_selection, *self.axis_names)

    def configure(self):
        # Configure Frame
        self.control_frame.configure(bg=self.colors[3], width=600)

        # Parameters
        entry_width = 10
        button_width = 20
        label_font = ("Arial Black", 10)
        menu_font = ("Arial Black", 8)

        # Configure Widgets
        self.start_button.configure(
            text="Start\nScan", width=button_width, height=2, bg=self.colors[4],
            command=lambda: self.start_exit_scan()
        )
        self.pause_button.configure(
            text="Pause\nScan", width=button_width, height=2, bg=self.colors[4],
            command=lambda: self.pause_scan()
        )
        self.scan_forwards_button.configure(
            text="Scan\nForwards", width=button_width, height=2, bg=self.colors[4],
            command=lambda: self.scan_forwards()
        )
        self.scan_backwards_button.configure(
            text="Scan\nBackwards", width=button_width, height=2, bg=self.colors[4],
            command=lambda: self.scan_backwards()
        )
        self.index_width_label.configure(
            text="Index Width", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.index_width_entry.configure(
            width=entry_width
        )
        self.index_width_unit.configure(
            text="mm", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.scan_speed_label.configure(
            text="Scan Speed", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.scan_speed_entry.configure(
            width=entry_width
        )
        self.scan_speed_unit.configure(
            text="deg/s", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.scan_accel_label.configure(
            text="Scan Accel", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.scan_accel_entry.configure(
            width=entry_width
        )
        self.scan_accel_unit.configure(
            text="rad/s^2", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotate_start_label.configure(
            text="Rotate Start Position", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotate_start_entry.configure(
            width=entry_width
        )
        self.rotate_start_unit.configure(
            text="deg", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.x_start_label.configure(
            text="X Start Position", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.x_start_entry.configure(
            width=entry_width
        )
        self.x_start_unit.configure(
            text="mm", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.x_stop_label.configure(
            text="X Stop Position", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.x_stop_entry.configure(
            width=entry_width
        )
        self.x_stop_unit.configure(
            text="mm", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.y_position_label.configure(
            text="Y Position", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.y_position_entry.configure(
            width=entry_width
        )
        self.y_position_unit.configure(
            text="mm", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.z_position_label.configure(
            text="Z Position", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.z_position_entry.configure(
            width=entry_width
        )
        self.z_position_unit.configure(
            text="mm", bg=self.colors[3], font=label_font, justify=LEFT
        )

        self.scan_axis_label.configure(
            text="Scan Axis", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.index_axis_label.configure(
            text="Index Axis", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.x_axis_label.configure(
            text="X Axis", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.y_axis_label.configure(
            text="Y Axis", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.z_axis_label.configure(
            text="Z Axis", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.r_axis_label.configure(
            text="Rotate Axis", bg=self.colors[3], font=label_font, justify=LEFT
        )

        self.scan_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.index_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.x_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.y_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.z_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.r_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )

    def draw_controls(self):
        # Configure Widgets
        self.configure()

        # Draw Frames
        self.control_frame.grid(row=0, column=0)

        # Draw Widgets
        self.start_button.grid(
            row=0, column=0, columnspan=2, padx=(10, 5), pady=10
        )
        self.pause_button.grid(
            row=0, column=2, columnspan=2, padx=(5, 10), pady=10
        )
        self.scan_forwards_button.grid(
            row=1, column=0, columnspan=2, padx=(10, 5), pady=10
        )
        self.scan_backwards_button.grid(
            row=1, column=2, columnspan=2, padx=(5, 10), pady=10
        )
        self.index_width_label.grid(
            row=2, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.index_width_entry.grid(
            row=3, column=0, padx=5, pady=(1, 10)
        )
        self.index_width_unit.grid(
            row=3, column=1, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.scan_speed_label.grid(
            row=2, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.scan_speed_entry.grid(
            row=3, column=2, padx=5, pady=(1, 10)
        )
        self.scan_speed_unit.grid(
            row=3, column=3, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.scan_accel_label.grid(
            row=4, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.scan_accel_entry.grid(
            row=5, column=0, padx=5, pady=(1, 10)
        )
        self.scan_accel_unit.grid(
            row=5, column=1, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.rotate_start_label.grid(
            row=4, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.rotate_start_entry.grid(
            row=5, column=2, padx=5, pady=(1, 10)
        )
        self.rotate_start_unit.grid(
            row=5, column=3, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.x_start_label.grid(
            row=6, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.x_start_entry.grid(
            row=7, column=0, padx=5, pady=(1, 10)
        )
        self.x_start_unit.grid(
            row=7, column=1, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.x_stop_label.grid(
            row=6, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.x_stop_entry.grid(
            row=7, column=2, padx=5, pady=(1, 10)
        )
        self.x_stop_unit.grid(
            row=7, column=3, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.y_position_label.grid(
            row=8, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.y_position_entry.grid(
            row=9, column=0, padx=5, pady=(1, 10)
        )
        self.y_position_unit.grid(
            row=9, column=1, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.z_position_label.grid(
            row=8, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.z_position_entry.grid(
            row=9, column=2, padx=5, pady=(1, 10)
        )
        self.z_position_unit.grid(
            row=9, column=3, padx=(1, 5), pady=(1, 10), sticky=W
        )

        self.scan_axis_label.grid(
            row=10, column=0, padx=5, pady=5
        )
        self.scan_axis_menu.grid(
            row=10, column=1, padx=5, pady=5
        )
        self.index_axis_label.grid(
            row=10, column=2, padx=5, pady=5
        )
        self.index_axis_menu.grid(
            row=10, column=3, padx=5, pady=5
        )
        self.x_axis_label.grid(
            row=11, column=0, padx=5, pady=5
        )
        self.x_axis_menu.grid(
            row=11, column=1, padx=5, pady=5
        )
        self.y_axis_label.grid(
            row=11, column=2, padx=5, pady=5
        )
        self.y_axis_menu.grid(
            row=11, column=3, padx=5, pady=5
        )
        self.z_axis_label.grid(
            row=12, column=0, padx=5, pady=5
        )
        self.z_axis_menu.grid(
            row=12, column=1, padx=5, pady=5
        )
        self.r_axis_label.grid(
            row=12, column=2, padx=5, pady=5
        )
        self.r_axis_menu.grid(
            row=12, column=3, padx=5, pady=5
        )

    def start_exit_scan(self):
        if not self.c.is_connected():
            return

        if self.scan_running:
            # Exit Scan
            self.c.client.get_node("ns=2;s=Application.Helical_Vars.iHelicalCommand") \
                .set_value(5, varianttype=ua.VariantType.Int16)
        else:
            # Read Scan Parameter Node
            node_array: [opcua.Node] = []
            for child in self.c.client.get_node(
                    "ns=2;s=Application.Helical_Vars.arHelicalValues"
            ).get_children():
                if child.get_data_type_as_variant_type() == ua.VariantType.Double:
                    node_array.append(child)
            values_array: [float] = [float(0)] * len(node_array)

            # Set Scan Parameters
            values_array[0] = float(self.axis_number_from_name(self.scan_axis_selection.get()))
            values_array[1] = float(self.axis_number_from_name(self.index_axis_selection.get()))
            values_array[2] = float(self.axis_number_from_name(self.x_axis_selection.get()))
            values_array[3] = float(self.axis_number_from_name(self.y_axis_selection.get()))
            values_array[4] = float(self.axis_number_from_name(self.z_axis_selection.get()))
            values_array[5] = float(self.axis_number_from_name(self.r_axis_selection.get()))

            values_array[6] = float(self.index_width_entry.get())
            values_array[7] = float(self.scan_speed_entry.get())
            values_array[8] = float(self.scan_accel_entry.get())

            values_array[9] = float(self.x_start_entry.get())
            values_array[10] = float(self.x_stop_entry.get())
            values_array[11] = float(self.y_position_entry.get())
            values_array[12] = float(self.z_position_entry.get())
            values_array[13] = float(self.rotate_start_entry.get())

            # Write Scan Parameters
            self.c.client.set_values(node_array, values_array)

            # Start Scan
            self.c.client.get_node("ns=2;s=Application.Helical_Vars.iHelicalCommand") \
                .set_value(1, varianttype=ua.VariantType.Int16)

    def axis_number_from_name(self, name: str):
        number = 0
        for axis in self.axes:
            if axis.axis_data.Name == name:
                number = axis.axis_data.AxisNo
                break

        return float(number)

    def pause_scan(self):
        if (not self.c.is_connected()) or (not self.scan_running):
            return

        self.c.client.get_node("ns=2;s=Application.Helical_Vars.iHelicalCommand") \
            .set_value(2, varianttype=ua.VariantType.Int16)

    def scan_forwards(self):
        if (not self.c.is_connected()) or (not self.scan_running):
            return

        self.c.client.get_node("ns=2;s=Application.Helical_Vars.iHelicalCommand") \
            .set_value(3, varianttype=ua.VariantType.Int16)

    def scan_backwards(self):
        if (not self.c.is_connected()) or (not self.scan_running):
            return

        self.c.client.get_node("ns=2;s=Application.Helical_Vars.iHelicalCommand") \
            .set_value(4, varianttype=ua.VariantType.Int16)

    def update(self):
        if self.c.is_connected():
            self.scan_running = self.c.client.get_node(
                "ns=2;s=Application.Helical_Vars.arHelicalOutputs[0]"
            ).get_value()

        if self.scan_running and (self.start_button["text"] == "Start\nScan"):
            self.start_button.configure(text="Exit\nScan")
        elif not self.scan_running and (self.start_button["text"] == "Exit\nScan"):
            self.start_button.configure(text="Start\nScan")
