from opcua import Client
import time


class ConnectionManagement:
    def __init__(self):
        self.connection_desired = False
        self.connection_okay = False
        self.connection_loop_time = 0.5
        self.client = Client("")
        self.error = False
        self.error_message = ""

    def is_connected(self):
        if self.connection_desired:
            try:
                self.client.get_node("i=2253")
                self.connection_okay = True
                return True

            except Exception as e:
                self.connection_okay = False
                self.error = True
                self.error_message = e
                return False
        else:
            return False

    def open_client(self, ip):
        try:
            if not self.connection_desired:
                self.connection_desired = True
                self.client = Client("opc.tcp://" + ip + ":4840", timeout=3)
                self.client.connect()
        except Exception as e:
            self.connection_desired = False
            self.error = True
            self.error_message = e

    def disconnect(self):
        try:
            if self.connection_desired:
                self.connection_desired = False
                time.sleep(0.2)
                self.client.disconnect()
        except Exception as e:
            self.error = True
            self.error_message = e
