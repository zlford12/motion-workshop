from motion.Axis import Axis
from motion.MachineConfig import MachineConfig
from motion.Commands import Commands
from motion.Outputs import Outputs
from utility.ConnectionManagement import ConnectionManagement
import xml.etree.ElementTree


class Motion:
    def __init__(self):
        self.axis_file = "config/MachineConfig.xml"
        self.axis_list = [Axis()]
        self.machine_config = MachineConfig(self.axis_file)
        self.commands = Commands()
        self.outputs = Outputs()
        self.communication_error = False
        self.error_message = ""

        self.link_status = False

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

    def read_axes_from_system(self, c: ConnectionManagement):
        self.axis_list = []
        number_of_axes = c.client.get_node("ns=2;s=Application.Custom_Vars.iNumberOfAxesToVar").get_value()
        for i in range(number_of_axes):
            axis = Axis()
            axis.axis_data.Name = \
                c.client.get_node(
                    "ns=2;s=Application.PersistentVars.arAxisNames[" + str(i + 1) + "]"
                ).get_value()
            axis.axis_data.AxisNo = \
                c.client.get_node(
                    "ns=2;s=Application.PersistentVars.arAxisList[" + str(i + 1) + "].AxisNo"
                ).get_value()
            axis.axis_data.Rotary = c.node_list.axis_data[axis.axis_data.AxisNo + 1][4].get_value()
            axis.axis_data.Linkable = c.node_list.axis_data[axis.axis_data.AxisNo + 1][5].get_value()
            axis.axis_data.Offset = c.node_list.axis_data[axis.axis_data.AxisNo + 1][6].get_value()
            self.axis_list.append(axis)

    def update(self, c: ConnectionManagement):

        for axis in self.axis_list:
            try:
                # Local Vars
                a1 = c.node_list.axis_data
                a2 = c.node_list.axis_limits
                i = axis.axis_data.AxisNo + 1

                # Axis Data
                axis.axis_data.Name = a1[i][0].get_value()
                axis.axis_data.Rotary = a1[i][4].get_value()
                axis.axis_data.Linkable = a1[i][5].get_value()
                axis.axis_data.Offset = a1[i][6].get_value()
                axis.axis_data.Position = a1[i][1].get_value()
                axis.axis_data.Velocity = a1[i][2].get_value()
                axis.axis_data.Torque = a1[i][3].get_value()
                status_bits = a1[i][7].get_value()
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
                axis.axis_limits.MinPosition = a2[i][1].get_value()
                axis.axis_limits.MaxPosition = a2[i][0].get_value()
                axis.axis_limits.MinCrashPosition = a2[i][11].get_value()
                axis.axis_limits.MaxCrashPosition = a2[i][10].get_value()
                axis.axis_limits.MaxVelocity = a2[i][2].get_value()
                axis.axis_limits.MaxAcceleration = a2[i][4].get_value()
                axis.axis_limits.MaxDeceleration = a2[i][6].get_value()
                axis.axis_limits.SetVelocity = a2[i][12].get_value()
                axis.axis_limits.SetAcceleration = a2[i][13].get_value()
                axis.axis_limits.SetDeceleration = a2[i][14].get_value()

            except Exception as e:
                self.communication_error = True
                self.error_message = e
                print(e)

        try:
            self.link_status = c.client.get_node(
                "ns=2;s=Application.MNDT_Vars.arOutputs[" + str(self.outputs.output_list["Linked"]) + "]"
            ).get_value()
        except Exception as e:
            self.communication_error = True
            self.error_message = e
