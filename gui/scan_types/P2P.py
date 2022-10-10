import opcua
from opcua import ua
from tkinter import *
from utility.ConnectionManagement import ConnectionManagement


class P2P:
    def __init__(self, frame, colors, c: ConnectionManagement):
        # Create Frames
        self.frame = frame
        self.colors = colors
        self.control_frame = Frame(self.frame)
        self.points_frame = Frame(self.frame)

        # Connection Manager
        self.c = c

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

        self.add_point_button = Button(self.control_frame)
        self.remove_point_button = Button(self.control_frame)
        self.copy_point_button = Button(self.control_frame)
        self.go_to_point_button = Button(self.control_frame)

    def configure(self):
        # Configure Frame
        self.control_frame.configure(bg=self.colors[3], width=500)

        # Parameters
        entry_width = 10
        label_font = ("Arial Black", 10)

        # Configure Widgets
        self.start_button.configure(
            text="Start Scan", width=12, height=2, bg=self.colors[4],
            command=lambda: self.start_scan()
        )
        self.stop_button.configure(
            text="Stop Scan", width=12, height=2, bg=self.colors[4]
        )
        self.linear_velocity_label.configure(
            text="Linear Velocity", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.linear_velocity_entry.configure(
            width=entry_width
        )
        self.linear_velocity_unit.configure(
            text="mm/s", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotary_velocity_label.configure(
            text="Rotary Velocity", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotary_velocity_entry.configure(
            width=entry_width
        )
        self.rotary_velocity_unit.configure(
            text="RPM", bg=self.colors[3], font=label_font, justify=LEFT
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

        values_array[10] = float(1)     # X
        values_array[11] = float(2)     # Y
        values_array[12] = float(3)     # Z
        values_array[13] = float(4)     # S
        values_array[14] = float(5)     # G

        values_array[20] = float(5000)  # X
        values_array[21] = float(1800)   # Y
        values_array[22] = float(500)   # Z
        values_array[23] = float(0)     # S
        values_array[24] = float(0)     # G

        # Write Scan Parameters
        self.c.client.set_values(node_array, values_array)

        # Start Scan
        self.c.client.get_node("ns=2;s=Application.P2P_Vars.iP2PCommand").set_value(1, varianttype=ua.VariantType.Int16)
