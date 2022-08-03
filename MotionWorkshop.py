from tkinter import *
from tkinter import messagebox, Entry
from opcua import Client, ua
import threading
import time


class ConnectionManagement:
    def __init__(self):
        self.connection_monitor_thread = threading.Thread(target=self.is_connected)
        self.connection_desired = False
        self.connection_okay = False
        self.close_requested = False
        self.connection_loop_time = 0.5

    def start_connection_monitor_thread(self):
        self.connection_monitor_thread.start()

    def is_connected(self):
        while not self.close_requested:
            try:
                client.get_node("i=2253")
                self.connection_okay = True
            except Exception as e:
                self.connection_okay = False
                print(e)

            time.sleep(self.connection_loop_time)

    def open_client(self):
        try:
            if not self.connection_desired:
                self.connection_desired = True
                client.connect()
        except Exception as e:
            self.connection_desired = False
            messagebox.showerror(title="OPC Error", message="Failure Connecting\nto OPC UA Server")
            print(e)
            return

    def disconnect(self):

        try:
            if self.connection_desired:
                client.disconnect()
                self.connection_desired = False
        except Exception as e:
            messagebox.showerror(title="OPC Error", message="Failed to\nDisconnect")
            print(e)

        for child in user_interface.right_side.winfo_children():
            child.destroy()


class UserInterface:
    def __init__(self):
        self.root = Tk()
        self.body = Frame(self.root)
        self.header = Frame(self.root)
        self.footer = Frame(self.root)
        self.left_side = Frame(self.root)
        self.right_side = Frame(self.root)

        # Header Elements
        self.status_display = None

        # Footer Elements
        self.jog_speed_entry = None
        self.jog_accel_entry = None

    def draw_header(self):
        btnx = 10
        btny = 3

        self.header.configure(bg="#555555")
        self.header.grid(row=0, column=0, columnspan=3, sticky=N+E+W)
        self.header.grid_columnconfigure(100, weight=1)

        openclientbtn = Button(self.header)
        openclientbtn.configure(text="Connect\nClient", width=btnx, height=btny, command=self.dummyfunc, bg="#999999")
        openclientbtn.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        disconnectbtn = Button(self.header)
        disconnectbtn.configure(text="Disconnect\nClient", width=btnx, height=btny, command=self.dummyfunc, bg="#999999")
        disconnectbtn.grid(row=0, column=1, sticky=W, pady=10)

        clearerrbtn = Button(self.header)
        clearerrbtn.configure(text="Reset", width=btnx, height=btny, command=self.dummyfunc, bg="#999999")
        clearerrbtn.grid(row=0, column=100, sticky=E, padx=10, pady=10)

        self.status_display = Label(self.header)
        self.status_display.configure(text="Disconnected", bg="#FF0000")
        self.status_display.grid(row=0, column=2, padx=10)

    def draw_footer(self):

        self.footer.configure(bg="#555555")
        self.footer.grid(row=2, column=0, columnspan=3, sticky=S+E+W)

        for child in self.footer.winfo_children():
            child.destroy()

        self.jog_speed_entry = Entry(self.footer)
        self.jog_speed_entry.configure(width=30, bg="#cccccc")
        self.jog_speed_entry.grid(row=0, column=0, padx=10, pady=10)
        self.jog_speed_entry.insert(0, "")

        self.jog_accel_entry = Entry(self.footer)
        self.jog_accel_entry.configure(width=30, bg="#cccccc")
        self.jog_accel_entry.grid(row=1, column=0, padx=10, pady=10)
        self.jog_accel_entry.insert(0, "")

        speed_label = Label(self.footer)
        speed_label.configure(text="Velocity ()", bg="#555555")
        speed_label.grid(row=0, column=1, padx=10, pady=10)

        accel_label = Label(self.footer)
        accel_label.configure(text="Acceleration ()", bg="#555555")
        accel_label.grid(row=1, column=1, padx=10, pady=10)

    def draw_left_side(self):
        btnx = 12
        btny = 2

        self.left_side.configure(bg="#999999")
        self.left_side.grid(row=1, column=0, sticky=W + N + S)

        body1_button = Button(self.left_side)
        body1_button.configure(text="Jog Controls", width=btnx, height=btny, command=self.dummyfunc, bg="#cccccc")
        body1_button.grid(row=0, column=0, padx=10, pady=10)

        body2_button = Button(self.left_side)
        body2_button.configure(text="Gear Axes", width=btnx, height=btny, command=self.dummyfunc, bg="#cccccc")
        body2_button.grid(row=1, column=0, padx=10)

        body3_button = Button(self.left_side)
        body3_button.configure(text="Set Limits", width=btnx, height=btny, command=self.dummyfunc, bg="#cccccc")
        body3_button.grid(row=2, column=0, padx=10, pady=10)

    def draw_body(self):
        self.body.configure(bg="#333333")
        self.body.grid(row=1, column=1)

    def update_status_display(self):
        false_boolean = False
        if false_boolean:
            self.status_display.configure(text="Connected", bg="#00FF00")
        else:
            self.status_display.configure(text="Disconnected", bg="#FF0000")

    def cleanup(self):
        user_interface.root.update()
        user_interface.root.destroy()
        exit()

    def dummyfunc(self):
        return


def main():
    # Initialize Tkinter
    user_interface.root.protocol("WM_DELETE_WINDOW", user_interface.cleanup)
    user_interface.root.title("Bosch Rexroth Commissioning Tool")
    user_interface.root.geometry("640x480")
    user_interface.root.resizable(width=False, height=False)
    user_interface.root.configure(bg="#333333")
    user_interface.root.grid_columnconfigure(1, weight=1)
    user_interface.root.grid_rowconfigure(1, weight=1)

    # Draw Frames
    user_interface.draw_header()
    user_interface.draw_footer()
    user_interface.draw_left_side()
    user_interface.draw_body()

    # Connect OPCUA Client
    connection_management.open_client()
    connection_management.start_connection_monitor_thread()

    # Tkinter Main Loop
    user_interface.root.mainloop()


if __name__ == "__main__":
    # Create Global Instances of Class Objects
    connection_management = ConnectionManagement()
    # motion_control = MotionControl()
    # axis_positioning = AxisPositioning()
    user_interface = UserInterface()
    client = Client("opc.tcp://" + open("ip.txt", "r").read() + ":4840", timeout=3)

    main()
