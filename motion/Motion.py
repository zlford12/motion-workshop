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
