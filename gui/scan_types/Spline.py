from motion.Motion import Motion
import opcua
from opcua import ua
from tkinter import *
from tkinter import filedialog, messagebox
from utility.ConnectionManagement import ConnectionManagement
import xml.etree.ElementTree


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
        self.load_spline_button = Button(self.control_frame)
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
        self.load_spline_button.configure(
            text="Load Spline", width=12, height=2, bg=self.colors[4],
            command=self.load_spline
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
        self.load_spline_button.grid(
            row=7, column=0, padx=5, pady=10
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

    def load_spline(self):
        self.x_spline = []
        self.y_spline = []
        self.z_spline = []
        self.gx_spline = []
        self.gy_spline = []
        self.gz_spline = []
        self.speed_spline = []
        self.scan_spline = []
        self.index_spline = []
        self.spline_loaded = False

        self.spline_file = filedialog.askopenfilename()
        if self.spline_file == "":
            return

        # Generate Spline Data
        try:
            root = xml.etree.ElementTree.parse(self.spline_file).getroot()
            for value in root.find("X"):
                self.x_spline.append(float(value.text))
            for value in root.find("Y"):
                self.y_spline.append(float(value.text))
            for value in root.find("Z"):
                self.z_spline.append(float(value.text))
            for value in root.find("Gx"):
                self.gx_spline.append(float(value.text))
            for value in root.find("Gy"):
                self.gy_spline.append(float(value.text))
            for value in root.find("Gz"):
                self.gz_spline.append(float(value.text))
            for value in root.find("Speed"):
                self.speed_spline.append(float(value.text))
            for value in root.find("ScanEncode"):
                self.scan_spline.append(float(value.text))
            for value in root.find("IndexEncode"):
                self.index_spline.append(float(value.text))
        except Exception as e:
            print(e)
            messagebox.showerror(message="Failed To Get Spline Data")
            return

        self.spline_loaded = True

        # Send Spline To PLC
        buffer_size = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1a_XSpline.IndexMax").get_value()[0] + 1
        spline_length = len(self.x_spline)

        # Max Spline Size
        if spline_length > (buffer_size * 3):
            messagebox.showerror(message="Spline data too long for static buffer.")
            self.spline_loaded = False
            return

        # Fill Buffer A
        points_in_buffer = int(min(buffer_size, spline_length) / 5)
        buffer_min = self.x_spline[0]
        buffer_max = buffer_min + self.x_spline[(points_in_buffer - 1) * 5]
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1aFlag").set_value(
            True
        )
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1aSize").set_value(
            points_in_buffer, ua.VariantType.UInt16
        )
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1aMin").set_value(
            buffer_min, ua.VariantType.Double
        )
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1aMax").set_value(
            buffer_max, ua.VariantType.Double
        )

        if spline_length < buffer_size:
            self.x_spline.extend([0.0] * (buffer_size - spline_length))
            self.y_spline.extend([0.0] * (buffer_size - spline_length))
            self.z_spline.extend([0.0] * (buffer_size - spline_length))
            self.gx_spline.extend([0.0] * (buffer_size - spline_length))
            self.gy_spline.extend([0.0] * (buffer_size - spline_length))
            self.gz_spline.extend([0.0] * (buffer_size - spline_length))
            self.speed_spline.extend([0.0] * (buffer_size - spline_length))
            self.scan_spline.extend([0.0] * (buffer_size - spline_length))
            self.index_spline.extend([0.0] * (buffer_size - spline_length))

        x_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1a_XSpline")
        y_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1a_YSpline")
        z_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1a_ZSpline")
        gx_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1a_GxSpline")
        gy_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1a_GySpline")
        gz_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1a_GzSpline")
        speed_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1a_SpeedSpline")
        scan_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1a_ScanEncodeSpline")
        index_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1a_IndexEncodeSpline")

        x_spline_node.set_value(self.x_spline[0:buffer_size])
        y_spline_node.set_value(self.y_spline[0:buffer_size])
        z_spline_node.set_value(self.z_spline[0:buffer_size])
        gx_spline_node.set_value(self.gx_spline[0:buffer_size])
        gy_spline_node.set_value(self.gy_spline[0:buffer_size])
        gz_spline_node.set_value(self.gz_spline[0:buffer_size])
        speed_spline_node.set_value(self.speed_spline[0:buffer_size])
        scan_spline_node.set_value(self.scan_spline[0:buffer_size])
        index_spline_node.set_value(self.index_spline[0:buffer_size])

        self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1aFlag").set_value(False)

        # Fill Buffer B
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1bFlag").set_value(True)

        if spline_length > buffer_size:
            points_in_buffer = int((min(buffer_size * 2, spline_length) - buffer_size) / 5)
            buffer_min = self.x_spline[buffer_size]
            buffer_max = self.x_spline[buffer_size + ((points_in_buffer - 1) * 5)]
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1bSize").set_value(
                points_in_buffer, ua.VariantType.UInt16
            )
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1bMin").set_value(
                buffer_min, ua.VariantType.Double
            )
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1bMax").set_value(
                buffer_max, ua.VariantType.Double
            )

            if spline_length < (buffer_size * 2):
                self.x_spline.extend([0.0] * ((buffer_size * 2) - spline_length))
                self.y_spline.extend([0.0] * ((buffer_size * 2) - spline_length))
                self.z_spline.extend([0.0] * ((buffer_size * 2) - spline_length))
                self.gx_spline.extend([0.0] * ((buffer_size * 2) - spline_length))
                self.gy_spline.extend([0.0] * ((buffer_size * 2) - spline_length))
                self.gz_spline.extend([0.0] * ((buffer_size * 2) - spline_length))
                self.speed_spline.extend([0.0] * ((buffer_size * 2) - spline_length))
                self.scan_spline.extend([0.0] * ((buffer_size * 2) - spline_length))
                self.index_spline.extend([0.0] * ((buffer_size * 2) - spline_length))

            x_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1b_XSpline")
            y_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1b_YSpline")
            z_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1b_ZSpline")
            gx_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1b_GxSpline")
            gy_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1b_GySpline")
            gz_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1b_GzSpline")
            speed_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1b_SpeedSpline")
            scan_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1b_ScanEncodeSpline")
            index_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1b_IndexEncodeSpline")

            x_spline_node.set_value(self.x_spline[buffer_size:buffer_size * 2])
            y_spline_node.set_value(self.y_spline[buffer_size:buffer_size * 2])
            z_spline_node.set_value(self.z_spline[buffer_size:buffer_size * 2])
            gx_spline_node.set_value(self.gx_spline[buffer_size:buffer_size * 2])
            gy_spline_node.set_value(self.gy_spline[buffer_size:buffer_size * 2])
            gz_spline_node.set_value(self.gz_spline[buffer_size:buffer_size * 2])
            speed_spline_node.set_value(self.speed_spline[buffer_size:buffer_size * 2])
            scan_spline_node.set_value(self.scan_spline[buffer_size:buffer_size * 2])
            index_spline_node.set_value(self.index_spline[buffer_size:buffer_size * 2])

        else:
            points_in_buffer = 0
            buffer_min = 0
            buffer_max = 0
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1bSize").set_value(
                points_in_buffer, ua.VariantType.UInt16
            )
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1bMin").set_value(
                buffer_min, ua.VariantType.Double
            )
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1bMax").set_value(
                buffer_max, ua.VariantType.Double
            )

        self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1bFlag").set_value(False)

        # Fill Buffer C
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1cFlag").set_value(True)

        if spline_length > (buffer_size * 2):
            points_in_buffer = int((min(buffer_size * 3, spline_length) - (buffer_size * 2)) / 5)
            buffer_min = self.x_spline[buffer_size * 2]
            buffer_max = self.x_spline[buffer_size * 2 + ((points_in_buffer - 1) * 5)]
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1cSize").set_value(
                points_in_buffer, ua.VariantType.UInt16
            )
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1cMin").set_value(
                buffer_min, ua.VariantType.Double
            )
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1cMax").set_value(
                buffer_max, ua.VariantType.Double
            )

            if spline_length < (buffer_size * 3):
                self.x_spline.extend([0.0] * ((buffer_size * 3) - spline_length))
                self.y_spline.extend([0.0] * ((buffer_size * 3) - spline_length))
                self.z_spline.extend([0.0] * ((buffer_size * 3) - spline_length))
                self.gx_spline.extend([0.0] * ((buffer_size * 3) - spline_length))
                self.gy_spline.extend([0.0] * ((buffer_size * 3) - spline_length))
                self.gz_spline.extend([0.0] * ((buffer_size * 3) - spline_length))
                self.speed_spline.extend([0.0] * ((buffer_size * 3) - spline_length))
                self.scan_spline.extend([0.0] * ((buffer_size * 3) - spline_length))
                self.index_spline.extend([0.0] * ((buffer_size * 3) - spline_length))

            x_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1c_XSpline")
            y_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1c_YSpline")
            z_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1c_ZSpline")
            gx_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1c_GxSpline")
            gy_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1c_GySpline")
            gz_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1c_GzSpline")
            speed_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1c_SpeedSpline")
            scan_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1c_ScanEncodeSpline")
            index_spline_node = self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1c_IndexEncodeSpline")

            x_spline_node.set_value(self.x_spline[buffer_size * 2:buffer_size * 3])
            y_spline_node.set_value(self.y_spline[buffer_size * 2:buffer_size * 3])
            z_spline_node.set_value(self.z_spline[buffer_size * 2:buffer_size * 3])
            gx_spline_node.set_value(self.gx_spline[buffer_size * 2:buffer_size * 3])
            gy_spline_node.set_value(self.gy_spline[buffer_size * 2:buffer_size * 3])
            gz_spline_node.set_value(self.gz_spline[buffer_size * 2:buffer_size * 3])
            speed_spline_node.set_value(self.speed_spline[buffer_size * 2:buffer_size * 3])
            scan_spline_node.set_value(self.scan_spline[buffer_size * 2:buffer_size * 3])
            index_spline_node.set_value(self.index_spline[buffer_size * 2:buffer_size * 3])

        else:
            points_in_buffer = 0
            buffer_min = 0
            buffer_max = 0
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1cSize").set_value(
                points_in_buffer, ua.VariantType.UInt16
            )
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1cMin").set_value(
                buffer_min, ua.VariantType.Double
            )
            self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1cMax").set_value(
                buffer_max, ua.VariantType.Double
            )

        self.c.client.get_node("ns=2;s=Application.Spline_Vars.S1bFlag").set_value(False)

    def enter_scan_mode(self):
        # Read Scan Parameter Node
        node_array: [opcua.Node] = []
        for child in self.c.client.get_node(
            "ns=2;s=Application.Spline_Vars.arSplineValues"
        ).get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.Double:
                node_array.append(child)
        values_array: [float] = [float(0)] * len(node_array)

        # Write Scan Parameters
        self.c.client.set_values(node_array, values_array)

        # Enter Scan Mode
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.iSplineCommand") \
            .set_value(1, varianttype=ua.VariantType.Int16)

    def exit_scan_mode(self):
        self.scan_button.configure(
            text="Enter\nScan Mode", width=12, height=2, bg=self.colors[4],
            command=self.enter_scan_mode
        )

        # Stop Scan
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.iSplineCommand") \
            .set_value(2, varianttype=ua.VariantType.Int16)

    def go_to_spline(self):
        # Go To Spline
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.iSplineCommand") \
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

            self.c.client.get_node("ns=2;s=Application.Spline_Vars.arSplineValues")\
                .set_value(axis_numbers, varianttype=ua.VariantType.Double)

            self.c.client.get_node("ns=2;s=Application.Spline_Vars.iSplineCommand")\
                .set_value(7, varianttype=ua.VariantType.Int16)

    def spline_scan_forward(self):
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.iSplineCommand")\
            .set_value(9, varianttype=ua.VariantType.Int16)

    def spline_scan_reverse(self):
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.iSplineCommand")\
            .set_value(10, varianttype=ua.VariantType.Int16)

    def spline_scan_stop(self):
        self.c.client.get_node("ns=2;s=Application.Spline_Vars.iSplineCommand")\
            .set_value(11, varianttype=ua.VariantType.Int16)

    def update(self):
        # Set Spline Axes
        self.set_spline_axes()

        # Check Spline Scan Status
        if self.c.is_connected():
            in_scan_mode = self.c.client.get_node("ns=2;s=Application.Spline_Vars.arSplineOutputs[0]").get_value()
            part_in_range = self.c.client.get_node("ns=2;s=Application.Spline_Vars.arSplineOutputs[1]").get_value()
            scan_mode_failure = self.c.client.get_node("ns=2;s=Application.Spline_Vars.arSplineOutputs[2]").get_value()
            spline_axes_set = self.c.client.get_node("ns=2;s=Application.Spline_Vars.arSplineOutputs[3]").get_value()
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

        # Disable Load Spline Button
        if spline_axes_set and not in_scan_mode:
            self.load_spline_button["state"] = "normal"
        else:
            self.load_spline_button["state"] = "disable"

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
