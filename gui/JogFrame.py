from tkinter import *
from gui.JogControl import JogControl
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


class JogFrame:
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

        # Jog Frame Elements
        self.jog_canvas = Canvas(self.root)
        self.jog_frame = Frame(self.jog_canvas)
        self.jog_scroll = Scrollbar(self.root)
        self.jog_controls = JogControl

    def draw(self):
        # Delete Jog Controls
        for child in self.jog_frame.winfo_children():
            child.destroy()

        # Configure Jog UI
        self.jog_canvas.configure(
            bg=self.colors[1], highlightthickness=0, xscrollcommand=self.jog_scroll.set
        )
        self.jog_frame.configure(bg=self.colors[1])
        self.jog_scroll.configure(orient="horizontal", command=self.jog_canvas.xview)

        # Populate Jog Frame
        self.jog_controls = []
        row = 0
        column = 0
        for i in range(len(self.motion.axis_list)):
            self.jog_controls.append(JogControl(
                self.jog_frame, self.motion.axis_list[i], self.colors,
                self.connection_manager, self.application_settings, self.motion
            ))
            self.jog_controls[i].draw_controls(row, column)
            row += 1
            if row > int(self.application_settings.settings["JogControlHeight"]) - 1:
                row = 0
                column += 1

        # Display Jog UI
        self.jog_canvas.grid(row=2, column=0, sticky=S + E + W)
        self.jog_canvas.create_window(0, 0, anchor=W, window=self.jog_frame)
        self.jog_scroll.grid(row=3, column=0, sticky=S + E + W)

        # Update Canvas
        self.jog_canvas.update_idletasks()
        self.jog_canvas.configure(scrollregion=self.jog_canvas.bbox("all"), height=self.jog_frame.winfo_height())
        self.jog_canvas.bind("Configure", self.update_jog_canvas)

    def update_jog_canvas(self):
        self.jog_canvas.configure(scrollregion=self.jog_canvas.bbox("all"))
