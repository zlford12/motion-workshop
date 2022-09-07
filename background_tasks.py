from opcua import Client, ua
import xml.etree.ElementTree


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
        self.axis_list = [self.Axis()]
        self.machine_config = self.MachineConfig(self.axis_file)
        self.commands = self.Commands()

        self.read_axes_from_file()

    def read_axes_from_file(self):
        self.axis_list = []
        for axis_element in xml.etree.ElementTree.parse(self.axis_file).getroot().find("AxisList").findall("Axis"):
            axis = self.Axis()
            axis.AxisData.Name = axis_element.find("Name").text
            axis.AxisData.AxisNo = axis_element.find("AxisNo").text
            axis.AxisData.Rotary = axis_element.find("Rotary").text == "True"
            axis.AxisData.Linkable = axis_element.find("Linkable").text == "True"
            axis.AxisData.Offset = axis_element.find("Offset").text == "True"
            self.axis_list.append(axis)

    def read_axes_from_system(self, client=Client("")):
        self.axis_list = []
        number_of_axes = client.get_node("ns=2;s=Application.Custom_Vars.iNumberOfAxesToVar").get_value()
        for i in range(number_of_axes):
            axis = self.Axis()
            axis.AxisData.Name = \
                client.get_node(
                    "ns=2;s=Application.PersistentVars.arAxisNames[" + str(i + 1) + "]"
                ).get_value()
            axis.AxisData.AxisNo = \
                client.get_node(
                    "ns=2;s=Application.PersistentVars.arAxisList[" + str(i + 1) + "].AxisNo"
                ).get_value()
            axis.AxisData.Rotary = \
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(i + 1) + "].Rotary"
                ).get_value()
            axis.AxisData.Linkable = \
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(i + 1) + "].LinkableAxis"
                ).get_value()
            axis.AxisData.Offset = \
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(i + 1) + "].OffsetAxis"
                ).get_value()
            self.axis_list.append(axis)

    class Axis:
        def __init__(self):
            self.AxisLimits = Motion.AxisLimits()
            self.AxisData = Motion.AxisData()

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
            self.Name = ""
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

        def update(self, client=Client("")):
            self.Position = \
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(self.AxisNo) + "].Position"
                ).get_value()
            self.Velocity = \
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(self.AxisNo) + "].Velocity"
                ).get_value()
            self.Torque = \
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(self.AxisNo) + "].Torque"
                ).get_value()
            status_bits = \
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(self.AxisNo) + "].StatusBits"
                ).get_value()
            self.Error = status_bits & (1 << 0) != 0
            self.Power = status_bits & (1 << 0) != 0
            self.Standstill = status_bits & (1 << 0) != 0
            self.InReference = status_bits & (1 << 0) != 0
            self.Warning = status_bits & (1 << 0) != 0
            self.ContinuousMotion = status_bits & (1 << 0) != 0
            self.Homing = status_bits & (1 << 0) != 0
            self.InPosition = status_bits & (1 << 0) != 0
            self.Stopping = status_bits & (1 << 0) != 0

    class MachineConfig:
        def __init__(self, config_file):
            self.config_file = config_file
            self.default_scan_type = ""
            self.available_scan_types = []
            self.safety_devices = []

            self.read_config_from_file()

        def read_config_from_file(self):
            self.available_scan_types = []
            self.safety_devices = []
            config = xml.etree.ElementTree.parse(self.config_file).getroot()
            self.default_scan_type = config.find("DefaultScanType").text
            for scan_type in config.find("AvailableScanTypes").findall("ScanType"):
                self.available_scan_types.append(scan_type.text)
            for safety_device in config.find("SafetyDevices").findall("SafetyDevice"):
                self.safety_devices.append(safety_device.text)

        def read_config_from_system(self, client=Client("to be determined", timeout=3)):
            return

    class Commands:
        def __init__(self):
            self.command_list = {}

        def command(self, client=Client(""), command_name="None"):
            if command_name == "None":
                command_int = 0
            else:
                command_int = self.command_list[command_name]

            client.get_node("ns=2;s=Application.MNDT_Vars.iCommand").set_value(command_int)

        def populate_commands(self, client=Client("")):
            self.command_list = {}
            command_names = client.get_node("ns=2;s=Application.MNDT_Vars.arCommandNames").get_children()
            for i in range(len(command_names)):
                if command_names[i].get_value() != "" \
                        and command_names[i].get_data_type_as_variant_type() == ua.VariantType.String:
                    print(command_names[i].get_value(), i)
