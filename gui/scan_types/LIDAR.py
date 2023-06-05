from motion.Motion import Motion
import opcua
from opcua import ua
from tkinter import *
from utility.ConnectionManagement import ConnectionManagement


class LIDAR:
    def __init__(self, frame, colors, c: ConnectionManagement, m: Motion):
        # Create Frames
        self.frame = frame
        self.colors = colors
        self.control_frame = Frame(self.frame)

        # Connection Manager
        self.c = c
        self.m = m

        # Create Widgets
        self.start_button = Button(self.control_frame)
        self.pps_label = Label(self.control_frame)
        self.pps_entry = Entry(self.control_frame)
        self.max_distance_label = Label(self.control_frame)
        self.max_distance_entry = Entry(self.control_frame)
        self.scan_width_label = Label(self.control_frame)
        self.scan_width_entry = Entry(self.control_frame)
        self.resolution_label = Label(self.control_frame)
        self.resolution_entry = Entry(self.control_frame)
        self.min_density_label = Label(self.control_frame)
        self.min_density_entry = Entry(self.control_frame)
        self.line_spacing_label = Label(self.control_frame)
        self.line_spacing_entry = Entry(self.control_frame)
        self.x_start_label = Label(self.control_frame)
        self.x_start_entry = Entry(self.control_frame)
        self.x_stop_label = Label(self.control_frame)
        self.x_stop_entry = Entry(self.control_frame)
        self.z_start_label = Label(self.control_frame)
        self.z_start_entry = Entry(self.control_frame)
        self.z_stop_label = Label(self.control_frame)
        self.z_stop_entry = Entry(self.control_frame)
        self.tcp_offset_label = Label(self.control_frame)
        self.tcp_offset_x_label = Label(self.control_frame)
        self.tcp_offset_x_entry = Entry(self.control_frame)
        self.tcp_offset_y_label = Label(self.control_frame)
        self.tcp_offset_y_entry = Entry(self.control_frame)
        self.tcp_offset_z_label = Label(self.control_frame)
        self.tcp_offset_z_entry = Entry(self.control_frame)

        # Axes
        self.axes = self.m.axis_list
        self.axis_names = ["None"]
        for axis in self.axes:
            if not axis.axis_data.Offset and not axis.axis_data.Linkable and not axis.axis_data.ScanAxis:
                self.axis_names.append(axis.axis_data.Name)

        # Axis Labels
        self.axis_0_label = Label(self.control_frame)
        self.axis_1_label = Label(self.control_frame)
        self.axis_2_label = Label(self.control_frame)
        self.axis_3_label = Label(self.control_frame)
        self.axis_4_label = Label(self.control_frame)
        self.axis_5_label = Label(self.control_frame)
        self.axis_6_label = Label(self.control_frame)
        self.axis_7_label = Label(self.control_frame)
        self.axis_8_label = Label(self.control_frame)
        self.axis_9_label = Label(self.control_frame)

        # Axis Selections
        self.axis_0_selection = StringVar()
        self.axis_1_selection = StringVar()
        self.axis_2_selection = StringVar()
        self.axis_3_selection = StringVar()
        self.axis_4_selection = StringVar()
        self.axis_5_selection = StringVar()
        self.axis_6_selection = StringVar()
        self.axis_7_selection = StringVar()
        self.axis_8_selection = StringVar()
        self.axis_9_selection = StringVar()

        # Axis Names
        self.axis_0_menu = OptionMenu(self.control_frame, self.axis_0_selection, *self.axis_names)
        self.axis_1_menu = OptionMenu(self.control_frame, self.axis_1_selection, *self.axis_names)
        self.axis_2_menu = OptionMenu(self.control_frame, self.axis_2_selection, *self.axis_names)
        self.axis_3_menu = OptionMenu(self.control_frame, self.axis_3_selection, *self.axis_names)
        self.axis_4_menu = OptionMenu(self.control_frame, self.axis_4_selection, *self.axis_names)
        self.axis_5_menu = OptionMenu(self.control_frame, self.axis_5_selection, *self.axis_names)
        self.axis_6_menu = OptionMenu(self.control_frame, self.axis_6_selection, *self.axis_names)
        self.axis_7_menu = OptionMenu(self.control_frame, self.axis_7_selection, *self.axis_names)
        self.axis_8_menu = OptionMenu(self.control_frame, self.axis_8_selection, *self.axis_names)
        self.axis_9_menu = OptionMenu(self.control_frame, self.axis_9_selection, *self.axis_names)

    def configure(self):
        # Configure Frame
        self.control_frame.configure(bg=self.colors[3], width=500)

        # Parameters
        entry_width = 10
        label_font = ("Arial Black", 10)
        menu_font = ("Arial Black", 10)

        # Configure Widgets
        self.start_button.configure(
            text="Start Scan", width=24, height=2, bg=self.colors[4],
            command=lambda: self.start_scan()
        )
        self.pps_label.configure(
            text="Points\nPer Scan", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.pps_entry.configure(
            width=entry_width
        )
        self.max_distance_label.configure(
            text="Max\nDistance (mm)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.max_distance_entry.configure(
            width=entry_width
        )
        self.scan_width_label.configure(
            text="Scan\nWidth (mm)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.scan_width_entry.configure(
            width=entry_width
        )
        self.resolution_label.configure(
            text="Resolution (mm)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.resolution_entry.configure(
            width=entry_width
        )
        self.min_density_label.configure(
            text="Minimum\nDensity (mm)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.min_density_entry.configure(
            width=entry_width
        )
        self.line_spacing_label.configure(
            text="Line\nSpacing (mm)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.line_spacing_entry.configure(
            width=entry_width
        )
        self.x_start_label.configure(
            text="X Start", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.x_start_entry.configure(
            width=entry_width
        )
        self.x_stop_label.configure(
            text="X Stop", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.x_stop_entry.configure(
            width=entry_width
        )
        self.z_start_label.configure(
            text="Z Start", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.z_start_entry.configure(
            width=entry_width
        )
        self.z_stop_label.configure(
            text="Z Stop", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.z_stop_entry.configure(
            width=entry_width
        )
        self.tcp_offset_label.configure(
            text="TCP Offset", bg=self.colors[3], font=label_font, justify=CENTER
        )
        self.tcp_offset_x_label.configure(
            text="X", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.tcp_offset_x_entry.configure(
            width=entry_width
        )
        self.tcp_offset_y_label.configure(
            text="Y", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.tcp_offset_y_entry.configure(
            width=entry_width
        )
        self.tcp_offset_z_label.configure(
            text="Z", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.tcp_offset_z_entry.configure(
            width=entry_width
        )

        self.axis_0_label.configure(
            text="X Axis", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_1_label.configure(
            text="Y Axis", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_2_label.configure(
            text="Z Axis", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_3_label.configure(
            text="Water Path", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_4_label.configure(
            text="Gimbal", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_5_label.configure(
            text="Gimbal", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_6_label.configure(
            text="Gimbal", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_7_label.configure(
            text="Gimbal", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_8_label.configure(
            text="Gimbal", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_9_label.configure(
            text="Gimbal", bg=self.colors[3], font=label_font, justify=LEFT
        )

        self.axis_0_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.axis_1_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.axis_2_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.axis_3_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.axis_4_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.axis_5_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.axis_6_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.axis_7_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.axis_8_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.axis_9_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )

    def draw_controls(self):
        # Configure Widgets
        self.configure()

        # Draw Frames
        self.control_frame.grid(row=0, column=0)

        # Draw Widgets
        self.start_button.grid(
            row=0, column=0, columnspan=4, padx=10, pady=10
        )
        self.pps_label.grid(
            row=1, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.pps_entry.grid(
            row=2, column=0, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.max_distance_label.grid(
            row=1, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.max_distance_entry.grid(
            row=2, column=2, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.scan_width_label.grid(
            row=3, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.scan_width_entry.grid(
            row=4, column=0, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.resolution_label.grid(
            row=3, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.resolution_entry.grid(
            row=4, column=2, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.min_density_label.grid(
            row=5, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.min_density_entry.grid(
            row=6, column=0, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.line_spacing_label.grid(
            row=5, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.line_spacing_entry.grid(
            row=6, column=2, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.x_start_label.grid(
            row=7, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.x_start_entry.grid(
            row=8, column=0, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.x_stop_label.grid(
            row=7, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.x_stop_entry.grid(
            row=8, column=2, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.z_start_label.grid(
            row=9, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.z_start_entry.grid(
            row=10, column=0, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.z_stop_label.grid(
            row=9, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.z_stop_entry.grid(
            row=10, column=2, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.tcp_offset_label.grid(
            row=11, column=0, columnspan=4, padx=5, pady=(10, 1), sticky=W
        )
        self.tcp_offset_x_label.grid(
            row=12, column=0, columnspan=1, padx=5, pady=(10, 1), sticky=W
        )
        self.tcp_offset_x_entry.grid(
            row=13, column=0, columnspan=1, padx=5, pady=(1, 10), sticky=W
        )
        self.tcp_offset_y_label.grid(
            row=12, column=1, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.tcp_offset_y_entry.grid(
            row=13, column=1, columnspan=2, padx=5, pady=(1, 10), sticky=W
        )
        self.tcp_offset_z_label.grid(
            row=12, column=3, columnspan=1, padx=5, pady=(10, 1), sticky=W
        )
        self.tcp_offset_z_entry.grid(
            row=13, column=3, columnspan=1, padx=5, pady=(1, 10), sticky=W
        )

        self.axis_0_label.grid(
            row=14, column=0, padx=5, pady=5
        )
        self.axis_0_menu.grid(
            row=14, column=1, columnspan=3, padx=5, pady=5
        )
        self.axis_1_label.grid(
            row=15, column=0, padx=5, pady=5
        )
        self.axis_1_menu.grid(
            row=15, column=1, columnspan=3, padx=5, pady=5
        )
        self.axis_2_label.grid(
            row=16, column=0, padx=5, pady=5
        )
        self.axis_2_menu.grid(
            row=16, column=1, columnspan=3, padx=5, pady=5
        )
        self.axis_3_label.grid(
            row=17, column=0, padx=5, pady=5
        )
        self.axis_3_menu.grid(
            row=17, column=1, columnspan=3, padx=5, pady=5
        )
        self.axis_4_label.grid(
            row=18, column=0, padx=5, pady=5
        )
        self.axis_4_menu.grid(
            row=18, column=1, columnspan=3, padx=5, pady=5
        )
        self.axis_5_label.grid(
            row=19, column=0, padx=5, pady=5
        )
        self.axis_5_menu.grid(
            row=19, column=1, columnspan=3, padx=5, pady=5
        )
        self.axis_6_label.grid(
            row=20, column=0, padx=5, pady=5
        )
        self.axis_6_menu.grid(
            row=20, column=1, columnspan=3, padx=5, pady=5
        )
        self.axis_7_label.grid(
            row=21, column=0, padx=5, pady=5
        )
        self.axis_7_menu.grid(
            row=21, column=1, columnspan=3, padx=5, pady=5
        )
        self.axis_8_label.grid(
            row=22, column=0, padx=5, pady=5
        )
        self.axis_8_menu.grid(
            row=22, column=1, columnspan=3, padx=5, pady=5
        )
        self.axis_9_label.grid(
            row=23, column=0, padx=5, pady=5
        )
        self.axis_9_menu.grid(
            row=23, column=1, columnspan=3, padx=5, pady=5
        )

    def start_scan(self):
        # Read Scan Parameter Node
        node_array: [opcua.Node] = []
        for child in self.c.client.get_node(
            "ns=2;s=Application.LIDAR_Vars.arLIDARValues"
        ).get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.Double:
                node_array.append(child)
        values_array: [float] = [float(0)] * len(node_array)

        # Set Scan Parameters
        values_array[0] = float(self.pps_entry.get())
        values_array[1] = float(self.max_distance_entry.get())
        values_array[2] = float(self.scan_width_entry.get())
        values_array[3] = float(self.resolution_entry.get())
        values_array[4] = float(self.min_density_entry.get())
        values_array[5] = float(self.tcp_offset_x_entry.get())
        values_array[6] = float(self.tcp_offset_y_entry.get())
        values_array[7] = float(self.tcp_offset_z_entry.get())
        values_array[8] = float(self.x_start_entry.get())
        values_array[9] = float(self.x_stop_entry.get())
        values_array[10] = float(self.z_start_entry.get())
        values_array[11] = float(self.z_stop_entry.get())
        values_array[12] = float(self.line_spacing_entry.get())

        values_array[20] = float(self.axis_number_from_name(self.axis_0_selection.get()))
        values_array[21] = float(self.axis_number_from_name(self.axis_1_selection.get()))
        values_array[22] = float(self.axis_number_from_name(self.axis_2_selection.get()))
        values_array[23] = float(self.axis_number_from_name(self.axis_3_selection.get()))
        values_array[24] = float(self.axis_number_from_name(self.axis_4_selection.get()))
        values_array[25] = float(self.axis_number_from_name(self.axis_5_selection.get()))
        values_array[26] = float(self.axis_number_from_name(self.axis_6_selection.get()))
        values_array[27] = float(self.axis_number_from_name(self.axis_7_selection.get()))
        values_array[28] = float(self.axis_number_from_name(self.axis_8_selection.get()))
        values_array[29] = float(self.axis_number_from_name(self.axis_9_selection.get()))

        # Write Scan Parameters
        self.c.client.set_values(node_array, values_array)

        # Start Scan
        self.c.client.get_node("ns=2;s=Application.LIDAR_Vars.iLIDARCommand") \
            .set_value(1, varianttype=ua.VariantType.Int16)

    def axis_number_from_name(self, name: str):
        number = 0
        for axis in self.axes:
            if axis.axis_data.Name == name:
                number = axis.axis_data.AxisNo
                break

        return float(number)