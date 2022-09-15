from tkinter import *
from opcua import ua
from motion.Motion import Motion
from utility.ApplicationSettings import ApplicationSettings
from utility.ConnectionManagement import ConnectionManagement


# noinspection PyArgumentList
class JogControl:
    def __init__(
            self, jog_frame, axis, colors,
            connection_manager: ConnectionManagement, application_settings: ApplicationSettings, motion: Motion
    ):
        # Class Objects
        self.connection_manager = connection_manager
        self.application_settings = application_settings
        self.motion = motion

        # Coordinates
        self.row = None
        self.column = None

        # Create Frame
        self.jog_frame = jog_frame
        self.axis = axis
        self.colors = colors
        self.subframe = Frame(self.jog_frame)

        # Create Widgets
        self.jog_negative_button = Button(self.subframe)
        self.jog_negative_slow_button = Button(self.subframe)
        self.axis_position_label = Label(self.subframe)
        self.go_to_entry = Entry(self.subframe)
        self.go_to_button = Button(self.subframe)
        self.jog_positive_button = Button(self.subframe)
        self.jog_positive_slow_button = Button(self.subframe)
        self.settings_canvas = Canvas(self.subframe)

        # Create Settings Widgets

    def configure_controls(self):
        # Unit
        if self.axis.axis_data.Rotary:
            position_unit = "°"
        else:
            position_unit = "mm"

        # Configure Frames
        self.subframe.configure(bg=self.colors[0], width=400, height=95)
        self.settings_canvas.configure(bg=self.colors[0], width=50, height=95, highlightthickness=0)
        self.settings_canvas.create_text(25, 50, text="Settings", angle=90, fill=self.colors[5])
        self.subframe.columnconfigure(2, weight=1)
        self.subframe.grid_propagate(False)
        self.settings_canvas.grid_propagate(False)

        # Configure Widgets
        self.jog_negative_button.configure(
            text="<<", width=2, height=4, bg=self.colors[3]
        )
        self.jog_negative_slow_button.configure(
            text="<", width=2, height=4, bg=self.colors[3]
        )
        self.axis_position_label.configure(
            text=self.axis.axis_data.Name + " \n" +
            str(round(self.axis.axis_data.Position, 2)) + " " + position_unit,
            bg=self.colors[0], fg=self.colors[5], justify=LEFT, font=("Arial Black", 12)
        )
        self.go_to_entry.configure(
            width=10, bg=self.colors[3]
        )
        self.go_to_button.configure(
            text="Go To", width=5, height=1, bg=self.colors[3], command=self.go_to
        )
        self.jog_positive_slow_button.configure(
            text=">", width=2, height=4, bg=self.colors[3]
        )
        self.jog_positive_button.configure(
            text=">>", width=2, height=4, bg=self.colors[3]
        )

        # Bind Widgets
        self.jog_negative_button.bind(
            "<ButtonPress>", lambda state: self.jog_negative(True, False)
        )
        self.jog_negative_button.bind(
            "<ButtonRelease>", lambda state: self.jog_negative(False, False)
        )
        self.jog_negative_slow_button.bind(
            "<ButtonPress>", lambda state: self.jog_negative(True, True)
        )
        self.jog_negative_slow_button.bind(
            "<ButtonRelease>", lambda state: self.jog_negative(False, True)
        )
        self.jog_positive_button.bind(
            "<ButtonPress>", lambda state: self.jog_positive(True, False)
        )
        self.jog_positive_button.bind(
            "<ButtonRelease>", lambda state: self.jog_positive(False, False)
        )
        self.jog_positive_slow_button.bind(
            "<ButtonPress>", lambda state: self.jog_positive(True, True)
        )
        self.jog_positive_slow_button.bind(
            "<ButtonRelease>", lambda state: self.jog_positive(False, True)
        )
        self.settings_canvas.bind(
            "<Enter>", lambda state: self.recolor_settings(True)
        )
        self.settings_canvas.bind(
            "<Leave>", lambda state: self.recolor_settings(False)
        )
        self.settings_canvas.bind(
            "<ButtonPress>", lambda instance: self.draw_settings()
        )

    def draw_controls(self, row, column):
        # Save Coordinates
        self.row = row
        self.column = column

        # Clear Subframe
        for child in self.subframe.winfo_children():
            child.grid_forget()

        # Configure Widgets
        self.configure_controls()

        # Draw Frame
        if column == 0:
            pad_l = 10
        else:
            pad_l = 5
        pad_r = 5
        if row == 0:
            pad_t = 10
        else:
            pad_t = 5
        if row == int(self.application_settings.settings["JogControlHeight"]) - 1:
            pad_b = 10
        else:
            pad_b = 5
        self.subframe.grid(row=row, column=column, padx=(pad_l, pad_r), pady=(pad_t, pad_b))
        self.settings_canvas.grid(row=0, column=6, rowspan=2)

        # Draw Widgets
        self.jog_negative_button.grid(
            row=0, column=0, rowspan=2, padx=(5, 0), pady=5
        )
        self.jog_negative_slow_button.grid(
            row=0, column=1, rowspan=2, pady=5
        )
        self.axis_position_label.grid(
            row=0, column=2, padx=10, pady=5, rowspan=2, sticky=W
        )
        self.go_to_entry.grid(
            row=0, column=3, padx=10, pady=(10, 0), sticky=S
        )
        self.go_to_button.grid(
            row=1, column=3, padx=5, pady=5
        )
        self.jog_positive_slow_button.grid(
            row=0, column=4, rowspan=2, pady=5
        )
        self.jog_positive_button.grid(
            row=0, column=5, rowspan=2, padx=(0, 5), pady=5
        )

    def update(self):
        # Unit
        if self.axis.axis_data.Rotary:
            unit_string = "°"
        else:
            unit_string = "mm"

        # Update Widgets
        self.axis_position_label.configure(
            text=self.axis.axis_data.Name + " \n" +
            str(round(self.axis.axis_data.Position, 2)) + " " + unit_string,
            bg=self.colors[0], fg=self.colors[5], justify=LEFT, font=("Arial Black", 12)
        )

    def configure_settings(self):
        # Unit
        # if self.axis.axis_data.Rotary:
        #     position_unit = "°"
        #     velocity_unit = "RPM"
        #     acceleration_unit = "rad/s^2"
        # else:
        #     position_unit = "mm"
        #     velocity_unit = "mm/min"
        #     acceleration_unit = "mm/s^2"

        # Configure Frames
        self.subframe.configure(bg=self.colors[0], width=400, height=95)
        self.settings_canvas.configure(bg=self.colors[0], width=50, height=95, highlightthickness=0)
        self.settings_canvas.create_text(25, 600, text="Exit", angle=90, fill=self.colors[5])
        self.subframe.columnconfigure(2, weight=1)
        self.subframe.grid_propagate(False)
        self.settings_canvas.grid_propagate(False)

        # Configure Widgets

        # Bind Widgets
        self.settings_canvas.bind(
            "<Enter>", lambda state: self.recolor_settings(True)
        )
        self.settings_canvas.bind(
            "<Leave>", lambda state: self.recolor_settings(False)
        )
        self.settings_canvas.bind(
            "<ButtonPress>", lambda coordinates: self.draw_controls(self.row, self.column)
        )

    def draw_settings(self):
        # Clear Subframe
        for child in self.subframe.winfo_children():
            child.grid_forget()

        # Configure Widgets
        self.configure_settings()

        # Draw Frame
        if self.column == 0:
            pad_l = 10
        else:
            pad_l = 5
        pad_r = 5
        if self.row == 0:
            pad_t = 10
        else:
            pad_t = 5
        if self.row == int(self.application_settings.settings["JogControlHeight"]) - 1:
            pad_b = 10
        else:
            pad_b = 5
        self.subframe.grid(row=self.row, column=self.column, padx=(pad_l, pad_r), pady=(pad_t, pad_b))
        self.settings_canvas.grid(row=0, column=6, rowspan=2)

        # Draw Widgets

    def jog_positive(self, button_state, half_speed):
        if self.connection_manager.is_connected():
            client = self.connection_manager.client
            i = self.axis.axis_data.AxisNo
            client.get_node(
                "ns=2;s=Application.MNDT_Vars.arHalfSpeed[" + str(i) + "]"
            ).set_value(half_speed)
            client.get_node(
                "ns=2;s=Application.MNDT_Vars.arJogPositive[" + str(i) + "]"
            ).set_value(button_state)

    def jog_negative(self, button_state, half_speed):
        if self.connection_manager.is_connected():
            client = self.connection_manager.client
            i = self.axis.axis_data.AxisNo
            client.get_node(
                "ns=2;s=Application.MNDT_Vars.arHalfSpeed[" + str(i) + "]"
            ).set_value(half_speed)
            client.get_node(
                "ns=2;s=Application.MNDT_Vars.arJogNegative[" + str(i) + "]"
            ).set_value(button_state)

    def go_to(self):
        if self.connection_manager.is_connected():
            client = self.connection_manager.client
            i = self.axis.axis_data.AxisNo
            client.get_node(
                "ns=2;s=Application.MNDT_Vars.arHalfSpeed[" + str(i) + "]"
            ).set_value(False)
            client.get_node(
                "ns=2;s=Application.MNDT_Vars.arGoToPosition[" + str(i) + "]"
            ).set_value(float(self.go_to_entry.get()), ua.VariantType.Float)
            client.get_node(
                "ns=2;s=Application.MNDT_Vars.arGoToCommand[" + str(i) + "]"
            ).set_value(True)

    def recolor_settings(self, hover_state):
        if hover_state:
            self.settings_canvas.configure(bg=self.colors[6])
        else:
            self.settings_canvas.configure(bg=self.colors[0])
