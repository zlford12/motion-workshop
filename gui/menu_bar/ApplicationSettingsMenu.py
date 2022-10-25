import tkinter
from tkinter import *
from utility.ApplicationSettings import ApplicationSettings


class ApplicationSettingsMenu:

    def __init__(
        self, colors, root: Tk, application_settings: ApplicationSettings
    ):
        # Class Objects
        self.application_settings = application_settings
        self.root = root

        # Color Scheme
        self.colors = colors

        # Window
        self.window = None

        # Widgets
        self.setting_labels: [Label] = []
        self.setting_entries: [Entry] = []
        self.setting_keys: [str] = []

    def open_settings(self):
        self.window = tkinter.Toplevel()
        self.window.title("Application Settings")
        self.window.configure(bg=self.colors[3])
        self.window.iconphoto(False, PhotoImage(file='config/icon.png'))

        self.setting_labels = []
        self.setting_entries = []
        self.setting_keys = []
        current_row = 0

        for setting in self.application_settings.settings:
            self.setting_labels.append(Label(self.window))
            self.setting_labels[current_row].configure(
                text=setting, bg=self.colors[3]
            )
            self.setting_labels[current_row].grid(
                row=current_row, column=0, sticky=E, padx=5, pady=(5, 0)
            )

            self.setting_entries.append(Entry(self.window))
            self.setting_entries[current_row].configure(
                width=15
            )
            self.setting_entries[current_row].insert(0, self.application_settings.settings[setting])
            self.setting_entries[current_row].grid(
                row=current_row, column=1, sticky=W, padx=5, pady=(5, 0)
            )

            self.setting_keys.append(setting)

            current_row = current_row + 1

        apply_button = Button(self.window)
        apply_button.configure(
            text="Apply", bg=self.colors[4],
            command=self.apply_settings
        )
        apply_button.grid(
            row=current_row, column=0, columnspan=2, padx=5, pady=5
        )

    def apply_settings(self):
        for i in range(len(self.setting_keys)):
            self.application_settings.settings[self.setting_keys[i]] = \
                self.setting_entries[i].get()

        self.application_settings.write_xml()
