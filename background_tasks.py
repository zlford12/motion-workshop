from opcua import Client
import time


class ConnectionManagement:
    def __init__(self):
        self.connection_desired = False
        self.connection_okay = False
        self.close_requested = False
        self.connection_loop_time = 0.5
        self.client = Client("opc.tcp://" + open("ip.txt", "r").read() + ":4840", timeout=3)

    def is_connected(self):
        while not self.close_requested:
            try:
                self.client.get_node("i=2253")
                self.connection_okay = True

            except Exception as e:
                self.connection_okay = False
                print(e)

            time.sleep(self.connection_loop_time)

    def open_client(self):
        try:
            if not self.connection_desired:
                self.connection_desired = True
                self.client.connect()
        except Exception as e:
            self.connection_desired = False
            # messagebox.showerror(title="OPC Error", message="Failure Connecting\nto OPC UA Server")
            print(e)
            return

    def disconnect(self):
        try:
            if self.connection_desired:
                self.client.disconnect()
                self.connection_desired = False
        except Exception as e:
            # messagebox.showerror(title="OPC Error", message="Failed to\nDisconnect")
            print(e)
