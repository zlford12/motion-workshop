from motion.Motion import Motion
import opcua
from opcua import ua
from tkinter import *
from utility.ConnectionManagement import ConnectionManagement


class Spline:
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
        for axis in self.axes:
            if not axis.axis_data.Offset and not axis.axis_data.Linkable and not axis.axis_data.ScanAxis:
                self.axis_names.append(axis.axis_data.Name)
            if axis.axis_data.ScanAxis:
                self.scan_axes.append(axis.axis_data.Name)

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

    def configure(self):
        # Configure Frame
        self.control_frame.configure(bg=self.colors[3], width=500)
        self.jog_frame.configure(bg=self.colors[3], width=500)

        # Parameters
        entry_width = 10
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
        self.scan_axis_label.grid(
            row=5, column=0, padx=5, pady=5, sticky=W
        )
        self.index_axis_label.grid(
            row=5, column=1, padx=5, pady=5, sticky=W
        )
        self.path_axis_label.grid(
            row=5, column=2, padx=5, pady=5, sticky=W
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

    def start_scan(self):
        # Read Scan Parameter Node
        node_array: [opcua.Node] = []
        for child in self.c.client.get_node(
            "ns=2;s=Application.Raster_3D_Vars.arRaster_3DValues"
        ).get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.Double:
                node_array.append(child)
        values_array: [float] = [float(0)] * len(node_array)

        # Write Scan Parameters
        self.c.client.set_values(node_array, values_array)

        # Start Scan
        self.c.client.get_node("ns=2;s=Application.Raster_3D_Vars.iRaster_3DCommand") \
            .set_value(1, varianttype=ua.VariantType.Int16)

    def stop_scan(self):
        # Stop Scan
        self.c.client.get_node("ns=2;s=Application.Raster_3D_Vars.iRaster_3DCommand") \
            .set_value(2, varianttype=ua.VariantType.Int16)
