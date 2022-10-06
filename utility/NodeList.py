import opcua
from opcua import Client, ua


class NodeList:
    def __init__(self):
        self.axis_data = [[opcua.Node]]
        self.axis_limits = [[opcua.Node]]
        self.output_names = [opcua.Node]
        self.outputs = [opcua.Node]
        self.command_names = [opcua.Node]
        self.command = opcua.Node
        self.plc_status = opcua.Node
        self.axis_status = [opcua.Node]

    def get_nodes(self, client: Client):
        # Axis Data
        self.axis_data = [[]]
        for child in client.get_node("ns=2;s=Application.MNDT_Vars.arMNDTAxisData").get_children():
            if str(child.get_node_class()) == "NodeClass.Object":
                structure = []
                for node in child.get_children():
                    structure.append(node)
                self.axis_data.append(structure)

        # Axis Limits
        self.axis_limits = [[]]
        for child in client.get_node("ns=2;s=Application.PersistentVars.arMNDTAxisLimits").get_children():
            if str(child.get_node_class()) == "NodeClass.Object":
                structure = []
                for node in child.get_children():
                    structure.append(node)
                self.axis_limits.append(structure)

        # Outputs
        self.output_names = []
        self.outputs = []
        for child in client.get_node("ns=2;s=Application.MNDT_Vars.arOutputNames").get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.String:
                self.output_names.append(child)

        for child in client.get_node("ns=2;s=Application.MNDT_Vars.arOutputs").get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.Boolean:
                self.outputs.append(child)

        # Commands
        self.command_names = []
        self.command = []
        for child in client.get_node("ns=2;s=Application.MNDT_Vars.arCommandNames").get_children():
            if child.get_data_type_as_variant_type() == ua.VariantType.String:
                self.command_names.append(child)

        self.command = client.get_node("ns=2;s=Application.MNDT_Vars.iCommand")

        # Diagnostics
        self.plc_status = client.get_node("ns=18;s=System.DisplayedDiagnosis")

        self.axis_status = []
        for child in client.get_node("ns=12;s=Motion.AxisSet.LocalControl").get_children():
            for node in child.get_children():
                if "DiagnosisText" in str(node):
                    self.axis_status.append(node)
