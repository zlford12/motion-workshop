from opcua import Client
import time
import xml.etree.ElementTree


class ConnectionManagement:
    def __init__(self):
        self.connection_desired = False
        self.connection_okay = False
        self.connection_loop_time = 0.5
        self.client = Client("to be determined", timeout=3)
        self.error = False
        self.error_message = ""

    def is_connected(self):
        while True:
            if self.connection_desired:
                try:
                    self.client.get_node("i=2253")
                    self.connection_okay = True

                except Exception as e:
                    self.connection_okay = False
                    print(e)

            time.sleep(self.connection_loop_time)

    def open_client(self, ip):
        try:
            if not self.connection_desired:
                self.connection_desired = True
                print("opc.tcp://" + ip + ":4840")
                self.client = Client("opc.tcp://" + ip + ":4840", timeout=3)
                self.client.connect()
        except Exception as e:
            self.connection_desired = False
            self.error = True
            self.error_message = e

    def disconnect(self):
        try:
            if self.connection_desired:
                self.client.disconnect()
                self.connection_desired = False
        except Exception as e:
            self.error = True
            self.error_message = e


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
        self.axis_list = {"NoAxis": self.Axis}

        self.read_axes_from_file()

    def read_axes_from_file(self):
        self.axis_list = {}
        for axis_element in xml.etree.ElementTree.parse(self.axis_file).getroot().find("AxisList").findall("Axis"):
            axis = self.Axis()
            axis.AxisData.name = axis_element.find("Name").text
            print(axis.AxisData.name)
            axis.AxisData.AxisNo = axis_element.find("AxisNo").text
            axis.AxisData.Rotary = axis_element.find("Rotary").text == "True"
            axis.AxisData.Linkable = axis_element.find("Linkable").text == "True"
            axis.AxisData.Offset = axis_element.find("Offset").text == "True"

    class Axis:
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
                self.name = ""
                self.AxisNo = 0
                self.Rotary = False
                self.Linkable = False
                self.Offset = False
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
