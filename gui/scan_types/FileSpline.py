from motion.Motion import Motion
import opcua
from opcua import ua
from tkinter import *
from tkinter import messagebox
from utility.ConnectionManagement import ConnectionManagement


class FileSpline:
    def __init__(self, frame, colors, c: ConnectionManagement, m: Motion):
        # Create Frames
        self.frame = frame
        self.colors = colors
        self.control_frame = Frame(self.frame)
        self.jog_frame = Frame(self.frame)

        # Connection Manager
        self.c = c
        self.m = m

        # Axes
        self.axes = self.m.axis_list
        self.axis_names = ["None"]
        self.scan_axes = ["None"]
        self.selected_axes: [str] = []
        for axis in self.axes:
            if not axis.axis_data.Offset and not axis.axis_data.Linkable and not axis.axis_data.ScanAxis:
                self.axis_names.append(axis.axis_data.Name)
            if axis.axis_data.ScanAxis:
                self.scan_axes.append(axis.axis_data.Name)

        # Spline
        self.spline_file = ""
        self.spline_loaded = False
        self.x_spline: [float] = []
        self.y_spline: [float] = []
        self.z_spline: [float] = []
        self.gx_spline: [float] = []
        self.gy_spline: [float] = []
        self.gz_spline: [float] = []
        self.speed_spline: [float] = []
        self.scan_spline: [float] = []
        self.index_spline: [float] = []

        # Axis Labels
        self.axis_selection_label = Label(self.control_frame)
        self.x_axis_label = Label(self.control_frame)
        self.y_axis_label = Label(self.control_frame)
        self.z_axis_label = Label(self.control_frame)
        self.gx_axis_label = Label(self.control_frame)
        self.gy_axis_label = Label(self.control_frame)
        self.gz_axis_label = Label(self.control_frame)
        self.scan_axis_label = Label(self.control_frame)
        self.index_axis_label = Label(self.control_frame)
        self.path_axis_label = Label(self.control_frame)

        # Axis Selections
        self.x_selection = StringVar()
        self.y_selection = StringVar()
        self.z_selection = StringVar()
        self.gx_selection = StringVar()
        self.gy_selection = StringVar()
        self.gz_selection = StringVar()
        self.scan_selection = StringVar()
        self.index_selection = StringVar()
        self.path_selection = StringVar()

        # Axis Menus
        self.x_axis_menu = OptionMenu(self.control_frame, self.x_selection, *self.axis_names)
        self.y_axis_menu = OptionMenu(self.control_frame, self.y_selection, *self.axis_names)
        self.z_axis_menu = OptionMenu(self.control_frame, self.z_selection, *self.axis_names)
        self.gx_axis_menu = OptionMenu(self.control_frame, self.gx_selection, *self.axis_names)
        self.gy_axis_menu = OptionMenu(self.control_frame, self.gy_selection, *self.axis_names)
        self.gz_axis_menu = OptionMenu(self.control_frame, self.gz_selection, *self.axis_names)
        self.scan_axis_menu = OptionMenu(self.control_frame, self.scan_selection, *self.scan_axes)
        self.index_axis_menu = OptionMenu(self.control_frame, self.index_selection, *self.scan_axes)
        self.path_axis_menu = OptionMenu(self.control_frame, self.path_selection, *self.scan_axes)

        # Buttons
        self.scan_button = Button(self.control_frame)
        self.go_to_scan_button = Button(self.control_frame)
        self.forward_button = Button(self.control_frame)
        self.reverse_button = Button(self.control_frame)
        self.stop_button = Button(self.control_frame)

    def configure(self):
        # Configure Frame
        self.control_frame.configure(bg=self.colors[3], width=500)
        self.jog_frame.configure(bg=self.colors[3], width=500)

        # Parameters
        entry_width = 12
        label_font = ("Arial Black", 10)
        menu_font = ("Arial Black", 8)

        # Configure Widgets
        self.axis_selection_label.configure(
            text="Axis Selection", bg=self.colors[3], font=label_font, justify=CENTER
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
        self.scan_axis_label.configure(
            text="Scan", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.index_axis_label.configure(
            text="Index", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.path_axis_label.configure(
            text="Path", bg=self.colors[3], font=label_font, justify=LEFT
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
        self.scan_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.index_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.path_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )

        self.scan_button.configure(
            text="Enter\nScan Mode", width=12, height=2, bg=self.colors[4],
            command=self.enter_scan_mode
        )
        self.go_to_scan_button.configure(
            text="Go To\nScan Position", width=12, height=2, bg=self.colors[4],
            command=self.go_to_spline
        )
        self.forward_button.configure(
            text="Spline Scan\nForward", width=12, height=2, bg=self.colors[4],
            command=self.spline_scan_forward
        )
        self.reverse_button.configure(
            text="Spline Scan\nReverse", width=12, height=2, bg=self.colors[4],
            command=self.spline_scan_reverse
        )
        self.stop_button.configure(
            text="Stop\nSpline Scan", width=12, height=2, bg=self.colors[4],
            command=self.spline_scan_stop
        )

    def draw_controls(self):
        # Configure Widgets
        self.configure()

        # Draw Frames
        self.control_frame.grid(row=0, column=0)
        self.jog_frame.grid(row=1, column=0)

        # Draw Widgets
        self.axis_selection_label.grid(
            row=0, column=0, columnspan=5, padx=5, pady=5
        )
        self.x_axis_label.grid(
            row=1, column=0, padx=5, pady=(5, 1), sticky=W
        )
        self.y_axis_label.grid(
            row=1, column=1, padx=5, pady=(5, 1), sticky=W
        )
        self.z_axis_label.grid(
            row=1, column=2, padx=5, pady=(5, 1), sticky=W
        )
        self.gx_axis_label.grid(
            row=3, column=0, padx=5, pady=(5, 1), sticky=W
        )
        self.gy_axis_label.grid(
            row=3, column=1, padx=5, pady=(5, 1), sticky=W
        )
        self.gz_axis_label.grid(
            row=3, column=2, padx=5, pady=(5, 1), sticky=W
        )
        self.scan_axis_label.grid(
            row=5, column=0, padx=5, pady=(5, 1), sticky=W
        )
        self.index_axis_label.grid(
            row=5, column=1, padx=5, pady=(5, 1), sticky=W
        )
        self.path_axis_label.grid(
            row=5, column=2, padx=5, pady=(5, 1), sticky=W
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
        self.scan_axis_menu.grid(
            row=6, column=0, padx=5, pady=0, sticky=W
        )
        self.index_axis_menu.grid(
            row=6, column=1, padx=5, pady=0, sticky=W
        )
        self.path_axis_menu.grid(
            row=6, column=2, padx=5, pady=0, sticky=W
        )

        self.scan_button.grid(
            row=7, column=2, padx=5, pady=10
        )
        self.go_to_scan_button.grid(
            row=7, column=1, padx=5, pady=10
        )
        self.forward_button.grid(
            row=8, column=0, padx=5
        )
        self.reverse_button.grid(
            row=8, column=1, padx=5
        )
        self.stop_button.grid(
            row=8, column=2, padx=5
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

    def enter_scan_mode(self):
        # Read Scan Parameter Node
        node_array: [opcua.Node] = []
        for child in self.c.client.get_node(
            "ns=2;s=Application.FileSpline_Vars.arSplineValues"
        ).get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.Double:
                node_array.append(child)
        values_array: [float] = [float(0)] * len(node_array)

        # Write Scan Parameters
        self.c.client.set_values(node_array, values_array)

        # Enter Scan Mode
        self.c.client.get_node("ns=2;s=Application.FileSpline_Vars.iSplineCommand") \
            .set_value(1, varianttype=ua.VariantType.Int16)

    def exit_scan_mode(self):
        self.scan_button.configure(
            text="Enter\nScan Mode", width=12, height=2, bg=self.colors[4],
            command=self.enter_scan_mode
        )

        # Stop Scan
        self.c.client.get_node("ns=2;s=Application.FileSpline_Vars.iSplineCommand") \
            .set_value(2, varianttype=ua.VariantType.Int16)

    def go_to_spline(self):
        # Go To Spline
        self.c.client.get_node("ns=2;s=Application.FileSpline_Vars.iSplineCommand") \
            .set_value(4, varianttype=ua.VariantType.Int16)

    def set_spline_axes(self):
        current_selection = \
            [
                self.x_selection.get(),
                self.y_selection.get(),
                self.z_selection.get(),
                self.gx_selection.get(),
                self.gy_selection.get(),
                self.gz_selection.get(),
                self.scan_selection.get(),
                self.index_selection.get(),
                self.path_selection.get()
            ]

        if current_selection != self.selected_axes:
            self.selected_axes = current_selection

            axis_numbers: [int] = []
            for name in current_selection:
                axis_numbers.append(self.axis_number_from_name(name))

            self.c.client.get_node("ns=2;s=Application.FileSpline_Vars.arFileSplineValues")\
                .set_value(axis_numbers, varianttype=ua.VariantType.Double)

            self.c.client.get_node("ns=2;s=Application.FileSpline_Vars.iFileSplineCommand")\
                .set_value(7, varianttype=ua.VariantType.Int16)

    def spline_scan_forward(self):
        self.c.client.get_node("ns=2;s=Application.FileSpline_Vars.iSplineCommand")\
            .set_value(9, varianttype=ua.VariantType.Int16)

    def spline_scan_reverse(self):
        self.c.client.get_node("ns=2;s=Application.FileSpline_Vars.iSplineCommand")\
            .set_value(10, varianttype=ua.VariantType.Int16)

    def spline_scan_stop(self):
        self.c.client.get_node("ns=2;s=Application.FileSpline_Vars.iSplineCommand")\
            .set_value(11, varianttype=ua.VariantType.Int16)

    def update(self):
        # Set Spline Axes
        self.set_spline_axes()

        # Check Spline Scan Status
        if self.c.is_connected():
            in_scan_mode = self.c.client.get_node(
                "ns=2;s=Application.FileSpline_Vars.arFileSplineOutputs[0]").get_value()
            part_in_range = self.c.client.get_node(
                "ns=2;s=Application.FileSpline_Vars.arFileSplineOutputs[1]").get_value()
            scan_mode_failure = self.c.client.get_node(
                "ns=2;s=Application.FileSpline_Vars.arFileSplineOutputs[2]").get_value()
            spline_axes_set = self.c.client.get_node(
                "ns=2;s=Application.FileSpline_Vars.arFileSplineOutputs[3]").get_value()
        else:
            in_scan_mode = False
            part_in_range = False
            scan_mode_failure = False
            spline_axes_set = False

        # Configure Scan Button
        if (self.scan_button["text"] == "Enter\nScan Mode") and in_scan_mode:
            self.scan_button.configure(
                text="Exit\nScan Mode",
                command=self.exit_scan_mode
            )
        elif (self.scan_button["text"] == "Exit\nScan Mode") and not in_scan_mode:
            self.scan_button.configure(
                text="Enter\nScan Mode",
                command=self.enter_scan_mode
            )

        # Disable Scan Button
        if in_scan_mode or (part_in_range and spline_axes_set and self.spline_loaded):
            self.scan_button["state"] = "normal"
        else:
            self.scan_button["state"] = "disable"

        # Disable Go To Scan Button
        if not in_scan_mode and not part_in_range and spline_axes_set and self.spline_loaded:
            self.go_to_scan_button["state"] = "normal"
        else:
            self.go_to_scan_button["state"] = "disable"

        # Disable Scan Controls
        if in_scan_mode and self.spline_loaded:
            self.forward_button["state"] = "normal"
            self.reverse_button["state"] = "normal"
            self.stop_button["state"] = "normal"
        else:
            self.forward_button["state"] = "disable"
            self.reverse_button["state"] = "disable"
            self.stop_button["state"] = "disable"

        # Scan Mode Failure
        if scan_mode_failure:
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.iSplineCommand").set_value(
                8, varianttype=ua.VariantType.Int16
            )
            messagebox.showerror(
                title="Scan Mode Failure", message="Failed To Enter Scan Mode"
            )
