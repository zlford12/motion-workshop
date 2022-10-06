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

            c.node_list.command.set_value(int(command_int), ua.VariantType.Int16)

    def populate_commands(self, c: ConnectionManagement):
        self.command_list = {}
        for i in range(len(c.node_list.command_names)):
            if c.node_list.command_names[i].get_value() != "":
                self.command_list[c.node_list.command_names[i].get_value()] = i
