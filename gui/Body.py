from tkinter import *
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class Body:
    def __init__(
            self, colors, root: Tk,
            connection_manager: ConnectionManagement, application_settings: ApplicationSettings, motion: Motion
    ):
        # Class Objects
        self.connection_manager = connection_manager
        self.application_settings = application_settings
        self.motion = motion
        self.root = root

        # Color Scheme
        self.colors = colors

        # Frame
        self.body = Frame(self.root)

        # Widgets
        self.plc_status = Label(self.body)
        self.axis_status = [(Label(self.body), int(0))]

    def draw(self):
        self.body.configure(bg=self.colors[0])
        self.body.grid(row=1, column=0, sticky=N + E + S + W)

    def create_status_labels(self):
        self.axis_status = []
        for child in self.body.winfo_children():
            child.destroy()
        self.plc_status = Label(self.body)
        self.axis_status = [(Label(self.body), int(0))]

        self.plc_status.configure(
            text="PLC Status", bg=self.colors[0], fg=self.colors[5]
        )
        self.plc_status.grid(row=0, column=0, sticky=W)

        for axis in self.motion.axis_list:
            axis_number = int(axis.axis_data.AxisNo)
            label = Label(self.body)
            label.configure(
                text="Axis Status", bg=self.colors[0], fg=self.colors[5]
            )
            label.grid(row=axis_number, column=0, sticky=W)
            self.axis_status.append((label, axis_number))

    def update_status_labels(self):
        try:
            text = \
                self.connection_manager.client.get_node(
                    "ns=18;s=System.DisplayedDiagnosis"
                ).get_value()
            self.plc_status.configure(text=text)

            for label, axis_number in self.axis_status:
                if axis_number > 0:
                    text = \
                        self.connection_manager.client.get_node(
                            "ns=12;s=Motion.AxisSet.LocalControl.Axis" + str(axis_number) + ".DiagnosisText"
                        ).get_value()

                    name = ""
                    for axis in self.motion.axis_list:
                        if axis.axis_data.AxisNo == axis_number:
                            name = axis.axis_data.Name

                    label.configure(text=name + ": " + text, justify=LEFT)
        except Exception as e:
            print(e)
