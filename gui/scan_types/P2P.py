from tkinter import *


class P2P:
    def __init__(self, frame, colors):
        # Create Frames
        self.frame = frame
        self.colors = colors
        self.control_frame = Frame(self.frame)
        self.points_frame = Frame(self.frame)

        # Create Widgets
        self.start_button = Button(self.control_frame)
        self.stop_button = Button(self.control_frame)
        self.linear_velocity_label = Label(self.control_frame)
        self.linear_velocity_entry = Entry(self.control_frame)
        self.linear_velocity_unit = Label(self.control_frame)
        self.rotary_velocity_label = Label(self.control_frame)
        self.rotary_velocity_entry = Entry(self.control_frame)
        self.rotary_velocity_unit = Label(self.control_frame)
        self.linear_position_delta_label = Label(self.control_frame)
        self.linear_position_delta_entry = Entry(self.control_frame)
        self.linear_position_delta_unit = Label(self.control_frame)
        self.rotary_position_delta_label = Label(self.control_frame)
        self.rotary_position_delta_entry = Entry(self.control_frame)
        self.rotary_position_delta_unit = Label(self.control_frame)
        self.dwell_time_label = Label(self.control_frame)
        self.dwell_time_entry = Entry(self.control_frame)
        self.dwell_time_unit = Label(self.control_frame)
        self.vector_mode_selection = Checkbutton(self.control_frame)

        self.add_point_button = Button(self.control_frame)
        self.remove_point_button = Button(self.control_frame)
        self.copy_point_button = Button(self.control_frame)
        self.go_to_point_button = Button(self.control_frame)

    def configure(self):
        # Configure Frame
        self.control_frame.configure(bg=self.colors[3], width=500)

        # Parameters
        entry_width = 10
        label_font = ("Arial Black", 10)

        # Configure Widgets
        self.start_button.configure(
            text="Start Scan", width=12, height=2, bg=self.colors[4]
        )
        self.stop_button.configure(
            text="Stop Scan", width=12, height=2, bg=self.colors[4]
        )
        self.linear_velocity_label.configure(
            text="Linear Velocity", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.linear_velocity_entry.configure(
            width=entry_width
        )
        self.linear_velocity_unit.configure(
            text="mm/s", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotary_velocity_label.configure(
            text="Rotary Velocity", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotary_velocity_entry.configure(
            width=entry_width
        )
        self.rotary_velocity_unit.configure(
            text="RPM", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.linear_position_delta_label.configure(
            text="Linear Position\nDelta", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.linear_position_delta_entry.configure(
            width=entry_width
        )
        self.linear_position_delta_unit.configure(
            text="mm", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotary_position_delta_label.configure(
            text="Rotary Position\nDelta", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.rotary_position_delta_entry.configure(
            width=entry_width
        )
        self.rotary_position_delta_unit.configure(
            text="deg", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.dwell_time_label.configure(
            text="Dwell Time", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.dwell_time_entry.configure(
            width=entry_width
        )
        self.dwell_time_unit.configure(
            text="ms", bg=self.colors[3], font=label_font, justify=LEFT
        )
        self.vector_mode_selection.configure(
            text="Vector Mode", bg=self.colors[3], font=label_font, justify=LEFT
        )

    def draw_controls(self):
        # Configure Widgets
        self.configure()

        # Draw Frames
        self.control_frame.grid(row=0, column=0)

        # Draw Widgets
        self.start_button.grid(
            row=0, column=0, columnspan=2, padx=(10, 5), pady=10
        )
        self.stop_button.grid(
            row=0, column=2, columnspan=2, padx=(5, 10), pady=10
        )
        self.linear_velocity_label.grid(
            row=1, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.linear_velocity_entry.grid(
            row=2, column=0, padx=5, pady=(1, 10)
        )
        self.linear_velocity_unit.grid(
            row=2, column=1, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.rotary_velocity_label.grid(
            row=1, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.rotary_velocity_entry.grid(
            row=2, column=2, padx=5, pady=(1, 10)
        )
        self.rotary_velocity_unit.grid(
            row=2, column=3, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.linear_position_delta_label.grid(
            row=3, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.linear_position_delta_entry.grid(
            row=4, column=0, padx=5, pady=(1, 10)
        )
        self.linear_position_delta_unit.grid(
            row=4, column=1, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.rotary_position_delta_label.grid(
            row=3, column=2, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.rotary_position_delta_entry.grid(
            row=4, column=2, padx=5, pady=(1, 10)
        )
        self.rotary_position_delta_unit.grid(
            row=4, column=3, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.dwell_time_label.grid(
            row=5, column=0, columnspan=2, padx=5, pady=(10, 1), sticky=W
        )
        self.dwell_time_entry.grid(
            row=6, column=0, padx=5, pady=(1, 10)
        )
        self.dwell_time_unit.grid(
            row=6, column=1, padx=(1, 5), pady=(1, 10), sticky=W
        )
        self.vector_mode_selection.grid(
            row=5, column=2, rowspan=2, padx=5, pady=5
        )
