from motion.Motion import Motion
import opcua
from opcua import ua
from tkinter import *
from utility.ConnectionManagement import ConnectionManagement


class P2P:
    def __init__(self, frame, colors, c: ConnectionManagement, m: Motion):
        # Create Frames
        self.frame = frame
        self.colors = colors
        self.control_frame = Frame(self.frame)
        self.points_frame = Frame(self.frame)

        # Connection Manager
        self.c = c
        self.m = m

        # Create Widgets
        self.start_button = Button(self.control_frame)
        self.stop_button = Button(self.control_frame)
        self.linear_velocity_label = Label(self.control_frame)
        self.linear_velocity_entry = Entry(self.control_frame)
        self.linear_velocity_unit = Label(self.control_frame)
        self.rotary_velocity_label = Label(self.control_frame)
        self.rotary_velocity_entry = Entry(self.control_frame)
        self.rotary_velocity_unit = Label(self.control_frame)
        self.linear_position_delta_label = Label(self.control_frame)
        self.linear_position_delta_entry = Entry(self.control_frame)
        self.linear_position_delta_unit = Label(self.control_frame)
        self.rotary_position_delta_label = Label(self.control_frame)
        self.rotary_position_delta_entry = Entry(self.control_frame)
        self.rotary_position_delta_unit = Label(self.control_frame)
        self.dwell_time_label = Label(self.control_frame)
        self.dwell_time_entry = Entry(self.control_frame)
        self.dwell_time_unit = Label(self.control_frame)
        self.vector_mode_selection = Checkbutton(self.control_frame)
        self.vector_mode_value = IntVar()

        # Axes
        self.axes = self.m.axis_list
        self.axis_names = ["None"]
        for axis in self.axes:
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

        # Axis Menus
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

        # Position Entries
        self.axis_0_entry = Entry(self.control_frame)
        self.axis_1_entry = Entry(self.control_frame)
        self.axis_2_entry = Entry(self.control_frame)
        self.axis_3_entry = Entry(self.control_frame)
        self.axis_4_entry = Entry(self.control_frame)
        self.axis_5_entry = Entry(self.control_frame)
        self.axis_6_entry = Entry(self.control_frame)
        self.axis_7_entry = Entry(self.control_frame)
        self.axis_8_entry = Entry(self.control_frame)
        self.axis_9_entry = Entry(self.control_frame)

    def configure(self):
        # Configure Frame
        self.control_frame.configure(bg=self.colors[3], width=500)

        # Parameters
        entry_width = 10
        label_font = ("Arial Black", 10)
        menu_font = ("Arial Black", 8)

        # Configure Widgets
        self.start_button.configure(
            text="Start Scan", width=12, height=2, bg=self.colors[4],
            command=lambda: self.start_scan()
        )
        self.stop_button.configure(
            text="Stop Scan", width=12, height=2, bg=self.colors[4],
            command=lambda: self.stop_scan()
        )
        self.linear_velocity_label.configure(
            text="Linear Velocity", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.linear_velocity_entry.configure(
            width=entry_width
        )
        self.linear_velocity_unit.configure(
            text="mm/min", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotary_velocity_label.configure(
            text="Rotary Velocity", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotary_velocity_entry.configure(
            width=entry_width
        )
        self.rotary_velocity_unit.configure(
            text="deg/s", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.linear_position_delta_label.configure(
            text="Linear Position\nDelta", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.linear_position_delta_entry.configure(
            width=entry_width
        )
        self.linear_position_delta_unit.configure(
            text="mm", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotary_position_delta_label.configure(
            text="Rotary Position\nDelta", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotary_position_delta_entry.configure(
            width=entry_width
        )
        self.rotary_position_delta_unit.configure(
            text="deg", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.dwell_time_label.configure(
            text="Dwell Time", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.dwell_time_entry.configure(
            width=entry_width
        )
        self.dwell_time_unit.configure(
            text="ms", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.vector_mode_selection.configure(
            text="Vector Mode", bg=self.colors[3], font=label_font, justify=LEFT,
            variable=self.vector_mode_value
        )

        self.axis_0_label.configure(
            text="Axis 0", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_1_label.configure(
            text="Axis 1", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_2_label.configure(
            text="Axis 2", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_3_label.configure(
            text="Axis 3", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_4_label.configure(
            text="Axis 4", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_5_label.configure(
            text="Axis 5", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_6_label.configure(
            text="Axis 6", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_7_label.configure(
            text="Axis 7", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_8_label.configure(
            text="Axis 8", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.axis_9_label.configure(
            text="Axis 9", bg=self.colors[3], font=label_font, justify=LEFT
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

        self.axis_0_entry.configure(
            width=entry_width
        )
        self.axis_1_entry.configure(
            width=entry_width
        )
        self.axis_2_entry.configure(
            width=entry_width
        )
        self.axis_3_entry.configure(
            width=entry_width
        )
        self.axis_4_entry.configure(
            width=entry_width
        )
        self.axis_5_entry.configure(
            width=entry_width
        )
        self.axis_6_entry.configure(
            width=entry_width
        )
        self.axis_7_entry.configure(
            width=entry_width
        )
        self.axis_8_entry.configure(
            width=entry_width
        )
        self.axis_9_entry.configure(
            width=entry_width
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
        self.stop_button.grid(
            row=0, column=2, columnspan=2, padx=(5, 10), pady=10
        )
        self.linear_velocity_label.grid(
            row=1, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.linear_velocity_entry.grid(
            row=2, column=0, padx=5, pady=(1, 10)
        )
        self.linear_velocity_unit.grid(
            row=2, column=1, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.rotary_velocity_label.grid(
            row=1, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.rotary_velocity_entry.grid(
            row=2, column=2, padx=5, pady=(1, 10)
        )
        self.rotary_velocity_unit.grid(
            row=2, column=3, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.linear_position_delta_label.grid(
            row=3, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.linear_position_delta_entry.grid(
            row=4, column=0, padx=5, pady=(1, 10)
        )
        self.linear_position_delta_unit.grid(
            row=4, column=1, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.rotary_position_delta_label.grid(
            row=3, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.rotary_position_delta_entry.grid(
            row=4, column=2, padx=5, pady=(1, 10)
        )
        self.rotary_position_delta_unit.grid(
            row=4, column=3, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.dwell_time_label.grid(
            row=5, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.dwell_time_entry.grid(
            row=6, column=0, padx=5, pady=(1, 10)
        )
        self.dwell_time_unit.grid(
            row=6, column=1, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.vector_mode_selection.grid(
            row=5, column=2, rowspan=2, padx=5, pady=5
        )

        self.axis_0_label.grid(
            row=8, column=0, padx=5, pady=5
        )
        self.axis_0_menu.grid(
            row=8, column=1, padx=5, pady=5
        )
        self.axis_0_entry.grid(
            row=8, column=2, padx=5, pady=5, sticky=E
        )
        self.axis_1_label.grid(
            row=9, column=0, padx=5, pady=5
        )
        self.axis_1_menu.grid(
            row=9, column=1, padx=5, pady=5
        )
        self.axis_1_entry.grid(
            row=9, column=2, padx=5, pady=5, sticky=E
        )
        self.axis_2_label.grid(
            row=10, column=0, padx=5, pady=5
        )
        self.axis_2_menu.grid(
            row=10, column=1, padx=5, pady=5
        )
        self.axis_2_entry.grid(
            row=10, column=2, padx=5, pady=5, sticky=E
        )
        self.axis_3_label.grid(
            row=11, column=0, padx=5, pady=5
        )
        self.axis_3_menu.grid(
            row=11, column=1, padx=5, pady=5
        )
        self.axis_3_entry.grid(
            row=11, column=2, padx=5, pady=5, sticky=E
        )
        self.axis_4_label.grid(
            row=12, column=0, padx=5, pady=5
        )
        self.axis_4_menu.grid(
            row=12, column=1, padx=5, pady=5
        )
        self.axis_4_entry.grid(
            row=12, column=2, padx=5, pady=5, sticky=E
        )
        self.axis_5_label.grid(
            row=13, column=0, padx=5, pady=5
        )
        self.axis_5_menu.grid(
            row=13, column=1, padx=5, pady=5
        )
        self.axis_5_entry.grid(
            row=13, column=2, padx=5, pady=5, sticky=E
        )
        self.axis_6_label.grid(
            row=14, column=0, padx=5, pady=5
        )
        self.axis_6_menu.grid(
            row=14, column=1, padx=5, pady=5
        )
        self.axis_6_entry.grid(
            row=14, column=2, padx=5, pady=5, sticky=E
        )
        self.axis_7_label.grid(
            row=15, column=0, padx=5, pady=5
        )
        self.axis_7_menu.grid(
            row=15, column=1, padx=5, pady=5
        )
        self.axis_7_entry.grid(
            row=15, column=2, padx=5, pady=5, sticky=E
        )
        self.axis_8_label.grid(
            row=16, column=0, padx=5, pady=5
        )
        self.axis_8_menu.grid(
            row=16, column=1, padx=5, pady=5
        )
        self.axis_8_entry.grid(
            row=16, column=2, padx=5, pady=5, sticky=E
        )
        self.axis_9_label.grid(
            row=17, column=0, padx=5, pady=5
        )
        self.axis_9_menu.grid(
            row=17, column=1, padx=5, pady=5
        )
        self.axis_9_entry.grid(
            row=17, column=2, padx=5, pady=5, sticky=E
        )

    def axis_number_from_name(self, name: str):
        number = 0
        for axis in self.axes:
            if axis.axis_data.Name == name:
                number = axis.axis_data.AxisNo
                break

        return float(number)

    def start_scan(self):
        # Read Scan Parameter Node
        node_array: [opcua.Node] = []
        for child in self.c.client.get_node(
            "ns=2;s=Application.P2P_Vars.arP2PValues"
        ).get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.Double:
                node_array.append(child)
        values_array: [float] = [float(0)] * len(node_array)

        # Set Scan Parameters
        values_array[0] = float(self.linear_velocity_entry.get())
        values_array[1] = float(self.rotary_velocity_entry.get())
        values_array[2] = float(self.dwell_time_entry.get())
        values_array[3] = float(self.linear_position_delta_entry.get())
        values_array[4] = float(self.rotary_position_delta_entry.get())
        values_array[5] = float(self.vector_mode_value.get())

        values_array[10] = float(self.axis_number_from_name(self.axis_0_selection.get()))
        values_array[11] = float(self.axis_number_from_name(self.axis_1_selection.get()))
        values_array[12] = float(self.axis_number_from_name(self.axis_2_selection.get()))
        values_array[13] = float(self.axis_number_from_name(self.axis_3_selection.get()))
        values_array[14] = float(self.axis_number_from_name(self.axis_4_selection.get()))
        values_array[15] = float(self.axis_number_from_name(self.axis_5_selection.get()))
        values_array[16] = float(self.axis_number_from_name(self.axis_6_selection.get()))
        values_array[17] = float(self.axis_number_from_name(self.axis_7_selection.get()))
        values_array[18] = float(self.axis_number_from_name(self.axis_8_selection.get()))
        values_array[19] = float(self.axis_number_from_name(self.axis_9_selection.get()))

        if self.axis_0_entry.get() != "":
            values_array[20] = float(self.axis_0_entry.get())
        else:
            values_array[20] = 0.0
        if self.axis_1_entry.get() != "":
            values_array[21] = float(self.axis_1_entry.get())
        else:
            values_array[21] = 0.0
        if self.axis_2_entry.get() != "":
            values_array[22] = float(self.axis_2_entry.get())
        else:
            values_array[22] = 0.0
        if self.axis_3_entry.get() != "":
            values_array[23] = float(self.axis_3_entry.get())
        else:
            values_array[23] = 0.0
        if self.axis_4_entry.get() != "":
            values_array[24] = float(self.axis_4_entry.get())
        else:
            values_array[24] = 0.0
        if self.axis_5_entry.get() != "":
            values_array[25] = float(self.axis_5_entry.get())
        else:
            values_array[25] = 0.0
        if self.axis_6_entry.get() != "":
            values_array[26] = float(self.axis_6_entry.get())
        else:
            values_array[26] = 0.0
        if self.axis_7_entry.get() != "":
            values_array[27] = float(self.axis_7_entry.get())
        else:
            values_array[27] = 0.0
        if self.axis_8_entry.get() != "":
            values_array[28] = float(self.axis_8_entry.get())
        else:
            values_array[28] = 0.0
        if self.axis_9_entry.get() != "":
            values_array[29] = float(self.axis_9_entry.get())
        else:
            values_array[29] = 0.0

        # Write Scan Parameters
        self.c.client.set_values(node_array, values_array)

        # Start Scan
        self.c.client.get_node("ns=2;s=Application.P2P_Vars.iP2PCommand").set_value(1, varianttype=ua.VariantType.Int16)

    def stop_scan(self):
        # Stop Scan
        self.c.client.get_node("ns=2;s=Application.P2P_Vars.iP2PCommand").set_value(2, varianttype=ua.VariantType.Int16)
