from utility.ConnectionManagement import ConnectionManagement


class Outputs:
    def __init__(self):
        self.output_list = {}

    def populate_outputs(self, c: ConnectionManagement):
        self.output_list = {}
        output_names = c.client.get_values(c.node_list.output_names)
        for i in range(len(output_names)):
            if output_names[i] != "":
                self.output_list[output_names[i]] = i
