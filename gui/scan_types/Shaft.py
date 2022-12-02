from motion.Motion import Motion
import opcua
from opcua import ua
from tkinter import *
from tkinter import messagebox
from utility.ConnectionManagement import ConnectionManagement


class Shaft:
    def __init__(self, frame, colors, c: ConnectionManagement, m: Motion):
        # Create Frames
        self.frame = frame
        self.colors = colors
        self.control_frame = Frame(self.frame)

        # Connection Manager
        self.c = c
        self.m = m

        # Axes
        self.axes = self.m.axis_list
        self.axis_names = ["None"]
        for axis in self.axes:
            if not axis.axis_data.Offset and not axis.axis_data.Linkable and not axis.axis_data.ScanAxis:
                self.axis_names.append(axis.axis_data.Name)

        # Create Widgets
        self.axis_selection_label = Label(self.control_frame)
        self.r_axis_label = Label(self.control_frame)
        self.x_axis_label = Label(self.control_frame)
        self.y_axis_label = Label(self.control_frame)
        self.z_axis_label = Label(self.control_frame)
        self.gx_axis_label = Label(self.control_frame)
        self.gy_axis_label = Label(self.control_frame)
        self.gz_axis_label = Label(self.control_frame)
        self.r_selection = StringVar()
        self.x_selection = StringVar()
        self.y_selection = StringVar()
        self.z_selection = StringVar()
        self.gx_selection = StringVar()
        self.gy_selection = StringVar()
        self.gz_selection = StringVar()
        self.r_axis_menu = OptionMenu(self.control_frame, self.r_selection, *self.axis_names)
        self.x_axis_menu = OptionMenu(self.control_frame, self.x_selection, *self.axis_names)
        self.y_axis_menu = OptionMenu(self.control_frame, self.y_selection, *self.axis_names)
        self.z_axis_menu = OptionMenu(self.control_frame, self.z_selection, *self.axis_names)
        self.gx_axis_menu = OptionMenu(self.control_frame, self.gx_selection, *self.axis_names)
        self.gy_axis_menu = OptionMenu(self.control_frame, self.gy_selection, *self.axis_names)
        self.gz_axis_menu = OptionMenu(self.control_frame, self.gz_selection, *self.axis_names)

        self.scan_parameters_label = Label(self.control_frame)
        self.diameter_label = Label(self.control_frame)
        self.speed_label = Label(self.control_frame)
        self.resolution_label = Label(self.control_frame)
        self.diameter_entry = Entry(self.control_frame)
        self.speed_entry = Entry(self.control_frame)
        self.resolution_entry = Entry(self.control_frame)

        self.scan_label = Label(self.control_frame)
        self.x_position_label = Label(self.control_frame)
        self.y_position_label = Label(self.control_frame)
        self.z_position_label = Label(self.control_frame)
        self.gx_position_label = Label(self.control_frame)
        self.gy_position_label = Label(self.control_frame)
        self.gz_position_label = Label(self.control_frame)
        self.gz_position_label = Label(self.control_frame)
        self.x_position_entry = Entry(self.control_frame)
        self.y_position_entry = Entry(self.control_frame)
        self.z_position_entry = Entry(self.control_frame)
        self.gx_position_entry = Entry(self.control_frame)
        self.gy_position_entry = Entry(self.control_frame)
        self.gz_position_entry = Entry(self.control_frame)

        self.go_to_point_button = Button(self.control_frame)
        self.start_scan_button = Button(self.control_frame)
        self.mark_part_button = Button(self.control_frame)

    def configure(self):
        # Configure Frame
        self.control_frame.configure(bg=self.colors[3], width=500)

        # Parameters
        entry_width = 12
        label_font = ("Arial Black", 10)
        menu_font = ("Arial Black", 8)

        # Configure Widgets
        self.axis_selection_label.configure(
            text="Axis\nSelection:", bg=self.colors[3], font=label_font, justify=CENTER
        )
        self.r_axis_label.configure(
            text="R", bg=self.colors[3], font=label_font, justify=RIGHT
        )
        self.x_axis_label.configure(
            text="X", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.y_axis_label.configure(
            text="Y", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.z_axis_label.configure(
            text="Z", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.gx_axis_label.configure(
            text="Gx", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.gy_axis_label.configure(
            text="Gy", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.gz_axis_label.configure(
            text="Gz", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.r_axis_menu.configure(
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
        self.gx_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.gy_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.gz_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )

        self.scan_parameters_label.configure(
            text="Scan Parameters", bg=self.colors[3], font=label_font, justify=CENTER
        )
        self.diameter_label.configure(
            text="Part Diameter (mm)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.speed_label.configure(
            text="Scan Speed (RPM)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.resolution_label.configure(
            text="Scan Resolution (mm)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.diameter_entry.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.speed_entry.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.resolution_entry.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )

        self.scan_label.configure(
            text="Scan Point", bg=self.colors[3], font=label_font, justify=CENTER
        )
        self.x_position_label.configure(
            text="X", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.y_position_label.configure(
            text="Y", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.z_position_label.configure(
            text="Z", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.gx_position_label.configure(
            text="Gx", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.gy_position_label.configure(
            text="Gy", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.gz_position_label.configure(
            text="Gz", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.x_position_entry.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.y_position_entry.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.z_position_entry.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.gx_position_entry.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.gy_position_entry.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.gz_position_entry.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.go_to_point_button.configure(
            text="Go To\nPoint", width=12, height=2, bg=self.colors[4],
            command=lambda: self.go_to_point()
        )
        self.start_scan_button.configure(
            text="Start\nScan", width=12, height=2, bg=self.colors[4],
            command=lambda: self.start_scan()
        )
        self.mark_part_button.configure(
            text="Mark\nPart", width=12, height=2, bg=self.colors[4],
            command=lambda: self.mark_part()
        )

    def draw_controls(self):
        # Configure Widgets
        self.configure()

        # Draw Frames
        self.control_frame.grid(row=0, column=0)

        # Draw Widgets
        self.axis_selection_label.grid(
            row=0, column=0, padx=5, pady=5
        )
        self.r_axis_label.grid(
            row=0, column=1, padx=5, pady=5, sticky=E
        )
        self.x_axis_label.grid(
            row=1, column=0, padx=5, pady=5, sticky=W
        )
        self.y_axis_label.grid(
            row=1, column=1, padx=5, pady=5, sticky=W
        )
        self.z_axis_label.grid(
            row=1, column=2, padx=5, pady=5, sticky=W
        )
        self.gx_axis_label.grid(
            row=3, column=0, padx=5, pady=5, sticky=W
        )
        self.gy_axis_label.grid(
            row=3, column=1, padx=5, pady=5, sticky=W
        )
        self.gz_axis_label.grid(
            row=3, column=2, padx=5, pady=5, sticky=W
        )
        self.r_axis_menu.grid(
            row=0, column=2, padx=5, pady=5, sticky=W
        )
        self.x_axis_menu.grid(
            row=2, column=0, padx=5, pady=0, sticky=W
        )
        self.y_axis_menu.grid(
            row=2, column=1, padx=5, pady=0, sticky=W
        )
        self.z_axis_menu.grid(
            row=2, column=2, padx=5, pady=0, sticky=W
        )
        self.gx_axis_menu.grid(
            row=4, column=0, padx=5, pady=0, sticky=W
        )
        self.gy_axis_menu.grid(
            row=4, column=1, padx=5, pady=0, sticky=W
        )
        self.gz_axis_menu.grid(
            row=4, column=2, padx=5, pady=0, sticky=W
        )

        self.scan_parameters_label.grid(
            row=5, column=0, columnspan=3, padx=5, pady=(10, 5)
        )
        self.diameter_label.grid(
            row=6, column=0, padx=5, pady=5, sticky=W
        )
        self.speed_label.grid(
            row=6, column=1, padx=5, pady=5, sticky=W
        )
        self.resolution_label.grid(
            row=6, column=2, padx=5, pady=5, sticky=W
        )
        self.diameter_entry.grid(
            row=7, column=0, padx=5, pady=5
        )
        self.speed_entry.grid(
            row=7, column=1, padx=5, pady=5
        )
        self.resolution_entry.grid(
            row=7, column=2, padx=5, pady=5
        )
        self.scan_label.grid(
            row=8, column=0, columnspan=5, padx=5, pady=(10, 5)
        )

        self.x_position_label.grid(
            row=9, column=0, padx=5, pady=5, sticky=W
        )
        self.y_position_label.grid(
            row=9, column=1, padx=5, pady=5, sticky=W
        )
        self.z_position_label.grid(
            row=9, column=2, padx=5, pady=5, sticky=W
        )
        self.gx_position_label.grid(
            row=11, column=0, padx=5, pady=5, sticky=W
        )
        self.gy_position_label.grid(
            row=11, column=1, padx=5, pady=5, sticky=W
        )
        self.gz_position_label.grid(
            row=11, column=2, padx=5, pady=5, sticky=W
        )
        self.x_position_entry.grid(
            row=10, column=0, padx=5, pady=5, sticky=W
        )
        self.y_position_entry.grid(
            row=10, column=1, padx=5, pady=5, sticky=W
        )
        self.z_position_entry.grid(
            row=10, column=2, padx=5, pady=5, sticky=W
        )
        self.gx_position_entry.grid(
            row=12, column=0, padx=5, pady=5, sticky=W
        )
        self.gy_position_entry.grid(
            row=12, column=1, padx=5, pady=5, sticky=W
        )
        self.gz_position_entry.grid(
            row=12, column=2, padx=5, pady=5, sticky=W
        )

        self.go_to_point_button.grid(
            row=13, column=0, padx=5, pady=(10, 5)
        )
        self.start_scan_button.grid(
            row=13, column=1, padx=5, pady=(10, 5)
        )
        self.mark_part_button.grid(
            row=13, column=2, padx=5, pady=(10, 5)
        )

    def axis_number_from_name(self, name: str):
        number = 0
        for axis in self.axes:
            if axis.axis_data.Name == name:
                number = axis.axis_data.AxisNo
                break

        return float(number)

    def axis_position_from_name(self, name: str):
        position = 0.0
        for axis in self.axes:
            if axis.axis_data.Name == name:
                position = axis.axis_data.Position
                break

        return position

    def go_to_point(self):
        # Read Scan Parameter Node
        node_array: [opcua.Node] = []
        for child in self.c.client.get_node(
            "ns=2;s=Application.Shaft_Vars.arShaftValues"
        ).get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.Double:
                node_array.append(child)
        values_array: [float] = [float(0)] * 16

        # Set Scan Parameters
        values_array[0] = self.axis_number_from_name(self.x_selection.get())        # X Axis No
        values_array[1] = self.axis_number_from_name(self.y_selection.get())        # Y Axis No
        values_array[2] = self.axis_number_from_name(self.z_selection.get())        # Z Axis No
        values_array[3] = self.axis_number_from_name(self.gx_selection.get())       # Gx Axis No
        values_array[4] = self.axis_number_from_name(self.gy_selection.get())       # Gy Axis No
        values_array[5] = self.axis_number_from_name(self.gz_selection.get())       # Gz Axis No
        values_array[6] = self.axis_number_from_name(self.r_selection.get())        # R Axis No
        values_array[7] = float(self.x_position_entry.get())                        # X Position
        values_array[8] = float(self.y_position_entry.get())                        # Y Position
        values_array[9] = float(self.z_position_entry.get())                        # Z Position
        values_array[10] = float(self.gx_position_entry.get())                      # Gx Position
        values_array[11] = float(self.gy_position_entry.get())                      # Gy Position
        values_array[12] = float(self.gz_position_entry.get())                      # Gz Position
        values_array[13] = float(self.diameter_entry.get())                         # Diameter (mm)
        values_array[14] = float(self.speed_entry.get())                            # Speed (RPM)
        values_array[15] = float(self.resolution_entry.get())                       # Resolution (mm)

        # Write Scan Parameters
        self.c.client.set_values(node_array, values_array)

        # Start Go To Point
        self.c.client.get_node("ns=2;s=Application.Shaft_Vars.iShaftCommand") \
            .set_value(1, varianttype=ua.VariantType.Int16)

    def start_scan(self):
        # Start Scan
        self.c.client.get_node("ns=2;s=Application.Shaft_Vars.iShaftCommand") \
            .set_value(2, varianttype=ua.VariantType.Int16)

    def mark_part(self):
        # Start Mark Part
        self.c.client.get_node("ns=2;s=Application.Shaft_Vars.iShaftCommand") \
            .set_value(3, varianttype=ua.VariantType.Int16)

    def acknowledge_failure(self):
        # Acknowledge Failure
        self.c.client.get_node("ns=2;s=Application.Shaft_Vars.iShaftCommand") \
            .set_value(4, varianttype=ua.VariantType.Int16)

    def update(self):
        if self.c.client.get_node("ns=2;s=Application.Shaft_Vars.arShaftOutputs[2]").get_value():
            messagebox.showerror(message="Shaft Scan Failure")
            self.acknowledge_failure()
