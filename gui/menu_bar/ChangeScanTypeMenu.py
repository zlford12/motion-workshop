from motion.Motion import Motion
from opcua import ua
import tkinter
from tkinter import *
from utility.ConnectionManagement import ConnectionManagement


class ChangeScanTypeMenu:

    def __init__(
        self, colors, root: Tk, motion: Motion, c: ConnectionManagement
    ):
        # Class Objects
        self.motion = motion
        self.root = root
        self.c = c

        # Color Scheme
        self.colors = colors

        # Window
        self.window = None

        # Widgets
        self.scan_types: [str] = []
        self.selected_scan_type = StringVar()

    def open_selection(self):
        self.window = tkinter.Toplevel()
        self.window.title("Change Scan Type")
        self.window.configure(bg=self.colors[3])
        self.window.iconphoto(False, PhotoImage(file='config/icon.png'))

        select_label = Label(self.window)
        select_label.configure(
            text="Select Scan Type", font=("Arial Black", 10), bg=self.colors[3]
        )
        select_label.grid(
            row=0, column=0, padx=5, pady=5
        )

        self.scan_types = self.motion.machine_config.available_scan_types
        scan_type_menu = OptionMenu(
            self.window, self.selected_scan_type, *self.scan_types
        )
        scan_type_menu.configure(
            width=10, bg=self.colors[4], font=("Arial Black", 8), highlightthickness=0
        )
        scan_type_menu.grid(
            row=1, column=0, padx=5, pady=5
        )

        apply_button = Button(self.window)
        apply_button.configure(
            text="Apply", bg=self.colors[4],
            command=self.change_scan_type
        )
        apply_button.grid(
            row=2, column=0, padx=5, pady=5
        )

    def change_scan_type(self):
        if self.selected_scan_type.get() in self.motion.machine_config.available_scan_types:
            if self.c.is_connected():
                for i in range(len(self.motion.machine_config.available_scan_types)):
                    if self.motion.machine_config.available_scan_types[i] == self.selected_scan_type.get():
                        self.c.node_list.selected_scan_type.set_value(int(i), ua.VariantType.Int16)
            else:
                self.motion.machine_config.selected_scan_type = self.selected_scan_type.get()

        self.window.destroy()
