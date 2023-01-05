import csv
import ftplib
import struct
from motion.Motion import Motion
import opcua
from opcua import ua
from tkinter import *
from tkinter import filedialog, messagebox
from utility.ConnectionManagement import ConnectionManagement
from utility.MeshGeneration import generate_mesh


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
        self.mesh_loaded = True

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
        self.generate_mesh_button = Button(self.control_frame)

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
        self.generate_mesh_button.configure(
            text="Generate Mesh", width=12, height=2, bg=self.colors[4],
            command=generate_mesh()
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
        self.generate_mesh_button.grid(
            row=9, column=0, padx=5, pady=10
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
        mesh_file = filedialog.askopenfilename(filetypes=[("Mesh File", "*.mesh")])
        if mesh_file == "":
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
        parameters = open(mesh_file, "rb").read(20)
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

        # Wait For File To Be Unloaded
        file_loaded = self.c.client.get_node("ns=2;s=Application.Mesh_Vars.arMeshOutputs[2]").get_value()
        while file_loaded:
            file_loaded = self.c.client.get_node("ns=2;s=Application.Mesh_Vars.arMeshOutputs[2]").get_value()

        # Upload Mesh File
        ftp = ftplib.FTP(self.c.ip)
        try:
            ftp.login("MNDT", "1bmhkchMNDT")
        except Exception as e:
            print(e)
            messagebox.showerror(
                title="FTP Error",
                message="Invalid Credentials"
            )
            return

        if "ata0b" in ftp.nlst():
            ftp.cwd("ata0b")
        elif "USER" in ftp.nlst():
            ftp.cwd("USER")
        else:
            messagebox.showerror(
                title="FTP Error",
                message="Directory Does Not Exist"
            )
            return

        try:
            ftp.storbinary("STOR mesh_data", open(mesh_file, "rb"))
        except Exception as e:
            print(e)
            messagebox.showerror(
                title="FTP Error",
                message="Failed To Write Mesh File"
            )
            return

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

    @staticmethod
    def trim_scan_lines(points: [[str]]):
        trim = points
        smallest_scan_line = len(trim)
        current_scan_line_start = 0
        trash_values = []

        for i in range(len(trim)):
            if float(trim[i][1]) != float(trim[current_scan_line_start][1]):
                if (i - current_scan_line_start) < smallest_scan_line:
                    smallest_scan_line = (i - current_scan_line_start)
                current_scan_line_start = i

        current_scan_line_start = 0
        for i in range(len(trim)):
            if float(trim[i][1]) != float(trim[current_scan_line_start][1]):
                current_scan_line_start = i

            if (i + 1 - current_scan_line_start) > smallest_scan_line:
                trash_values.append(trim[i])

        for value in trash_values:
            trim.remove(value)

        return trim

    def create_mesh_from_csv(self):
        csv_file = filedialog.askopenfilename(filetypes=[("CSV File", "*.csv")])
        if ".csv" not in csv_file:
            messagebox.showerror(
                title="File Error",
                message="CSV File Invalid"
            )
            return
        points_reader = csv.reader(open(csv_file))

        mesh_file = filedialog.asksaveasfilename(filetypes=[("Mesh File", "*.mesh")], defaultextension=".mesh")
        if ".mesh" not in mesh_file:
            messagebox.showerror(
                title="File Error",
                message="Mesh File Invalid"
            )
            return
        mesh = open(mesh_file, "wb")

        # Create Point Cloud Array
        points = []
        for row in points_reader:
            if row[0] != "Scan":
                points.append(row)

        # Trim Scan Lines
        points = self.trim_scan_lines(points)

        # Determine Point Cloud Dimensions
        mesh_resolution = float(points[1][0]) - float(points[0][0])
        index_start = points[0][1]
        scan_dimension = 1
        index_dimension = 1

        for i in range(len(points)):
            if points[i][1] != index_start:
                scan_dimension = i
                if (len(points) % scan_dimension) == 0:
                    index_dimension = len(points) / scan_dimension
                    break
                else:
                    messagebox.showerror(
                        title="File Error",
                        message="Scan Lines Must Be Uniform In Length"
                    )
                    return

        # Write Parameters
        mesh.write(struct.pack('f', float(scan_dimension)))
        mesh.write(struct.pack('f', float(index_dimension)))
        mesh.write(struct.pack('f', float(mesh_resolution)))
        mesh.write(struct.pack('f', 0.0))
        mesh.write(struct.pack('f', 0.0))
        mesh.write(struct.pack('f', 0.0))
        mesh.write(struct.pack('f', 0.0))
        mesh.write(struct.pack('f', 0.0))

        # Write Point Cloud
        for i in range(len(points)):
            mesh.write(struct.pack('f', float(points[i][2])))
            mesh.write(struct.pack('f', float(points[i][3])))
            mesh.write(struct.pack('f', float(points[i][4])))
            mesh.write(struct.pack('f', float(points[i][6])))
            mesh.write(struct.pack('f', 0.0))
            mesh.write(struct.pack('f', float(points[i][5])))
            mesh.write(struct.pack('b', True))
