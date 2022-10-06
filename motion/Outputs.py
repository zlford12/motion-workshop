from utility.ConnectionManagement import ConnectionManagement


class Outputs:
    def __init__(self):
        self.output_list = {}

    def populate_outputs(self, c: ConnectionManagement):
        self.output_list = {}
        for i in range(len(c.node_list.output_names)):
            if c.node_list.output_names[i].get_value() != "":
                self.output_list[c.node_list.output_names[i].get_value()] = i
