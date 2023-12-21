from tkinter import *
from tkinter import ttk
from motion.Motion import Motion
import opcua.ua
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class AxisStatus:
    def __init__(
            self, colors, tabs: ttk.Notebook,
            connection_manager: ConnectionManagement, application_settings: ApplicationSettings, motion: Motion
    ):
        # Class Objects
        self.connection_manager = connection_manager
        self.application_settings = application_settings
        self.motion = motion
        self.tabs = tabs

        # Color Scheme
        self.colors = colors

        # Tab Frame
        self.axis_status_tab_frame = ttk.Frame(self.tabs)

        # Tab Frame Elements
        self.axis_status_canvas = Canvas(self.axis_status_tab_frame)
        self.axis_status_frame = Frame(self.axis_status_canvas)
        self.axis_status_scroll = Scrollbar(self.axis_status_tab_frame)

        # Widgets
        self.plc_status = Label(self.axis_status_canvas)
        self.axis_status = [(Label(self.axis_status_canvas), int(0))]

        # Controller Compatibility
        self.failure_count = 0
        self.controller_incompatible = False

    def draw(self):
        self.axis_status_tab_frame.rowconfigure(0, weight=1)
        self.axis_status_tab_frame.columnconfigure(0, weight=1)
        self.tabs.add(self.axis_status_tab_frame, text="Axis Status")
        self.axis_status_canvas.configure(
            bg=self.colors[1], highlightthickness=0, yscrollcommand=self.axis_status_scroll.set
        )
        self.axis_status_scroll.configure(orient="vertical", command=self.axis_status_canvas.yview)
        self.axis_status_frame.configure(bg=self.colors[0])

    def create_status_labels(self):
        self.axis_status = []
        for child in self.axis_status_frame.winfo_children():
            child.destroy()
        self.plc_status = Label(self.axis_status_frame)
        self.axis_status = [(Label(self.axis_status_frame), int(0))]

        self.plc_status.configure(
            text="PLC Status", bg=self.colors[0], fg=self.colors[5]
        )
        self.plc_status.grid(row=0, column=0, sticky=W)

        for axis in self.motion.axis_list:
            axis_number = int(axis.axis_data.AxisNo)
            label = Label(self.axis_status_frame)
            label.configure(
                text="Axis Status", bg=self.colors[0], fg=self.colors[5]
            )
            label.grid(row=axis_number, column=0, sticky=W)
            self.axis_status.append((label, axis_number))

        # Display Axis Status
        self.axis_status_canvas.grid(row=0, column=0, sticky=W + N + S)
        self.axis_status_canvas.create_window(0, 0, anchor=W, window=self.axis_status_frame)
        self.axis_status_scroll.grid(row=0, column=1, sticky=E + N + S)

        # Update Canvas
        self.axis_status_canvas.update_idletasks()
        self.axis_status_canvas.configure(
            scrollregion=self.axis_status_canvas.bbox("all"), height=self.axis_status_frame.winfo_height(),
            width=self.axis_status_frame.winfo_width()
        )
        self.axis_status_canvas.bind("Configure", self.update_status_labels())

    def update_status_labels(self):

        if self.controller_incompatible:
            return

        try:
            text = self.connection_manager.node_list.plc_status.get_value()
            self.plc_status.configure(text=text)

            axis_status_values = \
                self.connection_manager.client.get_values(self.connection_manager.node_list.axis_status)
            axis_status_nodes = \
                self.connection_manager.node_list.axis_status

            for label, axis_number in self.axis_status:
                if axis_number > 0:
                    for i in range(len(axis_status_nodes)):
                        if ("Axis" + str(axis_number)) in str(axis_status_nodes[i]):
                            text = axis_status_values[i]

                    name = ""
                    for axis in self.motion.axis_list:
                        if axis.axis_data.AxisNo == axis_number:
                            name = axis.axis_data.Name

                    label.configure(text=name + ": " + text, justify=LEFT)

            self.failure_count = 0

        except opcua.ua.UaStatusCodeError:
            self.failure_count += 1

            if self.failure_count >= 5:
                self.controller_incompatible = True

                for label, axis_number in self.axis_status:
                    label.configure(text="Controller Incompatible. Status Not Available", justify=LEFT)

        self.axis_status_canvas.configure(
            width=self.axis_status_frame.winfo_width()
        )
