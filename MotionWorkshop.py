import threading
from tkinter import *
from tkinter import messagebox  # Entry
from background_tasks import ConnectionManagement


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
        self.status_display = None

        # Footer Elements
        self.jog_speed_entry = None
        self.jog_accel_entry = None

        # Draw UI
        self.draw_header()
        self.create_menubar()
        self.draw_body()
        self.draw_scan_frame()
        self.draw_jog_frame()
        self.draw_footer()

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
            text="Connect\nClient", width=button_x, height=button_y, command=self.dummy_function, bg="#999999")
        open_client_button.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        disconnect_button = Button(self.header)
        disconnect_button.configure(
            text="Disconnect\nClient", width=button_x, height=button_y, command=self.dummy_function, bg="#999999")
        disconnect_button.grid(row=0, column=1, sticky=W, pady=10)

        clear_error_button = Button(self.header)
        clear_error_button.configure(
            text="Reset", width=button_x, height=button_y, command=self.dummy_function, bg="#999999")
        clear_error_button.grid(row=0, column=100, sticky=E, padx=10, pady=10)

        self.status_display = Label(self.header)
        self.status_display.configure(text="Disconnected", bg="#FF0000")
        self.status_display.grid(row=0, column=2, padx=10)

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
        self.footer.grid(row=3, column=0, columnspan=2, sticky=S+E+W)

        for child in self.footer.winfo_children():
            child.destroy()

        # self.jog_speed_entry = Entry(self.footer)
        # self.jog_speed_entry.configure(width=30, bg="#cccccc")
        # self.jog_speed_entry.grid(row=0, column=0, padx=10, pady=10)
        # self.jog_speed_entry.insert(0, "")
        #
        # self.jog_accel_entry = Entry(self.footer)
        # self.jog_accel_entry.configure(width=30, bg="#cccccc")
        # self.jog_accel_entry.grid(row=1, column=0, padx=10, pady=10)
        # self.jog_accel_entry.insert(0, "")
        #
        # speed_label = Label(self.footer)
        # speed_label.configure(text="Velocity ()", bg="#555555")
        # speed_label.grid(row=0, column=1, padx=10, pady=10)
        #
        # accel_label = Label(self.footer)
        # accel_label.configure(text="Acceleration ()", bg="#555555")
        # accel_label.grid(row=1, column=1, padx=10, pady=10)

    def update_status_display(self):
        false_boolean = False
        if false_boolean:
            self.status_display.configure(text="Connected", bg="#00FF00")
        else:
            self.status_display.configure(text="Disconnected", bg="#FF0000")

    def cleanup(self):
        self.root.update()
        self.root.destroy()
        connection_manager.close_requested = True
        connection_manager_thread.join()
        exit()

    def dummy_function(self):
        return

    @staticmethod
    def make_message_box():
        messagebox.showerror(title="title", message="message")


def main():
    # Connect OPCUA Client
    connection_manager_thread.start()

    # Tkinter Main Loop
    user_interface.root.mainloop()


if __name__ == "__main__":
    # Create Global Instances of Class Objects
    connection_manager = ConnectionManagement()
    user_interface = UserInterface()

    # Create Global Instances of Thread Objects
    connection_manager_thread = threading.Thread(target=connection_manager.is_connected)
    user_interface_thread = threading.Thread(target=None)

    main()
