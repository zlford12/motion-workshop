from tkinter import *
from tkinter import messagebox  # Entry
from background_tasks import ConnectionManagement, ApplicationSettings, Motion


class UserInterface:
    def __init__(self):
        # Root Window
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.cleanup)
        self.root.title("Motion Workshop")
        self.root.geometry("1600x900")
        self.root.resizable(width=True, height=True)
        self.root.configure(bg="#333333")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Screen Elements
        self.menu_bar = Menu(self.root)
        self.header = Frame(self.root)
        self.body = Frame(self.root)
        self.scan_frame = Frame(self.root)
        self.jog_frame = Frame(self.root)
        self.footer = Frame(self.root)

        # Header Elements

        # Footer Elements
        self.connection_status_display = None

        # Draw UI
        self.draw_header()
        self.create_menubar()
        self.draw_body()
        self.draw_scan_frame()
        self.draw_jog_frame()
        self.draw_footer()

        # Update Loop
        self.stop_update = False
        self.update_loop_time = 200

    def create_menubar(self):
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.dummy_function)

        # Display Menus
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Display Menubar
        self.root.configure(menu=self.menu_bar)

    def draw_header(self):
        button_x = 10
        button_y = 3

        self.header.configure(bg="#555555")
        self.header.grid(row=0, column=0, columnspan=2, sticky=N+E+W)
        self.header.grid_columnconfigure(100, weight=1)

        open_client_button = Button(self.header)
        open_client_button.configure(
            text="Connect\nClient", width=button_x, height=button_y,
            command=lambda: connection_manager.open_client(application_settings.settings["ControllerIP"]), bg="#999999")
        open_client_button.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        disconnect_button = Button(self.header)
        disconnect_button.configure(
            text="Disconnect\nClient", width=button_x, height=button_y,
            command=connection_manager.disconnect, bg="#999999")
        disconnect_button.grid(row=0, column=1, sticky=W, pady=10)

        clear_error_button = Button(self.header)
        clear_error_button.configure(
            text="Reset", width=button_x, height=button_y, command=self.dummy_function, bg="#999999")
        clear_error_button.grid(row=0, column=100, sticky=E, padx=10, pady=10)

    def draw_body(self):
        self.body.configure(bg="#000000")
        self.body.grid(row=1, column=0, sticky=N+E+S+W)

    def draw_scan_frame(self):
        button_x = 12
        button_y = 2

        self.scan_frame.configure(bg="#999999")
        self.scan_frame.grid(row=1, column=1, rowspan=2, sticky=E+N+S)

        body1_button = Button(self.scan_frame)
        body1_button.configure(
            text="Jog Controls", width=button_x, height=button_y, command=self.dummy_function, bg="#cccccc")
        body1_button.grid(row=0, column=0, padx=10, pady=10)

        body2_button = Button(self.scan_frame)
        body2_button.configure(
            text="Gear Axes", width=button_x, height=button_y, command=self.dummy_function, bg="#cccccc")
        body2_button.grid(row=1, column=0, padx=10)

        body3_button = Button(self.scan_frame)
        body3_button.configure(
            text="Set Limits", width=button_x, height=button_y, command=self.dummy_function, bg="#cccccc")
        body3_button.grid(row=2, column=0, padx=10, pady=10)

    def draw_jog_frame(self):
        self.jog_frame.configure(bg="#333333", height=200)
        self.jog_frame.grid(row=2, column=0, sticky=S + E + W)

        for child in self.jog_frame.winfo_children():
            child.destroy()

    def draw_footer(self):

        self.footer.configure(bg="#555555", height=20)
        self.footer.columnconfigure(100, weight=1)
        self.footer.grid(row=3, column=0, columnspan=2, sticky=S+E+W)

        for child in self.footer.winfo_children():
            child.destroy()

        self.connection_status_display = Label(self.footer)
        self.connection_status_display.configure(text="Disconnected", bg="#555555")
        self.connection_status_display.grid(row=0, column=100, padx=10, sticky=E)

    def update_loop(self):
        # Update Connection Status Display
        if connection_manager.is_connected():
            self.connection_status_display.configure(text="Connected")
        else:
            self.connection_status_display.configure(text="Disconnected")

        # Check For Connection Management Error
        if connection_manager.error:
            connection_manager.error = False
            messagebox.showerror(title="Connection Error", message=connection_manager.error_message)

        # Loop
        if not self.stop_update:
            self.root.after(self.update_loop_time, self.update_loop)
            return

    def cleanup(self):
        connection_manager.disconnect()
        self.stop_update = True
        self.root.update()
        self.root.destroy()
        exit()

    def dummy_function(self):
        return

    @staticmethod
    def make_message_box():
        messagebox.showerror(title="title", message="message")

    class JogControl:
        def __init__(self):
            return

    class ScanTypes:
        def __init__(self):
            return


def main():
    # Connect To OPCUA Server
    if application_settings.settings["ConnectAtStartup"] == "True":
        connection_manager.open_client(application_settings.settings["ControllerIP"])

    # Test Code
    print("nothing")

    # Tkinter Main Loop
    user_interface.root.after(user_interface.update_loop_time, user_interface.update_loop)
    user_interface.root.mainloop()


if __name__ == "__main__":
    # Create Global Instances of Class Objects
    application_settings = ApplicationSettings()
    motion = Motion()
    connection_manager = ConnectionManagement()
    user_interface = UserInterface()

    main()
