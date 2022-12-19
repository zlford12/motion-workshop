import csv
import ftplib
import struct
from motion.Motion import Motion
import opcua
from opcua import ua
from tkinter import *
from tkinter import filedialog, messagebox
from utility.ConnectionManagement import ConnectionManagement


class Mesh:
    def __init__(self, frame, colors, c: ConnectionManagement, m: Motion):
        # Create Frames
        self.frame = frame
        self.colors = colors
        self.control_frame = Frame(self.frame)
        self.jog_frame = Frame(self.frame)

        # Connection Manager
        self.c = c
        self.m = m

        # Mesh
        self.mesh_file = ""
        self.mesh_loaded = True

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

        # Axis Selections
        self.x_selection = StringVar()
        self.y_selection = StringVar()
        self.z_selection = StringVar()
        self.gx_selection = StringVar()
        self.gy_selection = StringVar()
        self.gz_selection = StringVar()
        self.scan_selection = StringVar()
        self.index_selection = StringVar()

        # Axis Menus
        self.x_axis_menu = OptionMenu(self.control_frame, self.x_selection, *self.axis_names)
        self.y_axis_menu = OptionMenu(self.control_frame, self.y_selection, *self.axis_names)
        self.z_axis_menu = OptionMenu(self.control_frame, self.z_selection, *self.axis_names)
        self.gx_axis_menu = OptionMenu(self.control_frame, self.gx_selection, *self.axis_names)
        self.gy_axis_menu = OptionMenu(self.control_frame, self.gy_selection, *self.axis_names)
        self.gz_axis_menu = OptionMenu(self.control_frame, self.gz_selection, *self.axis_names)
        self.scan_axis_menu = OptionMenu(self.control_frame, self.scan_selection, *self.scan_axes)
        self.index_axis_menu = OptionMenu(self.control_frame, self.index_selection, *self.scan_axes)

        # Buttons
        self.scan_button = Button(self.control_frame)
        self.go_to_mesh_button = Button(self.control_frame)
        self.load_mesh_button = Button(self.control_frame)
        self.create_mesh_button = Button(self.control_frame)

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

        self.scan_button.configure(
            text="Enter\nScan Mode", width=12, height=2, bg=self.colors[4],
            command=self.enter_scan_mode
        )
        self.go_to_mesh_button.configure(
            text="Go To\nScan Position", width=12, height=2, bg=self.colors[4],
            command=self.go_to_mesh
        )
        self.load_mesh_button.configure(
            text="Load Mesh", width=12, height=2, bg=self.colors[4],
            command=self.load_mesh
        )
        self.create_mesh_button.configure(
            text="Create Mesh\nFrom CSV", width=12, height=2, bg=self.colors[4],
            command=self.create_mesh_from_csv
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

        self.scan_button.grid(
            row=7, column=2, padx=5, pady=10
        )
        self.go_to_mesh_button.grid(
            row=7, column=1, padx=5, pady=10
        )
        self.load_mesh_button.grid(
            row=7, column=0, padx=5, pady=10
        )
        self.create_mesh_button.grid(
            row=8, column=0, padx=5, pady=10
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

    def load_mesh(self):

        # Select Mesh File
        self.mesh_file = filedialog.askopenfilename()
        if self.mesh_file == "":
            return

        # Read Scan Parameter Node
        node_array: [opcua.Node] = []
        for child in self.c.client.get_node(
                "ns=2;s=Application.Mesh_Vars.arMeshValues"
        ).get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.Double:
                node_array.append(child)
        values_array: [float] = [float(0)] * len(node_array)

        # Set Mesh Parameters
        parameters = open(self.mesh_file, "rb").read(20)
        values_array[0] = struct.unpack('f', parameters[0:4])[0]
        values_array[1] = struct.unpack('f', parameters[4:8])[0]
        values_array[2] = struct.unpack('f', parameters[8:12])[0]
        values_array[3] = self.axis_number_from_name(self.x_selection.get())
        values_array[4] = self.axis_number_from_name(self.y_selection.get())
        values_array[5] = self.axis_number_from_name(self.z_selection.get())
        values_array[6] = self.axis_number_from_name(self.gx_selection.get())
        values_array[7] = self.axis_number_from_name(self.gy_selection.get())
        values_array[8] = self.axis_number_from_name(self.gz_selection.get())
        values_array[9] = self.axis_number_from_name(self.scan_selection.get())
        values_array[10] = self.axis_number_from_name(self.index_selection.get())

        # Write Scan Parameters
        self.c.client.set_values(node_array, values_array)

        self.c.client.get_node("ns=2;s=Application.Mesh_Vars.iMeshCommand") \
            .set_value(3, varianttype=ua.VariantType.Int16)

        # Upload Mesh File
        ftp = ftplib.FTP(self.c.ip)
        ftp.login("MNDT", "1bmhkchMNDT")
        ftp.cwd("ata0b")
        ftp.storbinary("STOR mesh_data", open(self.mesh_file, "rb"))

        # Load Mesh File In PLC
        self.c.client.get_node("ns=2;s=Application.Mesh_Vars.iMeshCommand") \
            .set_value(4, varianttype=ua.VariantType.Int16)

    def enter_scan_mode(self):
        # Enter Scan Mode
        self.c.client.get_node("ns=2;s=Application.Mesh_Vars.iMeshCommand") \
            .set_value(1, varianttype=ua.VariantType.Int16)

    def exit_scan_mode(self):
        self.scan_button.configure(
            text="Enter\nScan Mode", width=12, height=2, bg=self.colors[4],
            command=self.enter_scan_mode
        )

        # Stop Scan
        self.c.client.get_node("ns=2;s=Application.Mesh_Vars.iMeshCommand") \
            .set_value(2, varianttype=ua.VariantType.Int16)

    def go_to_mesh(self):
        # Go To Mesh
        self.c.client.get_node("ns=2;s=Application.Mesh_Vars.iMeshCommand") \
            .set_value(5, varianttype=ua.VariantType.Int16)

    def create_mesh_from_csv(self):
        csv_file = filedialog.askopenfilename()
        points = csv.reader(open(csv_file))

        for row in points:
            if row[0] != "Scan":
                print(row)