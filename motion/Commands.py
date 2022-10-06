from opcua import ua
from utility.ConnectionManagement import ConnectionManagement


class Commands:
    def __init__(self):
        self.command_list = {}

    def command(self, c: ConnectionManagement, command_name="None"):
        if c.is_connected():
            if command_name == "None":
                command_int = 0
            else:
                command_int = self.command_list[command_name]

            c.client.get_node("ns=2;s=Application.MNDT_Vars.iCommand")\
                .set_value(int(command_int), ua.VariantType.Int16)

    def populate_commands(self, c: ConnectionManagement):
        self.command_list = {}
        command_names = c.client.get_node("ns=2;s=Application.MNDT_Vars.arCommandNames").get_children()
        for i in range(len(command_names)):
            if command_names[i].get_value() != "" \
                    and command_names[i].get_data_type_as_variant_type() == ua.VariantType.String:
                self.command_list[command_names[i].get_value()] = i
