from motion.Motion import Motion
import opcua
from opcua import ua
from tkinter import *
from utility.ConnectionManagement import ConnectionManagement


class Raster3D:
    def __init__(self, frame, colors, c: ConnectionManagement, m: Motion):
        # Create Frames
        self.frame = frame
        self.colors = colors
        self.control_frame = Frame(self.frame)
        self.points_frame = Frame(self.frame)

        # Connection Manager
        self.c = c
        self.m = m

        # Axes
        self.axes = self.m.axis_list
        self.axis_names = []
        self.scan_axes = []
        for axis in self.axes:
            if not axis.axis_data.Offset and not axis.axis_data.Linkable and not axis.axis_data.ScanAxis:
                self.axis_names.append(axis.axis_data.Name)
            if axis.axis_data.ScanAxis:
                self.scan_axes.append(axis.axis_data.Name)

        # Scan Points
        self.scan_points = [[0.0] * 3] * 50
        self.scan_point_labels = [[Label(self.points_frame)] * 3] * 50
        self.current_row = 1

        # Create Widgets
        self.axis_selection_label = Label(self.control_frame)
        self.x_axis_label = Label(self.control_frame)
        self.y_axis_label = Label(self.control_frame)
        self.z_axis_label = Label(self.control_frame)
        self.scan_axis_label = Label(self.control_frame)
        self.index_axis_label = Label(self.control_frame)
        self.x_selection = StringVar()
        self.y_selection = StringVar()
        self.z_selection = StringVar()
        self.scan_selection = StringVar()
        self.index_selection = StringVar()
        self.x_axis_menu = OptionMenu(self.control_frame, self.x_selection, *self.axis_names)
        self.y_axis_menu = OptionMenu(self.control_frame, self.y_selection, *self.axis_names)
        self.z_axis_menu = OptionMenu(self.control_frame, self.z_selection, *self.axis_names)
        self.scan_axis_menu = OptionMenu(self.control_frame, self.scan_selection, *self.axis_names)
        self.index_axis_menu = OptionMenu(self.control_frame, self.index_selection, *self.axis_names)

        self.scan_parameters_label = Label(self.control_frame)
        self.scan_speed_label = Label(self.control_frame)
        self.scan_acceleration_label = Label(self.control_frame)
        self.index_width_label = Label(self.control_frame)
        self.scan_direction_label = Label(self.control_frame)
        self.scan_speed_entry = Entry(self.control_frame)
        self.scan_acceleration_entry = Entry(self.control_frame)
        self.index_width_entry = Entry(self.control_frame)
        self.scan_direction_entry = Entry(self.control_frame)

        self.scan_label = Label(self.control_frame)
        self.add_point_button = Button(self.control_frame)
        self.remove_point_button = Button(self.control_frame)
        self.start_scan_button = Button(self.control_frame)
        self.stop_scan_button = Button(self.control_frame)

        self.x_point_label = Label(self.points_frame)
        self.y_point_label = Label(self.points_frame)
        self.z_point_label = Label(self.points_frame)

    def configure(self):
        # Configure Frame
        self.control_frame.configure(bg=self.colors[3], width=500)
        self.points_frame.configure(bg=self.colors[3], width=500)

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
        self.scan_axis_label.configure(
            text="Scan", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.index_axis_label.configure(
            text="Index", bg=self.colors[3], font=label_font, justify=LEFT
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
        self.scan_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )
        self.index_axis_menu.configure(
            width=entry_width, bg=self.colors[4], font=menu_font, highlightthickness=0
        )

        self.scan_parameters_label.configure(
            text="Scan Parameters", bg=self.colors[3], font=label_font, justify=CENTER
        )
        self.scan_speed_label.configure(
            text="Scan Speed (mm/s)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.scan_acceleration_label.configure(
            text="Scan Acceleration (mm/s^2)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.index_width_label.configure(
            text="Index Width (mm)", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.scan_direction_label.configure(
            text="Scan Direction (°)", bg=self.colors[3], font=label_font, justify=LEFT
        )

        self.scan_label.configure(
            text="Scan Points", bg=self.colors[3], font=label_font, justify=CENTER
        )
        self.add_point_button.configure(
            text="Add Point", width=12, height=1, bg=self.colors[4],
            command=lambda: self.add_point()
        )
        self.remove_point_button.configure(
            text="Remove Point", width=12, height=1, bg=self.colors[4],
            command=lambda: self.remove_point()
        )
        self.start_scan_button.configure(
            text="Start Scan", width=12, height=1, bg=self.colors[4],
            command=lambda: self.start_scan()
        )
        self.stop_scan_button.configure(
            text="Stop Scan", width=12, height=1, bg=self.colors[4],
            command=lambda: self.stop_scan()
        )

        self.x_point_label.configure(
            text="X", bg=self.colors[3], font=label_font, justify=CENTER
        )
        self.y_point_label.configure(
            text="Y", bg=self.colors[3], font=label_font, justify=CENTER
        )
        self.z_point_label.configure(
            text="Z", bg=self.colors[3], font=label_font, justify=CENTER
        )

    def draw_controls(self):
        # Configure Widgets
        self.configure()

        # Draw Frames
        self.control_frame.grid(row=0, column=0)
        self.points_frame.grid(row=1, column=0)

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
        self.scan_axis_label.grid(
            row=1, column=3, padx=5, pady=5, sticky=W
        )
        self.index_axis_label.grid(
            row=1, column=4, padx=5, pady=5, sticky=W
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
        self.scan_axis_menu.grid(
            row=2, column=3, padx=5, pady=0, sticky=W
        )
        self.index_axis_menu.grid(
            row=2, column=4, padx=5, pady=0, sticky=W
        )

        self.scan_parameters_label.grid(
            row=3, column=0, columnspan=5, padx=5, pady=(10, 5)
        )
        self.scan_speed_label.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky=W
        )
        self.scan_acceleration_label.grid(
            row=6, column=0, columnspan=2, padx=5, pady=5, sticky=W
        )
        self.index_width_label.grid(
            row=4, column=2, columnspan=2, padx=5, pady=5, sticky=W
        )
        self.scan_direction_label.grid(
            row=6, column=2, columnspan=2, padx=5, pady=5, sticky=W
        )
        self.scan_speed_entry.grid(
            row=5, column=0, columnspan=2, padx=5, pady=0, sticky=W
        )
        self.scan_acceleration_entry.grid(
            row=7, column=0, columnspan=2, padx=5, pady=0, sticky=W
        )
        self.index_width_entry.grid(
            row=5, column=2, columnspan=2, padx=5, pady=0, sticky=W
        )
        self.scan_direction_entry.grid(
            row=7, column=2, columnspan=2, padx=5, pady=0, sticky=W
        )

        self.scan_label.grid(
            row=9, column=0, columnspan=5, padx=5, pady=(10, 5)
        )
        self.add_point_button.grid(
            row=8, column=0, padx=5, pady=(10, 5), sticky=W
        )
        self.remove_point_button.grid(
            row=8, column=1, padx=5, pady=(10, 5), sticky=W
        )
        self.start_scan_button.grid(
            row=8, column=2, padx=5, pady=(10, 5), sticky=W
        )
        self.stop_scan_button.grid(
            row=8, column=3, padx=5, pady=(10, 5), sticky=W
        )

        self.x_point_label.grid(
            row=0, column=0, padx=20, pady=5
        )
        self.y_point_label.grid(
            row=0, column=1, padx=20, pady=5
        )
        self.z_point_label.grid(
            row=0, column=2, padx=20, pady=5
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

    def add_point(self):
        # Get Coordinates
        x_position = self.axis_position_from_name(self.x_selection.get())
        y_position = self.axis_position_from_name(self.y_selection.get())
        z_position = self.axis_position_from_name(self.z_selection.get())

        self.scan_points[self.current_row - 1] = \
            [x_position, y_position, z_position]

        # Create Label Instances
        self.scan_point_labels[self.current_row - 1][0] = Label(self.points_frame)
        self.scan_point_labels[self.current_row - 1][1] = Label(self.points_frame)
        self.scan_point_labels[self.current_row - 1][2] = Label(self.points_frame)

        # Configure Labels
        self.scan_point_labels[self.current_row - 1][0].configure(
            text=str(round(x_position, 1)), bg=self.colors[3], font=("Arial", 8)
        )
        self.scan_point_labels[self.current_row - 1][1].configure(
            text=str(round(y_position, 1)), bg=self.colors[3], font=("Arial", 8)
        )
        self.scan_point_labels[self.current_row - 1][2].configure(
            text=str(round(z_position, 1)), bg=self.colors[3], font=("Arial", 8)
        )

        # Draw Labels
        self.scan_point_labels[self.current_row - 1][0].grid(
            row=self.current_row, column=0
        )
        self.scan_point_labels[self.current_row - 1][1].grid(
            row=self.current_row, column=1
        )
        self.scan_point_labels[self.current_row - 1][2].grid(
            row=self.current_row, column=2
        )

        self.current_row = self.current_row + 1

    def remove_point(self):
        if self.current_row > 1:
            self.scan_points[self.current_row - 2] = \
                [0.0] * 3

            self.current_row = self.current_row - 1

            self.refresh_points()

    def refresh_points(self):
        label_font = ("Arial Black", 10)

        for child in self.points_frame.winfo_children():
            child.destroy()

        self.x_point_label = Label(self.points_frame)
        self.y_point_label = Label(self.points_frame)
        self.z_point_label = Label(self.points_frame)

        self.x_point_label.configure(
            text="X", bg=self.colors[3], font=label_font, justify=CENTER
        )
        self.y_point_label.configure(
            text="Y", bg=self.colors[3], font=label_font, justify=CENTER
        )
        self.z_point_label.configure(
            text="Z", bg=self.colors[3], font=label_font, justify=CENTER
        )

        self.x_point_label.grid(
            row=0, column=0, padx=20, pady=5
        )
        self.y_point_label.grid(
            row=0, column=1, padx=20, pady=5
        )
        self.z_point_label.grid(
            row=0, column=2, padx=20, pady=5
        )

        for i in range(len(self.scan_points)):
            if i < (self.current_row - 1):
                # Create Label Instances
                self.scan_point_labels[i][0] = Label(self.points_frame)
                self.scan_point_labels[i][1] = Label(self.points_frame)
                self.scan_point_labels[i][2] = Label(self.points_frame)

                # Configure Labels
                self.scan_point_labels[i][0].configure(
                    text=str(round(self.scan_points[i][0], 1)), bg=self.colors[3], font=("Arial", 8)
                )
                self.scan_point_labels[i][1].configure(
                    text=str(round(self.scan_points[i][1], 1)), bg=self.colors[3], font=("Arial", 8)
                )
                self.scan_point_labels[i][2].configure(
                    text=str(round(self.scan_points[i][2], 1)), bg=self.colors[3], font=("Arial", 8)
                )

                # Draw Labels
                self.scan_point_labels[i][0].grid(
                    row=i + 1, column=0
                )
                self.scan_point_labels[i][1].grid(
                    row=i + 1, column=1
                )
                self.scan_point_labels[i][2].grid(
                    row=i + 1, column=2
                )

    def start_scan(self):
        # Read Scan Parameter Node
        node_array: [opcua.Node] = []
        for child in self.c.client.get_node(
            "ns=2;s=Application.Raster_3D_Vars.arRaster_3DValues"
        ).get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.Double:
                node_array.append(child)
        values_array: [float] = [float(0)] * 10
        point_array: [float] = [float(0)] * (len(node_array) - len(values_array))

        # Create Point Array
        point_index = 0
        for point in self.scan_points:
            for coordinate in point:
                point_array[point_index] = coordinate
                point_index = point_index + 1
        values_array.extend(point_array)

        # Set Scan Parameters
        values_array[0] = self.axis_number_from_name(self.scan_selection.get())     # Scan Axis No
        values_array[1] = self.axis_number_from_name(self.index_selection.get())    # Index Axis No
        values_array[2] = self.axis_number_from_name(self.x_selection.get())        # X Axis No
        values_array[3] = self.axis_number_from_name(self.y_selection.get())        # Y Axis No
        values_array[4] = self.axis_number_from_name(self.z_selection.get())        # Z Axis No
        values_array[5] = float(self.index_width_entry.get())                       # Index Width (mm)
        values_array[6] = float(self.scan_speed_entry.get())                        # Scan Speed (mm/sec)
        values_array[7] = float(self.scan_acceleration_entry.get())                 # Scan Acceleration (mm/sec^2)
        values_array[8] = float(self.scan_direction_entry.get())                    # Scan Direction (°)
        values_array[9] = float(self.current_row - 1)                               # Number Of Points

        # Write Scan Parameters
        self.c.client.set_values(node_array, values_array)

        # Start Scan
        self.c.client.get_node("ns=2;s=Application.Raster_3D_Vars.iRaster_3DCommand") \
            .set_value(1, varianttype=ua.VariantType.Int16)

    def stop_scan(self):
        # Stop Scan
        self.c.client.get_node("ns=2;s=Application.Raster_3D_Vars.iRaster_3DCommand") \
            .set_value(2, varianttype=ua.VariantType.Int16)
