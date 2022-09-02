from tkinter import *


class ScanTypes:
    def __init__(self):
        self.scan_types = {
            "P2P": self.P2P
        }

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
            self.linear_velocity_entry = Entry(self.control_frame)
            self.rotary_velocity_entry = Entry(self.control_frame)
            self.linear_position_delta_entry = Entry(self.control_frame)
            self.rotary_position_delta_entry = Entry(self.control_frame)
            self.dwell_time_entry = Entry(self.control_frame)
            self.vector_mode_selection = Checkbutton(self.control_frame)
            self.add_point_button = Button(self.control_frame)
            self.remove_point_button = Button(self.control_frame)
            self.copy_point_button = Button(self.control_frame)
            self.go_to_point_button = Button(self.control_frame)

        def configure(self):
            # Configure Widgets
            self.start_button.configure(
                text="Start Scan", width=12, height=2, bg=self.colors[3]
            )

        def draw(self):
            # Configure Widgets
            self.configure()

            # Draw Frames
            self.control_frame.grid(row=0, column=0)

            # Draw Widgets
            self.start_button.grid(
                row=0, column=0, rowspan=2, padx=5, pady=5
            )
