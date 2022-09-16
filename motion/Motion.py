from motion.Axis import Axis
from motion.MachineConfig import MachineConfig
from motion.Commands import Commands
from opcua import Client
import xml.etree.ElementTree


class Motion:
    def __init__(self):
        self.axis_file = "config/MachineConfig.xml"
        self.axis_list = [Axis()]
        self.machine_config = MachineConfig(self.axis_file)
        self.commands = Commands()
        self.communication_error = False
        self.error_message = ""

        self.read_axes_from_file()

    def read_axes_from_file(self):
        self.axis_list = []
        for axis_element in xml.etree.ElementTree.parse(self.axis_file).getroot().find("AxisList").findall("Axis"):
            axis = Axis()
            axis.axis_data.Name = axis_element.find("Name").text
            axis.axis_data.AxisNo = axis_element.find("AxisNo").text
            axis.axis_data.Rotary = axis_element.find("Rotary").text == "True"
            axis.axis_data.Linkable = axis_element.find("Linkable").text == "True"
            axis.axis_data.Offset = axis_element.find("Offset").text == "True"
            self.axis_list.append(axis)

    def read_axes_from_system(self, client: Client):
        self.axis_list = []
        number_of_axes = client.get_node("ns=2;s=Application.Custom_Vars.iNumberOfAxesToVar").get_value()
        for i in range(number_of_axes):
            axis = Axis()
            axis.axis_data.Name = \
                client.get_node(
                    "ns=2;s=Application.PersistentVars.arAxisNames[" + str(i + 1) + "]"
                ).get_value()
            axis.axis_data.AxisNo = \
                client.get_node(
                    "ns=2;s=Application.PersistentVars.arAxisList[" + str(i + 1) + "].AxisNo"
                ).get_value()
            axis.axis_data.Rotary = \
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(axis.axis_data.AxisNo) + "].Rotary"
                ).get_value()
            axis.axis_data.Linkable = \
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(axis.axis_data.AxisNo) + "].LinkableAxis"
                ).get_value()
            axis.axis_data.Offset = \
                client.get_node(
                    "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(axis.axis_data.AxisNo) + "].OffsetAxis"
                ).get_value()
            self.axis_list.append(axis)

    def update(self, client: Client):
        for axis in self.axis_list:
            try:
                # Axis Data
                axis.axis_data.Position = \
                    client.get_node(
                        "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(axis.axis_data.AxisNo) + "].Position"
                    ).get_value()
                axis.axis_data.Velocity = \
                    client.get_node(
                        "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(axis.axis_data.AxisNo) + "].Velocity"
                    ).get_value()
                axis.axis_data.Torque = \
                    client.get_node(
                        "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(axis.axis_data.AxisNo) + "].Torque"
                    ).get_value()
                status_bits = \
                    client.get_node(
                        "ns=2;s=Application.MNDT_Vars.arMNDTAxisData[" + str(axis.axis_data.AxisNo) + "].StatusBits"
                    ).get_value()
                axis.axis_data.Error = status_bits & (1 << 0) != 0
                axis.axis_data.Power = status_bits & (1 << 0) != 0
                axis.axis_data.Standstill = status_bits & (1 << 0) != 0
                axis.axis_data.InReference = status_bits & (1 << 0) != 0
                axis.axis_data.Warning = status_bits & (1 << 0) != 0
                axis.axis_data.ContinuousMotion = status_bits & (1 << 0) != 0
                axis.axis_data.Homing = status_bits & (1 << 0) != 0
                axis.axis_data.InPosition = status_bits & (1 << 0) != 0
                axis.axis_data.Stopping = status_bits & (1 << 0) != 0

                # Axis Limits
                axis.axis_limits.MinPosition = \
                    client.get_node(
                        "ns=2;s=Application.PersistentVars.arMNDTAxisLimits[" +
                        str(axis.axis_data.AxisNo) + "].MinPosition"
                    )
            except Exception as e:
                self.communication_error = True
                self.error_message = e
