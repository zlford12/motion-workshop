from opcua import Client


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
