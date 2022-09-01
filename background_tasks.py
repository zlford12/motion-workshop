from opcua import Client
import time
import xml.etree.ElementTree


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


class ApplicationSettings:
    def __init__(self):
        self.settings_file = "ApplicationSettings.xml"
        self.settings = {}

        self.read_xml()

    def read_xml(self):
        for setting in xml.etree.ElementTree.parse(self.settings_file).getroot():
            self.settings[setting.tag] = setting.text


class Motion:
    def __init__(self):
        self.axis_file = "MachineConfig.xml"
        self.axis_list = []

        self.read_axes_from_file()

    def read_axes_from_file(self):
        self.axis_list = []
        for axis_element in xml.etree.ElementTree.parse(self.axis_file).getroot().find("AxisList").findall("Axis"):
            axis = self.Axis()
            axis.name = axis_element.find("Name").text
            axis.AxisNo = axis_element.find("AxisNo").text
            self.axis_list.append(axis)

    class Axis:
        def __init__(self):
            self.name = ""
            self.AxisNo = 0
            self.Rotary = False
            self.Linkable = False
            self.Offset = False

        class AxisLimits:
            def __init__(self):
                self.MinPosition = 0
                self.MaxPosition = 0
                self.MinCrashPosition = 0
                self.MaxCrashPosition = 0
                self.MaxVelocity = 0
                self.MaxAcceleration = 0
                self.MaxDeceleration = 0

        class AxisData:
            def __init__(self):
                self.Position = 0
                self.Velocity = 0
                self.Torque = 0
                self.Error = False
                self.Power = False
                self.Standstill = False
                self.InReference = False
                self.Warning = False
                self.ContinuousMotion = False
                self.Homing = False
                self.InPosition = False
                self.Stopping = False
