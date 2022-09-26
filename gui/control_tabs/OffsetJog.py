from tkinter import *
from tkinter import ttk
from gui.JogControl import JogControl
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class OffsetJog:
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
        self.offset_jog_frame = ttk.Frame(self.tabs)

        # Jog Frame Elements
        self.jog_canvas = Canvas(self.offset_jog_frame)
        self.jog_frame = Frame(self.jog_canvas)
        self.jog_scroll = Scrollbar(self.offset_jog_frame)
        self.jog_controls = JogControl

    def draw(self):
        # Draw Tab Frame
        self.offset_jog_frame.rowconfigure(0, weight=1)
        self.tabs.add(self.offset_jog_frame, text="Offset Jog")

        # Delete Jog Controls
        for child in self.jog_frame.winfo_children():
            child.destroy()

        # Configure Jog UI
        self.jog_canvas.configure(
            bg=self.colors[1], highlightthickness=0, yscrollcommand=self.jog_scroll.set
        )
        self.jog_frame.configure(bg=self.colors[1])
        self.jog_scroll.configure(orient="vertical", command=self.jog_canvas.yview)

        # Populate Jog Frame
        self.jog_controls = []
        row = 0
        column = 0
        for i in range(len(self.motion.axis_list)):
            self.jog_controls.append(JogControl(
                self.jog_frame, self.motion.axis_list[i], self.colors,
                self.connection_manager, self.application_settings, self.motion
            ))

            if self.motion.axis_list[i].axis_data.Offset:
                self.jog_controls[i].draw_controls(row, column)
                row += 1

        # Display Jog UI
        self.jog_canvas.grid(row=0, column=0, sticky=W + N + S)
        self.jog_canvas.create_window(0, 0, anchor=W, window=self.jog_frame)
        self.jog_scroll.grid(row=0, column=1, sticky=E + N + S)

        # Update Canvas
        self.jog_canvas.update_idletasks()
        self.jog_canvas.configure(scrollregion=self.jog_canvas.bbox("all"), width=self.jog_frame.winfo_width())
        self.jog_canvas.bind("Configure", self.update_jog_canvas)

    def update_jog_canvas(self):
        self.jog_canvas.configure(scrollregion=self.jog_canvas.bbox("all"))
